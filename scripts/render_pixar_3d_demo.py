"""
Production-grade 3D Pixar Scene & Character Builder for Blender 4.2+ (bpy)
Creates Leo (3D stylized boy with hair locks, eyes, hoodie, backpack)
and Lumi (3D glowing fox companion) in a Bioluminescent Mushroom Forest.
"""

import bpy
import math
import os
import json
from pathlib import Path

# Clear existing scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# Configure Render Engine & Output
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
if hasattr(scene, "eevee"):
    scene.eevee.use_gtao = True
    scene.eevee.use_bloom = True
    scene.eevee.use_ssr = True

scene.render.resolution_x = 1080
scene.render.resolution_y = 1920  # 9:16 Vertical Short
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.render.image_settings.file_format = 'PNG'

output_dir = r"E:\YT\output\renders\demo_pixar_3d"
os.makedirs(output_dir, exist_ok=True)
scene.render.filepath = os.path.join(output_dir, "frame_")

# 1. World & Volumetric Atmosphere
world = bpy.data.worlds.new("PixarWorld")
scene.world = world
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links
nodes.clear()

bg = nodes.new(type='ShaderNodeBackground')
bg.inputs['Color'].default_value = (0.015, 0.02, 0.05, 1.0)  # Deep indigo night
bg.inputs['Strength'].default_value = 0.5

out = nodes.new(type='ShaderNodeOutputWorld')
links.new(bg.outputs['Background'], out.inputs['Surface'])

# Volume Scatter for atmospheric haze
volume = nodes.new(type='ShaderNodeVolumeScatter')
volume.inputs['Density'].default_value = 0.018
volume.inputs['Color'].default_value = (0.1, 0.3, 0.5, 1.0)
links.new(volume.outputs['Volume'], out.inputs['Volume'])

# 2. Materials
def make_mat(name, base_color, roughness=0.35, sss=0.0, emission=None, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    n = mat.node_tree.nodes
    bsdf = n.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
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

mat_skin = make_mat("Skin", (0.92, 0.74, 0.62, 1.0), roughness=0.38, sss=0.25)
mat_hair = make_mat("Hair", (0.28, 0.16, 0.08, 1.0), roughness=0.45)
mat_hoodie = make_mat("Hoodie", (0.85, 0.22, 0.15, 1.0), roughness=0.75)
mat_backpack = make_mat("Backpack", (0.15, 0.45, 0.55, 1.0), roughness=0.6)
mat_eye_white = make_mat("EyeWhite", (0.98, 0.98, 0.98, 1.0), roughness=0.05)
mat_iris = make_mat("Iris", (0.18, 0.52, 0.78, 1.0), roughness=0.05)
mat_pupil = make_mat("Pupil", (0.02, 0.02, 0.02, 1.0), roughness=0.05)
mat_fox_fur = make_mat("FoxFur", (0.95, 0.20, 0.65, 1.0), roughness=0.6)
mat_fox_glow = make_mat("FoxGlow", (0.2, 0.85, 0.98, 1.0), roughness=0.2, emission=((0.2, 0.85, 1.0, 1.0), 3.5))
mat_mushroom_cap = make_mat("MushroomCap", (0.05, 0.65, 0.55, 1.0), roughness=0.4, emission=((0.1, 0.7, 0.6, 1.0), 1.8))
mat_mushroom_purple = make_mat("MushroomPurple", (0.75, 0.25, 0.85, 1.0), roughness=0.4, emission=((0.8, 0.2, 0.9, 1.0), 2.0))
mat_stem = make_mat("Stem", (0.15, 0.25, 0.3, 1.0), roughness=0.6)
mat_crystal = make_mat("Crystal", (0.4, 0.85, 1.0, 1.0), roughness=0.1, emission=((0.3, 0.8, 1.0, 1.0), 1.2))

# 3. Build 3D Character: Leo (Stylized Boy)
# Head
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42, location=(0, 0, 1.48))
head = bpy.context.active_object
head.name = "Leo_Head"
head.scale = (1.05, 0.95, 1.1)
bpy.ops.object.transform_apply(scale=True)
head.data.materials.append(mat_skin)

# Add ShapeKeys for Speech Lip-Sync & Emotion
head.shape_key_add(name="Basis")
sk_jaw = head.shape_key_add(name="jawOpen")
sk_pucker = head.shape_key_add(name="mouthPucker")
sk_smile = head.shape_key_add(name="mouthSmile")

