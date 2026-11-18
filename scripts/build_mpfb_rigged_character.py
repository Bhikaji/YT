"""
Builds official MPFB2 Mixamo-Rigged Character in Blender 4.2 LTS
Imports base.obj, creates 52 Mixamo bones from vertex anchors, and applies exact weights.
"""

import bpy
import json
import math
import os
from pathlib import Path

def build_character(scale_factor=0.082):
    # Clear scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # 1. Import base.obj
    base_obj_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\3dobjs\base.obj"
    print("Importing base.obj...")
    bpy.ops.wm.obj_import(filepath=base_obj_path)
    mesh = bpy.context.active_object
    mesh.name = "Leo_Body"
    
    # Rotate upright and scale
    mesh.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    mesh.scale = (scale_factor, scale_factor, scale_factor)
    bpy.ops.object.transform_apply(scale=True)
    
    for p in mesh.data.polygons:
        p.use_smooth = True
        
    v_coords = [v.co.copy() for v in mesh.data.vertices]
    
    # 2. Load rig definition
    rig_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\rigs\standard\rig.mixamo.json"
    with open(rig_path, 'r', encoding='utf-8') as f:
        rig_data = json.load(f)["bones"]
        
    print(f"Building armature with {len(rig_data)} Mixamo bones...")
    arm_data = bpy.data.armatures.new("Leo_Armature_Data")
    arm_obj = bpy.data.objects.new("Leo_Armature", arm_data)
    bpy.context.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Helper to calculate position from strategy
    def get_pos(spec):
        if spec.get("strategy") == "MEAN" and "vertex_indices" in spec:
            indices = spec["vertex_indices"]
            avg_x = sum(v_coords[i].x for i in indices) / len(indices)
            avg_y = sum(v_coords[i].y for i in indices) / len(indices)
            avg_z = sum(v_coords[i].z for i in indices) / len(indices)
            return (avg_x, avg_y, avg_z)
        else:
            p = spec["default_position"]
            # Convert default position from raw decimeters to meters scaled
            return (p[0] * scale_factor * 10, -p[2] * scale_factor * 10, p[1] * scale_factor * 10)

    # First pass: Create edit bones
    edit_bones = {}
    for bone_name, bone_spec in rig_data.items():
        eb = arm_data.edit_bones.new(bone_name)
        eb.head = get_pos(bone_spec["head"])
        eb.tail = get_pos(bone_spec["tail"])
        if (eb.head - eb.tail).length < 0.001:
            eb.tail.z += 0.02
        eb.roll = bone_spec.get("roll", 0.0)
        edit_bones[bone_name] = eb
        
    # Second pass: Set parenting
    for bone_name, bone_spec in rig_data.items():
        parent_name = bone_spec.get("parent")
        if parent_name and parent_name in edit_bones:
            edit_bones[bone_name].parent = edit_bones[parent_name]
            edit_bones[bone_name].use_connect = bone_spec.get("use_connect", False)
            
    bpy.ops.object.mode_set(mode='OBJECT')
    print("Armature bones assembled successfully!")
    
    # 3. Load & Apply exact vertex weights
    weights_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\rigs\standard\weights.mixamo.json"
    with open(weights_path, 'r', encoding='utf-8') as f:
        weights_data = json.load(f)["weights"]
        
    print(f"Applying precalculated vertex weights for {len(weights_data)} groups...")
    for group_name, weight_list in weights_data.items():
        vg = mesh.vertex_groups.new(name=group_name)
        for vert_idx, w_val in weight_list:
            if vert_idx < len(mesh.data.vertices):
                vg.add([vert_idx], float(w_val), 'REPLACE')
                
    # Add Armature Modifier
    arm_mod = mesh.modifiers.new(name="Armature", type='ARMATURE')
    arm_mod.object = arm_obj
    arm_mod.use_vertex_groups = True
    
    print("Character mesh successfully skinned to Mixamo armature!")
    return mesh, arm_obj

if __name__ == "__main__":
    build_character()
    print("Test build complete.")
