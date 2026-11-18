"""
Builds high-quality 3D character using MakeHuman/MPFB base topology and targets
Renders Leo & Lumi in Blender 4.2 LTS with EEVEE-Next, Subsurface Scattering, and AgX color.
"""

import bpy
import gzip
import os
import math
from pathlib import Path

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# Configure Render Engine & Resolution
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
if hasattr(scene, "eevee"):
    scene.eevee.use_gtao = True
    scene.eevee.use_bloom = True
    scene.eevee.use_ssr = True

scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100

# Color Management (Filmic / AgX)
scene.view_settings.view_transform = 'AgX' if 'AgX' in [c.name for c in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
scene.view_settings.look = 'High Contrast'

# 1. World & Atmosphere
world = bpy.data.worlds.new("PixarWorld")
scene.world = world
world.use_nodes = True
n = world.node_tree.nodes
l = world.node_tree.links
n.clear()

bg = n.new(type='ShaderNodeBackground')
bg.inputs['Color'].default_value = (0.015, 0.02, 0.05, 1.0)
bg.inputs['Strength'].default_value = 0.6
out = n.new(type='ShaderNodeOutputWorld')
l.new(bg.outputs['Background'], out.inputs['Surface'])

# Volume Scatter
vol = n.new(type='ShaderNodeVolumeScatter')
vol.inputs['Density'].default_value = 0.015
vol.inputs['Color'].default_value = (0.1, 0.35, 0.6, 1.0)
l.new(vol.outputs['Volume'], out.inputs['Volume'])

# 2. Materials
def make_principled_mat(name, base_color, roughness=0.35, sss=0.0, sss_radius=(0.35, 0.15, 0.08), emission=None):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Roughness'].default_value = roughness
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = sss
            bsdf.inputs['Subsurface Radius'].default_value = sss_radius
        elif 'Subsurface' in bsdf.inputs:
            bsdf.inputs['Subsurface'].default_value = sss
        if emission:
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = emission[0]
                bsdf.inputs['Emission Strength'].default_value = emission[1]
            elif 'Emission' in bsdf.inputs:
                bsdf.inputs['Emission'].default_value = emission[0]
    return mat

mat_skin = make_principled_mat("Leo_Skin", (0.94, 0.76, 0.64, 1.0), roughness=0.36, sss=0.28)
mat_hair = make_principled_mat("Leo_Hair", (0.28, 0.16, 0.08, 1.0), roughness=0.42)
mat_hoodie = make_principled_mat("Leo_Hoodie", (0.85, 0.22, 0.15, 1.0), roughness=0.75)
mat_backpack = make_principled_mat("Leo_Backpack", (0.15, 0.45, 0.55, 1.0), roughness=0.6)
mat_eye_white = make_principled_mat("EyeWhite", (0.98, 0.98, 0.98, 1.0), roughness=0.04)
mat_iris = make_principled_mat("Iris", (0.2, 0.55, 0.8, 1.0), roughness=0.04)
mat_pupil = make_principled_mat("Pupil", (0.01, 0.01, 0.01, 1.0), roughness=0.02)
mat_fox_fur = make_principled_mat("Lumi_Fur", (0.95, 0.20, 0.65, 1.0), roughness=0.55)
mat_fox_glow = make_principled_mat("Lumi_Glow", (0.2, 0.85, 1.0, 1.0), roughness=0.2, emission=((0.2, 0.85, 1.0, 1.0), 3.8))
mat_crystal = make_principled_mat("Crystal", (0.4, 0.85, 1.0, 1.0), roughness=0.1, emission=((0.25, 0.8, 1.0, 1.0), 1.5))
mat_mushroom_cap = make_principled_mat("MushroomCap", (0.05, 0.65, 0.55, 1.0), roughness=0.4, emission=((0.1, 0.7, 0.6, 1.0), 2.2))
mat_mushroom_purple = make_principled_mat("MushroomPurple", (0.75, 0.25, 0.85, 1.0), roughness=0.4, emission=((0.8, 0.2, 0.9, 1.0), 2.5))
mat_stem = make_principled_mat("Stem", (0.15, 0.25, 0.3, 1.0), roughness=0.6)

# 3. Import Official MPFB Base Mesh (19,158 Quads)
base_obj_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\3dobjs\base.obj"
print(f"Loading MakeHuman base mesh from: {base_obj_path}...")
bpy.ops.wm.obj_import(filepath=base_obj_path)
body = bpy.context.active_object
body.name = "Leo_Body"

# Apply MakeHuman Child Target to morph from neutral adult to Child (Leo)
child_target_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\targets\macrodetails\caucasian-male-child.target.gz"
if os.path.exists(child_target_path):
    print("Applying MakeHuman Child morph target...")
    with gzip.open(child_target_path, "rt", encoding="utf-8") as f:
        target_lines = f.readlines()
    for line in target_lines:
        parts = line.strip().split()
        if len(parts) == 4:
            v_idx = int(parts[0])
            if v_idx < len(body.data.vertices):
                body.data.vertices[v_idx].co.x += float(parts[1])
                body.data.vertices[v_idx].co.y += float(parts[2])
                body.data.vertices[v_idx].co.z += float(parts[3])

# Smooth Shading & Subdivision Surface (Removes all faceting, perfectly smooth skin)
for poly in body.data.polygons:
    poly.use_smooth = True

subsurf = body.modifiers.new(name="Subdivision", type='SUBSURF')
subsurf.levels = 1
subsurf.render_levels = 2

# Scale and position Leo
body.scale = (0.9, 0.9, 0.9)
body.location = (0, 0, 0.1)
bpy.ops.object.transform_apply(location=True, scale=True)

# Assign Skin Material
body.data.materials.append(mat_skin)

# 4. Add Big Expressive Pixar Eyes
head_center_z = 1.48
eye_y = -0.15
eye_spacing = 0.085

for side, sign in [("L", 1), ("R", -1)]:
    # Sclera (White)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.052, location=(eye_spacing * sign, eye_y, head_center_z))
    eye_white = bpy.context.active_object
    eye_white.name = f"EyeWhite_{side}"
    eye_white.scale = (1.0, 0.7, 1.1)
    for p in eye_white.data.polygons: p.use_smooth = True
    eye_white.data.materials.append(mat_eye_white)

    # Iris (Vibrant Blue)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.032, location=(eye_spacing * sign, eye_y - 0.038, head_center_z))
    iris = bpy.context.active_object
    iris.name = f"Iris_{side}"
    iris.scale = (1.0, 0.3, 1.0)
    for p in iris.data.polygons: p.use_smooth = True
    iris.data.materials.append(mat_iris)

    # Pupil (Deep Black)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.016, location=(eye_spacing * sign, eye_y - 0.046, head_center_z))
    pupil = bpy.context.active_object
    pupil.name = f"Pupil_{side}"
    pupil.scale = (1.0, 0.3, 1.0)
    for p in pupil.data.polygons: p.use_smooth = True
    pupil.data.materials.append(mat_pupil)

# 5. Stylized Hair (Sculpted locks matching reference art)
hair_locks = [
    (0.0, -0.05, 1.68, 0.20, 1.0, 0.8),
    (0.12, -0.02, 1.65, 0.15, 0.9, 0.8),
    (-0.12, -0.02, 1.65, 0.15, 0.9, 0.8),
    (0.08, -0.14, 1.60, 0.10, 1.2, 0.6), # front locks
    (-0.08, -0.14, 1.60, 0.10, 1.2, 0.6),
    (0.0, -0.16, 1.62, 0.09, 1.1, 0.6),
    (0.16, 0.02, 1.50, 0.12, 0.7, 0.9), # sideburns
    (-0.16, 0.02, 1.50, 0.12, 0.7, 0.9),
]
for idx, (hx, hy, hz, hr, sx, sy) in enumerate(hair_locks):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=hr, location=(hx, hy, hz))
    h = bpy.context.active_object
    h.scale = (sx, sy, 1.0)
    for p in h.data.polygons: p.use_smooth = True
    sub = h.modifiers.new(name="Subsurf", type='SUBSURF')
    sub.levels = 1
    h.data.materials.append(mat_hair)

