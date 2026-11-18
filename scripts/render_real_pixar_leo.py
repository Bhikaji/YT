"""
Renders Real 3D Pixar-style Character Leo using MakeHuman Base Mesh & Proper Scale
"""

import bpy
import gzip
import os
import math

# 1. Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# Configure EEVEE-Next
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100

# Color Management
scene.view_settings.view_transform = 'AgX' if 'AgX' in [c.name for c in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
scene.view_settings.look = 'Medium High Contrast'

# 2. World Lighting & Ambient Mist
world = bpy.data.worlds.new("PixarWorld")
scene.world = world
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links
nodes.clear()

bg = nodes.new(type='ShaderNodeBackground')
bg.inputs['Color'].default_value = (0.015, 0.025, 0.06, 1.0)
bg.inputs['Strength'].default_value = 0.8
out = nodes.new(type='ShaderNodeOutputWorld')
links.new(bg.outputs['Background'], out.inputs['Surface'])

# 3. Materials
def make_mat(name, base_color, roughness=0.35, sss=0.0, emission=None):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    n = mat.node_tree.nodes
    bsdf = n.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
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

mat_skin = make_mat("LeoSkin", (0.94, 0.76, 0.64, 1.0), roughness=0.36, sss=0.28)
mat_hair = make_mat("LeoHair", (0.28, 0.16, 0.08, 1.0), roughness=0.42)
mat_hoodie = make_mat("LeoHoodie", (0.85, 0.22, 0.15, 1.0), roughness=0.75)
mat_eye_white = make_mat("EyeWhite", (0.98, 0.98, 0.98, 1.0), roughness=0.05)
mat_iris = make_mat("Iris", (0.18, 0.55, 0.82, 1.0), roughness=0.05)
mat_pupil = make_mat("Pupil", (0.01, 0.01, 0.01, 1.0), roughness=0.02)
mat_fox_fur = make_mat("LumiFur", (0.95, 0.20, 0.65, 1.0), roughness=0.55)
mat_fox_glow = make_mat("LumiGlow", (0.2, 0.85, 1.0, 1.0), roughness=0.2, emission=((0.2, 0.85, 1.0, 1.0), 3.5))
mat_crystal = make_mat("Crystal", (0.35, 0.85, 1.0, 1.0), roughness=0.1, emission=((0.25, 0.8, 1.0, 1.0), 1.2))
mat_mushroom_teal = make_mat("MushroomTeal", (0.05, 0.65, 0.55, 1.0), roughness=0.4, emission=((0.1, 0.7, 0.6, 1.0), 1.8))
mat_mushroom_purple = make_mat("MushroomPurple", (0.75, 0.25, 0.85, 1.0), roughness=0.4, emission=((0.8, 0.2, 0.9, 1.0), 2.0))
mat_stem = make_mat("MushroomStem", (0.15, 0.25, 0.3, 1.0), roughness=0.6)

# 4. Import & Morph Base Human Mesh
base_obj_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\3dobjs\base.obj"
print("Importing base human mesh...")
bpy.ops.wm.obj_import(filepath=base_obj_path)
body = bpy.context.active_object
body.name = "Leo_Body"

# Morph to child
child_target_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\targets\macrodetails\caucasian-male-child.target.gz"
if os.path.exists(child_target_path):
    print("Applying child target...")
    with gzip.open(child_target_path, "rt", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 4:
                idx = int(parts[0])
                if idx < len(body.data.vertices):
                    body.data.vertices[idx].co.x += float(parts[1])
                    body.data.vertices[idx].co.y += float(parts[2])
                    body.data.vertices[idx].co.z += float(parts[3])

# Rotate to standing upright and scale to child dimensions
body.rotation_euler = (math.radians(90), 0, 0)
bpy.ops.object.transform_apply(rotation=True)
body.scale = (0.082, 0.082, 0.082) # ~1.39 meters tall boy
bpy.ops.object.transform_apply(scale=True)

# Smooth Shading and Subsurf
for p in body.data.polygons:
    p.use_smooth = True
subsurf = body.modifiers.new(name="Subdivision", type='SUBSURF')
subsurf.levels = 1
subsurf.render_levels = 2

body.data.materials.append(mat_skin)

# Center of head
head_z = 1.30
eye_y = -0.095
eye_x = 0.038

# 5. Add Big Stylized Pixar Eyes
for side, sign in [("L", 1), ("R", -1)]:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.036, location=(eye_x * sign, eye_y, head_z + 0.015))
    ew = bpy.context.active_object
    ew.scale = (1.0, 0.65, 1.1)
    for p in ew.data.polygons: p.use_smooth = True
    ew.data.materials.append(mat_eye_white)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.024, location=(eye_x * sign, eye_y - 0.022, head_z + 0.015))
    ir = bpy.context.active_object
    ir.scale = (1.0, 0.3, 1.0)
    for p in ir.data.polygons: p.use_smooth = True
    ir.data.materials.append(mat_iris)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.012, location=(eye_x * sign, eye_y - 0.028, head_z + 0.015))
    pu = bpy.context.active_object
    pu.scale = (1.0, 0.3, 1.0)
    for p in pu.data.polygons: p.use_smooth = True
    pu.data.materials.append(mat_pupil)