# Deform jawOpen shapekey vertices (lower vertices move down)
for i, v in enumerate(head.data.vertices):
    if v.co.z < 1.35 and v.co.y < 0.2:
        sk_jaw.data[i].co.z -= 0.12
        sk_jaw.data[i].co.y += 0.04
    if v.co.z > 1.30 and abs(v.co.x) > 0.1 and v.co.y < 0.3:
        sk_smile.data[i].co.z += 0.05

# Eyes (Left & Right)
for side, sign in [("L", 1), ("R", -1)]:
    # Sclera
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(0.14 * sign, -0.34, 1.54))
    eye_white = bpy.context.active_object
    eye_white.name = f"EyeWhite_{side}"
    eye_white.scale = (1.0, 0.6, 1.1)
    eye_white.data.materials.append(mat_eye_white)
    
    # Iris
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.07, location=(0.14 * sign, -0.40, 1.54))
    iris = bpy.context.active_object
    iris.name = f"Iris_{side}"
    iris.scale = (1.0, 0.3, 1.0)
    iris.data.materials.append(mat_iris)

    # Pupil
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(0.14 * sign, -0.42, 1.54))
    pupil = bpy.context.active_object
    pupil.name = f"Pupil_{side}"
    pupil.scale = (1.0, 0.3, 1.0)
    pupil.data.materials.append(mat_pupil)

# Hair (Sculpted Stylized Locks)
hair_locs = [
    (0.0, -0.15, 1.95, 0.44, 0.9, 0.7),
    (0.25, -0.10, 1.88, 0.28, 0.8, 0.7),
    (-0.25, -0.10, 1.88, 0.28, 0.8, 0.7),
    (0.12, -0.32, 1.82, 0.20, 1.2, 0.5), # front lock
    (-0.12, -0.32, 1.82, 0.20, 1.2, 0.5),
    (0.0, -0.35, 1.84, 0.18, 1.1, 0.5), # center fringe
    (0.38, 0.0, 1.55, 0.22, 0.6, 1.0),   # sideburn L
    (-0.38, 0.0, 1.55, 0.22, 0.6, 1.0),  # sideburn R
]
for idx, (hx, hy, hz, hr, sx, sy) in enumerate(hair_locs):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=hr, location=(hx, hy, hz))
    hlock = bpy.context.active_object
    hlock.name = f"HairLock_{idx}"
    hlock.scale = (sx, sy, 1.0)
    hlock.data.materials.append(mat_hair)

# Eyebrows
for side, sign in [("L", 1), ("R", -1)]:
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0.14 * sign, -0.38, 1.70))
    brow = bpy.context.active_object
    brow.scale = (1.4, 0.2, 0.25)
    brow.rotation_euler = (0, 0.15 * sign, 0)
    brow.data.materials.append(mat_hair)

# Torso (Crimson Hoodie)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.48, location=(0, 0.05, 0.78))
torso = bpy.context.active_object
torso.name = "Leo_Torso"
torso.scale = (0.9, 0.75, 1.15)
torso.data.materials.append(mat_hoodie)

# Hoodie Drawstrings & Collar
bpy.ops.mesh.primitive_torus_add(major_radius=0.22, minor_radius=0.06, location=(0, -0.05, 1.15))
collar = bpy.context.active_object
collar.rotation_euler = (math.radians(25), 0, 0)
collar.data.materials.append(mat_hoodie)

# Backpack
bpy.ops.mesh.primitive_cube_add(size=0.42, location=(0, 0.40, 0.85))
bp = bpy.context.active_object
bp.scale = (0.85, 0.55, 1.0)
bp.data.materials.append(mat_backpack)

# 4. Build 3D Character: Lumi (Magical Companion Fox)
fox_base_x = 0.65
fox_base_y = -0.35
fox_base_z = 0.55

# Fox Head
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(fox_base_x, fox_base_y, fox_base_z + 0.35))
fhead = bpy.context.active_object
fhead.scale = (1.1, 1.2, 0.95)
fhead.data.materials.append(mat_fox_fur)