# 6. Crimson Adventure Hoodie
bpy.ops.mesh.primitive_cylinder_add(radius=0.26, depth=0.65, location=(0, 0.02, 0.98))
hoodie = bpy.context.active_object
hoodie.name = "Leo_Hoodie"
hoodie.scale = (1.05, 0.85, 1.0)
for p in hoodie.data.polygons: p.use_smooth = True
sub_h = hoodie.modifiers.new(name="Subsurf", type='SUBSURF')
sub_h.levels = 1
hoodie.data.materials.append(mat_hoodie)

# Hoodie Collar & Drawstrings
bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.04, location=(0, -0.02, 1.28))
collar = bpy.context.active_object
collar.rotation_euler = (math.radians(20), 0, 0)
for p in collar.data.polygons: p.use_smooth = True
collar.data.materials.append(mat_hoodie)

# Backpack
bpy.ops.mesh.primitive_cube_add(size=0.28, location=(0, 0.22, 1.05))
bp = bpy.context.active_object
bp.name = "Backpack"
bp.scale = (0.9, 0.55, 1.1)
for p in bp.data.polygons: p.use_smooth = True
sub_bp = bp.modifiers.new(name="Subsurf", type='SUBSURF')
sub_bp.levels = 1
bp.data.materials.append(mat_backpack)

