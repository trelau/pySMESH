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

#pragma once

// HACK: ngsolve uses relative imports so redefine those here...
#define OCCGEOMETRY 1

/* myadt.hpp */
#define FILE_MYADT 1
#include <mystdlib.h>
#include <mydefs.hpp>

#include "ngexception.hpp"
#include "parthreads.hpp"
// #include "moveablemem.hpp"
#include "dynamicmem.hpp"

#include "template.hpp"
#include "array.hpp"
#include "table.hpp"
#include "hashtabl.hpp"


#include "symbolta.hpp"
#include "bitarray.hpp"
#include "flags.hpp"
#include "spbita2d.hpp"

#include "seti.hpp"
#include "optmem.hpp"
#include "autoptr.hpp"
#include "sort.hpp"
#include "stack.hpp"
#include "mystring.hpp"
#include "profiler.hpp"

#include "mpi_interface.hpp"
#include "netgenout.hpp"
#include "gzstream.h"
#include "archive_base.hpp"
/* end myadt.hpp */

/* linalg.hpp */
#define FILE_LINALG 1
namespace netgen
{
#include "vector.hpp"
#include "densemat.hpp"
#include "polynomial.hpp"
}
/* end linalg.hpp */


/* meshing.hpp */
#define FILE_MESHING 1
#include <gprim.hpp>
#include <linalg/opti.hpp>

namespace netgen
{
  // extern int printmessage_importance;

  // class CSGeometry;
  class NetgenGeometry;
}


#include "msghandler.hpp"
#include "meshtype.hpp"
#include "localh.hpp"
#include "meshclass.hpp"
#include "global.hpp"

namespace netgen
{
#include "topology.hpp"
#include "meshtool.hpp"
#include "ruler2.hpp"
#include "adfront2.hpp"
#include "meshing2.hpp"
#include "improve2.hpp"


#include "geomsearch.hpp"
#include "adfront3.hpp"
#include "ruler3.hpp"

#define _INCLUDE_MORE

#include "findip.hpp"
#include "findip2.hpp"

#include "meshing3.hpp"
#include "improve3.hpp"

#include "curvedelems.hpp"
#include "clusters.hpp"

#include "meshfunc.hpp"

#include "bisect.hpp"
#include "hprefinement.hpp"
#include "boundarylayer.hpp"
#include "specials.hpp"
}

#include "validate.hpp"
#include "basegeom.hpp"

#ifdef PARALLEL
#include "paralleltop.hpp"
#endif
/* end meshing.hpp */

#include <occgeom.hpp>
