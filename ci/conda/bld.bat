mkdir build
cd build

cmake -G "Ninja" ^
    -DCMAKE_BUILD_TYPE="Release" ^
    -DCMAKE_INSTALL_PREFIX="%LIBRARY_PREFIX%" ^
    -DCMAKE_PREFIX_PATH="%LIBRARY_PREFIX%" ^
    -DCMAKE_SYSTEM_PREFIX_PATH="%LIBRARY_PREFIX%" ^
    -DSMESH_ROOT="%LIBRARY_PREFIX%" ^
    -DPTHREAD_INCLUDE_DIRS:FILEPATH="%LIBRARY_PREFIX%/include" ^
    -DPython_FIND_VIRTUALENV=FIRST ^
    -DPython_FIND_STRATEGY=LOCATION ^
    -DPython_FIND_REGISTRY=NEVER ^
    ..

if errorlevel 1 exit 1

ninja -j1
if errorlevel 1 exit 1

ninja install
if errorlevel 1 exit 1

cd ..
python setup.py install --prefix=%PREFIX%
