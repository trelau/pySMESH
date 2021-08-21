# pySMESH — Python bindings for SMESH
Work in progress. Plan is to:

1. Get this building with OCCT 7.4.0 and SMESH 8.3.0.4
2. Get pyOCCT building only OCCT 7.5.0
3. Get conda-forge feedstock of SMESH to build with OCCT 7.5.0 and Salome Platform 9.6.0
4. Update the sources of this project to OCCT 7.5.0 and SMESH 9.6.0

## Building from sources
To build from sources, you must generate the binding source code locally. This can be done using the
[pyOCCT_binder](https://github.com/trelau/pyOCCT_binder) project which is available as a git
submodule in this repository within the `binder/` folder.

Clone this repository and use the `--recurse-submodules` command to initialize and download the
external `pyOCCT_binder` project:

    git clone --recurse-submodules https://github.com/trelau/pySMESH.git

The binder uses `clang` to parse the C++ header files of the libraries and generate the source
code. If you are familiar with `conda`, an environment can be created for this task by:

    conda env create -f binder/environment.yml

If all the necessary dependencies are available, the binder can be run to generate the binding
sources:

    python binder/run.py -c binder/config.txt -o src

Be sure and check the output from the binding generation process in the command prompt in case there
are missing header files or other errors.

After the binding sources are generated:

    mkdir build
    cd build
    cmake ..

Note that `PTHREAD_INCLUDE_DIR` will likely need defined manually since it cannot typically not be
automatically found by CMake.
