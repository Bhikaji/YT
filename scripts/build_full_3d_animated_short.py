"""
Autonomous AI Cartoon Studio - Production 3D Rigged Animated Short Pipeline
Creates fully rigged 3D character (Leo) with:
- Skeletal Walk Cycle locomotion
- Hand gestures & pointing
- Eye saccades & blinking
- Emotional facial blendshapes & dialogue lip-sync
- Companion fox (Lumi) with wagging tail
- Bioluminescent Cavern 3D environment & volumetric lighting
Executes inside Blender 4.2 LTS headlessly.
"""

import bpy
import math
import os
import random
from pathlib import Path

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# 1. Render Settings (EEVEE-Next, 1080x1920 vertical Shorts, 30 fps)
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 300  # Exactly 10.0 seconds

# Fast quality samples for EEVEE-Next
if hasattr(scene, "eevee"):
    scene.eevee.taa_render_samples = 12

# Color Management
if 'AgX' in [c.name for c in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items]:
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'Medium High Contrast'

frames_dir = r"E:\YT\output\renders\rigged_short_10s"
os.makedirs(frames_dir, exist_ok=True)
scene.render.filepath = os.path.join(frames_dir, "frame_")
scene.render.image_settings.file_format = 'JPEG'
scene.render.image_settings.quality = 96

# 2. World Lighting & Bioluminescent Cavern Ambience
world = bpy.data.worlds.new("CavernDeepWorld")
scene.world = world
world.use_nodes = True
w_nodes = world.node_tree.nodes
w_links = world.node_tree.links
w_nodes.clear()

bg = w_nodes.new('ShaderNodeBackground')
bg.inputs['Color'].default_value = (0.015, 0.02, 0.045, 1.0)
bg.inputs['Strength'].default_value = 0.6
out_w = w_nodes.new('ShaderNodeOutputWorld')
w_links.new(bg.outputs['Background'], out_w.inputs['Surface'])

# 3. Materials Library (Pixar Stylized Shaders)
def create_mat(name, color, roughness=0.35, sss=0.0, emission=None):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = roughness
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = sss
            bsdf.inputs['Subsurface Radius'].default_value = (0.35, 0.15, 0.08)
        elif 'Subsurface' in bsdf.inputs:
            bsdf.inputs['Subsurface'].default_value = sss
        if emission:
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = emission[0]
                bsdf.inputs['Emission Strength'].default_value = emission[1]
            elif 'Emission' in bsdf.inputs:
                bsdf.inputs['Emission'].default_value = emission[0]
    return mat

mat_skin = create_mat("LeoSkin", (0.95, 0.76, 0.64, 1.0), roughness=0.32, sss=0.25)
mat_hair = create_mat("LeoHair", (0.28, 0.16, 0.08, 1.0), roughness=0.45)
mat_hoodie = create_mat("LeoHoodie", (0.86, 0.20, 0.16, 1.0), roughness=0.72)
mat_jeans = create_mat("LeoJeans", (0.16, 0.26, 0.44, 1.0), roughness=0.68)
mat_boots = create_mat("LeoBoots", (0.22, 0.14, 0.09, 1.0), roughness=0.55)
mat_backpack = create_mat("Backpack", (0.08, 0.55, 0.52, 1.0), roughness=0.50)
mat_eye_white = create_mat("EyeWhite", (0.98, 0.98, 0.98, 1.0), roughness=0.05)
mat_iris = create_mat("Iris", (0.18, 0.55, 0.82, 1.0), roughness=0.08)
mat_pupil = create_mat("Pupil", (0.01, 0.01, 0.01, 1.0), roughness=0.02)
mat_crystal = create_mat("CrystalBridge", (0.25, 0.85, 1.0, 1.0), roughness=0.1, emission=((0.2, 0.8, 1.0, 1.0), 2.2))
mat_shroom_p = create_mat("ShroomPurple", (0.75, 0.20, 0.85, 1.0), roughness=0.35, emission=((0.7, 0.2, 0.8, 1.0), 2.5))
mat_shroom_t = create_mat("ShroomTeal", (0.10, 0.70, 0.65, 1.0), roughness=0.35, emission=((0.1, 0.7, 0.6, 1.0), 2.2))
mat_lumi_fur = create_mat("LumiFur", (0.96, 0.25, 0.68, 1.0), roughness=0.55)
mat_lumi_glow = create_mat("LumiGlow", (0.25, 0.9, 1.0, 1.0), roughness=0.2, emission=((0.25, 0.9, 1.0, 1.0), 4.0))