# 7. Lumi (Magical Companion Fox)
fox_x = 0.42
fox_y = -0.15
fox_z = 0.85

# Fox Head
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(fox_x, fox_y, fox_z + 0.22))
fhead = bpy.context.active_object
fhead.scale = (1.1, 1.2, 0.95)
for p in fhead.data.polygons: p.use_smooth = True
fhead.data.materials.append(mat_fox_fur)

# Fox Snout
bpy.ops.mesh.primitive_cone_add(radius1=0.05, depth=0.10, location=(fox_x, fox_y - 0.12, fox_z + 0.18))
snout = bpy.context.active_object
snout.rotation_euler = (math.radians(-90), 0, 0)
for p in snout.data.polygons: p.use_smooth = True
snout.data.materials.append(mat_fox_glow)

# Fox Pointed Ears
for side, sign in [("L", 1), ("R", -1)]:
    bpy.ops.mesh.primitive_cone_add(radius1=0.055, depth=0.15, location=(fox_x + 0.08 * sign, fox_y, fox_z + 0.35))
    ear = bpy.context.active_object
    ear.rotation_euler = (0, 0.25 * sign, 0)
    for p in ear.data.polygons: p.use_smooth = True
    ear.data.materials.append(mat_fox_fur)

# Fox Glowing Anime Eyes
for side, sign in [("L", 1), ("R", -1)]:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.042, location=(fox_x + 0.06 * sign, fox_y - 0.09, fox_z + 0.24))
    feye = bpy.context.active_object
    feye.scale = (1.0, 0.4, 1.2)
    for p in feye.data.polygons: p.use_smooth = True
    feye.data.materials.append(mat_fox_glow)

# Fox Fluffy Body
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16, location=(fox_x, fox_y + 0.10, fox_z + 0.08))
fbody = bpy.context.active_object
fbody.scale = (0.8, 1.2, 0.9)
for p in fbody.data.polygons: p.use_smooth = True
fbody.data.materials.append(mat_fox_fur)

# Fox Enormous Bioluminescent Tail
tail_coords = [
    (fox_x, fox_y + 0.22, fox_z + 0.10, 0.10),
    (fox_x + 0.06, fox_y + 0.32, fox_z + 0.22, 0.14),
    (fox_x + 0.09, fox_y + 0.36, fox_z + 0.36, 0.15),
    (fox_x + 0.04, fox_y + 0.28, fox_z + 0.48, 0.11),
]
for idx, (tx, ty, tz, tr) in enumerate(tail_coords):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=tr, location=(tx, ty, tz))
    tseg = bpy.context.active_object
    for p in tseg.data.polygons: p.use_smooth = True
    tseg.data.materials.append(mat_fox_glow if idx >= 1 else mat_fox_fur)

