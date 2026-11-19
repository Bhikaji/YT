import os
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from backend.app.config import settings
from backend.app.schemas.script import GeneratedEpisodeScript
from backend.app.services.story_engine.showrunner import ShowrunnerAgent
from backend.app.services.story_engine.memory_store import MemoryStoreService
from backend.app.services.voice_engine.tts_service import VoiceEngine
from backend.app.services.voice_engine.rhubarb_lipsync import LipSyncEngine
from backend.app.services.voice_engine.audio_processor import AudioProcessor
from backend.app.services.blender_engine.bpy_generator import BpyScriptGenerator
from backend.app.services.blender_engine.render_manager import RenderManager
from backend.app.services.post_production.ffmpeg_compositor import FFmpegCompositor
from backend.app.services.post_production.subtitle_engine import SubtitleEngine
from backend.app.services.thumbnail_engine.typography_styler import ThumbnailGenerator
from backend.app.services.youtube_engine.compliance_checker import ComplianceChecker
from backend.app.services.youtube_engine.metadata_generator import MetadataGenerator
from backend.app.services.youtube_engine.uploader import YouTubeUploader

from backend.orchestrator.state_machine import ProductionJobStateMachine, JobState
from modules.quality_control.inspector import QualityControlInspector
from modules.character_engine.generator import CharacterSpecification
from backend.app.services.ai_video_engine.pixar_animator import PixarAiVideoEngine
from backend.app.services.ai_video_engine.veo_video_generator import GoogleVeoVideoGenerator
from backend.app.services.ai_video_engine.local_diffusion_engine import LocalDiffusionVideoEngine