# 4. Build Environment (Crystal Bridge & Cavern)
# Crystal Bridge walkway
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.08))
bridge = bpy.context.active_object
bridge.name = "CrystalBridge"
bridge.scale = (1.4, 12.0, 0.15)
bpy.ops.object.transform_apply(scale=True)
bridge.data.materials.append(mat_crystal)

# Crystal railing pillars
for y_pos in [-4.0, -2.0, 0.0, 2.0, 4.0]:
    for x_side in [-0.68, 0.68]:
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.08, radius2=0.02, depth=0.75, location=(x_side, y_pos, 0.35))
        c_pillar = bpy.context.active_object
        c_pillar.name = f"Pillar_{x_side}_{y_pos}"
        c_pillar.data.materials.append(mat_crystal)

# Giant Bioluminescent Mushrooms
for m_idx, (mx, my, mz, scale, is_purp) in enumerate([
    (-2.2, 1.5, 0.5, 1.8, True),
    (2.4, 2.8, 0.8, 2.2, False),
    (-2.6, -2.5, 0.2, 1.5, False),
    (2.1, -1.8, 0.4, 1.6, True)
]):
    # Stem
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18 * scale, depth=1.6 * scale, location=(mx, my, mz + 0.8 * scale))
    stem = bpy.context.active_object
    stem.data.materials.append(create_mat(f"StemMat_{m_idx}", (0.15, 0.22, 0.28, 1.0), roughness=0.6))
    # Cap
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.75 * scale, location=(mx, my, mz + 1.6 * scale))
    cap = bpy.context.active_object
    cap.scale = (1.0, 1.0, 0.45)
    bpy.ops.object.transform_apply(scale=True)
    cap.data.materials.append(mat_shroom_p if is_purp else mat_shroom_t)

# 5. Build Armature Rig for Leo
arm_data = bpy.data.armatures.new("LeoArmatureData")
arm_obj = bpy.data.objects.new("LeoArmature", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='EDIT')

b_root = arm_data.edit_bones.new("root")
b_root.head = (0, 0, 0)
b_root.tail = (0, 0.1, 0)

b_hips = arm_data.edit_bones.new("hips")
b_hips.parent = b_root
b_hips.head = (0, 0, 0.68)
b_hips.tail = (0, 0, 0.82)

b_spine = arm_data.edit_bones.new("spine")
b_spine.parent = b_hips
b_spine.head = (0, 0, 0.82)
b_spine.tail = (0, 0, 1.05)

b_neck = arm_data.edit_bones.new("neck")
b_neck.parent = b_spine
b_neck.head = (0, 0, 1.05)
b_neck.tail = (0, 0, 1.14)

b_head = arm_data.edit_bones.new("head")
b_head.parent = b_neck
b_head.head = (0, 0, 1.14)
b_head.tail = (0, 0, 1.40)

# Arms & Hands
b_arm_l = arm_data.edit_bones.new("upper_arm.L")
b_arm_l.parent = b_spine
b_arm_l.head = (0.18, 0, 1.02)
b_arm_l.tail = (0.38, 0, 0.82)

b_forearm_l = arm_data.edit_bones.new("forearm.L")
b_forearm_l.parent = b_arm_l
b_forearm_l.head = (0.38, 0, 0.82)
b_forearm_l.tail = (0.54, 0, 0.64)

