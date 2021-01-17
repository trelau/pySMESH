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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
from OCCT.Exchange import ExchangeBasic
from SMESH.NETGENPlugin import (NETGENPlugin_SimpleHypothesis_3D,
                                NETGENPlugin_NETGEN_2D3D)
from SMESH.SMESH import SMESH_Gen

from SMESH.Visualization.MeshViewerWx import MeshViewerWx

fn = './models/shape_names.step'
shape = ExchangeBasic.read_step(fn)

v = MeshViewerWx()
v.add(shape)
v.start()

gen = SMESH_Gen()
mesh = gen.CreateMesh(0, True)

hyp = NETGENPlugin_SimpleHypothesis_3D(0, 0, gen)
hyp.SetLocalLength(5)

alg = NETGENPlugin_NETGEN_2D3D(1, 0, gen)

mesh.ShapeToMesh(shape)
mesh.AddHypothesis(shape, 0)
mesh.AddHypothesis(shape, 1)

print('Computing mesh...')
done = gen.Compute(mesh, mesh.GetShapeToMesh())
print('done.')

v = MeshViewerWx()
v.add(mesh)
v.start()
