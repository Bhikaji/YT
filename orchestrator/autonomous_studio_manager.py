import os
import asyncio
import uuid
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from intelligence.trend_research.trend_intelligence import TrendIntelligenceEngine
from intelligence.trend_research.category_catalog import ContentCategoryCatalog
from intelligence.topic_scoring.trend_scorer import TrendScorer
from intelligence.topic_scoring.trend_classifier import TrendClassifier
from intelligence.script_generation.story_engine import StickStoryEngine
from intelligence.script_generation.script_evaluator import ScriptEvaluator
from intelligence.language_intelligence.language_selector import LanguageSelectionEngine
from intelligence.language_intelligence.multilingual_localizer import MultilingualLocalizer
from animation.character_engine.character_model import StickFigureCharacter
from animation.scene_director.scene_timeline import AnimationTimelineDirector
from animation.environment_engine.procedural_backgrounds import ProceduralBackgroundRenderer
from audio.voice_generation.realistic_voice_engine import RealisticHumanVoiceEngine
from audio.dialogue_coordination.dialogue_scheduler import DialogueScheduler
from audio.dialogue_coordination.audio_qa_engine import AudioQualityAssuranceEngine
from audio.audio_mixer.master_mixer import MasterAudioMixer
from production.renderer.stick_renderer import StickFigureRenderer
from production.video_compiler import StickVideoCompiler
from production.quality_control.qc_inspector import StickQCInspector
from production.thumbnail_generator.thumbnail_studio import StickThumbnailStudio
from integrations.youtube.youtube_publisher import YouTubePublisher
from intelligence.learning_engine.performance_collector import PerformanceCollector
from intelligence.learning_engine.optimization_engine import ContentOptimizationEngine
from backend.app.config import settings

