import argparse
import os
import sys

# Add the binding generator to the path
BINDER_ROOT = os.path.dirname(os.path.realpath(__file__))
PYBINDER_ROOT = os.path.join(BINDER_ROOT, 'pyOCCT_binder')
if not os.path.isdir(PYBINDER_ROOT):
    raise NotADirectoryError('Binding generator is not available.')

if PYBINDER_ROOT not in sys.path:
    sys.path.append(PYBINDER_ROOT)

from pybinder.core import Generator


def find_include_path(name, path, parent=False):
    """
    Attempt to find an include directory of a given header file.

    :param name: The header file to search for.
    :param path: The starting path.
    :param parent: Whether the parent folder should be returned

    :return: The full path to the directory of the given header file.
    """
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.dirname(root) if parent else root


def gen_occt_includes(occt_include_path):
    """
    Collect list of occt headers
    :return: All the available OCCT headers.
    :rtype: tuple(list[str], list[str])
    """
    # Generate all_includes.h and output modules
    all_includes = []

    # Header files to ignore
    ignored_includes = [
        'step.tab.hxx'
    ]

    occt_mods = set()
    for fin in os.listdir(occt_include_path):
        if fin.endswith('.hxx') and fin not in ignored_includes:
            all_includes.append(fin)
        if '_' in fin:
            mod = fin.split('_')[0]
        else:
            mod = fin.split('.')[0]
        occt_mods.add(mod)

    # OCCT modules
    occt_mods = list(occt_mods)
    occt_mods.sort(key=str.lower)

    return occt_mods, all_includes


def gen_netgen_includes(netgen_include_path):
    all_includes = []

    # Header files to ignore
    ignored_includes = []

    headers = ['.hpp']

    include_dirs = []

    for item in os.listdir(netgen_include_path):
        path = os.path.join(netgen_include_path, item)
        _, ext = os.path.splitext(item)
        if os.path.isdir(path):
            include_dirs.append(path)
            for item in os.listdir(path):
                _, ext = os.path.splitext(item)
                if ext in headers and item not in ignored_includes:
                    all_includes.append(item)
        elif ext in headers and item not in ignored_includes:
            all_includes.append(item)
    assert all_includes, "Netgen path is invalid"
    netgen_mods = ['OCCGeometry', 'Mesh']
    return netgen_mods, include_dirs, all_includes


def gen_includes(smesh_include_path, netgen_include_path,
                 occt_include_path, output_path):
    """
    Generate the "all_includes.h" header file for parsing the headers.

    :param str smesh_include_path: The directory containing the OCCT header files.
    :param str output_path: The path to write the all_includes.h file.

    :return: Tuple of the available SMESH modules.include dirs, and headers
    :rtype: tuple(list[str], list[str], list[str])
    """

    # Generate all_includes.h and output modules
    all_includes = []

    # Header files to ignore
    ignored_includes = [
        'libmesh5.h',
        'gzstream.h',
        'memoire.h',
        'nginterface.h',
        'nglib.h',
    ]

    smesh_mods = set()
    include_dirs = []
    for folder in os.listdir(smesh_include_path):
        subfolder = os.path.join(smesh_include_path, folder)
        include_dirs.append(subfolder)
        for fin in os.listdir(subfolder):
            pth, ext = os.path.splitext(fin)
            if ext in ('.hxx', '.h') and fin not in ignored_includes:
                all_includes.append(fin)
            if '_' in fin:
                mod = fin.split('_')[0]
            else:
                mod = fin.split('.')[0]
            smesh_mods.add(mod)


    # SMESH modules
    smesh_mods = list(smesh_mods)
    smesh_mods.sort(key=str.lower)

    # Build all includes so clang can figure out imports
    occt_mods, occt_includes = gen_occt_includes(occt_include_path)
    all_includes.extend(occt_includes)

    netgen_mods, netgen_include_dirs, netgen_includes = gen_netgen_includes(netgen_include_path)
    all_includes.extend(netgen_includes)
    include_dirs.extend(netgen_include_dirs)

    # Sort ignoring case
    all_includes.sort(key=str.lower)

    # all_includes.h
    with open(os.path.join(output_path, 'all_includes.h'), 'w') as fout:
        fout.write("#ifdef _WIN32\n")
        fout.write('    #include <Windows.h>\n')
        fout.write("#endif\n")

        for header in all_includes:
            fout.write('#include <{}>\n'.format(header))

    return smesh_mods, netgen_mods, occt_mods, include_dirs, all_includes


