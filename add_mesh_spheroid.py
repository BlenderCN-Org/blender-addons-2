# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Spherical surface",
    "author": "anex5.2008@gmail.com",
    "version": (1,0,0),
    "blender": (2, 70, 0),
    "location": "View3D > Add > Mesh",
    "description": "Add mesh spherical surface",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh"
}

import os
import bpy
from bpy.props import (IntProperty, FloatProperty, IntVectorProperty, FloatVectorProperty)
from math import sqrt, sin, cos, tan, pi, acos, asin, atan, radians
from mathutils import Vector
from bpy_extras.object_utils import object_data_add

threshold = 1e-6

def SpheresIntersection(s1,s2,d,R):
    if (s1-s2).length<=threshold:
        print(s1,s2,"zero distance!")
        return s1,s2

    R2=R**2
    R4=R2**2
    d2=d**2
    d4=d2**2

    s1_x2=s1[0]**2
    s1_y2=s1[1]**2
    s1_z2=s1[2]**2

    s2_x2=s2[0]**2
    s2_y2=s2[1]**2
    s2_z2=s2[2]**2

    s1_x3=s1[0]**3
    s1_y3=s1[1]**3
    s1_z3=s1[2]**3

    s2_x3=s2[0]**3
    s2_y3=s2[1]**3
    s2_z3=s2[2]**3

    dd=-(s1[2]*s2[1]-s1[1]*s2[2])**2*(d4*((s1[0]-s2[0])**2+(s1[1]-s2[1])**2+(s1[2]-s2[2])**2)+((s1[0]-s2[0])**2+(s1[1]-s2[1])**2+(s1[2]-s2[2])**2)*(R4-2*R2*(s1[0]*s2[0]+s1[1]*s2[1]+s1[2]*s2[2])+(s1_x2+s1_y2+s1_z2)*(s2_x2+s2_y2+s2_z2))+2*d2*(s1_x3*s2[0]-2*s1_y2*s2_x2-2*s1_z2*s2_x2+s1_y3*s2[1]+s1[1]*s1_z2*s2[1]+s1[1]*s2_x2*s2[1]-2*s1_y2*s2_y2-2*s1_z2*s2_y2+s1[1]*s2_y3-R2*((s1[0]-s2[0])**2+(s1[1]-s2[1])**2+(s1[2]-s2[2])**2)+s1[2]*(s1_y2+s1_z2+s2_x2+s2_y2)*s2[2]+(-2*(s1_y2+s1_z2)+s1[1]*s2[1])*s2_z2+s1[2]*s2_z3+s1_x2*(-2*s2_x2+(s1[1]-2*s2[1])*s2[1]+(s1[2]-2*s2[2])*s2[2])+s1[0]*s2[0]*(s1_y2+s1_z2+s2_x2+s2_y2+s2_z2)))
    if dd>0:
        dd=sqrt(dd)
    else:
        print(s1,s2,dd, "negative")
        dd=sqrt(-dd)

    x1=(s1_y2*s2_x3+s1_z2*s2_x3-s1_x2*s1[1]*s2[0]*s2[1]-s1_y3*s2[0]*s2[1]-s1[1]*s1_z2*s2[0]*s2[1]-s1[0]*s1[1]*s2_x2*s2[1]+s1_x3*s2_y2+s1[0]*s1_y2*s2_y2+s1[0]*s1_z2*s2_y2+s1_y2*s2[0]*s2_y2+s1_z2*s2[0]*s2_y2-s1[0]*s1[1]*s2_y3-s1[2]*(s2[0]*(s1_y2+s1_z2+s1[0]*(s1[0]+s2[0]))+s1[0]*s2_y2)*s2[2]+(s1_x3+(s1_y2+s1_z2)*s2[0]+s1[0]*(s1_y2+s1_z2-s1[1]*s2[1]))*s2_z2-s1[0]*s1[2]*s2_z3+R2*(s1_y2*s2[0]-s1[1]*(s1[0]+s2[0])*s2[1]+s1[0]*s2_y2+(s1[2]-s2[2])*(s1[2]*s2[0]-s1[0]*s2[2]))+d2*(-s1_y2*s2[0]-s1_z2*s2[0]+s1[1]*(s1[0]+s2[0])*s2[1]+s1[2]*(s1[0]+s2[0])*s2[2]-s1[0]*(s2_y2+s2_z2))-dd)/(2*(s1_z2*(s2_x2+s2_y2)-2*s1[0]*s1[2]*s2[0]*s2[2]-2*s1[1]*s2[1]*(s1[0]*s2[0]+s1[2]*s2[2])+s1_y2*(s2_x2+s2_z2)+s1_x2*(s2_y2+s2_z2)))
    y1=(-s1[1]**4*s2[2]*(s2_x2+s2_z2)+s1[2]*s2_y2*(R2*(s1_x2-s1[0]*s2[0]+s1[2]*(s1[2]-s2[2]))-(s1_x2+s1_z2)*((s1[0]-s2[0])*s2[0]-s2_y2+(s1[2]-s2[2])*s2[2]))+d2*(-s1[2]*s2[1]+s1[1]*s2[2])*(s1_x2*s2[1]-s1[0]*s2[0]*(s1[1]+s2[1])+s1[2]*s2[1]*(s1[2]-s2[2])+s1[1]*(s2_x2-s1[2]*s2[2]+s2_z2))+s1_y3*s2[1]*(s1[0]*s2[0]*s2[2]+s1[2]*(s2_x2+2*s2_z2))+s1[2]*s2[0]*dd-s1[0]*s2[2]*dd+s1_y2*(-s1_x2*s2[2]*(s2_x2+s2_z2)+s1[0]*s2[0]*(-s1[2]*s2_y2+s2[2]*(R2+s2_x2+s2_y2+s2_z2))+s2[2]*(-s1[2]*(s1[2]-s2[2])*(s2_x2+s2_y2+s2_z2)-R2*(s2_x2-s1[2]*s2[2]+s2_z2)))+s1[1]*s2[1]*(s1_x3*s2[0]*s2[2]+s1[0]*s1[2]*s2[0]*(-s2_x2-s2_y2+(s1[2]-s2[2])*s2[2])+s1_z2*(-2*s2[2]*(s2_x2+s2_y2+s2_z2)+s1[2]*(s2_x2+2*s2_z2))+s1_x2*(-s2[2]*(s2_x2+s2_y2+s2_z2)+s1[2]*(s2_x2+2*s2_z2))+R2*(-s1_x2*s2[2]+s1[0]*s2[0]*(-s1[2]+s2[2])+s1[2]*(s2_x2+2*s2[2]*(-s1[2]+s2[2])))))/(2*(s1[2]*s2[1]-s1[1]*s2[2])*(s1_z2*(s2_x2+s2_y2)-2*s1[0]*s1[2]*s2[0]*s2[2]-2*s1[1]*s2[1]*(s1[0]*s2[0]+s1[2]*s2[2])+s1_y2*(s2_x2+s2_z2)+s1_x2*(s2_y2+s2_z2)))
    z1=(s1[2]**4*s2[1]*(s2_x2+s2_y2)-s1_z3*(s1[0]*s2[0]*s2[1]+s1[1]*(s2_x2+2*s2_y2))*s2[2]+s1_z2*((s1_x2-s1[0]*s2[0]+s1[1]*(s1[1]-s2[1]))*s2[1]*(s2_x2+s2_y2)+R2*s2[1]*(-s1[0]*s2[0]+s2_x2-s1[1]*s2[1]+s2_y2)+(s1[1]-s2[1])*(s1[0]*s2[0]+s1[1]*s2[1])*s2_z2)-d2*(s1[2]*s2[1]-s1[1]*s2[2])*(s1[2]*(s2_x2-s1[1]*s2[1]+s2_y2)+s1_x2*s2[2]+s1[1]*(s1[1]-s2[1])*s2[2]-s1[0]*s2[0]*(s1[2]+s2[2]))+s1[1]*s2_z2*(-R2*(s1_x2-s1[0]*s2[0]+s1[1]*(s1[1]-s2[1]))+(s1_x2+s1_y2)*((s1[0]-s2[0])*s2[0]+(s1[1]-s2[1])*s2[1]-s2_z2))+s1[2]*s2[2]*(-s1_x3*s2[0]*s2[1]+R2*(s1[0]*s2[0]*(s1[1]-s2[1])+s1_x2*s2[1]+s1[1]*(-s2_x2+2*(s1[1]-s2[1])*s2[1]))+s1[0]*s1[1]*s2[0]*(s2_x2-s1[1]*s2[1]+s2_y2+s2_z2)+s1_x2*(-s1[1]*(s2_x2+2*s2_y2)+s2[1]*(s2_x2+s2_y2+s2_z2))+s1_y2*(-s1[1]*(s2_x2+2*s2_y2)+2*s2[1]*(s2_x2+s2_y2+s2_z2)))-s1[1]*s2[0]*dd+s1[0]*s2[1]*dd)/(2*(s1[2]*s2[1]-s1[1]*s2[2])*(s1_z2*(s2_x2+s2_y2)-2*s1[0]*s1[2]*s2[0]*s2[2]-2*s1[1]*s2[1]*(s1[0]*s2[0]+s1[2]*s2[2])+s1_y2*(s2_x2+s2_z2)+s1_x2*(s2_y2+s2_z2)))

    x2=(s1_y2*s2_x3+s1_z2*s2_x3-s1_x2*s1[1]*s2[0]*s2[1]-s1_y3*s2[0]*s2[1]-s1[1]*s1_z2*s2[0]*s2[1]-s1[0]*s1[1]*s2_x2*s2[1]+s1_x3*s2_y2+s1[0]*s1_y2*s2_y2+s1[0]*s1_z2*s2_y2+s1_y2*s2[0]*s2_y2+s1_z2*s2[0]*s2_y2-s1[0]*s1[1]*s2_y3-s1[2]*(s2[0]*(s1_y2+s1_z2+s1[0]*(s1[0]+s2[0]))+s1[0]*s2_y2)*s2[2]+(s1_x3+(s1_y2+s1_z2)*s2[0]+s1[0]*(s1_y2+s1_z2-s1[1]*s2[1]))*s2_z2-s1[0]*s1[2]*s2_z3+R2*(s1_y2*s2[0]-s1[1]*(s1[0]+s2[0])*s2[1]+s1[0]*s2_y2+(s1[2]-s2[2])*(s1[2]*s2[0]-s1[0]*s2[2]))+d2*(-s1_y2*s2[0]-s1_z2*s2[0]+s1[1]*(s1[0]+s2[0])*s2[1]+s1[2]*(s1[0]+s2[0])*s2[2]-s1[0]*(s2_y2+s2_z2))+dd)/(2*(s1_z2*(s2_x2+s2_y2)-2*s1[0]*s1[2]*s2[0]*s2[2]-2*s1[1]*s2[1]*(s1[0]*s2[0]+s1[2]*s2[2])+s1_y2*(s2_x2+s2_z2)+s1_x2*(s2_y2+s2_z2)))
    y2=(-s1[1]**4*s2[2]*(s2_x2+s2_z2)+s1[2]*s2_y2*(R2*(s1_x2-s1[0]*s2[0]+s1[2]*(s1[2]-s2[2]))-(s1_x2+s1_z2)*((s1[0]-s2[0])*s2[0]-s2_y2+(s1[2]-s2[2])*s2[2]))+d2*(-s1[2]*s2[1]+s1[1]*s2[2])*(s1_x2*s2[1]-s1[0]*s2[0]*(s1[1]+s2[1])+s1[2]*s2[1]*(s1[2]-s2[2])+s1[1]*(s2_x2-s1[2]*s2[2]+s2_z2))+s1_y3*s2[1]*(s1[0]*s2[0]*s2[2]+s1[2]*(s2_x2+2*s2_z2))-s1[2]*s2[0]*dd+s1[0]*s2[2]*dd+s1_y2*(-s1_x2*s2[2]*(s2_x2+s2_z2)+s1[0]*s2[0]*(-s1[2]*s2_y2+s2[2]*(R2+s2_x2+s2_y2+s2_z2))+s2[2]*(-s1[2]*(s1[2]-s2[2])*(s2_x2+s2_y2+s2_z2)-R2*(s2_x2-s1[2]*s2[2]+s2_z2)))+s1[1]*s2[1]*(s1_x3*s2[0]*s2[2]+s1[0]*s1[2]*s2[0]*(-s2_x2-s2_y2+(s1[2]-s2[2])*s2[2])+s1_z2*(-2*s2[2]*(s2_x2+s2_y2+s2_z2)+s1[2]*(s2_x2+2*s2_z2))+s1_x2*(-s2[2]*(s2_x2+s2_y2+s2_z2)+s1[2]*(s2_x2+2*s2_z2))+R2*(-s1_x2*s2[2]+s1[0]*s2[0]*(-s1[2]+s2[2])+s1[2]*(s2_x2+2*s2[2]*(-s1[2]+s2[2])))))/(2*(s1[2]*s2[1]-s1[1]*s2[2])*(s1_z2*(s2_x2+s2_y2)-2*s1[0]*s1[2]*s2[0]*s2[2]-2*s1[1]*s2[1]*(s1[0]*s2[0]+s1[2]*s2[2])+s1_y2*(s2_x2+s2_z2)+s1_x2*(s2_y2+s2_z2)))
    z2=(s1[2]**4*s2[1]*(s2_x2+s2_y2)-s1_z3*(s1[0]*s2[0]*s2[1]+s1[1]*(s2_x2+2*s2_y2))*s2[2]+s1_z2*((s1_x2-s1[0]*s2[0]+s1[1]*(s1[1]-s2[1]))*s2[1]*(s2_x2+s2_y2)+R2*s2[1]*(-s1[0]*s2[0]+s2_x2-s1[1]*s2[1]+s2_y2)+(s1[1]-s2[1])*(s1[0]*s2[0]+s1[1]*s2[1])*s2_z2)-d2*(s1[2]*s2[1]-s1[1]*s2[2])*(s1[2]*(s2_x2-s1[1]*s2[1]+s2_y2)+s1_x2*s2[2]+s1[1]*(s1[1]-s2[1])*s2[2]-s1[0]*s2[0]*(s1[2]+s2[2]))+s1[1]*s2_z2*(-R2*(s1_x2-s1[0]*s2[0]+s1[1]*(s1[1]-s2[1]))+(s1_x2+s1_y2)*((s1[0]-s2[0])*s2[0]+(s1[1]-s2[1])*s2[1]-s2_z2))+s1[2]*s2[2]*(-s1_x3*s2[0]*s2[1]+R2*(s1[0]*s2[0]*(s1[1]-s2[1])+s1_x2*s2[1]+s1[1]*(-s2_x2+2*(s1[1]-s2[1])*s2[1]))+s1[0]*s1[1]*s2[0]*(s2_x2-s1[1]*s2[1]+s2_y2+s2_z2)+s1_x2*(-s1[1]*(s2_x2+2*s2_y2)+s2[1]*(s2_x2+s2_y2+s2_z2))+s1_y2*(-s1[1]*(s2_x2+2*s2_y2)+2*s2[1]*(s2_x2+s2_y2+s2_z2)))+s1[1]*s2[0]*dd-s1[0]*s2[1]*dd)/(2*(s1[2]*s2[1]-s1[1]*s2[2])*(s1_z2*(s2_x2+s2_y2)-2*s1[0]*s1[2]*s2[0]*s2[2]-2*s1[1]*s2[1]*(s1[0]*s2[0]+s1[2]*s2[2])+s1_y2*(s2_x2+s2_z2)+s1_x2*(s2_y2+s2_z2)))

    return Vector((x1,y1,z1)),Vector((x2,y2,z2))

