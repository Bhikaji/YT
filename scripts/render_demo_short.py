import asyncio
import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.config import settings
from backend.app.services.voice_engine.tts_service import VoiceEngine
from backend.app.services.voice_engine.audio_processor import AudioProcessor
from backend.app.services.voice_engine.rhubarb_lipsync import LipSyncEngine
from backend.app.services.blender_engine.render_manager import RenderManager
from backend.app.services.post_production.ffmpeg_compositor import FFmpegCompositor
from backend.app.services.thumbnail_engine.typography_styler import ThumbnailGenerator

async def generate_character_demo():
    print("=================================================================")
    print("   GENERATING FEATURE-ANIMATION CHARACTER DEMO (LEO & LUMI)      ")
    print("=================================================================")

    demo_slug = "demo_leo_and_lumi"
    demo_dir = settings.OUTPUT_DIR / "renders" / demo_slug
    demo_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate Voice Lines with Natural Emotion
    print("\n[STEP 1/4] Synthesizing Leo's Expressive Dialogue...")
    dialogue_text = "Look at this place, Lumi! The giant mushrooms are glowing... and that crystal bridge is leading right to the hidden doorway!"
    
    audio_path = str(settings.ASSETS_DIR / "audio" / "voices" / f"{demo_slug}_dialogue.mp3")
    await VoiceEngine.generate_speech(
        text=dialogue_text,
        voice_id="en-US-ChristopherNeural",
        emotion="excited",
        output_path=audio_path
    )
    print(f"✔ Dialogue generated: {audio_path}")

    # 2. Extract Duration and Visemes
    print("\n[STEP 2/4] Computing 3D Facial Lip-Sync Visemes...")
    meta = AudioProcessor.process_dialogue_audio(
        text=dialogue_text,
        audio_file_path=audio_path
    )
    duration = meta["duration_seconds"]
    fps = 30
    total_frames = int(duration * fps)
    print(f"✔ Visemes computed: {meta['viseme_count']} blendshape cues across {duration:.2f}s ({total_frames} frames).")

    # Read viseme keyframes
    import json
    with open(meta["viseme_json_path"], "r", encoding="utf-8") as f:
        visemes = json.load(f)

    # 3. Render 3D Stylized Feature Animation Frames
    print("\n[STEP 3/4] Rendering 3D Animation Frames (Leo & Lumi in Bioluminescent Forest)...")
    frames = RenderManager.render_procedural_3d_simulation(
        output_frames_dir=str(demo_dir),
        total_frames=total_frames,
        viseme_keyframes=visemes,
        resolution=(1080, 1920),  # 9:16 Vertical Short
        fps=fps
    )
    print(f"✔ Rendered {len(frames)} stylized 3D frames into {demo_dir}")

    # 4. Final Video Assembly via FFmpeg
    print("\n[STEP 4/4] Encoding Final YouTube Short & Compositing Thumbnail...")
    output_video = str(settings.OUTPUT_DIR / "shorts" / "demo_pixar_characters.mp4")
    frames_pattern = os.path.join(str(demo_dir), "frame_%04d.png")

    FFmpegCompositor.assemble_video_with_audio(
        frames_pattern=frames_pattern,
        audio_file_path=audio_path,
        output_video_path=output_video,
        fps=fps
    )
    print(f"✔ Final Demo Video: {output_video} ({os.path.getsize(output_video)/(1024*1024):.2f} MB)")

    # 5. Generate Thumbnail from Hero Keyframe
    hero_frame = os.path.join(str(demo_dir), f"frame_{min(total_frames // 2, 60):04d}.png")
    thumbnail_path = str(settings.ASSETS_DIR / "thumbnails" / "demo_pixar_characters_thumb.jpg")
    
    ThumbnailGenerator.create_thumbnail(
        base_frame_path=hero_frame,
        output_thumbnail_path=thumbnail_path,
        headline_text="LUMI, LOOK AT THIS!",
        emotion_tag="SHOCK",
        format_type="SHORT"
    )
    print(f"✔ Final Demo Thumbnail: {thumbnail_path}")

    print("\n=================================================================")
    print("   CHARACTER DEMO GENERATION COMPLETE!                           ")
    print(f"   Video:     {output_video}")
    print(f"   Thumbnail: {thumbnail_path}")
    print("=================================================================")

if __name__ == "__main__":
    asyncio.run(generate_character_demo())
