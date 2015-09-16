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
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Drop objects",
    "author": "anex5.2008@gmail.com",
    "version": (1,0,0),
    "blender": (2, 70, 0),
    "location": "Edit panel of Tools tab, in Object mode, 3D View tools",
    "description": "Drops selected objects to the ground",
    "warning": "",
    "wiki_url": "",
    "category": "Object"
}

import bpy
import bmesh
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty)

from mathutils import Vector, Matrix
from bpy.types import Operator

def calc_to_ground_vector(obj, ground):
    down = Vector((0, 0, -10000)) 
    mat_to_world = obj.matrix_world.copy()
    to_ground_vec = None
    to_ground_norm = None

    if obj.type == 'MESH':
        lowest_verts = []
        hits = []
        lowest_vert = obj.data.vertices[0] 
              
        for v in obj.data.vertices:
            if (mat_to_world * v.co).z <= (mat_to_world * lowest_vert.co).z:
                lowest_verts.append(v)
        
        for v in lowest_verts:
            vert_world_co = mat_to_world * v.co
            hits.append((v, ground.ray_cast(vert_world_co, vert_world_co + down)))
            
        high_hit_index = hits.index(max(hits, key=lambda x: x[1][0][2]))

        # simple drop down
        if hits[high_hit_index][1][2] > -1:
            to_ground_vec = hits[high_hit_index][1][0] - mat_to_world * hits[high_hit_index][0].co
            to_ground_norm = hits[high_hit_index][1][1]
    else:
        hit_location, hit_normal, hit_index = ground.ray_cast(obj.location, obj.location + down)
        if hit_index>-1:
            to_ground_vec = hit_location - obj.location
            to_ground_norm = hit_normal
    
    return to_ground_vec, to_ground_norm

def main(objs, dst_surface, align):
    
    m = dst_surface.to_mesh(bpy.context.scene, True, 'PREVIEW')
    m.transform(dst_surface.matrix_world)
    ground = bpy.data.objects.new('tmpGround', m)
    bpy.context.scene.objects.link(ground)
    bpy.context.scene.update()
    
    for o in objs:
        g_vec, g_norm = calc_to_ground_vector(o, ground)
        
        if align and g_norm:
            o.rotation_mode = 'QUATERNION'
            o.rotation_quaternion = g_norm.to_track_quat('Z','Y')
            o.rotation_mode = 'XYZ'
            bpy.context.scene.update()
            g_vec, gnorm = calc_to_ground_vector(o, ground)
        
        if g_vec:    
            o.location += g_vec
            print(g_vec)
        else:
            print('Object', o.name, 'didn\'t hit the ground.')
            
    #cleanup
    bpy.context.scene.objects.unlink(ground)
    bpy.data.objects.remove(ground)
        
class Drop(bpy.types.Operator):

    bl_idname = "object.drop"
    bl_label = "Drop objects"
    bl_register = True
    bl_undo = True
    bl_options = {'REGISTER', 'UNDO'}

    align = bpy.props.BoolProperty(name="Align",
        description="Align objects to ground",
        default=False)

    def avail_objects(self,context):
        items = [(x.name, x.name, x.type) for x in bpy.context.scene.objects if x.type == 'MESH']
        return items
   
    dst_surface = bpy.props.EnumProperty(items = avail_objects, name = "Ground", description = "Ground object")

    def draw(self, context):
        #bpy.ops.object.mode_set(mode='OBJECT')
        layout = self.layout
        col = layout.column()
        col.prop(self, "align")
        col.prop(self, "dst_surface")

    def invoke(self, context, event):
        return self.execute(context)

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return len(context.selected_objects) >= 1 

    def execute(self, context):
        main(context.selected_objects, context.scene.objects[self.dst_surface], self.align)
        return {'FINISHED'}

#################################################
#### REGISTER ###################################
#################################################
def menu_func(self, context):
    layout = self.layout
    layout.label("Drop to ground:")
    layout.operator(Drop.bl_idname, text="Drop")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_PT_tools_object.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_PT_tools_object.remove(menu_func)

if __name__ == "__main__":
    register()