b_hand_l = arm_data.edit_bones.new("hand.L")
b_hand_l.parent = b_forearm_l
b_hand_l.head = (0.54, 0, 0.64)
b_hand_l.tail = (0.62, 0, 0.58)

b_arm_r = arm_data.edit_bones.new("upper_arm.R")
b_arm_r.parent = b_spine
b_arm_r.head = (-0.18, 0, 1.02)
b_arm_r.tail = (-0.38, 0, 0.82)

b_forearm_r = arm_data.edit_bones.new("forearm.R")
b_forearm_r.parent = b_arm_r
b_forearm_r.head = (-0.38, 0, 0.82)
b_forearm_r.tail = (-0.54, 0, 0.64)

b_hand_r = arm_data.edit_bones.new("hand.R")
b_hand_r.parent = b_forearm_r
b_hand_r.head = (-0.54, 0, 0.64)
b_hand_r.tail = (-0.62, 0, 0.58)

# Legs
b_thigh_l = arm_data.edit_bones.new("thigh.L")
b_thigh_l.parent = b_hips
b_thigh_l.head = (0.11, 0, 0.68)
b_thigh_l.tail = (0.11, 0, 0.36)

b_shin_l = arm_data.edit_bones.new("shin.L")
b_shin_l.parent = b_thigh_l
b_shin_l.head = (0.11, 0, 0.36)
b_shin_l.tail = (0.11, 0, 0.10)

b_foot_l = arm_data.edit_bones.new("foot.L")
b_foot_l.parent = b_shin_l
b_foot_l.head = (0.11, 0, 0.10)
b_foot_l.tail = (0.11, 0.16, 0.02)

b_thigh_r = arm_data.edit_bones.new("thigh.R")
b_thigh_r.parent = b_hips
b_thigh_r.head = (-0.11, 0, 0.68)
b_thigh_r.tail = (-0.11, 0, 0.36)

b_shin_r = arm_data.edit_bones.new("shin.R")
b_shin_r.parent = b_thigh_r
b_shin_r.head = (-0.11, 0, 0.36)
b_shin_r.tail = (-0.11, 0, 0.10)

b_foot_r = arm_data.edit_bones.new("foot.R")
b_foot_r.parent = b_shin_r
b_foot_r.head = (-0.11, 0, 0.10)
b_foot_r.tail = (-0.11, 0.16, 0.02)

bpy.ops.object.mode_set(mode='OBJECT')

# 6. Build Character Mesh Geometry (Leo)
# Head with Shapekeys
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.19, location=(0, 0, 1.25))
head_mesh = bpy.context.active_object
head_mesh.name = "Leo_Head"
head_mesh.scale = (1.0, 0.95, 1.05)
bpy.ops.object.transform_apply(scale=True)
head_mesh.data.materials.append(mat_skin)

# Add ShapeKeys for Facial Expressions and Dialogue
sk_basis = head_mesh.shape_key_add(name="Basis")
sk_jaw = head_mesh.shape_key_add(name="jawOpen")
sk_smile = head_mesh.shape_key_add(name="mouthSmile")
sk_brow = head_mesh.shape_key_add(name="browInnerUp")
sk_blink = head_mesh.shape_key_add(name="eyeBlink")

# Displace jaw vertices for jawOpen
for idx, vert in enumerate(head_mesh.data.vertices):
    if vert.co.z < 1.20 and vert.co.y > 0.05:
        sk_jaw.data[idx].co.z -= 0.045
        sk_jaw.data[idx].co.y += 0.015
    if vert.co.z > 1.30 and vert.co.y > 0.08:
        sk_brow.data[idx].co.z += 0.035
    if vert.co.z > 1.22 and vert.co.z < 1.32 and abs(vert.co.x) < 0.12 and vert.co.y > 0.10:
        sk_blink.data[idx].co.z -= 0.028

