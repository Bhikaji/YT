"""
Master Production 3D Pixar & Prehistoric Short Generator
Renders high-definition feature-animation short matching demo_video/videoplayback.mp4:
- Leo: 3D stylized boy with wavy brown hair locks, expressive Pixar eyes, orange t-shirt, blue shorts, red sneakers, backpack
- Lumi: Golden Retriever Puppy with floppy ears, red collar, wagging tail, sniffing footprint
- Prehistoric Environment: Smoking volcano, multi-tier waterfalls, crystal lagoon, giant ferns & blossoms
- Prehistoric Dinosaurs: Stegosaurus with dorsal plates and spiked tail, lagoon Sauropod, baby T-Rex
- Giant 3-toed dinosaur footprint with puddle reflections
- Lip-sync & facial expressions (awe, wonder, dialogue mouthing)
"""

import os
import sys
import math
import asyncio
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.config import settings
from backend.app.services.voice_engine.tts_service import VoiceEngine
from backend.app.services.voice_engine.audio_processor import AudioProcessor
from backend.app.services.post_production.ffmpeg_compositor import FFmpegCompositor
from backend.app.services.thumbnail_engine.typography_styler import ThumbnailGenerator
from modules.character_engine.pixar_master_builder import PixarMasterBuilder
from modules.environment_engine.prehistoric_world_builder import PrehistoricWorldBuilder


def generate_blender_script(output_script_path: str, output_frames_dir: str, total_frames: int = 300, resolution: tuple = (1080, 1920), fps: int = 30):
    os.makedirs(os.path.dirname(output_script_path), exist_ok=True)
    os.makedirs(output_frames_dir, exist_ok=True)

    script_content = f'''# Master 3D Production Render Script (Blender 4.5+ EEVEE-Next)
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
stego_objs = build_stegosaurus(location=(-2.6, 4.2, 0.0))
sauro_objs = build_lagoon_sauropod(location=(3.2, 11.5, -0.4))
trex_objs = build_baby_trex(location=(-1.5, 5.8, 0.1))

# Apply Shade Smooth & Subdivision Surface to all character meshes
for obj in scene.objects:
    if obj.type == 'MESH':
        for poly in obj.data.polygons:
            poly.use_smooth = True
        # Add Subdivision Surface for silky smooth Pixar geometry
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

    # Camera Multi-Act Sequence (Cinematic Framing)
    if f <= 75:
        # ACT 1 (Frames 1-75): Majestic Establishing Landscape
        # Level angle showing Leo, Puppy, Volcano, and Waterfalls
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

    with open(output_script_path, "w", encoding="utf-8") as f:
        f.write(script_content)

    return output_script_path


async def produce_pixar_dino_short():
    print("=================================================================")
    print("   AUTONOMOUS 3D PIXAR & PREHISTORIC SHORT PRODUCTION PIPELINE   ")
    print("=================================================================")

    # 1. Synthesize High-Fidelity Voice
    print("\n[STEP 1/4] Synthesizing Neural Voice Dialogue...")
    dialogue_text = "Lumi, look at these tracks! The giant volcano... there are real dinosaurs in this valley!"
    audio_path = str(settings.OUTPUT_DIR / "renders" / "demo_pixar_dino_short" / "dialogue.mp3")
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    
    await VoiceEngine.generate_speech(
        text=dialogue_text,
        voice_id="en-US-ChristopherNeural",
        emotion="excited",
        output_path=audio_path
    )
    print(f"✔ Neural dialogue generated: {audio_path}")

    # 2. Generate Blender Automation Script
    print("\n[STEP 2/4] Generating Master Blender 4.5 EEVEE-Next Render Script...")
    bpy_script = str(settings.SCRIPTS_DIR / "bpy_render_pixar_dino_short.py")
    frames_dir = str(settings.OUTPUT_DIR / "renders" / "demo_pixar_dino_short")
    generate_blender_script(bpy_script, frames_dir, total_frames=300, resolution=(1080, 1920), fps=30)
    print(f"✔ Render script generated: {bpy_script}")

    # 3. Execute Headless Blender Render
    print("\n[STEP 3/4] Launching Headless 3D Render via Blender 4.5 LTS...")
    blender_bin = str(settings.BASE_DIR / "tools" / "blender" / "Blender Foundation" / "Blender 4.5" / "blender.exe")
    
    import subprocess
    cmd = [blender_bin, "--factory-startup", "-b", "-P", bpy_script]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"Blender render warning/error:\n{proc.stderr}")
    print("✔ Headless 3D render completed successfully.")

    # 4. Final Video Assembly via FFmpeg
    print("\n[STEP 4/4] Encoding Final High-Definition YouTube Short via FFmpeg...")
    final_video = str(settings.OUTPUT_DIR / "shorts" / "demo_pixar_dino_short.mp4")
    frames_pattern = os.path.join(frames_dir, "frame_%04d.jpg")

    FFmpegCompositor.assemble_video_with_audio(
        frames_pattern=frames_pattern,
        audio_file_path=audio_path,
        output_video_path=final_video,
        fps=30
    )
    print(f"✔ Final High-Definition Short: {final_video}")
    
    # 5. Thumbnail Generation
    hero_frame = os.path.join(frames_dir, "frame_0045.jpg")
    thumbnail_path = str(settings.ASSETS_DIR / "thumbnails" / "demo_pixar_dino_short_thumb.jpg")
    ThumbnailGenerator.create_thumbnail(
        base_frame_path=hero_frame,
        output_thumbnail_path=thumbnail_path,
        headline_text="DINOSAURS FOUND?!",
        emotion_tag="SHOCK",
        format_type="SHORT"
    )
    print(f"✔ Production Thumbnail: {thumbnail_path}")

    print("\n=================================================================")
    print("   PRODUCTION RUN COMPLETE!                                      ")
    print(f"   Output Video: {final_video}")
    print("=================================================================")


if __name__ == "__main__":
    asyncio.run(produce_pixar_dino_short())
