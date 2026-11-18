"""
Autonomous AI Cartoon Studio - 10-Second 3D Pixar Cinematic Short Render Script
Executes inside Blender 4.2 LTS headlessly.
"""

import bpy
import math
import os

# 1. Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# 2. Render Settings (EEVEE-Next / AgX Color Management)
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 300  # Exactly 10.0 seconds at 30 fps

# Output path
frames_dir = r"E:\YT\output\renders\short_10s"
os.makedirs(frames_dir, exist_ok=True)
scene.render.filepath = os.path.join(frames_dir, "frame_")
scene.render.image_settings.file_format = 'PNG'

# AgX Color Profile
if 'AgX' in [c.name for c in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items]:
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'Medium High Contrast'

# 3. World Atmosphere (Dark Deep Bioluminescent Blue)
world = bpy.data.worlds.new("CavernAtmosphere")
scene.world = world
world.use_nodes = True
w_nodes = world.node_tree.nodes
w_links = world.node_tree.links
w_nodes.clear()

bg = w_nodes.new('ShaderNodeBackground')
bg.inputs['Color'].default_value = (0.01, 0.015, 0.035, 1.0)
bg.inputs['Strength'].default_value = 0.5
out_w = w_nodes.new('ShaderNodeOutputWorld')
w_links.new(bg.outputs['Background'], out_w.inputs['Surface'])

# 4. Animated Director Camera
cam_data = bpy.data.cameras.new("DirectorCamera")
cam_data.lens = 45.0
cam_data.dof.use_dof = True
cam_data.dof.focus_distance = 4.0
cam_data.dof.aperture_fstop = 2.8

