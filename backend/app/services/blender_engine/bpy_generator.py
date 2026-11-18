import json
import os
from pathlib import Path
from typing import Dict, Any, List
from backend.app.schemas.script import GeneratedEpisodeScript, ScriptScene

class BpyScriptGenerator:
    """Generates standalone Python scripts executed headlessly by Blender (bpy)."""

    @classmethod
    def generate_blender_render_script(
        cls,
        script: GeneratedEpisodeScript,
        output_script_path: str,
        output_frames_dir: str,
        viseme_data_map: Dict[str, str],  # dialogue line index -> viseme JSON path
        resolution: tuple = (1080, 1920),
        fps: int = 30
    ) -> str:
        """
        Creates a self-contained Python script to drive Blender headless rendering.
        """
        script_content = f'''# Auto-generated Blender Automation Script by Autonomous AI Cartoon Studio
import bpy
import json
import os
import math

# 1. Clear existing scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# 2. Render Settings
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
scene.render.resolution_x = {resolution[0]}
scene.render.resolution_y = {resolution[1]}
scene.render.resolution_percentage = 100
scene.render.fps = {fps}
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = os.path.join(r"{output_frames_dir}", "frame_")

# Set World Background & Color
world = bpy.data.worlds.new("StudioWorld")
bpy.context.scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs[0].default_value = (0.05, 0.05, 0.08, 1.0)
    bg_node.inputs[1].default_value = 0.5

# 3. Create Camera
cam_data = bpy.data.cameras.new("DirectorCamera")
cam_data.lens = 35.0
cam_data.dof.use_dof = True
cam_obj = bpy.data.objects.new("DirectorCamera", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Position Camera
cam_obj.location = (0.0, -4.5, 1.6)
cam_obj.rotation_euler = (math.radians(78), 0, 0)

# 4. Create 3-Point Lighting
# Key Light
key_data = bpy.data.lights.new(name="KeyLight", type='POINT')
key_data.energy = 1000
key_data.color = (1.0, 0.9, 0.75)
key_obj = bpy.data.objects.new(name="KeyLight", object_data=key_data)
key_obj.location = (2.5, -2.5, 3.5)
bpy.context.collection.objects.link(key_obj)

# Fill Light
fill_data = bpy.data.lights.new(name="FillLight", type='POINT')
fill_data.energy = 400
fill_data.color = (0.5, 0.7, 1.0)
fill_obj = bpy.data.objects.new(name="FillLight", object_data=fill_data)
fill_obj.location = (-2.5, -2.0, 2.0)
bpy.context.collection.objects.link(fill_obj)

# Rim Light
rim_data = bpy.data.lights.new(name="RimLight", type='POINT')
rim_data.energy = 1200
rim_data.color = (1.0, 1.0, 1.0)
rim_obj = bpy.data.objects.new(name="RimLight", object_data=rim_data)
rim_obj.location = (0.0, 3.0, 3.0)
bpy.context.collection.objects.link(rim_obj)

# 5. Create Stylized Character Model Placeholder (with ShapeKeys for LipSync)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.45, location=(0, 0, 1.4))
head = bpy.context.active_object
head.name = "Character_Head"

# Add ShapeKeys (Basis, jawOpen, mouthSmile, mouthPucker)
head.shape_key_add(name="Basis")
sk_jaw = head.shape_key_add(name="jawOpen")
sk_smile = head.shape_key_add(name="mouthSmile")
sk_pucker = head.shape_key_add(name="mouthPucker")

# Stylized Cartoon Material
mat = bpy.data.materials.new(name="StylizedToonMat")
mat.use_nodes = True
nodes = mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.95, 0.76, 0.65, 1.0)  # stylized warm skin
    bsdf.inputs['Roughness'].default_value = 0.35
head.data.materials.append(mat)

# 6. Apply Viseme Lip-Sync Keyframes
visemes_map = {json.dumps(viseme_data_map)}
total_frames = 150  # default 5 seconds

for d_key, v_path in visemes_map.items():
    if os.path.exists(v_path):
        with open(v_path, 'r', encoding='utf-8') as f:
            v_keyframes = json.load(f)
            for kf in v_keyframes:
                frame_num = int(kf["start"] * {fps}) + 1
                blendshapes = kf.get("blendshapes", {{}})
                
                # Keyframe jawOpen
                jaw_val = blendshapes.get("jawOpen", 0.0)
                sk_jaw.value = jaw_val
                sk_jaw.keyframe_insert(data_path="value", frame=frame_num)
                
                # Keyframe mouthPucker
                pucker_val = blendshapes.get("mouthPucker", 0.0)
                sk_pucker.value = pucker_val
                sk_pucker.keyframe_insert(data_path="value", frame=frame_num)

# Set timeline range and Render
scene.frame_start = 1
scene.frame_end = total_frames

print("[Blender Engine] Setup completed. Starting headless render...")
bpy.ops.render.render(animation=True)
print("[Blender Engine] Render finished successfully.")
'''
        with open(output_script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)

        return output_script_path