# Pixar Stylized Eyes (Cornea + Iris + Pupil)
eye_objs = []
for side, sign in [("L", 1), ("R", -1)]:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.048, location=(sign * 0.065, 0.145, 1.26))
    eye_sclera = bpy.context.active_object
    eye_sclera.name = f"Eye_{side}"
    eye_sclera.data.materials.append(mat_eye_white)
    
    # Iris
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.026, location=(sign * 0.065, 0.178, 1.26))
    iris = bpy.context.active_object
    iris.name = f"Iris_{side}"
    iris.scale = (1.0, 0.25, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    iris.data.materials.append(mat_iris)
    iris.parent = eye_sclera
    
    # Pupil
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.013, location=(sign * 0.065, 0.185, 1.26))
    pupil = bpy.context.active_object
    pupil.name = f"Pupil_{side}"
    pupil.scale = (1.0, 0.2, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    pupil.data.materials.append(mat_pupil)
    pupil.parent = eye_sclera
    
    eye_sclera.parent = arm_obj
    eye_sclera.parent_type = 'BONE'
    eye_sclera.parent_bone = "head"
    eye_objs.append(eye_sclera)

# Sculpted Cartoon Hair
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.21, location=(0, -0.02, 1.31))
hair_obj = bpy.context.active_object
hair_obj.name = "Leo_Hair"
hair_obj.scale = (1.02, 1.05, 0.95)
bpy.ops.object.transform_apply(scale=True)
hair_obj.data.materials.append(mat_hair)
hair_obj.parent = arm_obj
hair_obj.parent_type = 'BONE'
hair_obj.parent_bone = "head"

# Hair tufts (front stylized locks)
for tx, tz, tr in [(-0.06, 1.40, 0.07), (0.05, 1.42, 0.08), (0.0, 1.43, 0.09)]:
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=tr, depth=0.18, location=(tx, 0.16, tz))
    tuft = bpy.context.active_object
    tuft.rotation_euler = (math.radians(-45), 0, math.radians(tx * 120))
    tuft.data.materials.append(mat_hair)
    tuft.parent = arm_obj
    tuft.parent_type = 'BONE'
    tuft.parent_bone = "head"

# Hoodie Torso
bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.38, location=(0, 0, 0.88))
hoodie = bpy.context.active_object
hoodie.name = "Leo_Hoodie"
hoodie.scale = (1.1, 0.85, 1.0)
bpy.ops.object.transform_apply(scale=True)
hoodie.data.materials.append(mat_hoodie)
hoodie.parent = arm_obj
hoodie.parent_type = 'BONE'
hoodie.parent_bone = "spine"

# Backpack
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.16, 0.88))
pack = bpy.context.active_object
pack.name = "Backpack"
pack.scale = (0.24, 0.14, 0.32)
bpy.ops.object.transform_apply(scale=True)
pack.data.materials.append(mat_backpack)
pack.parent = arm_obj
pack.parent_type = 'BONE'
pack.parent_bone = "spine"