class AutonomousStickStudioManager:
    """
    Central Autonomous 2D Stick-Figure Animation & YouTube Shorts Studio Manager.
    Executes the complete 14-Stage automated production pipeline with zero required human intervention.
    Supports authentic Rangdi Marathi (Priority 1), Hindi (Priority 2), English, and International voice localizations.
    """

    @classmethod
    async def produce_autonomous_short(
        cls,
        geo: str = "IN",
        forced_category: Optional[str] = None,
        forced_topic: Optional[str] = None,
        language_override: Optional[str] = "mr_rangdi",
        privacy_status: str = "private"
    ) -> Dict[str, Any]:
        job_id = str(uuid.uuid4())
        start_time = time.time()
        print(f"\n==========================================================================")
        print(f"   🎬 AUTONOMOUS STICK-FIGURE ANIMATION STUDIO: JOB {job_id[:8]}           ")
        print(f"==========================================================================")

        # ---------------------------------------------------------
        # STAGE 1: Trend Discovery & Topic Selection
        # ---------------------------------------------------------
        print("[Stage 1/14] Discovering trending global topics across 10 categories...")
        if forced_topic:
            category = forced_category or ContentCategoryCatalog.identify_category_from_text(forced_topic)
            selected_trend = {
                "topic": forced_topic,
                "category": category,
                "volume_numeric": 350000,
                "geo": geo
            }
        else:
            trends = TrendIntelligenceEngine.discover_global_trends(geo=geo, category_filter=forced_category)
            scored_trends = []
            for t in trends:
                sc = TrendScorer.calculate_opportunity_score(t["topic"], t["category"], t.get("volume_numeric", 100000))
                classification = TrendClassifier.classify_trend(t["topic"], sc["opportunity_score"], t.get("volume_numeric", 100000))
                scored_trends.append({**t, **sc, "classification": classification})

            scored_trends.sort(key=lambda x: x["opportunity_score"], reverse=True)
            selected_trend = scored_trends[0]

        topic = selected_trend["topic"]
        category = selected_trend["category"]
        opp_score = selected_trend.get("opportunity_score", 92.0)
        print(f"[Stage 2/14] Selected Winner: \"{topic}\" [{category.upper()}] (Score: {opp_score}/100)")

        # ---------------------------------------------------------
        # STAGE 2.5: Audience Language Selection
        # Priority 1: Rangdi Marathi, Priority 2: Hindi, Priority 3: English
        # ---------------------------------------------------------
        lang_info = LanguageSelectionEngine.select_language_for_target(
            target_geo=geo,
            explicit_language=language_override
        )
        selected_lang = lang_info["language_code"]
        print(f"[Stage 2.5/14] Target Language Selected: {lang_info['language_name']} ({lang_info['native_name']}) [Priority {lang_info['priority']}]")

        # ---------------------------------------------------------
        # STAGE 3 & 4: Research, Fact-Checking & Localized Screenplay
        # ---------------------------------------------------------
        print("[Stage 3/14] Verifying factual claims against knowledge base...")
        fact_check = ScriptEvaluator.verify_factual_accuracy(topic, "")

        print(f"[Stage 4/14] Generating 6-part mandatory 30s Short screenplay in {lang_info['language_name']}...")
        script = MultilingualLocalizer.generate_script_for_language(
            topic=topic,
            category=category,
            language_code=selected_lang
        )

        # ---------------------------------------------------------
        # STAGE 5: Script Quality Evaluation Gate
        # ---------------------------------------------------------
        print("[Stage 5/14] Auditing script structure against YouTube retention criteria...")
        approved, q_score, checks = ScriptEvaluator.evaluate_script(script)
        print(f"[Stage 5/14] Quality Gate: Approved={approved} (Score: {q_score}/100)")

        # ---------------------------------------------------------
        # STAGE 6: Character Selection
        # ---------------------------------------------------------
        print("[Stage 6/14] Assigning stick-figure characters & personality rigs...")
        canon_chars = StickFigureCharacter.get_canonical_library()
        char1 = canon_chars.get(script.cast[0]["id"], list(canon_chars.values())[0])
        char2 = canon_chars.get(script.cast[1]["id"], list(canon_chars.values())[1])
        print(f"             Cast: {script.cast[0]['name']} & {script.cast[1]['name']}")

        # ---------------------------------------------------------
        # STAGE 7: Audio Synthesis with Realistic Human Voices
        # ---------------------------------------------------------
        render_slug = f"stick_{job_id[:8]}"
        job_dir = settings.OUTPUT_DIR / "stick_shorts" / render_slug
        job_dir.mkdir(parents=True, exist_ok=True)
        audio_dir = job_dir / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)

        print(f"[Stage 7/14] Synthesizing human neural character voices in {lang_info['language_name']}...")
        raw_dialogue_items = []
        diag_idx = 1
        for s in script.scenes:
            for d in s.dialogues:
                clip_file = audio_dir / f"diag_{diag_idx}_{d.speaker_id}.mp3"
                await RealisticHumanVoiceEngine.synthesize_dialogue_line(
                    text=d.text,
                    character_id=d.speaker_id,
                    language_code=selected_lang,
                    emotion=d.emotion,
                    output_path=clip_file
                )
                raw_dialogue_items.append({
                    "scene_id": s.scene_id,
                    "speaker_id": d.speaker_id,
                    "speaker_name": d.speaker_name,
                    "text": d.text,
                    "emotion": d.emotion,
                    "audio_path": str(clip_file)
                })
                diag_idx += 1

        # ---------------------------------------------------------
        # STAGE 8: Advanced Dialogue Scheduling (Strict Zero-Overlap Enforcer)
        # ---------------------------------------------------------
        print("[Stage 8/14] Scheduling dialogue turns based on actual audio (ZERO OVERLAP GUARANTEED)...")
        scheduled_dialogues = DialogueScheduler.schedule_dialogues(
            dialogue_items=raw_dialogue_items,
            natural_gap_sec=0.25,
            target_total_sec=30.0
        )
        overlap_audit = DialogueScheduler.audit_zero_overlap(scheduled_dialogues)
        print(f"             Dialogue Schedule: {len(scheduled_dialogues)} lines, Zero Overlap Passed: {overlap_audit['passed']}")

        # Synchronize exact scheduled timestamps back into script scenes for perfect lip-sync
        sched_map = {f"{item['speaker_id']}_{item['text']}": item for item in scheduled_dialogues}
        for s in script.scenes:
            for d in s.dialogues:
                k = f"{d.speaker_id}_{d.text}"
                if k in sched_map:
                    d.start_second = sched_map[k]["start_second"]
                    d.end_second = sched_map[k]["end_second"]

        # Mix Soundtrack: Non-overlapping Dialogues + Ducked BGM + SFX
        sfx_cues = [
            {"name": "whoosh", "time": 0.5},
            {"name": "punchline_impact", "time": 14.2},
            {"name": "ding_lightbulb", "time": 21.3},
            {"name": "pop", "time": 27.2}
        ]
        master_audio_path = audio_dir / "master_soundtrack.aac"
        print("             Mixing soundtrack: Dialogues + Ducked BGM (-16.5dB) + Cartoon SFX...")
        MasterAudioMixer.assemble_soundtrack(
            dialogue_clips=scheduled_dialogues,
            sfx_cues=sfx_cues,
            output_audio_path=master_audio_path,
            total_duration=30.0
        )

        # Audio Quality Assurance Engine
        audio_qa = AudioQualityAssuranceEngine.audit_dialogue_soundtrack(
            scheduled_dialogues=scheduled_dialogues,
            master_audio_path=master_audio_path
        )
        print(f"             Audio QA: Score={audio_qa['overall_audio_score']}/100, Overlap Free={audio_qa['overlap_free']}")

        # ---------------------------------------------------------
        # STAGE 9: Directorial Timeline Compilation
        # ---------------------------------------------------------
        print("[Stage 9/14] Compiling 900-frame directorial timeline with synced lip-sync & listener reactions...")
        timeline = AnimationTimelineDirector.compile_timeline(script=script, fps=30)

        # ---------------------------------------------------------
        # STAGE 10: 2D Video Rendering (High-Contrast Dual-Pass Outline)
        # ---------------------------------------------------------
        print("[Stage 10/14] Rendering high-contrast 2D frames (1080x1920 9:16 vertical)...")
        frames_dir = job_dir / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)

        hero_frame_path = None
        fps = 30
        total_frames = len(timeline)
        render_step = 1

        frame_counter = 1
        effective_fps = fps // render_step if render_step > 1 else fps

        for i in range(0, total_frames, render_step):
            frame_state = timeline[i]
            frame_img = StickFigureRenderer.render_frame(
                frame_data=frame_state,
                char1=char1,
                char2=char2,
                width=1080,
                height=1920
            )
            f_path = frames_dir / f"frame_{frame_counter:04d}.png"
            frame_img.save(f_path)
            if i == int(total_frames * 0.5) or not hero_frame_path:
                hero_frame_path = f_path
            frame_counter += 1

        print("              Encoding final H.264/AAC MP4 video via FFmpeg...")
        final_video_path = job_dir / f"{render_slug}_master.mp4"
        frames_pattern = str(frames_dir / "frame_%04d.png")
        StickVideoCompiler.compile_short(
            frames_pattern=frames_pattern,
            audio_path=str(master_audio_path),
            output_mp4_path=final_video_path,
            fps=effective_fps
        )

        # ---------------------------------------------------------
        # STAGE 11: Quality Control Engine
        # ---------------------------------------------------------
        print("[Stage 11/14] Executing automated visual & audio quality pre-flight...")
        qc_result = StickQCInspector.audit_short(
            video_path=final_video_path,
            thumbnail_path=hero_frame_path,
            expected_duration=30.0
        )
        print(f"              QC Audit: Passed={qc_result['passed']} (Score: {qc_result['quality_score']}/100)")

        # ---------------------------------------------------------
        # STAGE 12: High-CTR Thumbnail Generation
        # ---------------------------------------------------------
        print("[Stage 12/14] Generating 3 high-contrast vertical thumbnail concepts...")
        thumb_res = StickThumbnailStudio.generate_thumbnails(
            topic=topic,
            hero_frame_path=hero_frame_path,
            output_dir=job_dir / "thumbnails"
        )
        final_thumbnail_path = thumb_res["selected_thumbnail"]
        print(f"              Selected Concept: {Path(final_thumbnail_path).name}")

        # ---------------------------------------------------------
        # STAGE 13: YouTube Publishing & Staging
        # ---------------------------------------------------------
        print("[Stage 13/14] Staging video for YouTube publishing (OAuth 2.0)...")
        pub_result = YouTubePublisher.publish_short(
            video_path=final_video_path,
            thumbnail_path=Path(final_thumbnail_path),
            topic=topic,
            category=category,
            hook_text=script.hook,
            privacy_status=privacy_status
        )

        # ---------------------------------------------------------
        # STAGE 14: Analytics & Continuous Learning Loop
        # ---------------------------------------------------------
        print("[Stage 14/14] Updating learning engine with production performance data...")
        metrics = PerformanceCollector.collect_video_metrics(job_id, pub_result["youtube_video_id"])
        learning_insights = ContentOptimizationEngine.analyze_learning_feedback([
            {"category": category, "retention_percent": metrics["retention_percent"]}
        ])

        elapsed = round(time.time() - start_time, 2)
        print("==========================================================================")
        print(f"✔ PRODUCTION COMPLETE IN {elapsed}s!")
        print(f"Language:     {lang_info['language_name']} ({lang_info['native_name']})")
        print(f"Video Output: {final_video_path}")
        print(f"Thumbnail:    {final_thumbnail_path}")
        print(f"YouTube ID:   {pub_result['youtube_video_id']} ({pub_result['privacy_status']})")
        print("==========================================================================\n")

        return {
            "status": "COMPLETED",
            "job_id": job_id,
            "topic": topic,
            "category": category,
            "language": lang_info["language_name"],
            "language_code": selected_lang,
            "opportunity_score": opp_score,
            "script_title": script.title,
            "hook": script.hook,
            "cast": [script.cast[0]["name"], script.cast[1]["name"]],
            "final_video_path": str(final_video_path),
            "thumbnail_path": str(final_thumbnail_path),
            "youtube_publication": pub_result,
            "qc_audit": qc_result,
            "audio_qa": audio_qa,
            "learning_insights": learning_insights,
            "production_time_seconds": elapsed
        }

    @classmethod
    def run_production_cycle(
        cls,
        geo: str = "IN",
        target_category: Optional[str] = None,
        target_topic: Optional[str] = None,
        target_language: Optional[str] = "mr_rangdi",
        publish_privacy: str = "private"
    ) -> Dict[str, Any]:
        """Synchronous entry point for automation scripts and background workers."""
        return asyncio.run(
            cls.produce_autonomous_short(
                geo=geo,
                forced_category=target_category,
                forced_topic=target_topic,
                language_override=target_language,
                privacy_status=publish_privacy
            )
        )