cam_obj = bpy.data.objects.new("DirectorCamera", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Camera Keyframing:
# Scene 1: Frames 1 to 155 (Cavern Push-in with handheld drift)
# Frame 1
cam_obj.location = (0.0, -4.5, 0.0)
cam_obj.rotation_euler = (math.radians(90), 0, 0)
cam_obj.keyframe_insert(data_path="location", frame=1)
cam_obj.keyframe_insert(data_path="rotation_euler", frame=1)

# Frame 155 (Subtle slow cinematic dolly-in)
cam_obj.location = (0.04, -3.75, 0.08)
cam_obj.rotation_euler = (math.radians(91.2), math.radians(-0.6), math.radians(0.4))
cam_obj.keyframe_insert(data_path="location", frame=155)
cam_obj.keyframe_insert(data_path="rotation_euler", frame=155)

# Scene 2: Frames 156 to 300 (Close-Up Hero Shot with subtle float)
# Frame 156 (Cut to Low-angle Close-Up)
cam_obj.location = (-0.02, -2.65, -0.05)
cam_obj.rotation_euler = (math.radians(92.5), math.radians(0.5), math.radians(-0.8))
cam_obj.keyframe_insert(data_path="location", frame=156)
cam_obj.keyframe_insert(data_path="rotation_euler", frame=156)

# Frame 300 (Hero push-in)
cam_obj.location = (0.02, -2.25, 0.05)
cam_obj.rotation_euler = (math.radians(93.8), math.radians(-0.4), math.radians(0.6))
cam_obj.keyframe_insert(data_path="location", frame=300)
cam_obj.keyframe_insert(data_path="rotation_euler", frame=300)

# Helper function to create image textured plane
def create_textured_plane(name, image_path, width, height, location, emission_boost=0.2):
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=location)
    plane = bpy.context.active_object
    plane.name = name
    plane.scale = (width, height, 1.0)
    plane.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True, scale=True)

    mat = bpy.data.materials.new(name=name + "_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    img_node = nodes.new('ShaderNodeTexImage')
    if os.path.exists(image_path):
        img_node.image = bpy.data.images.load(image_path)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Roughness'].default_value = 0.4
    if 'Emission Color' in bsdf.inputs:
        links.new(img_node.outputs['Color'], bsdf.inputs['Emission Color'])
        bsdf.inputs['Emission Strength'].default_value = emission_boost
    elif 'Emission' in bsdf.inputs:
        links.new(img_node.outputs['Color'], bsdf.inputs['Emission'])

    out = nodes.new('ShaderNodeOutputMaterial')
    links.new(img_node.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    plane.data.materials.append(mat)
    return plane

# 5. Scene 1 Setup (Leo & Lumi on Crystal Bridge)
img_scene_1 = r"E:\YT\assets\characters\demo_leo_and_lumi_pixar.jpg"

# Background ambient fill (enlarged & slightly blurred behind)
bg_plane_1 = create_textured_plane("Scene1_BG", img_scene_1, width=3.8, height=6.7, location=(0, 0.4, 0), emission_boost=0.1)
# Main crisp hero plane
hero_plane_1 = create_textured_plane("Scene1_Hero", img_scene_1, width=2.9, height=1.62, location=(0, 0.0, 0), emission_boost=0.25)

# Visibility animation: Active frames 1-155, hidden frames 156-300
for plane in [bg_plane_1, hero_plane_1]:
    plane.hide_render = False
    plane.keyframe_insert(data_path="hide_render", frame=1)
    plane.keyframe_insert(data_path="hide_render", frame=155)
    plane.hide_render = True
    plane.keyframe_insert(data_path="hide_render", frame=156)

# 6. Scene 2 Setup (Leo Close-Up Hero Portrait)
img_scene_2 = r"E:\YT\assets\characters\char_leo_portrait.jpg"

# Background fill plane
bg_plane_2 = create_textured_plane("Scene2_BG", img_scene_2, width=3.5, height=6.2, location=(0, 0.3, 0), emission_boost=0.1)
# Hero portrait plane
hero_plane_2 = create_textured_plane("Scene2_Hero", img_scene_2, width=2.2, height=2.2, location=(0, -0.05, -0.15), emission_boost=0.3)

# Visibility animation: Hidden frames 1-155, Active frames 156-300
for plane in [bg_plane_2, hero_plane_2]:
    plane.hide_render = True
    plane.keyframe_insert(data_path="hide_render", frame=1)
    plane.keyframe_insert(data_path="hide_render", frame=155)
    plane.hide_render = False
    plane.keyframe_insert(data_path="hide_render", frame=156)
    plane.keyframe_insert(data_path="hide_render", frame=300)

# Subtle breathing oscillation on hero_plane_2 (Z scale & location)
for f in range(156, 301, 15):
    cycle = (f - 156) / 30.0 * math.pi
    scale_factor = 1.0 + 0.012 * math.sin(cycle)
    z_offset = -0.15 + 0.008 * math.sin(cycle)
    hero_plane_2.scale = (2.2 * scale_factor, 2.2 * scale_factor, 1.0)
    hero_plane_2.location = (0, -0.05, z_offset)
    hero_plane_2.keyframe_insert(data_path="scale", frame=f)
    hero_plane_2.keyframe_insert(data_path="location", frame=f)

# 7. 3D Bioluminescent Spores & Ember Particles
# Create glowing particle spheres floating through 3D space
for i in range(24):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.022, location=(
        (i % 5 - 2) * 0.45 + (i * 0.07 % 0.3),
        -1.0 - (i % 6) * 0.45,
        ((i * 7) % 19 - 9) * 0.15
    ))
    spore = bpy.context.active_object
    spore.name = f"BioluminescentSpore_{i}"
    
    # Glowing shader
    spore_mat = bpy.data.materials.new(name=f"SporeMat_{i}")
    spore_mat.use_nodes = True
    n = spore_mat.node_tree.nodes
    bsdf = n.get("Principled BSDF")
    if bsdf:
        # Alternating cyan and pink bioluminescent embers
        is_cyan = (i % 2 == 0)
        c = (0.2, 0.85, 1.0, 1.0) if is_cyan else (0.95, 0.35, 0.8, 1.0)
        if 'Emission Color' in bsdf.inputs:
            bsdf.inputs['Emission Color'].default_value = c
            bsdf.inputs['Emission Strength'].default_value = 8.0
        elif 'Emission' in bsdf.inputs:
            bsdf.inputs['Emission'].default_value = c
    spore.data.materials.append(spore_mat)
    
    # Animate gentle upward & drifting motion
    for f in [1, 75, 150, 225, 300]:
        t = f / 30.0
        drift_x = math.sin(t + i * 0.8) * 0.12
        drift_z = (t * 0.2 + (i * 0.1)) % 2.5 - 1.2
        spore.location.x += drift_x * 0.1
        spore.location.z = drift_z
        spore.keyframe_insert(data_path="location", frame=f)

# 8. Dynamic Cinematic Lighting
# Key Crystal Light (Cyan, pulsing)
crystal_light_data = bpy.data.lights.new(name="CrystalLight", type='POINT')
crystal_light_data.color = (0.25, 0.8, 1.0)
crystal_light_obj = bpy.data.objects.new(name="CrystalLight", object_data=crystal_light_data)
crystal_light_obj.location = (0.0, -1.8, -0.6)
bpy.context.collection.objects.link(crystal_light_obj)

# Keyframe pulsing crystal light
for f in range(1, 301, 20):
    pulse = math.sin(f / 15.0) * 0.35 + 1.0
    crystal_light_data.energy = 600 * pulse
    crystal_light_data.keyframe_insert(data_path="energy", frame=f)

# Hero Rim Light (Warm Golden Orange)
rim_light_data = bpy.data.lights.new(name="WarmRimLight", type='POINT')
rim_light_data.color = (1.0, 0.65, 0.35)
rim_light_obj = bpy.data.objects.new(name="WarmRimLight", object_data=rim_light_data)
rim_light_obj.location = (1.2, -1.5, 0.8)
bpy.context.collection.objects.link(rim_light_obj)

for f in range(1, 301, 15):
    flicker = 1.0 + 0.15 * math.sin(f * 0.8)
    rim_light_data.energy = 550 * flicker
    rim_light_data.keyframe_insert(data_path="energy", frame=f)

print("[Blender Engine] Setup complete. 300 frames configured for 10-second Short.")