# Fox Snout
bpy.ops.mesh.primitive_cone_add(radius1=0.08, depth=0.15, location=(fox_base_x, fox_base_y - 0.18, fox_base_z + 0.30))
snout = bpy.context.active_object
snout.rotation_euler = (math.radians(-90), 0, 0)
snout.data.materials.append(mat_fox_glow)

# Fox Ears (Pointed)
for side, sign in [("L", 1), ("R", -1)]:
    bpy.ops.mesh.primitive_cone_add(radius1=0.09, depth=0.22, location=(fox_base_x + 0.12 * sign, fox_base_y, fox_base_z + 0.55))
    ear = bpy.context.active_object
    ear.rotation_euler = (0, 0.25 * sign, 0)
    ear.data.materials.append(mat_fox_fur)

# Fox Eyes (Big Glowing Emotive Eyes)
for side, sign in [("L", 1), ("R", -1)]:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.065, location=(fox_base_x + 0.09 * sign, fox_base_y - 0.14, fox_base_z + 0.38))
    feye = bpy.context.active_object
    feye.scale = (1.0, 0.4, 1.2)
    feye.data.materials.append(mat_fox_glow)

# Fox Body
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=(fox_base_x, fox_base_y + 0.15, fox_base_z + 0.12))
fbody = bpy.context.active_object
fbody.scale = (0.8, 1.2, 0.9)
fbody.data.materials.append(mat_fox_fur)

# Fox Giant Bioluminescent Fluffy Tail
tail_coords = [
    (fox_base_x, fox_base_y + 0.35, fox_base_z + 0.15, 0.14),
    (fox_base_x + 0.08, fox_base_y + 0.50, fox_base_z + 0.32, 0.20),
    (fox_base_x + 0.12, fox_base_y + 0.55, fox_base_z + 0.52, 0.22), # Apex curve
    (fox_base_x + 0.06, fox_base_y + 0.42, fox_base_z + 0.68, 0.16),
]
for idx, (tx, ty, tz, tr) in enumerate(tail_coords):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=tr, location=(tx, ty, tz))
    tseg = bpy.context.active_object
    tseg.name = f"TailSeg_{idx}"
    tseg.data.materials.append(mat_fox_glow if idx >= 1 else mat_fox_fur)

# 5. Environment: Giant Bioluminescent Mushrooms & Crystal Bridge
# Giant Teal Mushroom (Left)
bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=2.8, location=(-1.4, 0.6, 1.2))
m_stem1 = bpy.context.active_object
m_stem1.data.materials.append(mat_stem)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.95, location=(-1.4, 0.6, 2.5))
m_cap1 = bpy.context.active_object
m_cap1.scale = (1.3, 1.3, 0.35)
m_cap1.data.materials.append(mat_mushroom_cap)

# Giant Purple Mushroom (Right)
bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=2.5, location=(1.5, 0.8, 1.0))
m_stem2 = bpy.context.active_object
m_stem2.data.materials.append(mat_stem)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.85, location=(1.5, 0.8, 2.2))
m_cap2 = bpy.context.active_object
m_cap2.scale = (1.2, 1.2, 0.35)
m_cap2.data.materials.append(mat_mushroom_purple)

# Crystal Cavern Arch / Bridge
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.2, 0.15))
bridge = bpy.context.active_object
bridge.scale = (2.2, 1.8, 0.2)
bridge.data.materials.append(mat_crystal)

# Floating Crystal Spire Shards
crystal_spires = [
    (-0.85, -0.6, 0.45, 0.08, 0.45),
    (0.95, -0.5, 0.40, 0.07, 0.38),
    (-0.45, 0.9, 0.65, 0.10, 0.55),
    (0.40, 1.1, 0.70, 0.09, 0.50),
]
for idx, (cx, cy, cz, cr, ch) in enumerate(crystal_spires):
    bpy.ops.mesh.primitive_cone_add(radius1=cr, depth=ch, location=(cx, cy, cz))
    cspire = bpy.context.active_object
    cspire.rotation_euler = (0.1, -0.15, 0.3)
    cspire.data.materials.append(mat_crystal)

# 6. Cinematic 3-Point + Colored Rim Lighting
# Key Warm Sunbeam Light
sun_data = bpy.data.lights.new(name="SunBeam", type='SUN')
sun_data.energy = 4.2
sun_data.color = (1.0, 0.92, 0.82)
sun_obj = bpy.data.objects.new(name="SunBeam", object_data=sun_data)
bpy.context.collection.objects.link(sun_obj)
sun_obj.rotation_euler = (math.radians(45), math.radians(20), math.radians(35))

