"""
Test Script: Perfect Framing & Lighting for 3 Acts
"""

import bpy
import math
import os

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 300

if hasattr(scene, "eevee"):
    scene.eevee.taa_render_samples = 8

if 'AgX' in [c.name for c in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items]:
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'Medium High Contrast'
else:
    scene.view_settings.view_transform = 'Filmic'

world = bpy.data.worlds.new("EnchantedWorld")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs['Color'].default_value = (0.015, 0.025, 0.05, 1.0)
    bg.inputs['Strength'].default_value = 0.55

# 1. Import Hero Leo
gltf_hero = r"E:\YT\assets\characters\kaykit_adventurers\addons\kaykit_character_pack_adventures\Characters\gltf\Rogue_Hooded.glb"
bpy.ops.import_scene.gltf(filepath=gltf_hero)

hero_rig = [o for o in bpy.data.objects if o.type == 'ARMATURE' and o.name == 'Rig'][0]
hero_rig.name = "Leo_Hero_Rig"
hero_rig.location = (0, 0, 0)

# Remove weapon objects
weapons_to_remove = ['1H_Crossbow', '2H_Crossbow', 'Knife', 'Knife_Offhand', 'Throwable']
for w_name in weapons_to_remove:
    obj = bpy.data.objects.get(w_name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)

# Apply Leo crimson hoodie texture
leo_tex_path = r"E:\YT\assets\characters\kaykit_adventurers\addons\kaykit_character_pack_adventures\Characters\fbx\leo_texture.png"
tex_image = bpy.data.images.load(leo_tex_path)

mat = bpy.data.materials.get("rogue_texture")
if mat and mat.use_nodes:
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    tex_node = [n for n in mat.node_tree.nodes if n.type == 'TEX_IMAGE']
    if tex_node:
        tex_node[0].image = tex_image
    else:
        new_tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
        new_tex.image = tex_image
        mat.node_tree.links.new(new_tex.outputs['Color'], bsdf.inputs['Base Color'])

# Import Animations
fbx_anim = r"E:\YT\assets\characters\kaykit_animations\Animations\KayKit Animated Character_v1.1.fbx"
bpy.ops.import_scene.fbx(filepath=fbx_anim)
temp_arm = [o for o in bpy.data.objects if o.type == 'ARMATURE' and o != hero_rig][0]

walk_action = bpy.data.actions.get("KayKit Animated Character|KayKit Animated Character|Walk")
wave_action = bpy.data.actions.get("KayKit Animated Character|KayKit Animated Character|Wave")
cheer_action = bpy.data.actions.get("KayKit Animated Character|KayKit Animated Character|Cheer")

bpy.data.objects.remove(temp_arm, do_unlink=True)

# 2. Import Companion Fox (Lumi)
gltf_fox = r"E:\YT\assets\animals\Fox.glb"
bpy.ops.import_scene.gltf(filepath=gltf_fox)

fox_rig = [o for o in bpy.data.objects if o.type == 'ARMATURE' and o != hero_rig][0]
fox_rig.name = "Lumi_Fox_Rig"
fox_rig.scale = (0.012, 0.012, 0.012)
fox_rig.location = (0.62, 0.25, 0.0)
fox_rig.rotation_euler = (0, 0, math.radians(20))

fox_walk = bpy.data.actions.get("Walk_root")
fox_survey = bpy.data.actions.get("Survey_root")

# 3. NLA Strips
hero_rig.animation_data_create()
hero_track = hero_rig.animation_data.nla_tracks.new()

s1 = hero_track.strips.new("WalkStrip", 1, walk_action)
walk_len = walk_action.frame_range[1] - walk_action.frame_range[0]
s1.repeat = 90.0 / walk_len
s1.frame_end = 90

s2 = hero_track.strips.new("WaveStrip", 91, wave_action)
wave_len = wave_action.frame_range[1] - wave_action.frame_range[0]
s2.repeat = 90.0 / wave_len
s2.frame_end = 180

s3 = hero_track.strips.new("CheerStrip", 181, cheer_action)
cheer_len = cheer_action.frame_range[1] - cheer_action.frame_range[0]
s3.repeat = 120.0 / cheer_len
s3.frame_end = 300

hero_rig.animation_data.action = None

fox_rig.animation_data_create()
fox_track = fox_rig.animation_data.nla_tracks.new()

fs1 = fox_track.strips.new("FoxWalk", 1, fox_walk)
f_walk_len = fox_walk.frame_range[1] - fox_walk.frame_range[0]
fs1.repeat = 90.0 / f_walk_len
fs1.frame_end = 90