# Arm Sleeves & Hands
for side, sign in [("L", 1), ("R", -1)]:
    # Sleeve
    bpy.ops.mesh.primitive_cylinder_add(radius=0.055, depth=0.28, location=(sign * 0.28, 0, 0.92))
    sleeve = bpy.context.active_object
    sleeve.name = f"Sleeve_{side}"
    sleeve.rotation_euler = (0, math.radians(-sign * 35), 0)
    sleeve.data.materials.append(mat_hoodie)
    sleeve.parent = arm_obj
    sleeve.parent_type = 'BONE'
    sleeve.parent_bone = f"upper_arm.{side}"
    
    # Forearm
    bpy.ops.mesh.primitive_cylinder_add(radius=0.048, depth=0.26, location=(sign * 0.46, 0, 0.74))
    forearm_m = bpy.context.active_object
    forearm_m.name = f"ForearmMesh_{side}"
    forearm_m.rotation_euler = (0, math.radians(-sign * 42), 0)
    forearm_m.data.materials.append(mat_hoodie)
    forearm_m.parent = arm_obj
    forearm_m.parent_type = 'BONE'
    forearm_m.parent_bone = f"forearm.{side}"
    
    # Stylized Hand
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.042, location=(sign * 0.58, 0, 0.60))
    hand_m = bpy.context.active_object
    hand_m.name = f"HandMesh_{side}"
    hand_m.scale = (1.0, 0.7, 1.2)
    bpy.ops.object.transform_apply(scale=True)
    hand_m.data.materials.append(mat_skin)
    hand_m.parent = arm_obj
    hand_m.parent_type = 'BONE'
    hand_m.parent_bone = f"hand.{side}"

# Legs (Jeans)
for side, sign in [("L", 1), ("R", -1)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.062, depth=0.34, location=(sign * 0.11, 0, 0.52))
    thigh_m = bpy.context.active_object
    thigh_m.name = f"ThighMesh_{side}"
    thigh_m.data.materials.append(mat_jeans)
    thigh_m.parent = arm_obj
    thigh_m.parent_type = 'BONE'
    thigh_m.parent_bone = f"thigh.{side}"
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.055, depth=0.30, location=(sign * 0.11, 0, 0.22))
    shin_m = bpy.context.active_object
    shin_m.name = f"ShinMesh_{side}"
    shin_m.data.materials.append(mat_jeans)
    shin_m.parent = arm_obj
    shin_m.parent_type = 'BONE'
    shin_m.parent_bone = f"shin.{side}"
    
    # Hiking Boot
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sign * 0.11, 0.05, 0.05))
    boot_m = bpy.context.active_object
    boot_m.name = f"BootMesh_{side}"
    boot_m.scale = (0.07, 0.16, 0.07)
    bpy.ops.object.transform_apply(scale=True)
    boot_m.data.materials.append(mat_boots)
    boot_m.parent = arm_obj
    boot_m.parent_type = 'BONE'
    boot_m.parent_bone = f"foot.{side}"

head_mesh.parent = arm_obj
head_mesh.parent_type = 'BONE'
head_mesh.parent_bone = "head"

# 7. Build Companion Creature (Lumi)
lumi_obj = bpy.data.objects.new("Lumi_Root", None)
bpy.context.collection.objects.link(lumi_obj)
lumi_obj.location = (0.38, -1.8, 0.10)

# Body
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(0.38, -1.8, 0.24))
lumi_body = bpy.context.active_object
lumi_body.name = "Lumi_Body"
lumi_body.scale = (0.9, 1.25, 0.9)
bpy.ops.object.transform_apply(scale=True)
lumi_body.data.materials.append(mat_lumi_fur)
lumi_body.parent = lumi_obj

# Head
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(0.38, -1.62, 0.36))
lumi_head = bpy.context.active_object
lumi_head.name = "Lumi_Head"
lumi_head.data.materials.append(mat_lumi_fur)
lumi_head.parent = lumi_obj

# Ears
for esign in [-1, 1]:
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.045, depth=0.14, location=(0.38 + esign * 0.07, -1.62, 0.48))
    ear = bpy.context.active_object
    ear.rotation_euler = (math.radians(-20), math.radians(esign * 25), 0)
    ear.data.materials.append(mat_lumi_glow)
    ear.parent = lumi_head

# Big Fluffy Glowing Tail
bpy.ops.mesh.primitive_cone_add(radius1=0.12, depth=0.38, location=(0.38, -2.05, 0.35))
lumi_tail = bpy.context.active_object
lumi_tail.name = "Lumi_Tail"
lumi_tail.rotation_euler = (math.radians(65), 0, 0)
lumi_tail.data.materials.append(mat_lumi_glow)
lumi_tail.parent = lumi_obj