def main():
    # Setup a parser
    parser = argparse.ArgumentParser()
    print('-' * 100)
    print("pySMESH Binder")
    print('-' * 100)

    parser.add_argument(
        '-r',
        help='Root path for the pySMESH repository',
        default='.',
        dest='pysmesh_root')

    parser.add_argument(
        '-c',
        help='Path to config.txt',
        dest='config_path',
        default='config.txt')

    parser.add_argument(
        '-o',
        help='Output path for the generated bindings',
        default=os.path.join(BINDER_ROOT, 'output'),
        dest='output_path')

    args = parser.parse_args()

    # Get the root directory of the conda environment
    conda_prefix = os.environ.get('CONDA_PREFIX')

    # Attempt to find include directories by searching for a known header file. Will likely
    # need to make this more robust.
    occt_include_path = find_include_path('Standard.hxx', conda_prefix)
    pyocct_root = os.path.join(os.path.dirname(os.path.dirname(BINDER_ROOT)), 'pyOCCT')
    pyocct_include_path = find_include_path('pyOCCT_Common.hxx', pyocct_root)
    smesh_include_path = find_include_path('SMESH_SMESH.hxx', conda_prefix, parent=True)
    netgen_include_path = find_include_path('ngcore.hpp', conda_prefix, parent=True)
    vtk_include_path = find_include_path('vtk_doubleconversion.h', conda_prefix)
    tbb_include_path = find_include_path('tbb.h', conda_prefix, parent=True)

    print('Include directories:')
    print('\tSMESH: {}'.format(smesh_include_path))
    print('\tNETGEN: {}'.format(netgen_include_path))
    print('\tOCCT: {}'.format(occt_include_path))
    print('\tpyOCCT: {}'.format(pyocct_include_path))
    print('\tVTK: {}'.format(vtk_include_path))
    print('\tTBB: {}'.format(tbb_include_path))

    clang_include_path = ''
    if sys.platform.startswith('linux'):
        clang_include_path = find_include_path('__stddef_max_align_t.h', conda_prefix)
        print('Found clangdev include directory: {}'.format(clang_include_path))

    for (name, path) in {
                'OCCT': occt_include_path,
                'pyOCCT': pyocct_include_path,
                'SMESH': smesh_include_path,
                'NETGEN': netgen_include_path,
            }.items():
        if not path or not os.path.exists(path):
            raise NotADirectoryError("{} include path does not exist: {}".format(name, path))

    if not os.path.exists(args.pysmesh_root):
        raise NotADirectoryError("pySMESH root path does not exist: {}".format(args.pysmesh_root))

    if not os.path.exists(args.config_path):
        raise FileNotFoundError("Configuration file not found: {}".format(args.config_path))

    # Force using conda's clangdev includes. This may not be needed on other systems but was
    # getting errors on linux.
    if sys.platform.startswith('linux') and not os.path.exists(clang_include_path):
        raise NotADirectoryError("clangdev not found: {}".format(clang_include_path))

    # Gather all the includes for the parser
    other_includes = [i for i in [smesh_include_path, occt_include_path, vtk_include_path, tbb_include_path, clang_include_path] if i]


    # Add extra includes for missing OCCT headers that cause issues during parsing
    other_includes.append(os.path.join(BINDER_ROOT, 'extra_includes'))

    print('\nGenerating all_includes.h file...')
    smesh_mods, netgen_mods, occt_mods, include_dirs, all_includes = gen_includes(
        smesh_include_path, netgen_include_path, occt_include_path, BINDER_ROOT)
    other_includes.extend(include_dirs)

    # Initialize the main binding generation tool
    gen = Generator(
        package_name='SMESH',
        namespace={
            'OCCT': occt_mods,
            'SMESH': smesh_mods,
            'netgen': netgen_mods,
        },
        all_includes=all_includes,
        main_includes=other_includes
    )

    # Output bindings path
    output_path = os.path.abspath(args.output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    print("\nWriting binding output files to: {}".format(output_path))

    # For debugging and dev
    gen.bind_enums = True
    gen.bind_functions = True
    gen.bind_classes = True
    gen.bind_typedefs = True
    gen.bind_class_templates = True

    # Process configuration file
    gen.process_config(args.config_path)

    print('\nParsing headers...')
    gen.parse(os.path.join(BINDER_ROOT, 'all_includes.h'))
    gen.dump_diagnostics()

    print('Traversing headers...')
    #import pdb; pdb.set_trace()
    gen.traverse()

    print('Sorting binders...')
    gen.sort_binders()

    print('Building includes...')
    gen.build_includes()

    print('Building imports...')
    gen.build_imports()

    print('Checking circular imports...')
    gen.check_circular()

    print('Binding templates...')
    gen.bind_templates(output_path)

    print('Binding...')
    gen.bind(output_path)
    print('Done!')
    print('-' * 100)


if __name__ == '__main__':
    main()