# 6. Stylized Hair Locks
hair_locks = [
    (0.0, -0.04, head_z + 0.12, 0.14, 1.0, 0.9),
    (0.08, -0.02, head_z + 0.10, 0.11, 0.9, 0.8),
    (-0.08, -0.02, head_z + 0.10, 0.11, 0.9, 0.8),
    (0.05, -0.10, head_z + 0.07, 0.08, 1.1, 0.6), # front fringe
    (-0.05, -0.10, head_z + 0.07, 0.08, 1.1, 0.6),
    (0.0, -0.11, head_z + 0.08, 0.07, 1.0, 0.6),
    (0.11, 0.01, head_z, 0.08, 0.6, 1.0), # sideburns
    (-0.11, 0.01, head_z, 0.08, 0.6, 1.0),
]
for hx, hy, hz, hr, sx, sy in hair_locks:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=hr, location=(hx, hy, hz))
    h = bpy.context.active_object
    h.scale = (sx, sy, 1.0)
    for p in h.data.polygons: p.use_smooth = True
    sub_h = h.modifiers.new(name="Subsurf", type='SUBSURF')
    sub_h.levels = 1
    h.data.materials.append(mat_hair)

# 7. Adventure Crimson Hoodie
bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=0.55, location=(0, 0.01, 0.88))
hoodie = bpy.context.active_object
hoodie.scale = (1.05, 0.82, 1.0)
for p in hoodie.data.polygons: p.use_smooth = True
sub_hd = hoodie.modifiers.new(name="Subsurf", type='SUBSURF')
sub_hd.levels = 1
hoodie.data.materials.append(mat_hoodie)

bpy.ops.mesh.primitive_torus_add(major_radius=0.11, minor_radius=0.035, location=(0, -0.02, 1.14))
collar = bpy.context.active_object
collar.rotation_euler = (math.radians(22), 0, 0)
for p in collar.data.polygons: p.use_smooth = True
collar.data.materials.append(mat_hoodie)

# 8. Lumi (Magical Companion Fox sitting beside Leo)
fox_x = 0.32
fox_y = -0.12
fox_z = 0.72

# Fox Head
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.09, location=(fox_x, fox_y, fox_z + 0.18))
fhead = bpy.context.active_object
fhead.scale = (1.1, 1.2, 0.95)
for p in fhead.data.polygons: p.use_smooth = True
fhead.data.materials.append(mat_fox_fur)

# Fox Snout
bpy.ops.mesh.primitive_cone_add(radius1=0.04, depth=0.08, location=(fox_x, fox_y - 0.09, fox_z + 0.15))
snout = bpy.context.active_object
snout.rotation_euler = (math.radians(-90), 0, 0)
for p in snout.data.polygons: p.use_smooth = True
snout.data.materials.append(mat_fox_glow)

# Fox Pointed Ears
for side, sign in [("L", 1), ("R", -1)]:
    bpy.ops.mesh.primitive_cone_add(radius1=0.045, depth=0.12, location=(fox_x + 0.06 * sign, fox_y, fox_z + 0.28))
    ear = bpy.context.active_object
    ear.rotation_euler = (0, 0.25 * sign, 0)
    for p in ear.data.polygons: p.use_smooth = True
    ear.data.materials.append(mat_fox_fur)

# Fox Glowing Eyes
for side, sign in [("L", 1), ("R", -1)]:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.032, location=(fox_x + 0.045 * sign, fox_y - 0.07, fox_z + 0.20))
    feye = bpy.context.active_object
    feye.scale = (1.0, 0.4, 1.2)
    for p in feye.data.polygons: p.use_smooth = True
    feye.data.materials.append(mat_fox_glow)

