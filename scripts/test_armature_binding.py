"""
Test script for automated bone skinning (ARMATURE_AUTO) on base.obj in Blender 4.2 LTS.
"""

import bpy
import math
import os

bpy.ops.wm.read_factory_settings(use_empty=True)

# Import base.obj
base_obj_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\3dobjs\base.obj"
print("Importing base.obj...")
bpy.ops.wm.obj_import(filepath=base_obj_path)
mesh = bpy.context.active_object
mesh.name = "Leo_Mesh"

# Rotate upright and scale to 1.35m boy
mesh.rotation_euler = (math.radians(90), 0, 0)
bpy.ops.object.transform_apply(rotation=True)
mesh.scale = (0.08, 0.08, 0.08)
bpy.ops.object.transform_apply(scale=True)

for p in mesh.data.polygons:
    p.use_smooth = True

print(f"Mesh ready: {len(mesh.data.vertices)} vertices, {len(mesh.data.polygons)} polygons.")

# Create matching armature
arm_data = bpy.data.armatures.new("LeoRigData")
arm_obj = bpy.data.objects.new("LeoRig", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='EDIT')

# Pelvis & Spine
root = arm_data.edit_bones.new("root")
root.head = (0, 0, 0)
root.tail = (0, 0, 0.1)

hips = arm_data.edit_bones.new("hips")
hips.parent = root
hips.head = (0, 0, 0.72)
hips.tail = (0, 0, 0.84)

spine = arm_data.edit_bones.new("spine")
spine.parent = hips
spine.head = (0, 0, 0.84)
spine.tail = (0, 0, 1.05)

neck = arm_data.edit_bones.new("neck")
neck.parent = spine
neck.head = (0, 0, 1.05)
neck.tail = (0, 0, 1.15)

head = arm_data.edit_bones.new("head")
head.parent = neck
head.head = (0, 0, 1.15)
head.tail = (0, 0, 1.38)

# Left Arm & Hand
shoulder_l = arm_data.edit_bones.new("shoulder.L")
shoulder_l.parent = spine
shoulder_l.head = (0.05, 0, 1.05)
shoulder_l.tail = (0.14, 0, 1.05)

arm_l = arm_data.edit_bones.new("upper_arm.L")
arm_l.parent = shoulder_l
arm_l.head = (0.14, 0, 1.05)
arm_l.tail = (0.32, 0, 0.88)

forearm_l = arm_data.edit_bones.new("forearm.L")
forearm_l.parent = arm_l
forearm_l.head = (0.32, 0, 0.88)
forearm_l.tail = (0.48, 0, 0.74)

hand_l = arm_data.edit_bones.new("hand.L")
hand_l.parent = forearm_l
hand_l.head = (0.48, 0, 0.74)
hand_l.tail = (0.58, 0, 0.68)

# Right Arm & Hand
shoulder_r = arm_data.edit_bones.new("shoulder.R")
shoulder_r.parent = spine
shoulder_r.head = (-0.05, 0, 1.05)
shoulder_r.tail = (-0.14, 0, 1.05)

arm_r = arm_data.edit_bones.new("upper_arm.R")
arm_r.parent = shoulder_r
arm_r.head = (-0.14, 0, 1.05)
arm_r.tail = (-0.32, 0, 0.88)

forearm_r = arm_data.edit_bones.new("forearm.R")
forearm_r.parent = arm_r
forearm_r.head = (-0.32, 0, 0.88)
forearm_r.tail = (-0.48, 0, 0.74)

hand_r = arm_data.edit_bones.new("hand.R")
hand_r.parent = forearm_r
hand_r.head = (-0.48, 0, 0.74)
hand_r.tail = (-0.58, 0, 0.68)

# Legs
thigh_l = arm_data.edit_bones.new("thigh.L")
thigh_l.parent = hips
thigh_l.head = (0.10, 0, 0.72)
thigh_l.tail = (0.10, 0, 0.38)

shin_l = arm_data.edit_bones.new("shin.L")
shin_l.parent = thigh_l
shin_l.head = (0.10, 0, 0.38)
shin_l.tail = (0.10, 0, 0.08)

foot_l = arm_data.edit_bones.new("foot.L")
foot_l.parent = shin_l
foot_l.head = (0.10, 0, 0.08)
foot_l.tail = (0.10, 0.14, 0.02)

thigh_r = arm_data.edit_bones.new("thigh.R")
thigh_r.parent = hips
thigh_r.head = (-0.10, 0, 0.72)
thigh_r.tail = (-0.10, 0, 0.38)

shin_r = arm_data.edit_bones.new("shin.R")
shin_r.parent = thigh_r
shin_r.head = (-0.10, 0, 0.38)
shin_r.tail = (-0.10, 0, 0.08)

foot_r = arm_data.edit_bones.new("foot.R")
foot_r.parent = shin_r
foot_r.head = (-0.10, 0, 0.08)
foot_r.tail = (-0.10, 0.14, 0.02)

bpy.ops.object.mode_set(mode='OBJECT')

print("Binding mesh to armature with ARMATURE_AUTO...")
bpy.ops.object.select_all(action='DESELECT')
mesh.select_set(True)
arm_obj.select_set(True)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
print("Armature binding complete! Total vertex groups:", len(mesh.vertex_groups))