# 8. Environment: Bioluminescent Giant Mushrooms & Crystal Cavern
# Giant Teal Mushroom (Left Background)
bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=2.8, location=(-1.1, 0.5, 1.2))
m1_stem = bpy.context.active_object
for p in m1_stem.data.polygons: p.use_smooth = True
m1_stem.data.materials.append(mat_stem)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.85, location=(-1.1, 0.5, 2.3))
m1_cap = bpy.context.active_object
m1_cap.scale = (1.3, 1.3, 0.32)
for p in m1_cap.data.polygons: p.use_smooth = True
m1_cap.data.materials.append(mat_mushroom_cap)

# Giant Purple Mushroom (Right Background)
bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=2.4, location=(1.2, 0.7, 1.0))
m2_stem = bpy.context.active_object
for p in m2_stem.data.polygons: p.use_smooth = True
m2_stem.data.materials.append(mat_stem)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.75, location=(1.2, 0.7, 2.0))
m2_cap = bpy.context.active_object
m2_cap.scale = (1.2, 1.2, 0.32)
for p in m2_cap.data.polygons: p.use_smooth = True
m2_cap.data.materials.append(mat_mushroom_purple)

# Crystal Arch Bridge Platform
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.15, 0.35))
bridge = bpy.context.active_object
bridge.scale = (1.8, 1.4, 0.15)
for p in bridge.data.polygons: p.use_smooth = True
bridge.data.materials.append(mat_crystal)

# 9. Cinematic 3-Point + Colored Rim Lighting
# Warm Key Light (Sunbeam / Lantern)
key = bpy.data.lights.new(name="WarmKey", type='POINT')
key.energy = 550
key.color = (1.0, 0.88, 0.74)
key_obj = bpy.data.objects.new(name="WarmKey", object_data=key)
key_obj.location = (0.7, -1.8, 2.2)
bpy.context.collection.objects.link(key_obj)

# Cool Cyan Fill Light (Reflecting Crystal Bridge)
fill = bpy.data.lights.new(name="CyanFill", type='POINT')
fill.energy = 380
fill.color = (0.2, 0.85, 1.0)
fill_obj = bpy.data.objects.new(name="CyanFill", object_data=fill)
fill_obj.location = (-1.5, -1.5, 1.3)
bpy.context.collection.objects.link(fill_obj)

# Vibrant Magenta/Pink Rim Light (Separates character from dark backdrop)
rim = bpy.data.lights.new(name="PinkRim", type='POINT')
rim.energy = 750
rim.color = (0.95, 0.35, 0.85)
rim_obj = bpy.data.objects.new(name="PinkRim", object_data=rim)
rim_obj.location = (0.1, 1.6, 2.2)
bpy.context.collection.objects.link(rim_obj)

# 10. Camera with Portrait Depth of Field
cam_data = bpy.data.cameras.new("HeroCam")
cam_data.lens = 50.0  # 50mm portrait lens
cam_data.dof.use_dof = True
cam_data.dof.focus_distance = 2.1
cam_data.dof.aperture_fstop = 2.2  # Shallow cinematic depth of field

cam_obj = bpy.data.objects.new("HeroCam", object_data=cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (0.05, -2.1, 1.42)
cam_obj.rotation_euler = (math.radians(88), 0, math.radians(2))

# 11. Render Single Master Hero Frame
output_file = r"E:\YT\output\renders\leo_3d_real.png"
scene.render.filepath = output_file
print(f"Rendering high-quality 3D Pixar character frame to: {output_file}...")
bpy.ops.render.render(write_still=True)
print("✔ Master 3D render finished successfully!")
