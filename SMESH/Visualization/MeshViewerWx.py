# This file is part of pySMESH which provides Python bindings to SMESH.
#
# Copyright (C) 2016-2018 Laughlin Research, LLC
# Copyright (C) 2019-2021 Trevor Laughlin and pySMESH contributors
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
import os

from OCCT.MeshVS import MeshVS_Mesh, MeshVS_MeshPrsBuilder, MeshVS_DrawerAttribute
from OCCT.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCCT.Visualization.WxViewer import ViewerWx
from SMESH.SMDSAbs import SMDSAbs_Node
from SMESH.SMESH import SMESH_MeshVSLink, SMESH_Mesh, SMESH_subMesh

__all__ = ['MeshViewerWx']

_icon = os.path.dirname(__file__) + '/_resources/icon.png'


class MeshViewerWx(ViewerWx):
    """
    Basic tool for viewing meshes built on pyOCCT basic viewer using wx.
    """

    def __init__(self, width=800, height=600):
        # Launch an app before initializing any wx types
        super(MeshViewerWx, self).__init__(width, height)

    def display_mesh(self, mesh, mode=2, group=None,
                     display_nodes=False, node_size=1, node_color=(1, 1, 1),
                     display_edges=True, edge_size=1, edge_color=(0.5, 0.5, 0.5),
                     beam_size=2, beam_color=(1, 1, 0),
                     face_color=(0, 0, 0.5), back_face_color=None):
        """
        Display a mesh.

        :param mesh: The mesh.
        :type mesh: OCCT.SMESH_SMESH_Mesh or OCCT.SMESH_SMESH_subMesh
        :param int mode: Display mode for mesh elements (1=wireframe, 2=solid).
        :param group: Option to display a group of mesh elements.
        :type group: None or OCCT.SMESH.SMESH_Group group
        :param bool display_nodes: Option to display mesh nodes or not. If a group of nodes is
            provided, then this option is turned on by default.
        :param float node_size: An option to scale the size of the node markers.
        :param node_color: The RGB values for the node markers between 0 and 1.
        :type node_color: tuple(float, float, float)
        :param bool display_edges: An option to display the edges of faces and beams.
        :param float edge_size: An option to scale the size of the edges.
        :param edge_color: The RGB values for the edges between 0 and 1.
        :type edge_color: tuple(float, float, float)
        :param float beam_size: An option to scale the size of the beams.
        :param beam_color: The RGB values for the beams between 0 and 1.
        :type beam_color: tuple(float, float, float)
        :param face_color: The RGB values for the faces between 0 and 1.
        :type face_color: tuple(float, float, float)
        :param back_face_color: The RGB values of the back side of the faces between 0 and 1. If not
            provided, then the back faces are colored the same as the faces.
        :type back_face_color: None or tuple(float, float, float)

        :return: The MeshVS_Mesh created for the mesh.
        :rtype: OCCT.MeshVS.MeshVS_Mesh
        """
        # Create the link
        if group:
            vs_link = SMESH_MeshVSLink(mesh, group)
        else:
            vs_link = SMESH_MeshVSLink(mesh)

        # Initialize
        mesh_vs = MeshVS_Mesh()
        mesh_vs.SetDataSource(vs_link)
        prs_builder = MeshVS_MeshPrsBuilder(mesh_vs)
        mesh_vs.AddBuilder(prs_builder)
        mesh_vs_drawer = mesh_vs.GetDrawer()

        # Node settings
        r, g, b = node_color
        color = Quantity_Color(r, g, b, Quantity_TOC_RGB)
        mesh_vs_drawer.SetColor(MeshVS_DrawerAttribute.MeshVS_DA_MarkerColor, color)
        mesh_vs_drawer.SetDouble(MeshVS_DrawerAttribute.MeshVS_DA_MarkerScale, node_size)
        # Always display nodes for a group of nodes
        if not group:
            mesh_vs_drawer.SetBoolean(MeshVS_DrawerAttribute.MeshVS_DA_DisplayNodes, display_nodes)
        elif group.GetGroupDS().GetType() == SMDSAbs_Node:
            mesh_vs_drawer.SetBoolean(MeshVS_DrawerAttribute.MeshVS_DA_DisplayNodes, True)

        # Edge settings
        r, g, b = edge_color
        color = Quantity_Color(r, g, b, Quantity_TOC_RGB)
        mesh_vs_drawer.SetColor(MeshVS_DrawerAttribute.MeshVS_DA_EdgeColor, color)
        mesh_vs_drawer.SetDouble(MeshVS_DrawerAttribute.MeshVS_DA_EdgeWidth, edge_size)
        mesh_vs_drawer.SetBoolean(MeshVS_DrawerAttribute.MeshVS_DA_ShowEdges, display_edges)

        # Beam settings
        r, g, b = beam_color
        color = Quantity_Color(r, g, b, Quantity_TOC_RGB)
        mesh_vs_drawer.SetColor(MeshVS_DrawerAttribute.MeshVS_DA_BeamColor, color)
        mesh_vs_drawer.SetDouble(MeshVS_DrawerAttribute.MeshVS_DA_BeamWidth, beam_size)

        # Face settings
        r, g, b = face_color
        color = Quantity_Color(r, g, b, Quantity_TOC_RGB)
        mesh_vs_drawer.SetColor(MeshVS_DrawerAttribute.MeshVS_DA_InteriorColor, color)
        if back_face_color:
            r, g, b = back_face_color
            color = Quantity_Color(r, g, b, Quantity_TOC_RGB)
            mesh_vs_drawer.SetColor(MeshVS_DrawerAttribute.MeshVS_DA_BackInteriorColor, color)

        # Display mode
        mesh_vs.SetDisplayMode(mode)

        self._my_context.Display(mesh_vs, True)
        return mesh_vs

    def add(self, entity, rgb=None, transparency=None, material=None, mode=2):
        """
        Add an entity to the view.

        :param entity: The entity.
        :param rgb: The RGB color (r, g, b).
        :type rgb: collections.Sequence(float) or OCCT.Quantity.Quantity_Color
        :param float transparency: The transparency (0 to 1).
        :param OCCT.Graphic3d.Graphic3d_NameOfMaterial material: The material.
        :param int mode: Display mode for mesh elements (1=wireframe, 2=solid).

        :return: The AIS_Shape created for the entity. Returns *None* if the
            entity cannot be converted to a shape.
        :rtype: OCCT.AIS.AIS_Shape or None
        """
        if isinstance(entity, (SMESH_Mesh, SMESH_subMesh)):
            return self.display_mesh(entity, mode)
        else:
            return super(MeshViewerWx, self).add(entity, rgb, transparency, material, mode)