def extend_with_unique_vectors(src_list, dst_list, threshold):
    a=0

    same=[d for d in dst_list for s in src_list if (s-d).length<threshold]
    for d in dst_list:
        if not d in same:
            src_list.append(d)
            a=+1

    return a

def spherical_to_cartesian(v):
    return Vector((v[0]*sin(v[1])*cos(v[2]), v[0]*sin(v[1])*sin(v[2]), v[0]*cos(v[1])))

def spheroid(r=1, d=1, sub=(0, 0), u=0.0, v=0.0):
    verts = []
    faces = []

    verts.append(spherical_to_cartesian(Vector((r,u,v))))

    try:
        u1=atan((r**2*(d**2-2*r**2)*cos(pi/2)*sin(u)-sqrt(r**4*cos(u)**2*(-(d**2-2*r**2)**2+4*r**4*(cos(u)**2+cos(pi/2)**2*sin(u)**2))))/(r**2*(d**2-2*r**2)*cos(u)+cos(pi/2)*sqrt(r**4*cos(u)**2*(-(d**2-2*r**2)**2+4*r**4*(cos(u)**2+cos(pi/2)**2*sin(u)**2)))*tan(u)))
    except:
        u1=u
        pass

    verts.append(spherical_to_cartesian(Vector((r,u1,v+pi/2))))

    for i in range(sub[0]*sub[1]):
        i1=i//sub[0]
        i2=len(verts)-1
        v1,v2 = SpheresIntersection(verts[i1],verts[i2],d,r)
        x = extend_with_unique_vectors(verts,[v1,v2],threshold)
        print(i,i1,i2,x,v1,v2)
        for j in range(x):
            faces.append((i2, i1, i2+j))
            print(i,i1,i2,j,faces[-1])

    return verts, faces