fs2 = fox_track.strips.new("FoxSurvey", 91, fox_survey)
f_surv_len = fox_survey.frame_range[1] - fox_survey.frame_range[0]
fs2.repeat = 210.0 / f_surv_len
fs2.frame_end = 300

fox_rig.animation_data.action = None

# 4. Environment
def create_pbr_mat(name, base_color, roughness=0.4, metallic=0.0, emission=None, emission_strength=1.0):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    nodes = m.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        if emission:
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = emission
                bsdf.inputs['Emission Strength'].default_value = emission_strength
    return m

mat_stone = create_pbr_mat("BridgeStone", (0.28, 0.30, 0.35, 1.0), roughness=0.7)
mat_gold = create_pbr_mat("GoldRune", (0.85, 0.70, 0.20, 1.0), roughness=0.25, metallic=0.8, emission=(0.95, 0.8, 0.2, 1.0), emission_strength=1.5)
mat_crystal = create_pbr_mat("CrystalCyan", (0.15, 0.85, 1.0, 1.0), roughness=0.15, emission=(0.10, 0.85, 1.0, 1.0), emission_strength=3.5)
mat_shroom_teal = create_pbr_mat("ShroomTeal", (0.08, 0.75, 0.70, 1.0), roughness=0.35, emission=(0.08, 0.75, 0.70, 1.0), emission_strength=2.2)
mat_shroom_purple = create_pbr_mat("ShroomPurple", (0.75, 0.20, 0.88, 1.0), roughness=0.35, emission=(0.75, 0.20, 0.88, 1.0), emission_strength=2.5)

# Bridge deck
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.15))
deck = bpy.context.active_object
deck.scale = (2.2, 22.0, 0.30)
bpy.ops.object.transform_apply(scale=True)
deck.data.materials.append(mat_stone)

# Edge curbs
for sx in [-1.05, 1.05]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sx, 0, 0.08))
    curb = bpy.context.active_object
    curb.scale = (0.18, 22.0, 0.16)
    bpy.ops.object.transform_apply(scale=True)
    curb.data.materials.append(mat_gold)

# Lantern Pillars
for py in [-6.0, -3.5, -1.0, 1.5, 4.0, 6.5]:
    for px in [-1.15, 1.15]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.08, depth=0.8, location=(px, py, 0.4))
        p = bpy.context.active_object
        p.data.materials.append(mat_stone)
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(px, py, 0.85))
        c = bpy.context.active_object
        c.data.materials.append(mat_crystal)

# Mushrooms
shrooms = [
    (-3.0, -2.0, 0.0, 1.8, mat_shroom_teal),
    (3.2, -0.5, 0.2, 2.2, mat_shroom_purple),
    (-3.4, 2.5, 0.3, 2.5, mat_shroom_purple),
    (3.0, 4.8, 0.1, 1.9, mat_shroom_teal),
    (-3.2, 6.5, 0.4, 2.3, mat_shroom_teal)
]
for mx, my, mz, scale_s, cap_mat in shrooms:
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.15 * scale_s, depth=2.0 * scale_s, location=(mx, my, mz + 1.0 * scale_s))
    st = bpy.context.active_object
    st.data.materials.append(mat_stone)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=0.9 * scale_s, location=(mx, my, mz + 2.0 * scale_s))
    cp = bpy.context.active_object
    cp.scale = (1.0, 1.0, 0.4)
    bpy.ops.object.transform_apply(scale=True)
    cp.data.materials.append(cap_mat)

# 5. Lighting (with dedicated Face Key Light)
# Main Key Light
l_key_data = bpy.data.lights.new("KeyLight", type='POINT')
l_key_data.energy = 200
l_key_data.color = (1.0, 0.88, 0.72)
l_key_data.shadow_soft_size = 0.35
l_key = bpy.data.objects.new("KeyLight", l_key_data)
bpy.context.collection.objects.link(l_key)
l_key.location = (-1.8, -2.5, 2.6)

# Face Upward Fill Light (illuminates face & eyes under hood)
l_face_data = bpy.data.lights.new("FaceFillLight", type='POINT')
l_face_data.energy = 95
l_face_data.color = (1.0, 0.94, 0.85)
l_face_data.shadow_soft_size = 0.5
l_face = bpy.data.objects.new("FaceFillLight", l_face_data)
bpy.context.collection.objects.link(l_face)
l_face.location = (-0.2, -2.2, 1.1)

