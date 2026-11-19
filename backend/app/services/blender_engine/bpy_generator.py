import json
import os
from pathlib import Path
from typing import Dict, Any, List
from backend.app.schemas.script import GeneratedEpisodeScript, ScriptScene
from modules.character_engine.pixar_master_builder import PixarMasterBuilder
from modules.environment_engine.prehistoric_world_builder import PrehistoricWorldBuilder

class BpyScriptGenerator:
    """Generates standalone Python scripts executed headlessly by Blender (bpy)."""

    @classmethod
    def generate_blender_render_script(
        cls,
        script: GeneratedEpisodeScript,
        output_script_path: str,
        output_frames_dir: str,
        viseme_data_map: Dict[str, str],
        resolution: tuple = (1080, 1920),
        fps: int = 30,
        total_frames: int = 300
    ) -> str:
        """
        Creates a self-contained Python script to drive Blender headless rendering
        with master Pixar stylized 3D characters (Leo & Lumi Puppy), prehistoric dinosaurs,
        lush lost world environment, speech viseme shapekeys, and multi-act cinematography.
        """
        script_content = f'''# Auto-generated Master 3D Production Render Script by Autonomous AI Cartoon Studio
import bpy
import math
import os

# 1. Clear Scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# 2. Render Settings (EEVEE-Next, High Definition {resolution[0]}x{resolution[1]} @ {fps}fps)
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
scene.render.resolution_x = {resolution[0]}
scene.render.resolution_y = {resolution[1]}
scene.render.resolution_percentage = 100
scene.render.fps = {fps}
scene.frame_start = 1
scene.frame_end = {total_frames}

if hasattr(scene, "eevee"):
    scene.eevee.taa_render_samples = 4

# AgX Color Management
if 'AgX' in [c.name for c in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items]:
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'Medium High Contrast'
else:
    scene.view_settings.view_transform = 'Filmic'

os.makedirs(r"{output_frames_dir}", exist_ok=True)
scene.render.filepath = os.path.join(r"{output_frames_dir}", "frame_")
scene.render.image_settings.file_format = 'JPEG'
scene.render.image_settings.quality = 95

# 3. Materials Palette
{PixarMasterBuilder.get_shader_definitions_code()}

# 4. Environment & Prehistoric World
{PrehistoricWorldBuilder.get_environment_code()}
build_prehistoric_world()

# 5. Characters & Creatures
{PixarMasterBuilder.get_leo_builder_code(location=(-0.35, 0.0, 0.0))}
head_leo, mouth_leo, leo_objs = build_pixar_leo()

{PixarMasterBuilder.get_lumi_puppy_code(location=(0.42, -0.25, 0.0))}
phead, ptail, puppy_objs = build_puppy_lumi()

{PixarMasterBuilder.get_prehistoric_creatures_code()}
stego_objs = build_stegosaurus(location=(-2.4, 3.8, 0.0))
sauro_objs = build_lagoon_sauropod(location=(2.8, 10.5, -0.4))
trex_objs = build_baby_trex(location=(-1.5, 5.2, 0.1))

# Apply Shade Smooth & Subdivision Surface to all character meshes
for obj in scene.objects:
    if obj.type == 'MESH':
        for poly in obj.data.polygons:
            poly.use_smooth = True
        if any(tag in obj.name for tag in ["Leo_Head", "Leo_Nose", "Leo_Mouth", "Leo_Torso", "Puppy_Head", "Puppy_Body", "Puppy_Ear", "HairCluster"]):
            sub = obj.modifiers.new(name="Subsurf", type='SUBSURF')
            sub.levels = 1
            sub.render_levels = 2

# 6. Camera Director & Multi-Act Cinematography
cam_data = bpy.data.cameras.new("DirectorCamera")
cam_data.lens = 38
cam_data.dof.use_dof = True
cam_data.dof.aperture_fstop = 3.2

cam_obj = bpy.data.objects.new("DirectorCamera", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

# 7. Animation Keyframing (4 Acts matching Demo Video)
for f in range(1, {total_frames} + 1):
    # Leo Lip-Sync & Emotion Blendshapes
    if head_leo and head_leo.data.shape_keys:
        kb = head_leo.data.shape_keys.key_blocks
        if "jawOpen" in kb:
            if (65 <= f <= 135) or (165 <= f <= 275):
                jaw_val = abs(math.sin(f * 0.48)) * 0.70 + 0.12
                smile_val = 0.60 + 0.20 * math.sin(f * 0.22)
            else:
                jaw_val = 0.04
                smile_val = 0.45
                
            kb["jawOpen"].value = jaw_val
            kb["jawOpen"].keyframe_insert(data_path="value", frame=f)
            kb["mouthSmile"].value = smile_val
            kb["mouthSmile"].keyframe_insert(data_path="value", frame=f)
            if "wonderEmotion" in kb:
                kb["wonderEmotion"].value = 0.75
                kb["wonderEmotion"].keyframe_insert(data_path="value", frame=f)

    # Puppy Tail Wagging Animation
    if ptail:
        wag = math.sin(f * 0.75) * math.radians(30)
        ptail.rotation_euler = (math.radians(-45), 0, wag)
        ptail.keyframe_insert(data_path="rotation_euler", frame=f)

    # Puppy Sniffing & Looking Up
    if phead:
        if f <= 140:
            sniff = math.radians(16 + math.sin(f * 0.35) * 6)
            phead.rotation_euler = (sniff, 0, math.radians(-12))
        else:
            look_up = math.radians(-16 + math.sin(f * 0.18) * 5)
            phead.rotation_euler = (look_up, 0, math.radians(14))
        phead.keyframe_insert(data_path="rotation_euler", frame=f)

    # Camera Multi-Act Sequence
    if f <= 75:
        # ACT 1 (Frames 1-75): Level Establishing View
        t1 = f / 75.0
        cam_obj.location = (0.05 + t1 * 0.1, -3.2 + t1 * 0.3, 1.25 + t1 * 0.05)
        cam_obj.rotation_euler = (math.radians(88), 0, math.radians(2))
        cam_data.lens = 35
        cam_data.dof.focus_distance = 3.0
    elif f <= 150:
        # ACT 2 (Frames 76-150): Medium Tracking Shot - Footprint Discovery
        t2 = (f - 75) / 75.0
        cam_obj.location = (0.15 + t2 * 0.1, -2.4 - t2 * 0.15, 0.95 - t2 * 0.1)
        cam_obj.rotation_euler = (math.radians(82 + t2 * 2), 0, math.radians(4))
        cam_data.lens = 42
        cam_data.dof.focus_distance = 2.0
    elif f <= 225:
        # ACT 3 (Frames 151-225): Macro Low-Angle Shot on Footprint
        t3 = (f - 150) / 75.0
        cam_obj.location = (0.28 - t3 * 0.12, -1.8 - t3 * 0.15, 0.65 + t3 * 0.15)
        cam_obj.rotation_euler = (math.radians(82), 0, math.radians(-3 + t3 * 4))
        cam_data.lens = 48
        cam_data.dof.focus_distance = 1.6
    else:
        # ACT 4 (Frames 226-300): Hero Close-Up & Grand Dinosaur Reveal
        t4 = (f - 225) / 75.0
        cam_obj.location = (-0.25 + t4 * 0.20, -1.85 - t4 * 0.35, 1.48 + t4 * 0.10)
        cam_obj.rotation_euler = (math.radians(88 - t4 * 3), 0, math.radians(-4 + t4 * 8))
        cam_data.lens = 50
        cam_data.dof.focus_distance = 1.85

    cam_obj.keyframe_insert(data_path="location", frame=f)
    cam_obj.keyframe_insert(data_path="rotation_euler", frame=f)
    cam_data.keyframe_insert(data_path="lens", frame=f)
    cam_data.dof.keyframe_insert(data_path="focus_distance", frame=f)

print("[MasterRenderer] Scene setup complete. Beginning high-definition animation render...")
bpy.ops.render.render(animation=True)
print("[MasterRenderer] 3D Animation render finished successfully.")
'''
        os.makedirs(os.path.dirname(output_script_path), exist_ok=True)
        with open(output_script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        return output_script_path
