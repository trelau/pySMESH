# This file is part of pySMESH which provides Python bindings to SMESH.
#
# Copyright (C) 2016-2018 Laughlin Research, LLC
# Copyright (C) 2019-2021 Trevor Laughlin and the pySMESH contributors
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
cmake_minimum_required(VERSION 3.15...3.20)
project(pySMESH VERSION 9.6.0 LANGUAGES C CXX)


# --------------------------------------------------------------------------- #
# OPTIONS
# --------------------------------------------------------------------------- #
option(ENABLE_WARNINGS "Disable warning output." OFF)

# --------------------------------------------------------------------------- #
# SETTINGS
# --------------------------------------------------------------------------- #
set(pySMESH_MAJOR_VERSION 9)
set(pySMESH_MINOR_VERSION 6)
set(pySMESH_PATCH_VERSION 0)
set(pySMESH_TWEAK_VERSION 0)

if(WIN32)
    set(EXTENSION ".pyd")
else(WIN32)
    set(EXTENSION ".so")
endif(WIN32)

# Known warnings
if(NOT ENABLE_WARNINGS)
    if(WIN32)
        set(WARNINGS "/wd4996 /wd4800 /wd4267 /wd4275 /wd4251 /wd4805 /wd4290 /wd4005 /wd4180 /wd4244 /wd4146 /wd4172")
    else(WIN32)
        set(WARNINGS "-Wall -Wno-deprecated-declarations -Wno-strict-aliasing")
    endif(WIN32)
else(NOT ENABLE_WARNINGS)
    set(WARNINGS)
endif(NOT ENABLE_WARNINGS)

if(NOT MSVC)
    # TODO: Figure out how to handle methods that return functions
    message(STATUS "Flags: ${CMAKE_CXX_FLAGS}")
    message(STATUS "Linker flags: ${CMAKE_MODULE_LINKER_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fpermissive")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wl,-z,defs")
endif()


# --------------------------------------------------------------------------- #
# PYTHON and PYBIND11
# --------------------------------------------------------------------------- #
message(STATUS "Searching for Python and pybind11...")
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)


# --------------------------------------------------------------------------- #
# TBB (for BVH header)
# --------------------------------------------------------------------------- #
message(STATUS "Searching for TBB...")
find_package(TBB REQUIRED)


# --------------------------------------------------------------------------- #
# OpenGL
# --------------------------------------------------------------------------- #
message(STATUS "Searching for OpenGL...")
if(WIN32 OR APPLE)
    find_package(OpenGL REQUIRED)
else()
    find_package(OpenGL REQUIRED GLX EGL)
endif()

message(STATUS "OpenGL include directory: ${OPENGL_INCLUDE_DIR}")
message(STATUS "OpenGL libraries: ${OPENGL_LIBRARIES}")
include_directories(${OPENGL_INCLUDE_DIR})

# --------------------------------------------------------------------------- #
# Freetype
# --------------------------------------------------------------------------- #
if (WIN32)
    message(STATUS "Searching for freetype...")
    find_package(Freetype REQUIRED)
endif()

# --------------------------------------------------------------------------- #
# GLEW
# --------------------------------------------------------------------------- #
if (WIN32)
    message(STATUS "Searching for GLEW...")
    find_package(GLEW REQUIRED)
endif()

# --------------------------------------------------------------------------- #
# OpenCASCADE
# --------------------------------------------------------------------------- #
# Must be included before opencascade so the InterfaceGraphic.hxx patch works
include_directories(inc)
if(NOT DEFINED OpenCASCADE_INCLUDE_DIR OR NOT DEFINED OpenCASCADE_LIBRARY_DIR)
    message(STATUS "Searching for OpenCASCADE...")
    find_package(OpenCASCADE 7.5.3 REQUIRED)
endif()

if(NOT EXISTS ${OpenCASCADE_INCLUDE_DIR})
    message(FATAL_ERROR "Failed to find OpenCASCADE include directory.")
endif()

if(NOT EXISTS ${OpenCASCADE_LIBRARY_DIR})
    message(FATAL_ERROR "Failed to find OpenCASCADE library directory.")
endif()

message(STATUS "OpenCASCADE include directory: ${OpenCASCADE_INCLUDE_DIR}")
message(STATUS "OpenCASCADE library directory: ${OpenCASCADE_LIBRARY_DIR}")
include_directories(${OpenCASCADE_INCLUDE_DIR})
link_directories(${OpenCASCADE_LIBRARY_DIR})

# ----------------------------------------------------------------------- #
# VTK
# ----------------------------------------------------------------------- #
message(STATUS "Searching for VTK...")
if(WIN32)
    find_package(VTK REQUIRED COMPONENTS CommonCore CommonDataModel FiltersVerdict)
else()
    find_package(VTK REQUIRED)
endif()

message(STATUS "VTK include directory: ${VTK_INCLUDE_DIRS}")
include_directories(${VTK_INCLUDE_DIRS})


# --------------------------------------------------------------------------- #
# SMESH
# --------------------------------------------------------------------------- #
set(SMESH_ABS_LIBS)
message(STATUS "Searching for SMESH...")
find_package(SMESH REQUIRED)

