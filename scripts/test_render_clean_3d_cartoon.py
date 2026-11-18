"""
Test Script: Generate Polished 3D Cartoon Scene & Render Verification Frames
Tests Leo character, Lumi companion, 3D environment, and lighting in Blender 4.2 LTS.
"""

import bpy
import bmesh
import math
import os
import sys

def build_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    
    # 1. Render Settings
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920
    scene.render.resolution_percentage = 100
    scene.render.fps = 30
    scene.frame_start = 1
    scene.frame_end = 300
    
    if hasattr(scene, "eevee"):
        scene.eevee.taa_render_samples = 16
        
    # AgX Color Management
    if 'AgX' in [c.name for c in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items]:
        scene.view_settings.view_transform = 'AgX'
        scene.view_settings.look = 'Medium High Contrast'
    else:
        scene.view_settings.view_transform = 'Filmic'
        
    world = bpy.data.worlds.new("EnchantedWorld")
    scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.015, 0.02, 0.045, 1.0)
        bg_node.inputs['Strength'].default_value = 0.6
        
    # Helper to create PBR material
    def create_pbr_mat(name, base_color, roughness=0.4, metallic=0.0, sss=0.0, sss_color=None, emission=None, emission_strength=1.0):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = base_color
            bsdf.inputs['Roughness'].default_value = roughness
            bsdf.inputs['Metallic'].default_value = metallic
            if sss > 0:
                if 'Subsurface Weight' in bsdf.inputs:
                    bsdf.inputs['Subsurface Weight'].default_value = sss
                    if sss_color and 'Subsurface Radius' in bsdf.inputs:
                        bsdf.inputs['Subsurface Radius'].default_value = sss_color
                elif 'Subsurface' in bsdf.inputs:
                    bsdf.inputs['Subsurface'].default_value = sss
            if emission:
                if 'Emission Color' in bsdf.inputs:
                    bsdf.inputs['Emission Color'].default_value = emission
                    bsdf.inputs['Emission Strength'].default_value = emission_strength
        return mat

    # Materials
    mat_skin = create_pbr_mat("Leo_Skin", (0.95, 0.76, 0.65, 1.0), roughness=0.32, sss=0.25, sss_color=(1.0, 0.4, 0.2))
    mat_hoodie = create_pbr_mat("Leo_Hoodie", (0.85, 0.12, 0.12, 1.0), roughness=0.65)
    mat_hoodie_dark = create_pbr_mat("Leo_HoodieTrim", (0.65, 0.08, 0.08, 1.0), roughness=0.7)
    mat_white_cord = create_pbr_mat("Leo_WhiteCord", (0.95, 0.95, 0.95, 1.0), roughness=0.5)
    mat_jeans = create_pbr_mat("Leo_Jeans", (0.12, 0.22, 0.42, 1.0), roughness=0.55)
    mat_leather_boot = create_pbr_mat("Leo_Boots", (0.24, 0.14, 0.08, 1.0), roughness=0.45)
    mat_boot_rubber = create_pbr_mat("Leo_BootSole", (0.08, 0.08, 0.09, 1.0), roughness=0.6)
    mat_hair = create_pbr_mat("Leo_AuburnHair", (0.28, 0.13, 0.06, 1.0), roughness=0.35)
    mat_eyebrows = create_pbr_mat("Leo_Eyebrows", (0.18, 0.08, 0.04, 1.0), roughness=0.5)
    mat_sclera = create_pbr_mat("Eye_Sclera", (0.98, 0.98, 0.98, 1.0), roughness=0.08)
    mat_iris = create_pbr_mat("Eye_Iris", (0.05, 0.48, 0.95, 1.0), roughness=0.04)
    mat_pupil = create_pbr_mat("Eye_Pupil", (0.01, 0.01, 0.01, 1.0), roughness=0.02)
    mat_mouth_inside = create_pbr_mat("Mouth_Inside", (0.45, 0.08, 0.10, 1.0), roughness=0.3)
    mat_teeth = create_pbr_mat("Teeth", (0.95, 0.95, 0.92, 1.0), roughness=0.1)

    mat_stone_bridge = create_pbr_mat("StoneBridge", (0.25, 0.28, 0.32, 1.0), roughness=0.68)
    mat_bridge_gold = create_pbr_mat("BridgeGoldRune", (0.85, 0.70, 0.20, 1.0), roughness=0.25, metallic=0.8, emission=(0.95, 0.80, 0.25, 1.0), emission_strength=1.5)
    mat_cyan_crystal = create_pbr_mat("CyanCrystal", (0.15, 0.85, 1.0, 1.0), roughness=0.15, emission=(0.10, 0.85, 1.0, 1.0), emission_strength=3.0)
    mat_shroom_cap_teal = create_pbr_mat("ShroomCapTeal", (0.08, 0.72, 0.70, 1.0), roughness=0.4, emission=(0.05, 0.75, 0.72, 1.0), emission_strength=2.2)
    mat_shroom_cap_purple = create_pbr_mat("ShroomCapPurple", (0.68, 0.18, 0.82, 1.0), roughness=0.4, emission=(0.72, 0.20, 0.88, 1.0), emission_strength=2.5)
    mat_shroom_stem = create_pbr_mat("ShroomStem", (0.18, 0.24, 0.28, 1.0), roughness=0.6)
    
    mat_lumi_fur = create_pbr_mat("Lumi_Fur", (0.98, 0.45, 0.18, 1.0), roughness=0.55)
    mat_lumi_white = create_pbr_mat("Lumi_White", (0.95, 0.95, 0.95, 1.0), roughness=0.5)
    mat_lumi_glow = create_pbr_mat("Lumi_CyanGlow", (0.2, 0.95, 1.0, 1.0), roughness=0.15, emission=(0.2, 0.95, 1.0, 1.0), emission_strength=4.0)

    # -------------------------------------------------------------
    # 2. Build Armature for Leo (Mixamo UHD-54 standard)
    # Ground at Z = 0.0
    # -------------------------------------------------------------
    arm_data = bpy.data.armatures.new("Leo_Rig_Data")
    arm_obj = bpy.data.objects.new("Leo_Rig", arm_data)
    bpy.context.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    bones = {}
    
    # Root bone at ground
    root = arm_data.edit_bones.new("mixamorig:Hips_Root")
    root.head = (0, 0, 0)
    root.tail = (0, 0, 0.1)
    bones["mixamorig:Hips_Root"] = root
    
    # Hips at Z = 0.68 (Leo is ~1.25m tall child)
    hips = arm_data.edit_bones.new("mixamorig:Hips")
    hips.head = (0, 0, 0.68)
    hips.tail = (0, 0, 0.77)
    hips.parent = root
    bones["mixamorig:Hips"] = hips
    
    spine = arm_data.edit_bones.new("mixamorig:Spine")
    spine.head = (0, 0, 0.77)
    spine.tail = (0, 0, 0.87)
    spine.parent = hips
    bones["mixamorig:Spine"] = spine
    
    spine1 = arm_data.edit_bones.new("mixamorig:Spine1")
    spine1.head = (0, 0, 0.87)
    spine1.tail = (0, 0, 0.97)
    spine1.parent = spine
    bones["mixamorig:Spine1"] = spine1
    
    neck = arm_data.edit_bones.new("mixamorig:Neck")
    neck.head = (0, 0, 0.97)
    neck.tail = (0, 0, 1.03)
    neck.parent = spine1
    bones["mixamorig:Neck"] = neck
    
    head = arm_data.edit_bones.new("mixamorig:Head")
    head.head = (0, 0, 1.03)
    head.tail = (0, 0, 1.25)
    head.parent = neck
    bones["mixamorig:Head"] = head
    
    # Legs (Hips -> UpLeg -> Leg -> Foot -> Toe)
    for side, sgn in [("Left", 1), ("Right", -1)]:
        upleg = arm_data.edit_bones.new(f"mixamorig:{side}UpLeg")
        upleg.head = (sgn * 0.10, 0, 0.67)
        upleg.tail = (sgn * 0.10, 0, 0.36)
        upleg.parent = hips
        bones[f"mixamorig:{side}UpLeg"] = upleg
        
        leg = arm_data.edit_bones.new(f"mixamorig:{side}Leg")
        leg.head = (sgn * 0.10, 0, 0.36)
        leg.tail = (sgn * 0.10, 0, 0.10)
        leg.parent = upleg
        bones[f"mixamorig:{side}Leg"] = leg
        
        foot = arm_data.edit_bones.new(f"mixamorig:{side}Foot")
        foot.head = (sgn * 0.10, 0, 0.10)
        foot.tail = (sgn * 0.10, -0.10, 0.02)
        foot.parent = leg
        bones[f"mixamorig:{side}Foot"] = foot
        
        toe = arm_data.edit_bones.new(f"mixamorig:{side}ToeBase")
        toe.head = (sgn * 0.10, -0.10, 0.02)
        toe.tail = (sgn * 0.10, -0.16, 0.02)
        toe.parent = foot
        bones[f"mixamorig:{side}ToeBase"] = toe
        
    # Arms (Spine1 -> Shoulder -> Arm -> ForeArm -> Hand)
    for side, sgn in [("Left", 1), ("Right", -1)]:
        sh = arm_data.edit_bones.new(f"mixamorig:{side}Shoulder")
        sh.head = (sgn * 0.04, 0, 0.95)
        sh.tail = (sgn * 0.14, 0, 0.95)
        sh.parent = spine1
        bones[f"mixamorig:{side}Shoulder"] = sh
        
        arm = arm_data.edit_bones.new(f"mixamorig:{side}Arm")
        arm.head = (sgn * 0.14, 0, 0.95)
        arm.tail = (sgn * 0.28, 0, 0.76)
        arm.parent = sh
        bones[f"mixamorig:{side}Arm"] = arm
        
        farm = arm_data.edit_bones.new(f"mixamorig:{side}ForeArm")
        farm.head = (sgn * 0.28, 0, 0.76)
        farm.tail = (sgn * 0.38, -0.04, 0.58)
        farm.parent = arm
        bones[f"mixamorig:{side}ForeArm"] = farm
        
        hand = arm_data.edit_bones.new(f"mixamorig:{side}Hand")
        hand.head = (sgn * 0.38, -0.04, 0.58)
        hand.tail = (sgn * 0.43, -0.06, 0.50)
        hand.parent = farm
        bones[f"mixamorig:{side}Hand"] = hand

    bpy.ops.object.mode_set(mode='OBJECT')

    # Helper function to bind mesh to armature bone
    def bind_to_armature(obj, vertex_weights=None, parent_bone=None):
        if parent_bone:
            obj.parent = arm_obj
            obj.parent_type = 'BONE'
            obj.parent_bone = parent_bone
        else:
            mod = obj.modifiers.new(name="Armature", type='ARMATURE')
            mod.object = arm_obj
            mod.use_vertex_groups = True
            if vertex_weights:
                for b_name, v_indices in vertex_weights.items():
                    vg = obj.vertex_groups.new(name=b_name)
                    vg.add(v_indices, 1.0, 'REPLACE')

    # -------------------------------------------------------------
    # 3. Model Stylized Cartoon Boy Mesh (Leo)
    # -------------------------------------------------------------
    
    # 3.1 Head (Stylized Pixar Child Head)
    head_z = 1.12
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=0.135, location=(0, -0.02, head_z))
    head_obj = bpy.context.active_object
    head_obj.name = "Leo_Head"
    head_obj.scale = (1.02, 1.08, 1.04)
    bpy.ops.object.transform_apply(scale=True)
    head_obj.data.materials.append(mat_skin)
    for p in head_obj.data.polygons:
        p.use_smooth = True
        
    # Sculpt cheek fullness / chin
    bm = bmesh.new()
    bm.from_mesh(head_obj.data)
    for v in bm.verts:
        # Pout/cheeks
        if v.co.y < -0.02 and v.co.z < head_z + 0.02:
            # Expand cheeks slightly
            if abs(v.co.x) > 0.05:
                v.co.x *= 1.10
                v.co.y *= 1.06
        # Chin
        if v.co.y < -0.04 and v.co.z < head_z - 0.07:
            v.co.y *= 1.12
            v.co.z -= 0.015
    bm.to_mesh(head_obj.data)
    bm.free()
    
    # Head Shapekeys (Facial Animation)
    head_obj.shape_key_add(name="Basis", from_mix=False)
    
    # Shapekey: Smile
    sk_smile = head_obj.shape_key_add(name="Smile", from_mix=False)
    for v in sk_smile.data:
        if v.co.y < -0.08 and abs(v.co.x) < 0.07 and head_z - 0.07 < v.co.z < head_z - 0.02:
            v.co.z += 0.012
            v.co.x *= 1.12
            
    # Shapekey: Mouth Open (Aperture / Speech)
    sk_mouth = head_obj.shape_key_add(name="Mouth_Open", from_mix=False)
    for v in sk_mouth.data:
        if v.co.y < -0.07 and abs(v.co.x) < 0.045 and head_z - 0.09 < v.co.z < head_z - 0.03:
            v.co.z -= 0.028
            v.co.y += 0.015
            
    # Shapekey: Wonder Brows
    sk_wonder = head_obj.shape_key_add(name="Brow_Wonder", from_mix=False)
    for v in sk_wonder.data:
        if v.co.y < -0.08 and abs(v.co.x) < 0.08 and head_z + 0.02 < v.co.z < head_z + 0.08:
            v.co.z += 0.022
            v.co.y -= 0.008

    bind_to_armature(head_obj, parent_bone="mixamorig:Head")
    
    # 3.2 Cartoon Eyes (Left & Right)
    # Eyeball with Sclera, Iris, Pupil
    eye_z = head_z + 0.015
    eye_y = -0.118
    eye_x = 0.048
    
    for side, sgn in [("L", 1), ("R", -1)]:
        # Sclera
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=18, radius=0.034, location=(sgn * eye_x, eye_y, eye_z))
        eye_obj = bpy.context.active_object
        eye_obj.name = f"Leo_Eye_{side}"
        eye_obj.rotation_euler = (math.radians(-90), 0, math.radians(sgn * 8))
        bpy.ops.object.transform_apply(rotation=True)
        eye_obj.data.materials.append(mat_sclera)
        for p in eye_obj.data.polygons:
            p.use_smooth = True
            
        # Iris disc
        bpy.ops.mesh.primitive_circle_add(vertices=24, radius=0.019, fill_type='NGON', location=(sgn * eye_x, eye_y - 0.032, eye_z))
        iris_obj = bpy.context.active_object
        iris_obj.name = f"Leo_Iris_{side}"
        iris_obj.rotation_euler = (math.radians(90), 0, 0)
        bpy.ops.object.transform_apply(rotation=True)
        iris_obj.data.materials.append(mat_iris)
        
        # Pupil disc
        bpy.ops.mesh.primitive_circle_add(vertices=18, radius=0.009, fill_type='NGON', location=(sgn * eye_x, eye_y - 0.0325, eye_z))
        pupil_obj = bpy.context.active_object
        pupil_obj.name = f"Leo_Pupil_{side}"
        pupil_obj.rotation_euler = (math.radians(90), 0, 0)
        bpy.ops.object.transform_apply(rotation=True)
        pupil_obj.data.materials.append(mat_pupil)
        
        # Eyebrows (Stylized Curved Geometry)
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.007, depth=0.052, location=(sgn * (eye_x + 0.005), eye_y - 0.015, eye_z + 0.042))
        brow_obj = bpy.context.active_object
        brow_obj.name = f"Leo_Brow_{side}"
        brow_obj.rotation_euler = (0, math.radians(sgn * 78), math.radians(sgn * -12))
        brow_obj.scale = (1.0, 1.4, 0.7)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        brow_obj.data.materials.append(mat_eyebrows)
        for p in brow_obj.data.polygons:
            p.use_smooth = True
            
        # Eyelids for Blinking
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.036, location=(sgn * eye_x, eye_y, eye_z))
        eyelid_obj = bpy.context.active_object
        eyelid_obj.name = f"Leo_Eyelid_{side}"
        eyelid_obj.scale = (1.02, 1.05, 0.2)
        bpy.ops.object.transform_apply(scale=True)
        eyelid_obj.data.materials.append(mat_skin)
        for p in eyelid_obj.data.polygons:
            p.use_smooth = True
        eyelid_obj.location.z += 0.025  # Rest open
        
        # Add blink shapekey to eyelid
        eyelid_obj.shape_key_add(name="Basis", from_mix=False)
        sk_blink = eyelid_obj.shape_key_add(name="Blink", from_mix=False)
        for v in sk_blink.data:
            v.co.z -= 0.038
            
        bind_to_armature(eye_obj, parent_bone="mixamorig:Head")
        bind_to_armature(iris_obj, parent_bone="mixamorig:Head")
        bind_to_armature(pupil_obj, parent_bone="mixamorig:Head")
        bind_to_armature(brow_obj, parent_bone="mixamorig:Head")
        bind_to_armature(eyelid_obj, parent_bone="mixamorig:Head")

    # 3.3 Stylized 3D Hair (Hero Spiky/Flowing Locks - Pixar Luca / Dash style)
    # Base hair volume cap
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, radius=0.144, location=(0, 0.015, head_z + 0.025))
    hair_cap = bpy.context.active_object
    hair_cap.name = "Leo_HairCap"
    hair_cap.scale = (1.03, 1.08, 0.96)
    bpy.ops.object.transform_apply(scale=True)
    hair_cap.data.materials.append(mat_hair)
    for p in hair_cap.data.polygons:
        p.use_smooth = True
    bind_to_armature(hair_cap, parent_bone="mixamorig:Head")
    
    # 6 Swept Stylized Hair Strands/Tufts across forehead & crown
    locks_data = [
        # (x, y, z, rot_x, rot_y, rot_z, scale_x, scale_y, scale_z)
        (0.00, -0.11, head_z + 0.11, 25, 0, -10, 0.038, 0.09, 0.032),   # Center Bang
        (-0.05, -0.10, head_z + 0.10, 20, -18, -30, 0.034, 0.08, 0.028), # Left Bang
        (0.06, -0.09, head_z + 0.10, 22, 18, 25, 0.035, 0.085, 0.030),  # Right Bang
        (-0.08, -0.04, head_z + 0.07, 10, -35, -45, 0.028, 0.07, 0.025), # Left Temple Lock
        (0.08, -0.03, head_z + 0.07, 12, 35, 45, 0.028, 0.07, 0.025),   # Right Temple Lock
        (0.02, 0.04, head_z + 0.15, -15, 8, -5, 0.042, 0.09, 0.038),    # Crown Crest
        (-0.04, 0.08, head_z + 0.13, -25, -12, -15, 0.038, 0.085, 0.035) # Back Volume
    ]
    
    for idx, (lx, ly, lz, rx, ry, rz, sx, sy, sz) in enumerate(locks_data):
        bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=1.0, radius2=0.1, depth=2.0, location=(lx, ly, lz))
        lock = bpy.context.active_object
        lock.name = f"Leo_HairLock_{idx}"
        lock.rotation_euler = (math.radians(rx), math.radians(ry), math.radians(rz))
        lock.scale = (sx, sy, sz)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        lock.data.materials.append(mat_hair)
        for p in lock.data.polygons:
            p.use_smooth = True
        bind_to_armature(lock, parent_bone="mixamorig:Head")

    # 3.4 Genuine 3D Crimson Hoodie
    # Torso Cylinder with hood collar, hem, pouch pocket
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.155, depth=0.38, location=(0, 0, 0.81))
    hoodie_body = bpy.context.active_object
    hoodie_body.name = "Leo_Hoodie_Torso"
    hoodie_body.scale = (1.08, 0.88, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    hoodie_body.data.materials.append(mat_hoodie)
    for p in hoodie_body.data.polygons:
        p.use_smooth = True
    bind_to_armature(hoodie_body, parent_bone="mixamorig:Spine")
    
    # 3D Draped Hood mesh on the back of the neck
    bpy.ops.mesh.primitive_torus_add(major_radius=0.13, minor_radius=0.032, location=(0, 0.04, 0.98))
    hood_mesh = bpy.context.active_object
    hood_mesh.name = "Leo_Hood_Collar"
    hood_mesh.rotation_euler = (math.radians(-25), 0, 0)
    hood_mesh.scale = (1.1, 1.25, 0.85)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    hood_mesh.data.materials.append(mat_hoodie_dark)
    for p in hood_mesh.data.polygons:
        p.use_smooth = True
    bind_to_armature(hood_mesh, parent_bone="mixamorig:Spine1")
    
    # Hanging white drawstrings
    for ds_sgn in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.005, depth=0.14, location=(ds_sgn * 0.045, -0.14, 0.88))
        cord = bpy.context.active_object
        cord.name = f"Leo_Drawstring_{ds_sgn}"
        cord.rotation_euler = (math.radians(-8), math.radians(ds_sgn * 4), 0)
        cord.data.materials.append(mat_white_cord)
        bind_to_armature(cord, parent_bone="mixamorig:Spine1")

    # Kangaroo Pouch Pocket on front
    bpy.ops.mesh.primitive_cube_add(size=0.14, location=(0, -0.135, 0.72))
    pocket = bpy.context.active_object
    pocket.name = "Leo_KangarooPocket"
    pocket.scale = (1.1, 0.2, 0.7)
    bpy.ops.object.transform_apply(scale=True)
    pocket.data.materials.append(mat_hoodie_dark)
    bind_to_armature(pocket, parent_bone="mixamorig:Spine")

    # 3.5 Arms and Hands
    for side, sgn in [("Left", 1), ("Right", -1)]:
        # Upper arm sleeve
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.048, depth=0.22, location=(sgn * 0.20, 0, 0.86))
        uarm_mesh = bpy.context.active_object
        uarm_mesh.name = f"Leo_Sleeve_Upper_{side}"
        uarm_mesh.rotation_euler = (0, math.radians(sgn * 42), 0)
        uarm_mesh.data.materials.append(mat_hoodie)
        for p in uarm_mesh.data.polygons:
            p.use_smooth = True
        bind_to_armature(uarm_mesh, parent_bone=f"mixamorig:{side}Arm")
        
        # Forearm sleeve
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.042, depth=0.20, location=(sgn * 0.33, -0.02, 0.67))
        farm_mesh = bpy.context.active_object
        farm_mesh.name = f"Leo_Sleeve_Lower_{side}"
        farm_mesh.rotation_euler = (math.radians(10), math.radians(sgn * 32), 0)
        farm_mesh.data.materials.append(mat_hoodie)
        for p in farm_mesh.data.polygons:
            p.use_smooth = True
        bind_to_armature(farm_mesh, parent_bone=f"mixamorig:{side}ForeArm")
        
        # 3D Stylized Cartoon Hand with Fingers
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.042, location=(sgn * 0.40, -0.05, 0.54))
        palm_mesh = bpy.context.active_object
        palm_mesh.name = f"Leo_Palm_{side}"
        palm_mesh.scale = (0.9, 1.2, 0.7)
        bpy.ops.object.transform_apply(scale=True)
        palm_mesh.data.materials.append(mat_skin)
        for p in palm_mesh.data.polygons:
            p.use_smooth = True
            
        # Pointing Index Finger / Grip Fingers
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.011, depth=0.048, location=(sgn * 0.43, -0.10, 0.53))
        finger = bpy.context.active_object
        finger.name = f"Leo_IndexFinger_{side}"
        finger.rotation_euler = (math.radians(75), 0, math.radians(sgn * 15))
        finger.data.materials.append(mat_skin)
        for p in finger.data.polygons:
            p.use_smooth = True
            
        bind_to_armature(palm_mesh, parent_bone=f"mixamorig:{side}Hand")
        bind_to_armature(finger, parent_bone=f"mixamorig:{side}Hand")

    # 3.6 Denim Jeans (Legs)
    for side, sgn in [("Left", 1), ("Right", -1)]:
        # Thigh / Upper Leg
        bpy.ops.mesh.primitive_cylinder_add(vertices=18, radius=0.064, depth=0.32, location=(sgn * 0.10, 0, 0.52))
        thigh = bpy.context.active_object
        thigh.name = f"Leo_Thigh_{side}"
        thigh.data.materials.append(mat_jeans)
        for p in thigh.data.polygons:
            p.use_smooth = True
        bind_to_armature(thigh, parent_bone=f"mixamorig:{side}UpLeg")
        
        # Shin / Lower Leg
        bpy.ops.mesh.primitive_cylinder_add(vertices=18, radius=0.058, depth=0.28, location=(sgn * 0.10, 0, 0.24))
        shin = bpy.context.active_object
        shin.name = f"Leo_Shin_{side}"
        shin.data.materials.append(mat_jeans)
        for p in shin.data.polygons:
            p.use_smooth = True
        bind_to_armature(shin, parent_bone=f"mixamorig:{side}Leg")

    # 3.7 Adventure Boots (Fitted firmly at Z = 0.0)
    for side, sgn in [("Left", 1), ("Right", -1)]:
        # Boot Rubber Sole at Z = 0.015 (Floor is Z = 0.0)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sgn * 0.10, -0.05, 0.022))
        sole = bpy.context.active_object
        sole.name = f"Leo_BootSole_{side}"
        sole.scale = (0.10, 0.22, 0.044)
        bpy.ops.object.transform_apply(scale=True)
        sole.data.materials.append(mat_boot_rubber)
        bind_to_armature(sole, parent_bone=f"mixamorig:{side}Foot")
        
        # Boot Leather Upper
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.062, location=(sgn * 0.10, -0.05, 0.075))
        upper = bpy.context.active_object
        upper.name = f"Leo_BootUpper_{side}"
        upper.scale = (0.9, 1.4, 0.9)
        bpy.ops.object.transform_apply(scale=True)
        upper.data.materials.append(mat_leather_boot)
        for p in upper.data.polygons:
            p.use_smooth = True
        bind_to_armature(upper, parent_bone=f"mixamorig:{side}Foot")

    # -------------------------------------------------------------
    # 4. Companion Lumi (Magical Fox Creature)
    # -------------------------------------------------------------
    lumi_root = bpy.data.objects.new("Lumi_Root", None)
    bpy.context.collection.objects.link(lumi_root)
    lumi_root.location = (0.42, -0.65, 0.0)  # Beside Leo on the bridge
    
    # Lumi Body (Z = 0.20 off the floor)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.13, location=(0, 0, 0.20))
    lumi_body = bpy.context.active_object
    lumi_body.name = "Lumi_Body"
    lumi_body.scale = (0.85, 1.35, 0.95)
    bpy.ops.object.transform_apply(scale=True)
    lumi_body.data.materials.append(mat_lumi_fur)
    for p in lumi_body.data.polygons:
        p.use_smooth = True
    lumi_body.parent = lumi_root
    
    # Lumi Chest / Bib (White Fur)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=10, radius=0.08, location=(0, -0.10, 0.22))
    lumi_chest = bpy.context.active_object
    lumi_chest.name = "Lumi_Chest"
    lumi_chest.scale = (0.7, 0.5, 1.1)
    bpy.ops.object.transform_apply(scale=True)
    lumi_chest.data.materials.append(mat_lumi_white)
    for p in lumi_chest.data.polygons:
        p.use_smooth = True
    lumi_chest.parent = lumi_body

    # Lumi Head
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.11, location=(0, -0.16, 0.32))
    lumi_head = bpy.context.active_object
    lumi_head.name = "Lumi_Head"
    lumi_head.scale = (1.05, 1.0, 0.95)
    bpy.ops.object.transform_apply(scale=True)
    lumi_head.data.materials.append(mat_lumi_fur)
    for p in lumi_head.data.polygons:
        p.use_smooth = True
    lumi_head.parent = lumi_root

    # Snout & Cute Nose
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.048, depth=0.10, location=(0, -0.25, 0.29))
    lumi_snout = bpy.context.active_object
    lumi_snout.name = "Lumi_Snout"
    lumi_snout.rotation_euler = (math.radians(-85), 0, 0)
    lumi_snout.data.materials.append(mat_lumi_white)
    for p in lumi_snout.data.polygons:
        p.use_smooth = True
    lumi_snout.parent = lumi_head

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.015, location=(0, -0.30, 0.30))
    lumi_nose = bpy.context.active_object
    lumi_nose.name = "Lumi_Nose"
    lumi_nose.data.materials.append(mat_pupil)
    lumi_nose.parent = lumi_snout

    # Cute Big Cartoon Eyes
    for sgn in [-1, 1]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=10, radius=0.024, location=(sgn * 0.052, -0.22, 0.34))
        l_eye = bpy.context.active_object
        l_eye.name = f"Lumi_Eye_{sgn}"
        l_eye.data.materials.append(mat_pupil)
        l_eye.parent = lumi_head
        
        # White highlight shine
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.007, location=(sgn * 0.048, -0.24, 0.35))
        l_shine = bpy.context.active_object
        l_shine.data.materials.append(mat_sclera)
        l_shine.parent = l_eye

    # Glowing Cyan Fox Ears
    for sgn in [-1, 1]:
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.052, depth=0.16, location=(sgn * 0.075, -0.14, 0.44))
        ear = bpy.context.active_object
        ear.name = f"Lumi_Ear_{sgn}"
        ear.rotation_euler = (math.radians(-15), math.radians(sgn * 28), 0)
        ear.scale = (0.7, 1.1, 1.0)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        ear.data.materials.append(mat_lumi_fur)
        ear.parent = lumi_head
        
        # Inner Glowing Cyan Tuft
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.035, depth=0.12, location=(sgn * 0.072, -0.16, 0.44))
        ear_glow = bpy.context.active_object
        ear_glow.rotation_euler = (math.radians(-15), math.radians(sgn * 28), 0)
        ear_glow.scale = (0.5, 0.7, 0.9)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        ear_glow.data.materials.append(mat_lumi_glow)
        ear_glow.parent = ear

    # 4 Legs with Paws Planted at Z = 0.0
    for lx, ly in [(-0.08, 0.08), (0.08, 0.08), (-0.08, -0.10), (0.08, -0.10)]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.026, depth=0.18, location=(lx, ly, 0.09))
        lumi_leg = bpy.context.active_object
        lumi_leg.data.materials.append(mat_lumi_fur)
        for p in lumi_leg.data.polygons:
            p.use_smooth = True
        lumi_leg.parent = lumi_root
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.032, location=(lx, ly - 0.02, 0.03))
        lumi_paw = bpy.context.active_object
        lumi_paw.scale = (1.0, 1.4, 0.6)
        bpy.ops.object.transform_apply(scale=True)
        lumi_paw.data.materials.append(mat_lumi_white)
        for p in lumi_paw.data.polygons:
            p.use_smooth = True
        lumi_paw.parent = lumi_leg

    # Fluffy Tail with Glowing Cyan Tip
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.08, location=(0, 0.16, 0.22))
    lumi_tail_base = bpy.context.active_object
    lumi_tail_base.name = "Lumi_Tail_Base"
    lumi_tail_base.scale = (0.8, 1.5, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    lumi_tail_base.data.materials.append(mat_lumi_fur)
    for p in lumi_tail_base.data.polygons:
        p.use_smooth = True
    lumi_tail_base.parent = lumi_body

    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.09, depth=0.28, location=(0, 0.28, 0.36))
    lumi_tail_tip = bpy.context.active_object
    lumi_tail_tip.name = "Lumi_Tail_Tip"
    lumi_tail_tip.rotation_euler = (math.radians(65), 0, 0)
    lumi_tail_tip.data.materials.append(mat_lumi_glow)
    for p in lumi_tail_tip.data.polygons:
        p.use_smooth = True
    lumi_tail_tip.parent = lumi_tail_base

    # -------------------------------------------------------------
    # 5. Environment: Ancient Bridge & Magical Cavern
    # -------------------------------------------------------------
    
    # Bridge Walkway (Paved Stone Deck at Z = 0.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.15))
    bridge_deck = bpy.context.active_object
    bridge_deck.name = "AncientBridgeDeck"
    bridge_deck.scale = (1.8, 16.0, 0.30)
    bpy.ops.object.transform_apply(scale=True)
    bridge_deck.data.materials.append(mat_stone_bridge)
    
    # Edge Curbs with Golden Runes
    for side_x in [-0.85, 0.85]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_x, 0, 0.06))
        curb = bpy.context.active_object
        curb.name = f"BridgeCurb_{side_x}"
        curb.scale = (0.16, 16.0, 0.12)
        bpy.ops.object.transform_apply(scale=True)
        curb.data.materials.append(mat_bridge_gold)
        
    # Stone Balustrade Pillars & Glowing Lantern Orbs
    for py in [-4.5, -2.5, -0.5, 1.5, 3.5, 5.5]:
        for px in [-0.92, 0.92]:
            bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.09, depth=0.72, location=(px, py, 0.36))
            pillar = bpy.context.active_object
            pillar.data.materials.append(mat_stone_bridge)
            
            # Glowing Crystal Orb on top
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.075, location=(px, py, 0.76))
            lantern = bpy.context.active_object
            lantern.data.materials.append(mat_cyan_crystal)

    # Giant Bioluminescent Mushrooms (Rich Curving Stems + Parasol Caps)
    shroom_configs = [
        (-2.6, -1.8, 0.0, 1.6, mat_shroom_cap_teal, -12),
        (2.8, -0.8, 0.2, 2.1, mat_shroom_cap_purple, 15),
        (-2.9, 1.8, 0.4, 2.4, mat_shroom_cap_purple, -8),
        (2.6, 3.2, 0.1, 1.8, mat_shroom_cap_teal, 10),
        (-3.2, 4.5, 0.5, 2.7, mat_shroom_cap_teal, -15)
    ]
    
    for mx, my, mz, scale_s, cap_mat, lean_deg in shroom_configs:
        # Curved Stem
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.14 * scale_s, depth=1.8 * scale_s, location=(mx, my, mz + 0.9 * scale_s))
        stem = bpy.context.active_object
        stem.rotation_euler = (0, math.radians(lean_deg), 0)
        stem.data.materials.append(mat_shroom_stem)
        for p in stem.data.polygons:
            p.use_smooth = True
            
        # Mushroom Cap
        cap_z = mz + 1.8 * scale_s
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=0.85 * scale_s, location=(mx, my, cap_z))
        cap = bpy.context.active_object
        cap.scale = (1.0, 1.0, 0.42)
        bpy.ops.object.transform_apply(scale=True)
        cap.data.materials.append(cap_mat)
        for p in cap.data.polygons:
            p.use_smooth = True

    # Floating Spore Motes (Small glowing particles)
    for sp_idx, (sx, sy, sz) in enumerate([
        (-0.6, -1.2, 0.8), (0.7, -0.4, 1.1), (-0.4, 0.6, 1.3),
        (0.5, 1.2, 0.9), (-0.8, 2.0, 1.5), (0.3, -1.8, 1.4)
    ]):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.022, location=(sx, sy, sz))
        spore = bpy.context.active_object
        spore.data.materials.append(mat_cyan_crystal)

    # -------------------------------------------------------------
    # 6. Cinematic 3-Point Lighting
    # -------------------------------------------------------------
    # 1. Warm Golden Key Light (Lantern/Sun glow)
    light_key_data = bpy.data.lights.new("KeyLight", type='POINT')
    light_key_data.energy = 220
    light_key_data.color = (1.0, 0.88, 0.72)
    light_key_data.shadow_soft_size = 0.45
    light_key = bpy.data.objects.new("KeyLight", light_key_data)
    bpy.context.collection.objects.link(light_key)
    light_key.location = (-1.8, -2.6, 2.5)

    # 2. Cool Blue Ambient Fill Light
    light_fill_data = bpy.data.lights.new("FillLight", type='POINT')
    light_fill_data.energy = 85
    light_fill_data.color = (0.42, 0.58, 0.95)
    light_fill_data.shadow_soft_size = 0.8
    light_fill = bpy.data.objects.new("FillLight", light_fill_data)
    bpy.context.collection.objects.link(light_fill)
    light_fill.location = (2.2, -1.2, 2.0)

    # 3. Vibrant Cyan Rim Light (Outlines character silhouette)
    light_rim_data = bpy.data.lights.new("RimLight", type='SPOT')
    light_rim_data.energy = 380
    light_rim_data.color = (0.2, 0.85, 1.0)
    light_rim_data.spot_size = math.radians(75)
    light_rim_data.shadow_soft_size = 0.25
    light_rim = bpy.data.objects.new("RimLight", light_rim_data)
    bpy.context.collection.objects.link(light_rim)
    light_rim.location = (0.8, 2.4, 2.2)
    light_rim.rotation_euler = (math.radians(-42), math.radians(15), math.radians(-160))

    # -------------------------------------------------------------
    # 7. Cinematic Cameras
    # -------------------------------------------------------------
    # Camera 1: Medium Action Shot (Leo & Lumi pointing on bridge)
    cam_data = bpy.data.cameras.new("CinematicCamera")
    cam_data.lens = 45
    cam_data.dof.use_dof = True
    cam_data.dof.focus_distance = 2.4
    cam_data.dof.aperture_fstop = 2.8
    
    cam_obj = bpy.data.objects.new("CinematicCamera", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # Position camera for full-body view of Leo standing on bridge
    cam_obj.location = (-0.35, -2.8, 1.15)
    cam_obj.rotation_euler = (math.radians(82), 0, math.radians(-8))

    return arm_obj, head_obj, cam_obj

if __name__ == "__main__":
    arm, head, cam = build_scene()
    
    # Test Render Frame 100 to check character quality
    output_test_path = r"E:\YT\output\renders\test_stylized_character.jpg"
    os.makedirs(os.path.dirname(output_test_path), exist_ok=True)
    bpy.context.scene.render.filepath = output_test_path
    bpy.ops.render.render(write_still=True)
    print(f"Successfully rendered test still to {output_test_path}")