# Cool Ambient Fill Light
l_fill_data = bpy.data.lights.new("FillLight", type='POINT')
l_fill_data.energy = 70
l_fill_data.color = (0.4, 0.55, 0.95)
l_fill_data.shadow_soft_size = 0.7
l_fill = bpy.data.objects.new("FillLight", l_fill_data)
bpy.context.collection.objects.link(l_fill)
l_fill.location = (2.2, -1.0, 2.2)

# Rim Light (cyan kicker)
l_rim_data = bpy.data.lights.new("RimLight", type='SPOT')
l_rim_data.energy = 420
l_rim_data.color = (0.2, 0.9, 1.0)
l_rim_data.spot_size = math.radians(70)
l_rim_data.shadow_soft_size = 0.25
l_rim = bpy.data.objects.new("RimLight", l_rim_data)
bpy.context.collection.objects.link(l_rim)
l_rim.location = (0.5, 2.5, 2.2)
l_rim.rotation_euler = (math.radians(-45), 0, math.radians(-160))

# 6. Camera Setup & Keyframing across 300 frames
cam_data = bpy.data.cameras.new("DirectorCamera")
cam_data.lens = 42
cam_data.dof.use_dof = True
cam_data.dof.focus_distance = 3.0
cam_data.dof.aperture_fstop = 2.8

cam_obj = bpy.data.objects.new("DirectorCamera", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

for f in range(1, 301):
    # ACT 1 (F1-90): Walk locomotion
    if f <= 90:
        y_travel = -2.5 + (f / 90.0) * 1.5
        hero_rig.location = (0.0, y_travel, 0.0)
        hero_rig.keyframe_insert(data_path="location", frame=f)
        
        fox_rig.location = (0.60, y_travel + 0.25, 0.0)
        fox_rig.keyframe_insert(data_path="location", frame=f)
        
        cam_obj.location = (0.05, y_travel - 3.4, 1.25)
        cam_obj.rotation_euler = (math.radians(82), 0, math.radians(2))
        cam_obj.keyframe_insert(data_path="location", frame=f)
        cam_obj.keyframe_insert(data_path="rotation_euler", frame=f)
        cam_data.dof.focus_distance = 3.4
        cam_data.keyframe_insert(data_path="dof.focus_distance", frame=f)
        
    # ACT 2 (F91-180): Settle & Look Up / Wave (Proper Head Framing)
    elif f <= 180:
        hero_rig.location = (0.0, -1.0, 0.0)
        hero_rig.keyframe_insert(data_path="location", frame=f)
        
        fox_rig.location = (0.60, -0.75, 0.0)
        fox_rig.keyframe_insert(data_path="location", frame=f)
        
        prog = (f - 90) / 90.0
        cam_x = -0.30 + prog * 0.15
        cam_y = -3.5 - prog * 0.1
        cam_z = 1.35 + prog * 0.10
        cam_obj.location = (cam_x, cam_y, cam_z)
        cam_obj.rotation_euler = (math.radians(82), 0, math.radians(-5 + prog * 3))
        cam_obj.keyframe_insert(data_path="location", frame=f)
        cam_obj.keyframe_insert(data_path="rotation_euler", frame=f)
        cam_data.dof.focus_distance = 2.9
        cam_data.keyframe_insert(data_path="dof.focus_distance", frame=f)
        
    # ACT 3 (F181-300): Hero Close-up & Celebration (Cheer) - Perfectly centered on face
    else:
        hero_rig.location = (0.0, -1.0, 0.0)
        hero_rig.keyframe_insert(data_path="location", frame=f)
        
        fox_rig.location = (0.60, -0.75, 0.0)
        fox_rig.keyframe_insert(data_path="location", frame=f)
        
        prog3 = (f - 180) / 120.0
        cam_obj.location = (-0.05, -2.55 - prog3 * 0.10, 1.55)
        cam_obj.rotation_euler = (math.radians(84), 0, math.radians(-2))
        cam_obj.keyframe_insert(data_path="location", frame=f)
        cam_obj.keyframe_insert(data_path="rotation_euler", frame=f)
        cam_data.lens = 48
        cam_data.keyframe_insert(data_path="lens", frame=f)
        cam_data.dof.focus_distance = 1.65
        cam_data.keyframe_insert(data_path="dof.focus_distance", frame=f)

# Re-render test frames 45, 135, 240
test_frames = [45, 135, 240]
for tf in test_frames:
    scene.frame_set(tf)
    p = rf"E:\YT\output\renders\perfect_act_{tf:04d}.png"
    scene.render.filepath = p
    bpy.ops.render.render(write_still=True)
    print(f"Rendered perfect frame {tf} to {p}")