if(NOT EXISTS ${SMESH_INCLUDE_PATH})
    message(FATAL_ERROR "Failed to find SMESH include directory.")
endif()

if(NOT EXISTS ${SMESH_LIB_PATH})
    message(FATAL_ERROR "Failed to find SMESH library directory.")
endif()
message(STATUS "SMESH include directory: ${SMESH_INCLUDE_PATH}")
message(STATUS "SMESH library directory: ${SMESH_LIB_PATH}")
include_directories(${SMESH_INCLUDE_PATH})
link_directories(${SMESH_LIB_PATH})

# Include each subdir
FILE(GLOB SMESH_INCLUDE_SUBDIRS RELATIVE ${SMESH_INCLUDE_PATH} ${SMESH_INCLUDE_PATH}/*)
foreach(SUBDIR ${SMESH_INCLUDE_SUBDIRS})
    message(STATUS "SMESH include ${SMESH_INCLUDE_PATH}/${SUBDIR}")
    include_directories("${SMESH_INCLUDE_PATH}/${SUBDIR}")
endforeach(SUBDIR)

# Build full library paths since they have the same name as the Python
# libraries

# Needed for trace collector
list(APPEND SMESH_LIBRARIES "Kernel")

foreach(LIB ${SMESH_LIBRARIES})
    message(STATUS "SMESH library: ${LIB}")
    set(FOUND_LIB "FOUND_LIB-NOTFOUND")
    find_library(FOUND_LIB ${LIB} PATHS ${SMESH_LIB_PATH})
    message(STATUS "SMESH found library: ${FOUND_LIB}")
    list(APPEND SMESH_ABS_LIBS ${FOUND_LIB})
endforeach(LIB)
unset(FOUND_LIB CACHE)
message(STATUS "SMESH libs: ${SMESH_ABS_LIBS}")

# ----------------------------------------------------------------------- #
# BOOST
# ----------------------------------------------------------------------- #
message(STATUS "Searching for Boost...")
find_package(Boost REQUIRED COMPONENTS filesystem thread serialization)

if(MSVC)
  # Find the shared boost libs
  add_definitions(-DBOOST_ALL_DYN_LINK)
  # Set postfix for debug libs
  if(NOT CMAKE_DEBUG_POSTFIX)
      set(CMAKE_DEBUG_POSTFIX d)
  endif()
endif()

message(STATUS "Boost include directory: ${Boost_INCLUDE_DIR}")
message(STATUS "Boost libraires: ${Boost_LIBRARIES}")
include_directories(${Boost_INCLUDE_DIR})

# ----------------------------------------------------------------------- #
# PTHREAD
# ----------------------------------------------------------------------- #
if(WIN32)
  set(PTHREAD_INCLUDE_DIRS "" CACHE PATH "pthread include directory.")
  if(NOT EXISTS ${PTHREAD_INCLUDE_DIRS})
    message(FATAL_ERROR "pthread include directory is required.")
  endif()
  message(STATUS "pthread include directory: ${PTHREAD_INCLUDE_DIRS}")
  include_directories(${PTHREAD_INCLUDE_DIRS})
endif()

# ----------------------------------------------------------------------- #
# NETGEN
# ----------------------------------------------------------------------- #
message(STATUS "Searching for Netgen...")
find_package(Netgen REQUIRED)

message(STATUS "Netgen include directory: ${NETGEN_INCLUDE_DIR}")
include_directories(${NETGEN_INCLUDE_DIR})

set(Netgen_LIBRARIES "nglib4smesh")

# --------------------------------------------------------------------------- #
# pyOCCT
# --------------------------------------------------------------------------- #
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/pyOCCT/inc/)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/pyOCCT/src/)

# --------------------------------------------------------------------------- #
# pySMESH
# --------------------------------------------------------------------------- #
set(OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG "${OUTPUT_PATH}")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE "${OUTPUT_PATH}")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG "${OUTPUT_PATH}")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE "${OUTPUT_PATH}")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG "${OUTPUT_PATH}")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE "${OUTPUT_PATH}")

# Treat each .cxx file in src/modules as a module
file(GLOB SMESH_SRCS ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cxx)

# SMESH modules
foreach(SRC ${SMESH_SRCS})

    # Get module name
    get_filename_component(MOD ${SRC} NAME_WE)

    # Add pybind11 module
    pybind11_add_module(py${MOD} ${SRC})

    target_link_libraries(py${MOD} PUBLIC ${OpenCASCADE_LIBRARIES}
                                          ${Python_LIBRARIES}
                                          ${SMESH_LIBRARIES}
                                          ${Netgen_LIBRARIES}
                                          ${Boost_LIBRARIES})
    set_target_properties(py${MOD} PROPERTIES SUFFIX ${EXTENSION} COMPILE_FLAGS ${WARNINGS})
    target_include_directories(py${MOD} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)
    install(FILES ${OUTPUT_PATH}/py${MOD}${EXTENSION}
            RENAME ${MOD}${EXTENSION}
            DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/SMESH)


    # Special hack for handling static member variables causing link errors
    # with pybind11
    if(MSVC AND ${MOD} STREQUAL "SMESHDS")
        set_property(TARGET py${MOD} APPEND_STRING PROPERTY LINK_FLAGS " /FORCE")
    endif()

endforeach()
