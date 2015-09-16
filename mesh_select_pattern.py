# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Select pattern",
    "author": "anex5.2008@gmail.com",
    "version": (1, 0),
    "blender": (2, 74, 0),
    "location": "Toolbox",
    "description": "Selects pattern of vertex/edge/face groups",
    #"warning": "Buggy", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"
}

import bpy, bmesh

class SelVert(bpy.types.Operator):
    bl_idname = 'mesh.select_vert_pattern'
    bl_label = 'Verts'
    bl_description = 'Select vertices by pattern'
    bl_options = {'REGISTER', 'UNDO'}

    indice = bpy.props.FloatProperty(name='Selected', default=0, min=0, max=100, description='Percentage of selected edges', precision = 2, subtype = 'PERCENTAGE')
    delta = bpy.props.BoolProperty(name='Use Cursor', default=False, description='Select by Index / Distance to Cursor')
    flip = bpy.props.BoolProperty(name='Reverse Order', default=False, description='Reverse selecting order')

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'MESH')

    def draw(self, context):
        layout = self.layout
        layout.prop(self,'indice', slider=True)
        layout.prop(self,'delta')
        layout.prop(self,'flip')

    def execute(self, context):
        obj = bpy.context.object
        mode = [a for a in bpy.context.tool_settings.mesh_select_mode]
        if mode != [True, False, False]:
            bpy.context.tool_settings.mesh_select_mode = [True, False, False]
        ver = obj.data.vertices
        loc = context.scene.cursor_location
        sel = []
        for v in ver:
            d = v.co - loc
            sel.append((d.length, v.index))
        sel.sort(reverse=self.flip)
        bpy.ops.object.mode_set()
        valor = round(len(sel) / 100 * self.indice)
        if self.delta:
            for i in range(len(sel[:valor])):
                ver[sel[i][1]].select = True
        else:
            for i in range(len(sel[:valor])):
                if self.flip:
                    ver[len(sel)-i-1].select = True
                else:
                    ver[i].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

class SelEdge(bpy.types.Operator):
    bl_idname = 'mesh.select_edge_pattern'
    bl_label = 'Edges'
    bl_description = 'Select edges by pattern'
    bl_options = {'REGISTER', 'UNDO'}

    indice = bpy.props.FloatProperty(name='Selected', default=0, min=0, max=100, description='Percentage of selected edges', precision = 2, subtype = 'PERCENTAGE')
    delta = bpy.props.BoolProperty(name='Use Edges Length', default=False, description='Select Edges by Index / Length')
    flip = bpy.props.BoolProperty(name='Reverse Order', default=False, description='Reverse selecting order')

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'MESH')

    def draw(self, context):
        layout = self.layout
        layout.prop(self,'indice', slider=True)
        layout.prop(self,'delta')
        layout.prop(self,'flip')

    def execute(self, context):
        obj = bpy.context.object
        mode = [a for a in bpy.context.tool_settings.mesh_select_mode]
        if mode != [False, True, False]:
            bpy.context.tool_settings.mesh_select_mode = [False, True, False]
        ver = obj.data.vertices
        edg = obj.data.edges
        sel = []
        for e in edg:
            d = ver[e.vertices[0]].co - ver[e.vertices[1]].co
            sel.append((d.length, e.index))
        sel.sort(reverse=self.flip)
        bpy.ops.object.mode_set()
        valor = round(len(sel) / 100 * self.indice)
        if self.delta:
            for i in range(len(sel[:valor])):
                edg[sel[i][1]].select = True
        else:
            for i in range(len(sel[:valor])):
                if self.flip:
                    edg[len(sel)-i-1].select = True
                else:
                    edg[i].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

class SelFace(bpy.types.Operator):
    bl_idname = 'mesh.select_face_pattern'
    bl_label = 'Faces'
    bl_description = 'Select faces by pattern'
    bl_options = {'REGISTER', 'UNDO'}

    indice = bpy.props.FloatProperty(name='Selected', default=0, min=0, max=100, description='Percentage of selected faces', precision = 2, subtype = 'PERCENTAGE')
    delta = bpy.props.BoolProperty(name='Use Faces Area', default=False, description='Select Faces by Index / Area')
    flip = bpy.props.BoolProperty(name='Reverse Order', default=False, description='Reverse selecting order')

    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'MESH')

    def draw(self, context):
        layout = self.layout
        layout.prop(self,'indice', slider=True)
        layout.prop(self,'delta')
        layout.prop(self,'flip')

    def execute(self, context):
        obj = bpy.context.object
        mode = [a for a in bpy.context.tool_settings.mesh_select_mode]
        if mode != [False, False, True]:
            bpy.context.tool_settings.mesh_select_mode = [False, False, True]
        fac = obj.data.polygons

        pat = [f for f in fac if f.select]

        if len(pat) == 0:
            self.report({'WARNING'}, "No pattern selected.")
            return {'FINISHED'}

        print (pat)

        #sel = []
        #for f in fac:
        #    sel.append((f.area, f.index))
        #    sel.sort(reverse=self.flip)

        bpy.ops.object.mode_set()
        for i in range(len(fac)):
            fac[i].select = pat[i % len(pat)].select

        #valor = round(len(sel) / 100 * self.indice)
        #if self.delta:
        #    for i in range(len(sel[:valor])):
        #        fac[sel[i][1]].select = True
        #else:
        #    for i in range(len(sel[:valor])):
        #        if self.flip:
        #            fac[len(sel)-i-1].select = True
        #        else:
        #            fac[i].select = True

        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

class VIEW3D_MT_selectface_edit_mesh_add(bpy.types.Menu):
    # Define the "Mesh_Select_pattern" menu
    bl_idname = "mesh.face_select_pattern"
    bl_label = "Select by Face"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.label(text = 'Face Select')
        layout.separator()
        layout.operator(SelFace.bl_idname, text="Select faces")

class VIEW3D_MT_selectedge_edit_mesh_add(bpy.types.Menu):
    # Define the "Mesh_Select_pattern" menu
    bl_idname = "mesh.edge_select_pattern"
    bl_label = "Select by Edge"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.label(text = 'Edge Select')
        layout.separator()
        layout.operator(SelEdge.bl_idname, text="Select edges")

class VIEW3D_MT_selectvert_edit_mesh_add(bpy.types.Menu):
    # Define the "Mesh_Select_pattern" menu
    bl_idname = "mesh.vert_select_pattern"
    bl_label = "Select by Vert"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.label(text = 'Vert Select')
        layout.separator()
        layout.operator(SelVert.bl_idname, text="Select vertices")

# Register all operators and panels

# Define "Extras" menu
def menu_func(self, context):
    if context.tool_settings.mesh_select_mode[2]:
        self.layout.menu("mesh.face_select_pattern", icon="PLUGIN")
    if context.tool_settings.mesh_select_mode[1]:
        self.layout.menu("mesh.edge_select_pattern", icon="PLUGIN")
    if context.tool_settings.mesh_select_mode[0]:
        self.layout.menu("mesh.vert_select_pattern", icon="PLUGIN")

def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_select_edit_mesh.append(menu_func)
    # handle the keymap
    #wm = bpy.context.window_manager
    #km = wm.keyconfigs.addon.keymaps.new(name = 'Mesh', space_type = 'EMPTY')
    #kmi = km.keymap_items.new(SelVert.bl_idname, 'P', 'ANY', shift=True, ctrl=True)
    #kmi.properties.my_prop = 'some'
    #addon_keymaps.append((km, kmi))


def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.VIEW3D_MT_select_edit_mesh.remove(menu_func)

if __name__ == "__main__":
	register()