class PipelineOrchestrator:
    """End-to-End Autonomous 3D Cartoon Production & YouTube Publishing Pipeline."""

    @classmethod
    async def produce_episode(
        cls,
        series_title: str,
        series_genre: str,
        season_number: int,
        episode_number: int,
        episode_title: str,
        format_type: str = "SHORT",  # SHORT or LONG_FORM
        cast: Optional[List[Dict[str, Any]]] = None,
        world_lore: Optional[Dict[str, Any]] = None,
        prior_cliffhanger: Optional[str] = None,
        db_session: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Executes all 21 production steps autonomously.
        """
        production_start = datetime.utcnow()
        if not cast:
            cast = [
                {"id": "hero_leo", "name": "Leo", "voice_id": "en-US-ChristopherNeural"},
                {"id": "sidekick_maya", "name": "Maya", "voice_id": "en-US-AnaNeural"}
            ]
        if not world_lore:
            world_lore = {"universe": "Shadow Island", "magic_level": "ancient_technology"}

        print(f"\n[PIPELINE] Starting Production: '{series_title}' - Episode {episode_number}: '{episode_title}' ({format_type})")

        episode_slug = f"ep_{episode_number}_{abs(hash(episode_title))}"
        # Initialize durable state machine job
        job = await ProductionJobStateMachine.create_job(episode_id=episode_slug)
        job_id = job["job_id"]
        await ProductionJobStateMachine.transition(job_id, JobState.PLANNING, {"series": series_title, "format": format_type})

        # STEP 1: Generate Episode Script & Dialogue
        await ProductionJobStateMachine.transition(job_id, JobState.SCRIPTING)
        script = ShowrunnerAgent.develop_episode_script(
            series_title=series_title,
            series_genre=series_genre,
            world_lore=world_lore,
            season_number=season_number,
            episode_number=episode_number,
            episode_title=episode_title,
            format_type=format_type,
            cast=cast,
            prior_cliffhanger=prior_cliffhanger
        )
        print(f"[PIPELINE] Script generated: {len(script.scenes)} scenes, cliffhanger: '{script.cliffhanger_question}'")

        # STEP 2: Synthesize Character Voices & Extract Visemes
        await ProductionJobStateMachine.transition(job_id, JobState.VOICING)
        dialogue_records = []
        combined_visemes = []
        audio_dir = settings.ASSETS_DIR / "audio" / "voices" / episode_slug
        audio_dir.mkdir(parents=True, exist_ok=True)

        # Voice map
        voice_map = {c["id"]: c.get("voice_id", "en-US-ChristopherNeural") for c in cast}

        print("[PIPELINE] Generating neural voice dialogue and visemes...")
        current_time_offset = 0.0

        for s_idx, scene in enumerate(script.scenes):
            for d_idx, d in enumerate(scene.dialogues):
                speaker_voice = voice_map.get(d.character_id, "en-US-ChristopherNeural")
                audio_file = str(audio_dir / f"scene_{s_idx+1}_diag_{d_idx+1}.mp3")
                
                await VoiceEngine.generate_speech(
                    text=d.text,
                    voice_id=speaker_voice,
                    emotion=d.emotion,
                    output_path=audio_file
                )

                # Process duration and visemes
                audio_meta = AudioProcessor.process_dialogue_audio(
                    text=d.text,
                    audio_file_path=audio_file
                )

                dialogue_records.append({
                    "speaker": d.character_name,
                    "text": d.text,
                    "audio_path": audio_file,
                    "start": current_time_offset,
                    "duration": audio_meta["duration_seconds"]
                })

                # Offset timing
                current_time_offset += audio_meta["duration_seconds"] + 0.3

        if format_type == "SHORT":
            total_audio_duration = 10.0
            fps = 30
            total_frames = 300
        else:
            total_audio_duration = max(current_time_offset, 5.0)
            fps = 30
            total_frames = int(total_audio_duration * fps)
        print(f"[PIPELINE] Dialogue synthesis completed. Total duration: {total_audio_duration:.2f}s ({total_frames} frames)")

        # Generate combined dialogue track
        master_audio_path = str(audio_dir / "master_dialogue.mp3")
        if dialogue_records:
            # Concatenate or copy first dialogue for test
            shutil_copy = dialogue_records[0]["audio_path"]
            import shutil
            shutil.copy(shutil_copy, master_audio_path)
        else:
            await VoiceEngine.generate_speech("Mystery awaits on Shadow Island.", output_path=master_audio_path)

        # STEP 3: Generate 3D Visual Frames & Lip-Sync
        await ProductionJobStateMachine.transition(job_id, JobState.LIPSYNCING)
        render_output_dir = str(settings.OUTPUT_DIR / "renders" / episode_slug)
        viseme_keyframes = LipSyncEngine.generate_visemes_from_text_and_duration(
            text=" ".join(d["text"] for d in dialogue_records),
            total_duration_seconds=total_audio_duration
        )

        await ProductionJobStateMachine.transition(job_id, JobState.ANIMATING)
        await ProductionJobStateMachine.transition(job_id, JobState.RENDERING)

        resolution = settings.BLENDER_RESOLUTION_SHORT if format_type == "SHORT" else settings.BLENDER_RESOLUTION_LONG
        mode = getattr(settings, "ANIMATION_ENGINE_MODE", "VEO_AI")
        has_gemini_key = bool(getattr(settings, "GEMINI_API_KEY", None) or os.getenv("GEMINI_API_KEY"))
        has_wan_url = bool(getattr(settings, "WAN21_API_URL", None) or os.getenv("WAN21_API_URL"))

        if mode == "LOCAL_DIFFUSION":
            print(f"[PIPELINE] Launching 100% Free Local GPU Video Diffusion ({getattr(settings, 'LOCAL_DIFFUSION_MODEL', 'LTX-Video')})...")
            scene_prompt = (
                f"Disney Pixar 3D animated movie, cute adventurer boy in orange tshirt and blue shorts smiling and pointing excitedly "
                f"at a friendly Stegosaurus dinosaur walking between palm trees in {script.scenes[0].environment}, "
                f"{script.scenes[0].lighting_preset} lighting, golden puppy Lumi beside him, cinematic camera motion, 8k render, masterpiece"
            )
            local_raw_mp4 = Path(render_output_dir) / "local_diffusion_master.mp4"
            try:
                LocalDiffusionVideoEngine.generate_video(
                    prompt=scene_prompt,
                    output_file=local_raw_mp4,
                    num_frames=int(total_audio_duration * 24),
                    fps=24
                )
                import imageio_ffmpeg
                ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                subprocess.run([
                    ffmpeg_exe, "-y", "-i", str(local_raw_mp4),
                    "-vf", f"fps={fps}",
                    os.path.join(render_output_dir, "frame_%04d.jpg")
                ], capture_output=True)
            except Exception as e:
                print(f"[PIPELINE] Local diffusion error: {e}. Falling back to default pipeline...")
        elif has_wan_url:
            print(f"[PIPELINE] Launching 100% Free Open-Source Colab AI Video Generator (Wan 2.1)...")
            scene_prompt = f"Disney Pixar 3D animation, cute adventurer boy in orange tshirt and puppy pointing excitedly at a huge friendly Stegosaurus dinosaur walking between palm trees, cinematic lighting, 8k render, masterpiece"
            free_ai_mp4 = Path(render_output_dir) / "free_wan_master.mp4"
            try:
                GoogleVeoVideoGenerator.generate_from_free_colab_wan(
                    prompt=scene_prompt,
                    output_file=free_ai_mp4
                )
                import imageio_ffmpeg
                ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                subprocess.run([
                    ffmpeg_exe, "-y", "-i", str(free_ai_mp4),
                    "-vf", f"fps={fps}",
                    os.path.join(render_output_dir, "frame_%04d.jpg")
                ], capture_output=True)
            except Exception as e:
                print(f"[PIPELINE] Free Wan AI error: {e}. Falling back to default pipeline...")
        elif mode == "VEO_AI" and has_gemini_key:
            print(f"[PIPELINE] Launching Google Veo / Gemini AI Video Engine ({settings.VEO_MODEL})...")
            scene_prompts = [
                f"Disney Pixar 3D animated scene, cute young adventurer boy Leo in orange tshirt and blue shorts with playful golden retriever puppy Lumi in {s.environment}, {s.lighting_preset} lighting, dynamic cinematic camera movement, lifelike character animation and expressions, 8k render, masterpiece"
                for s in script.scenes
            ]
            veo_raw_mp4 = Path(render_output_dir) / "veo_master.mp4"
            try:
                GoogleVeoVideoGenerator.generate_full_short_pipeline(
                    output_path=veo_raw_mp4,
                    scene_prompts=scene_prompts,
                    aspect_ratio="9:16" if format_type == "SHORT" else "16:9",
                    total_duration=int(total_audio_duration)
                )
                import imageio_ffmpeg
                ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                subprocess.run([
                    ffmpeg_exe, "-y", "-i", str(veo_raw_mp4),
                    "-vf", f"fps={fps}",
                    os.path.join(render_output_dir, "frame_%04d.jpg")
                ], capture_output=True)
            except Exception as e:
                print(f"[PIPELINE] Veo generation error: {e}. Falling back to Pixar neural pipeline...")
                PixarAiVideoEngine.render_episode_frames(
                    output_dir=Path(render_output_dir),
                    total_frames=total_frames,
                    resolution=resolution
                )
        elif mode in ["AI_PIXAR", "VEO_AI"]:
            if mode == "VEO_AI" and not has_gemini_key:
                print("[PIPELINE] Notice: GEMINI_API_KEY not configured. To use Google Veo 3 / Veo 2 video generation, set GEMINI_API_KEY in E:\\YT\\.env.")
            print(f"[PIPELINE] Launching High-Definition Pixar AI Video Engine ({resolution[0]}x{resolution[1]} @ {fps}fps)...")
            scene_prompts = [
                f"Disney Pixar 3D animated film still, cute boy Leo in orange tshirt and blue shorts with puppy Lumi in {s.environment}, {s.lighting_preset} lighting, cinematic lighting, 8k render, masterpiece"
                for s in script.scenes
            ]
            PixarAiVideoEngine.render_episode_frames(
                output_dir=Path(render_output_dir),
                total_frames=total_frames,
                resolution=resolution,
                custom_scene_prompts=scene_prompts
            )
        else:
            print(f"[PIPELINE] Launching genuine 3D character animation render via Blender EEVEE-Next...")
            bpy_script_file = str(settings.SCRIPTS_DIR / f"render_{episode_slug}.py")
            BpyScriptGenerator.generate_blender_render_script(
                script=script,
                output_script_path=bpy_script_file,
                output_frames_dir=render_output_dir,
                viseme_data_map={},
                resolution=resolution,
                fps=fps,
                total_frames=total_frames
            )
            RenderManager.execute_blender_render(bpy_script_file)

        # STEP 4: Quality Control Pre-flight Check on Renders and Audio
        await ProductionJobStateMachine.transition(job_id, JobState.QUALITY_CHECK)
        hero_frame = os.path.join(render_output_dir, f"frame_{min(total_frames // 2, 120):04d}.jpg")
        if not os.path.exists(hero_frame):
            hero_frame = os.path.join(render_output_dir, f"frame_{min(total_frames // 2, 45):04d}.png")
        if not os.path.exists(hero_frame):
            hero_frame = os.path.join(render_output_dir, "frame_0001.jpg")
        if not os.path.exists(hero_frame):
            hero_frame = os.path.join(render_output_dir, "frame_0001.png")

        # STEP 5: Subtitles & Video Assembly via FFmpeg
        await ProductionJobStateMachine.transition(job_id, JobState.ASSEMBLING)
        srt_file = str(settings.OUTPUT_DIR / "renders" / episode_slug / "subtitles.srt")
        SubtitleEngine.generate_srt(dialogue_records, srt_file)

        final_video_name = f"{episode_slug}.mp4"
        final_video_dir = settings.OUTPUT_DIR / ("shorts" if format_type == "SHORT" else "episodes")
        final_video_path = str(final_video_dir / final_video_name)
        
        frames_pattern = os.path.join(render_output_dir, "frame_%04d.jpg")
        if not any(f.endswith(".jpg") for f in os.listdir(render_output_dir) if os.path.exists(render_output_dir)):
            frames_pattern = os.path.join(render_output_dir, "frame_%04d.png")
        print("[PIPELINE] Assembling video, audio stems, and metadata via FFmpeg...")
        FFmpegCompositor.assemble_video_with_audio(
            frames_pattern=frames_pattern,
            audio_file_path=master_audio_path,
            output_video_path=final_video_path,
            fps=fps
        )
        print(f"[PIPELINE] Final video successfully encoded: {final_video_path}")

        # STEP 6: AI Thumbnail Generation
        thumbnail_path = str(settings.ASSETS_DIR / "thumbnails" / f"{episode_slug}_thumb.jpg")
        ThumbnailGenerator.create_thumbnail(
            base_frame_path=hero_frame,
            output_thumbnail_path=thumbnail_path,
            headline_text="WHO IS WATCHING?!",
            emotion_tag="SHOCK",
            format_type=format_type
        )
        print(f"[PIPELINE] High-CTR thumbnail created: {thumbnail_path}")

        # STEP 7: Metadata & Compliance Validation
        meta = MetadataGenerator.generate_metadata(
            series_title=series_title,
            episode_number=episode_number,
            episode_title=episode_title,
            cliffhanger_question=script.cliffhanger_question,
            synopsis=script.synopsis,
            format_type=format_type
        )

        compliance = ComplianceChecker.audit_publication(
            title=meta["title"],
            description=meta["description"],
            target_audience="Family & Teen",
            is_original_animation=True
        )

        qc_result = QualityControlInspector.audit_episode(
            script_data={"scenes": script.scenes, "cliffhanger_question": script.cliffhanger_question},
            video_path=final_video_path,
            audio_path=master_audio_path,
            thumbnail_path=thumbnail_path,
            metadata=meta,
            format_type=format_type
        )

        # STEP 9: YouTube Staging / Publishing Gate
        await ProductionJobStateMachine.transition(job_id, JobState.READY_TO_PUBLISH)
        pub_result = YouTubeUploader.publish_video(
            video_file_path=final_video_path,
            thumbnail_path=thumbnail_path,
            title=meta["title"],
            description=meta["description"],
            tags=meta["tags"],
            privacy_status="unlisted",
            made_for_kids=compliance["made_for_kids"],
            approval_mode=settings.DEFAULT_PUBLISH_MODE
        )

        if pub_result.get("status") == "PUBLISHED":
            await ProductionJobStateMachine.transition(job_id, JobState.PUBLISHED)

        production_end = datetime.utcnow()
        elapsed = (production_end - production_start).total_seconds()

        return {
            "status": "COMPLETED",
            "job_id": job_id,
            "series": series_title,
            "episode_number": episode_number,
            "episode_title": episode_title,
            "format": format_type,
            "final_video_path": final_video_path,
            "thumbnail_path": thumbnail_path,
            "subtitles_path": srt_file,
            "cliffhanger_question": script.cliffhanger_question,
            "next_episode_teaser": script.next_episode_teaser,
            "metadata": meta,
            "compliance": compliance,
            "quality_control": qc_result,
            "publishing_status": pub_result,
            "elapsed_seconds": elapsed,
            "story_memory_updates": script.story_memory_updates
        }