# 8. Animate the Rig: Walk Cycle, Hand Pointing, Eye Movements & Emotions
# Pose mode
pose = arm_obj.pose

# Frame 1 to 90: Walk Locomotion along bridge
walk_cycle_frames = 28  # ~1.0 second per cycle

for f in range(1, 151):
    t = f / 30.0
    
    if f <= 90:
        # WALKING PHASE:
        phase = (f % walk_cycle_frames) / float(walk_cycle_frames) * (2 * math.pi)
        
        # Root moves forward along bridge Y
        root_y = -2.2 + (f / 90.0) * 1.5
        pose.bones["root"].location = (0, root_y, 0)
        pose.bones["root"].keyframe_insert(data_path="location", frame=f)
        
        # Hips bounce & sway
        hips_bounce = math.sin(2 * phase) * 0.03
        pose.bones["hips"].location = (0, 0, hips_bounce)
        pose.bones["hips"].rotation_euler = (0, math.sin(phase) * 0.04, 0)
        pose.bones["hips"].keyframe_insert(data_path="location", frame=f)
        pose.bones["hips"].keyframe_insert(data_path="rotation_euler", frame=f)
        
        # Legs swing
        leg_swing_l = math.sin(phase) * 0.48
        leg_swing_r = -math.sin(phase) * 0.48
        pose.bones["thigh.L"].rotation_euler = (leg_swing_l, 0, 0)
        pose.bones["thigh.R"].rotation_euler = (leg_swing_r, 0, 0)
        pose.bones["shin.L"].rotation_euler = (max(0.0, -math.sin(phase) * 0.55), 0, 0)
        pose.bones["shin.R"].rotation_euler = (max(0.0, math.sin(phase) * 0.55), 0, 0)
        
        pose.bones["thigh.L"].keyframe_insert(data_path="rotation_euler", frame=f)
        pose.bones["thigh.R"].keyframe_insert(data_path="rotation_euler", frame=f)
        pose.bones["shin.L"].keyframe_insert(data_path="rotation_euler", frame=f)
        pose.bones["shin.R"].keyframe_insert(data_path="rotation_euler", frame=f)
        
        # Arms swing in opposition
        pose.bones["upper_arm.L"].rotation_euler = (-leg_swing_l * 0.8, 0, 0)
        pose.bones["upper_arm.R"].rotation_euler = (-leg_swing_r * 0.8, 0, 0)
        pose.bones["upper_arm.L"].keyframe_insert(data_path="rotation_euler", frame=f)
        pose.bones["upper_arm.R"].keyframe_insert(data_path="rotation_euler", frame=f)
        
        # Lumi trotting alongside
        lumi_obj.location = (0.36, root_y + 0.15, 0.10 + math.sin(2 * phase) * 0.02)
        lumi_obj.keyframe_insert(data_path="location", frame=f)
        lumi_tail.rotation_euler = (math.radians(65), math.sin(phase * 1.5) * 0.35, 0)
        lumi_tail.keyframe_insert(data_path="rotation_euler", frame=f)
        
    elif f <= 150:
        # GESTURE & DIALOGUE PHASE (Leo stops, points hand, expresses wonder)
        progress = (f - 90) / 60.0
        
        # Settle hips
        pose.bones["hips"].location = (0, 0, 0)
        pose.bones["thigh.L"].rotation_euler = (0.05, 0, 0)
        pose.bones["thigh.R"].rotation_euler = (-0.08, 0, 0)
        pose.bones["shin.L"].rotation_euler = (0, 0, 0)
        pose.bones["shin.R"].rotation_euler = (0, 0, 0)
        
        # Right Arm & Hand raises and points forward!
        arm_up = min(1.0, progress * 1.8)
        pose.bones["upper_arm.R"].rotation_euler = (math.radians(72 * arm_up), 0, math.radians(-25 * arm_up))
        pose.bones["forearm.R"].rotation_euler = (math.radians(45 * arm_up), 0, 0)
        pose.bones["hand.R"].rotation_euler = (math.radians(15 * arm_up), 0, 0)
        
        pose.bones["upper_arm.R"].keyframe_insert(data_path="rotation_euler", frame=f)
        pose.bones["forearm.R"].keyframe_insert(data_path="rotation_euler", frame=f)
        pose.bones["hand.R"].keyframe_insert(data_path="rotation_euler", frame=f)
        
        # Facial Emotion: Awe & Wonder
        sk_brow.value = min(0.85, progress * 1.5)
        sk_brow.keyframe_insert(data_path="value", frame=f)
        sk_smile.value = min(0.50, progress * 1.2)
        sk_smile.keyframe_insert(data_path="value", frame=f)
        
        # Mouth Viseme Lip-Sync for "Whoa... Lumi, look! The ancient crystals are glowing!"
        dialogue_speech = math.sin((f - 90) * 0.45) * 0.45 + 0.35 if f > 95 and f < 145 else 0.0
        sk_jaw.value = max(0.0, dialogue_speech)
        sk_jaw.keyframe_insert(data_path="value", frame=f)
        
        # Natural Blink at frame 110-116
        if 110 <= f <= 116:
            sk_blink.value = math.sin((f - 110) / 6.0 * math.pi)
        else:
            sk_blink.value = 0.0
        sk_blink.keyframe_insert(data_path="value", frame=f)