class OBJECT_OT_add_spherical_surface(bpy.types.Operator):

    bl_idname = "mesh.add_spherical_surface"
    bl_label = "Spherical surface"
    bl_description = "Add spherical surface"
    bl_options = {'REGISTER', 'UNDO'}

    size = FloatProperty(name = "Size", description = "Radius of the sphere through the vertices",
        min = 0.01, soft_min = 0.01, max = 1000, soft_max = 1000, default = 1.0, step=0.1, subtype='DISTANCE')

    dist = FloatProperty(name = "Distance", description = "Distance between vertices",
        min = 0.01, soft_min = 0.01, max = 1000, soft_max = 1000, default = 1.0, step=0.1, subtype='DISTANCE')

    sub = IntVectorProperty(name = "Subdivisions", description = "Number of faces",
        min = 1, soft_min = 1, max = 1000, soft_max = 1000, default = (1,1), step=1, size=2)

    u = FloatProperty(name = "U", description = "Spherical coordinate U of the first point",
        min = 0.00, soft_min = 0.00, max = pi/3, soft_max = pi/3, default = 0, step=0.1, precision=3, subtype='ANGLE')

    v = FloatProperty(name = "V", description = "Spherical coordinate V of the first point",
        min = 0.00, soft_min = 0.00, max = pi, soft_max = pi, default = 0, step=0.1, precision=3, subtype='ANGLE')

    def execute(self,context):
        # turn off undo for better performance (3-5x faster), also makes sure
        # that mesh ops are undoable and entire script acts as one operator
        bpy.context.user_preferences.edit.use_global_undo = False

        os.system("cls")

        # generate object
        verts, faces = spheroid(self.size, self.dist, self.sub, self.u, self.v)

        # Create new mesh
        mesh = bpy.data.meshes.new("Spherical surface")

        # Make a mesh from a list of verts/edges/faces.
        mesh.from_pydata(verts, [], faces)

        # Update mesh geometry after adding stuff.
        mesh.update(calc_edges=True)

        object_data_add(context, mesh, operator=None)
        # object generation done

        # turn undo back on
        bpy.context.user_preferences.edit.use_global_undo = True

        return {'FINISHED'}


# Register all operators


# This allows you to right click on a button and link to the manual
#def add_spherical_surface_manual_map():
 #   url_manual_prefix = "http://wiki.blender.org/index.php/Doc:2.6/Manual/"
 #   url_manual_mapping = (
 #       ("bpy.ops.mesh.add_spherical_surface", "Modeling/Objects"),
  #      )
  #  return url_manual_prefix, url_manual_mapping

# Define "Extras" menu
def menu_func(self, context):
    self.layout.operator(OBJECT_OT_add_spherical_surface.bl_idname, text="Spherical surface", icon='PLUGIN')

def register():
    bpy.utils.register_class(OBJECT_OT_add_spherical_surface)
    #bpy.utils.register_manual_map(add_spherical_surface_manual_map)

    # Add "Extras" menu to the "Add Mesh" menu
    bpy.types.INFO_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_spherical_surface)
    #bpy.utils.unregister_manual_map(add_spherical_surface_manual_map)

    # Remove "Extras" menu from the "Add Mesh" menu.
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()