# Front Key Character Light
key_data = bpy.data.lights.new(name="KeyPoint", type='POINT')
key_data.energy = 650
key_data.color = (1.0, 0.88, 0.75)
key_obj = bpy.data.objects.new(name="KeyPoint", object_data=key_data)
key_obj.location = (0.8, -2.2, 2.2)
bpy.context.collection.objects.link(key_obj)

# Cool Cyan Fill Light (Reflecting Cavern Crystals)
fill_data = bpy.data.lights.new(name="CyanFill", type='POINT')
fill_data.energy = 450
fill_data.color = (0.2, 0.85, 1.0)
fill_obj = bpy.data.objects.new(name="CyanFill", object_data=fill_data)
fill_obj.location = (-1.8, -1.8, 1.4)
bpy.context.collection.objects.link(fill_obj)

# Magenta Rim Light (Backlight separating character from dark background)
rim_data = bpy.data.lights.new(name="MagentaRim", type='POINT')
rim_data.energy = 850
rim_data.color = (0.95, 0.3, 0.85)
rim_obj = bpy.data.objects.new(name="MagentaRim", object_data=rim_data)
rim_obj.location = (0.0, 1.8, 2.4)
bpy.context.collection.objects.link(rim_obj)

# 7. Cinematic Camera with Depth of Field
cam_data = bpy.data.cameras.new("HeroCamera")
cam_data.lens = 45.0  # 45mm portrait lens
cam_data.dof.use_dof = True
cam_data.dof.focus_object = head
cam_data.dof.aperture_fstop = 2.4  # Shallow cinematic depth of field

cam_obj = bpy.data.objects.new("HeroCamera", object_data=cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (0.05, -2.8, 1.52)
cam_obj.rotation_euler = (math.radians(88), 0, math.radians(2))

# 8. Animate Scene & Visemes over 210 Frames (7 seconds)
total_frames = 210
scene.frame_start = 1
scene.frame_end = total_frames

# Dynamic animated dialogue line: "Look at this place, Lumi! The giant mushrooms are glowing!"
# Lip-sync wave cycle
for f in range(1, total_frames + 1):
    scene.frame_set(f)
    
    # Subtle camera drift (organic handheld motion)
    cam_obj.location.x = 0.05 + math.sin(f * 0.04) * 0.02
    cam_obj.location.z = 1.52 + math.cos(f * 0.03) * 0.015
    cam_obj.keyframe_insert(data_path="location", frame=f)

    # Leo head tilt and breathing
    head.rotation_euler.x = math.sin(f * 0.06) * 0.04
    head.rotation_euler.z = math.sin(f * 0.03) * 0.05
    head.keyframe_insert(data_path="rotation_euler", frame=f)

    # Lip-Sync Shapekey Animation (jawOpen active while talking)
    if f < 180:
        speech_phase = f % 12
        if speech_phase < 6:
            jaw_val = math.sin(speech_phase / 6.0 * math.pi) * 0.75
            pucker_val = math.cos(speech_phase / 6.0 * math.pi) * 0.35
        else:
            jaw_val = 0.05
            pucker_val = 0.0
    else:
        # Smile at the end of sentence
        jaw_val = 0.0
        pucker_val = 0.0
        sk_smile.value = min(1.0, (f - 180) / 20.0) * 0.8
        sk_smile.keyframe_insert(data_path="value", frame=f)

    sk_jaw.value = max(0.0, jaw_val)
    sk_jaw.keyframe_insert(data_path="value", frame=f)
    sk_pucker.value = max(0.0, pucker_val)
    sk_pucker.keyframe_insert(data_path="value", frame=f)

    # Lumi Tail Wag & Ear Twitch
    for idx, (tx, ty, tz, tr) in enumerate(tail_coords):
        tobj = bpy.data.objects.get(f"TailSeg_{idx}")
        if tobj:
            tobj.location.x = tx + math.sin(f * 0.15 + idx * 0.6) * 0.06
            tobj.keyframe_insert(data_path="location", frame=f)

print("[3D Pixar Engine] Scene built successfully. Starting headless render...")
bpy.ops.render.render(animation=True)
print("[3D Pixar Engine] Headless 3D render completed successfully!")
