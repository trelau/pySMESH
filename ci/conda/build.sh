#!/usr/bin/env bash

# Fail on error
set -e

rm -Rf build
mkdir build
cd build

cmake -G "Ninja" \
    -DCMAKE_BUILD_TYPE="Release" \
    -DPTHREAD_INCLUDE_DIRS="$PREFIX" \
    -DSMESH_INCLUDE_PATH="$PREFIX/include/smesh" \
    -DSMESH_LIB_PATH="$PREFIX/lib" \
    -DPython_FIND_VIRTUALENV=FIRST \
    -DPython_FIND_STRATEGY=LOCATION \
    -DPython_FIND_FRAMEWORK=NEVER \
    ..

ninja install

cd ..
python setup.py install --prefix="$PREFIX"