# Frames 151 to 300: Hero Close-Up Phase (Dialogue 2, Eye Saccades, Hand relaxed on strap)
for f in range(151, 301):
    local_f = f - 151
    progress = local_f / 150.0
    
    # Hand relaxes to grip backpack strap
    pose.bones["upper_arm.R"].rotation_euler = (math.radians(35), 0, math.radians(-15))
    pose.bones["forearm.R"].rotation_euler = (math.radians(65), 0, 0)
    pose.bones["hand.R"].rotation_euler = (math.radians(20), 0, 0)
    pose.bones["upper_arm.R"].keyframe_insert(data_path="rotation_euler", frame=f)
    pose.bones["forearm.R"].keyframe_insert(data_path="rotation_euler", frame=f)
    pose.bones["hand.R"].keyframe_insert(data_path="rotation_euler", frame=f)
    
    # Head slight inquisitive tilt
    pose.bones["head"].rotation_euler = (math.radians(8 + math.sin(local_f * 0.06) * 3), math.radians(-6), 0)
    pose.bones["head"].keyframe_insert(data_path="rotation_euler", frame=f)
    
    # Eye Saccades & Gaze: looking up at crystals, then down to camera
    gaze_y = 1.26 + (0.04 if local_f < 75 else -0.01)
    gaze_x = math.sin(local_f * 0.05) * 0.008
    for eye_scl in eye_objs:
        eye_scl.location.z = 1.26 + (0.008 if local_f < 75 else -0.005)
        eye_scl.keyframe_insert(data_path="location", frame=f)
        
    # Double blink at frame 210-218
    if 210 <= f <= 218:
        sk_blink.value = math.sin((f - 210) / 8.0 * math.pi)
    else:
        sk_blink.value = 0.0
    sk_blink.keyframe_insert(data_path="value", frame=f)
    
    # Facial Emotion: Intense curiosity & determination
    sk_brow.value = 0.45 + math.sin(local_f * 0.08) * 0.1
    sk_brow.keyframe_insert(data_path="value", frame=f)
    
    # Mouth Lip-Sync for: "Whatever is powering this place... it knows we are here!"
    if 165 <= f <= 285:
        sk_jaw.value = max(0.0, math.sin((f - 165) * 0.40) * 0.40 + 0.25)
    else:
        sk_jaw.value = 0.0
    sk_jaw.keyframe_insert(data_path="value", frame=f)

