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
    scene.eevee.taa_render_samples = 16

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
    bg.inputs['Strength'].default_value = 0.5

# 1. Import Rogue (Hero Leo)
gltf_hero = r"E:\YT\assets\characters\kaykit_adventurers\addons\kaykit_character_pack_adventures\Characters\gltf\Rogue_Hooded.glb"
bpy.ops.import_scene.gltf(filepath=gltf_hero)

hero_rig = [o for o in bpy.data.objects if o.type == 'ARMATURE' and o.name == 'Rig'][0]
hero_rig.name = "Leo_Hero_Rig"
hero_rig.location = (0, 0, 0)

# Import Animations from KayKit Animated Character FBX
fbx_anim = r"E:\YT\assets\characters\kaykit_animations\Animations\KayKit Animated Character_v1.1.fbx"
bpy.ops.import_scene.fbx(filepath=fbx_anim)
temp_arm = [o for o in bpy.data.objects if o.type == 'ARMATURE' and o != hero_rig][0]

# Find Walk and Wave actions
walk_action = bpy.data.actions.get("KayKit Animated Character|KayKit Animated Character|Walk")
cheer_action = bpy.data.actions.get("KayKit Animated Character|KayKit Animated Character|Wave")

# Assign walk action to hero rig
if walk_action:
    hero_rig.animation_data_create()
    hero_rig.animation_data.action = walk_action

# Remove temp armature
bpy.data.objects.remove(temp_arm, do_unlink=True)

# 2. Import Companion Fox (Lumi)
gltf_fox = r"E:\YT\assets\animals\Fox.glb"
bpy.ops.import_scene.gltf(filepath=gltf_fox)

fox_rig = [o for o in bpy.data.objects if o.type == 'ARMATURE' and o != hero_rig][0]
fox_rig.name = "Lumi_Fox_Rig"
fox_rig.scale = (0.012, 0.012, 0.012)
fox_rig.location = (0.6, -0.2, 0.0)
fox_rig.rotation_euler = (0, 0, math.radians(15))

fox_walk = bpy.data.actions.get("Walk_root")
if fox_walk:
    fox_rig.animation_data_create()
    fox_rig.animation_data.action = fox_walk

# 3. Build Fantasy Bridge & Environment
def create_pbr_mat(name, base_color, roughness=0.4, metallic=0.0, emission=None, emission_strength=1.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        if emission:
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = emission
                bsdf.inputs['Emission Strength'].default_value = emission_strength
    return mat

mat_stone = create_pbr_mat("BridgeStone", (0.28, 0.30, 0.35, 1.0), roughness=0.7)
mat_gold = create_pbr_mat("GoldRune", (0.85, 0.70, 0.20, 1.0), roughness=0.25, metallic=0.8, emission=(0.95, 0.8, 0.2, 1.0), emission_strength=1.5)
mat_crystal = create_pbr_mat("CrystalCyan", (0.15, 0.85, 1.0, 1.0), roughness=0.15, emission=(0.10, 0.85, 1.0, 1.0), emission_strength=3.5)
mat_shroom_teal = create_pbr_mat("ShroomTeal", (0.08, 0.75, 0.70, 1.0), roughness=0.35, emission=(0.08, 0.75, 0.70, 1.0), emission_strength=2.2)
mat_shroom_purple = create_pbr_mat("ShroomPurple", (0.75, 0.20, 0.88, 1.0), roughness=0.35, emission=(0.75, 0.20, 0.88, 1.0), emission_strength=2.5)

# Bridge deck
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.15))
deck = bpy.context.active_object
deck.scale = (2.2, 18.0, 0.30)
bpy.ops.object.transform_apply(scale=True)
deck.data.materials.append(mat_stone)

# Edge curbs
for sx in [-1.05, 1.05]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sx, 0, 0.08))
    curb = bpy.context.active_object
    curb.scale = (0.18, 18.0, 0.16)
    bpy.ops.object.transform_apply(scale=True)
    curb.data.materials.append(mat_gold)

# Lantern Pillars
for py in [-4.0, -1.5, 1.0, 3.5, 6.0]:
    for px in [-1.15, 1.15]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.08, depth=0.8, location=(px, py, 0.4))
        p = bpy.context.active_object
        p.data.materials.append(mat_stone)
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(px, py, 0.85))
        c = bpy.context.active_object
        c.data.materials.append(mat_crystal)

# Mushrooms
shrooms = [
    (-3.0, -1.0, 0.0, 1.8, mat_shroom_teal),
    (3.2, 0.5, 0.2, 2.2, mat_shroom_purple),
    (-3.4, 2.5, 0.3, 2.5, mat_shroom_purple),
    (3.0, 3.8, 0.1, 1.9, mat_shroom_teal)
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

# 4. Lighting
# Key light
l_key_data = bpy.data.lights.new("KeyLight", type='POINT')
l_key_data.energy = 180
l_key_data.color = (1.0, 0.88, 0.72)
l_key = bpy.data.objects.new("KeyLight", l_key_data)
bpy.context.collection.objects.link(l_key)
l_key.location = (-1.8, -2.5, 2.6)

# Fill light
l_fill_data = bpy.data.lights.new("FillLight", type='POINT')
l_fill_data.energy = 70
l_fill_data.color = (0.4, 0.55, 0.95)
l_fill = bpy.data.objects.new("FillLight", l_fill_data)
bpy.context.collection.objects.link(l_fill)
l_fill.location = (2.2, -1.0, 2.2)

# Rim light
l_rim_data = bpy.data.lights.new("RimLight", type='SPOT')
l_rim_data.energy = 320
l_rim_data.color = (0.2, 0.9, 1.0)
l_rim_data.spot_size = math.radians(70)
l_rim = bpy.data.objects.new("RimLight", l_rim_data)
bpy.context.collection.objects.link(l_rim)
l_rim.location = (0.5, 2.5, 2.2)
l_rim.rotation_euler = (math.radians(-45), 0, math.radians(-160))

# 5. Camera
cam_data = bpy.data.cameras.new("MainCam")
cam_data.lens = 45
cam_obj = bpy.data.objects.new("MainCam", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Camera looking at Leo and Lumi
cam_obj.location = (-0.3, -3.2, 1.35)
cam_obj.rotation_euler = (math.radians(78), 0, math.radians(-6))

# Render frame 10 (mid-walk stride)
scene.frame_set(10)
out_path = r"E:\YT\output\renders\test_kaykit_hero_render.png"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
scene.render.filepath = out_path
bpy.ops.render.render(write_still=True)
print(f"Rendered test frame to {out_path}")
