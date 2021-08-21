from setuptools import setup

setup(
    name='SMESH',
    version='9.6.0.0',
    packages=['SMESH', 'SMESH.Visualization'],
    package_data={'SMESH': ['*.so', '*.pyd', '*.dll', 'Visualization/_resources/*']},
    author='Trevor Laughlin',
    description='Python bindings for SMESH.',
    url='https://github.com/trelau/pySMESH',
    license='LGPL v2.1',
    platforms=['Windows', 'Linux']
)