# 9. Animated 3D Director Cameras
# Camera for Scene 1 (Frames 1-150: Wide Medium Shot pushing in)
cam_data = bpy.data.cameras.new("DirectorCamera")
cam_data.lens = 38.0
cam_data.dof.use_dof = True
cam_data.dof.focus_distance = 3.6
cam_data.dof.aperture_fstop = 2.8

cam_obj = bpy.data.objects.new("DirectorCamera", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Camera 1 Keyframes
cam_obj.location = (0.35, -4.6, 1.25)
cam_obj.rotation_euler = (math.radians(84), 0, math.radians(-4))
cam_obj.keyframe_insert(data_path="location", frame=1)
cam_obj.keyframe_insert(data_path="rotation_euler", frame=1)

cam_obj.location = (0.15, -2.8, 1.15)
cam_obj.rotation_euler = (math.radians(86), 0, math.radians(-2))
cam_obj.keyframe_insert(data_path="location", frame=150)
cam_obj.keyframe_insert(data_path="rotation_euler", frame=150)

# Camera Cut at Frame 151 to Close-Up Hero framing!
cam_obj.location = (-0.18, -1.25, 1.22)
cam_obj.rotation_euler = (math.radians(93), 0, math.radians(8))
cam_obj.keyframe_insert(data_path="location", frame=151)
cam_obj.keyframe_insert(data_path="rotation_euler", frame=151)

cam_obj.location = (-0.14, -1.05, 1.24)
cam_obj.rotation_euler = (math.radians(94), 0, math.radians(6))
cam_obj.keyframe_insert(data_path="location", frame=300)
cam_obj.keyframe_insert(data_path="rotation_euler", frame=300)

# 10. Dynamic Cinematic 3-Point Lighting
# Key Light (Warm Key)
key_light = bpy.data.lights.new("WarmKey", type='POINT')
key_light.energy = 850
key_light.color = (1.0, 0.88, 0.72)
key_obj = bpy.data.objects.new("WarmKey", key_light)
key_obj.location = (-1.2, -1.5, 2.2)
bpy.context.collection.objects.link(key_obj)

# Crystal Fill Light (Cyan)
fill_light = bpy.data.lights.new("CrystalFill", type='POINT')
fill_light.energy = 600
fill_light.color = (0.2, 0.8, 1.0)
fill_obj = bpy.data.objects.new("CrystalFill", fill_light)
fill_obj.location = (1.5, 0.0, 0.8)
bpy.context.collection.objects.link(fill_obj)

# Warm Rim Light
rim_light = bpy.data.lights.new("SunRim", type='SUN')
rim_light.energy = 2.5
rim_light.color = (1.0, 0.70, 0.40)
rim_obj = bpy.data.objects.new("SunRim", rim_light)
rim_obj.rotation_euler = (math.radians(45), math.radians(30), math.radians(-120))
bpy.context.collection.objects.link(rim_obj)

# 11. Floating 3D Bioluminescent Particle Spores
for sp_idx in range(30):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.018, location=(
        (sp_idx % 6 - 2.5) * 0.45,
        -2.5 + (sp_idx % 8) * 0.5,
        0.2 + (sp_idx * 0.12)
    ))
    spore = bpy.context.active_object
    spore.name = f"Spore_{sp_idx}"
    is_cyan = (sp_idx % 2 == 0)
    spore.data.materials.append(mat_crystal if is_cyan else mat_shroom_p)
    
    # Animate spore floating
    for f in [1, 100, 200, 300]:
        t = f / 30.0
        spore.location.z = 0.2 + ((t * 0.3 + sp_idx * 0.1) % 2.0)
        spore.location.x += math.sin(t + sp_idx) * 0.04
        spore.keyframe_insert(data_path="location", frame=f)

print("[Blender Engine] Fully rigged 3D character with walk cycle, hand pointing, eyes & emotions assembled!")