# Fox Fluffy Body
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(fox_x, fox_y + 0.08, fox_z + 0.06))
fbody = bpy.context.active_object
fbody.scale = (0.8, 1.2, 0.9)
for p in fbody.data.polygons: p.use_smooth = True
fbody.data.materials.append(mat_fox_fur)

# Fox Glowing Tail
tail_coords = [
    (fox_x, fox_y + 0.16, fox_z + 0.08, 0.08),
    (fox_x + 0.05, fox_y + 0.25, fox_z + 0.18, 0.11),
    (fox_x + 0.07, fox_y + 0.28, fox_z + 0.29, 0.12),
    (fox_x + 0.03, fox_y + 0.22, fox_z + 0.38, 0.09),
]
for idx, (tx, ty, tz, tr) in enumerate(tail_coords):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=tr, location=(tx, ty, tz))
    tseg = bpy.context.active_object
    for p in tseg.data.polygons: p.use_smooth = True
    tseg.data.materials.append(mat_fox_glow if idx >= 1 else mat_fox_fur)

# 9. Bioluminescent Mushrooms & Cavern Crystals in Background
# Teal Mushroom
bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=2.4, location=(-0.95, 0.6, 1.1))
m1_s = bpy.context.active_object
for p in m1_s.data.polygons: p.use_smooth = True
m1_s.data.materials.append(mat_stem)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.75, location=(-0.95, 0.6, 2.1))
m1_c = bpy.context.active_object
m1_c.scale = (1.3, 1.3, 0.3)
for p in m1_c.data.polygons: p.use_smooth = True
m1_c.data.materials.append(mat_mushroom_teal)

# Purple Mushroom
bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=2.2, location=(1.05, 0.8, 0.9))
m2_s = bpy.context.active_object
for p in m2_s.data.polygons: p.use_smooth = True
m2_s.data.materials.append(mat_stem)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.65, location=(1.05, 0.8, 1.8))
m2_c = bpy.context.active_object
m2_c.scale = (1.2, 1.2, 0.3)
for p in m2_c.data.polygons: p.use_smooth = True
m2_c.data.materials.append(mat_mushroom_purple)

# 10. Studio Balanced Lighting (No over-exposure)
# Key Warm Sun Light
sun = bpy.data.lights.new(name="Sun", type='SUN')
sun.energy = 2.2
sun.color = (1.0, 0.94, 0.86)
sun_obj = bpy.data.objects.new(name="Sun", object_data=sun)
sun_obj.rotation_euler = (math.radians(52), math.radians(18), math.radians(25))
bpy.context.collection.objects.link(sun_obj)

# Front Soft Point Key
key = bpy.data.lights.new(name="KeyPoint", type='POINT')
key.energy = 35.0
key.color = (1.0, 0.90, 0.78)
key_obj = bpy.data.objects.new(name="KeyPoint", object_data=key)
key_obj.location = (0.5, -1.2, 1.6)
bpy.context.collection.objects.link(key_obj)

# Soft Cyan Fill Light
fill = bpy.data.lights.new(name="CyanFill", type='POINT')
fill.energy = 25.0
fill.color = (0.2, 0.85, 1.0)
fill_obj = bpy.data.objects.new(name="CyanFill", object_data=fill)
fill_obj.location = (-0.9, -1.0, 1.2)
bpy.context.collection.objects.link(fill_obj)

# Dramatic Pink Rim Light
rim = bpy.data.lights.new(name="PinkRim", type='POINT')
rim.energy = 60.0
rim.color = (0.98, 0.35, 0.88)
rim_obj = bpy.data.objects.new(name="PinkRim", object_data=rim)
rim_obj.location = (0.0, 0.9, 1.8)
bpy.context.collection.objects.link(rim_obj)

# 11. Camera Focused on Leo
cam_data = bpy.data.cameras.new("DirectorCam")
cam_data.lens = 55.0  # Portrait lens
cam_data.dof.use_dof = True
cam_data.dof.focus_distance = 1.35
cam_data.dof.aperture_fstop = 2.8

cam_obj = bpy.data.objects.new("DirectorCam", object_data=cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (0.04, -1.35, 1.28)
cam_obj.rotation_euler = (math.radians(91), 0, math.radians(2))

# 12. Render Still Output
output_path = r"E:\YT\output\renders\leo_3d_real.png"
scene.render.filepath = output_path
print(f"Rendering calibrated 3D Pixar character frame to: {output_path}...")
bpy.ops.render.render(write_still=True)
print("✔ 3D Pixar character render completed!")
