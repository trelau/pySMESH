/*
This file is part of pySMESH which provides Python bindings to SMESH.

Copyright (C) 2016-2018 Laughlin Research, LLC
Copyright (C) 2019-2021 Trevor Laughlin and the pySMESH contributors

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*/

#ifndef __pySMESH_Common_Header__
#define __pySMESH_Common_Header__

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include <Standard_Handle.hxx>

#include <boost/shared_ptr.hpp>

namespace py = pybind11;

// Use opencascade::handle as holder type for Standard_Transient types
PYBIND11_DECLARE_HOLDER_TYPE(T, opencascade::handle<T>, true);

// Use boost::shared_ptr for some SMESH iterators
PYBIND11_DECLARE_HOLDER_TYPE(T, boost::shared_ptr<T>);

// Deleter template for mixed holder types with public/hidden destructors
template<typename T> struct Deleter { void operator() (T *o) const { delete o; } };

#endif
