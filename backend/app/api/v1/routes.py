import os
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from backend.app.repositories import SeriesRepo, CharacterRepo, EpisodeRepo
from backend.app.schemas.series import SeriesCreate
from backend.app.schemas.character import CharacterCreate
from backend.app.services.pipeline_orchestrator import PipelineOrchestrator
from backend.app.services.blender_engine.render_manager import RenderManager
from backend.app.services.voice_engine.audio_processor import AudioProcessor
from backend.orchestrator.state_machine import ProductionJobStateMachine
from modules.character_engine.generator import CharacterSpecification
from backend.app.config import settings

api_router = APIRouter()

@api_router.get("/health")
async def health_check():
    """System health check and runtime tool status."""
    blender_path = RenderManager.find_blender_binary()
    ffmpeg_path = AudioProcessor.get_ffmpeg_path()
    return {
        "status": "HEALTHY",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "tools": {
            "blender_available": blender_path is not None,
            "blender_path": blender_path,
            "ffmpeg_available": ffmpeg_path is not None,
            "ffmpeg_path": ffmpeg_path,
            "tts_provider": settings.DEFAULT_TTS_PROVIDER,
            "publish_mode": settings.DEFAULT_PUBLISH_MODE
        }
    }

@api_router.get("/characters/presets")
async def get_character_presets():
    """Returns canonical Pixar/DreamWorks character specifications."""
    return CharacterSpecification.get_pixar_style_presets()

@api_router.get("/jobs")
async def list_production_jobs():
    """Lists recent production jobs and state machine lifecycle statuses."""
    return await ProductionJobStateMachine.get_active_jobs()

@api_router.get("/series")
async def list_series():
    return await SeriesRepo.list_all()

@api_router.post("/series")
async def create_series(data: SeriesCreate):
    return await SeriesRepo.create(data.model_dump())

@api_router.post("/characters")
async def create_character(data: CharacterCreate):
    return await CharacterRepo.create(data.model_dump())

@api_router.get("/series/{series_id}/characters")
async def list_characters(series_id: str):
    return await CharacterRepo.list_by_series(series_id)

@api_router.post("/episodes/produce")
async def trigger_episode_production(
    series_title: str = "Shadow Island Chronicles",
    episode_number: int = 1,
    episode_title: str = "The Whispering Cavern",
    format_type: str = "SHORT"
):
    """
    Triggers end-to-end production of an animated episode or YouTube Short.
    """
    result = await PipelineOrchestrator.produce_episode(
        series_title=series_title,
        series_genre="Mystery / Adventure",
        season_number=1,
        episode_number=episode_number,
        episode_title=episode_title,
        format_type=format_type
    )

    # Persist episode record
    await EpisodeRepo.create({
        "season_id": "s1",
        "episode_number": episode_number,
        "title": episode_title,
        "format": format_type,
        "synopsis": result.get("synopsis", ""),
        "cliffhanger_question": result.get("cliffhanger_question", ""),
        "next_episode_teaser": result.get("next_episode_teaser", ""),
        "final_video_path": result.get("final_video_path", ""),
        "primary_thumbnail_path": result.get("thumbnail_path", ""),
        "status": "COMPLETED"
    })

    return result

@api_router.get("/settings/colab")
async def get_colab_settings():
    """Returns current Google Colab Wan 2.1 GPU Worker configuration."""
    url = getattr(settings, "WAN21_API_URL", None) or os.getenv("WAN21_API_URL")
    return {
        "wan21_api_url": url,
        "animation_engine_mode": getattr(settings, "ANIMATION_ENGINE_MODE", "COLAB_WAN"),
        "is_connected": bool(url),
        "colab_notebook_url": "https://colab.research.google.com/github/Bhikaji/YT/blob/main/scripts/Wan21_Free_AI_Video_Colab.ipynb"
    }

@api_router.post("/settings/colab")
async def set_colab_settings(gradio_url: str):
    """Connects and persists the free Google Colab Wan 2.1 Gradio tunnel URL."""
    url = gradio_url.strip()
    if not url.startswith("http"):
        url = "https://" + url

    settings.WAN21_API_URL = url
    settings.ANIMATION_ENGINE_MODE = "COLAB_WAN"
    os.environ["WAN21_API_URL"] = url
    os.environ["ANIMATION_ENGINE_MODE"] = "COLAB_WAN"

    env_file = settings.BASE_DIR / ".env"
    existing_lines = []
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            existing_lines = [
                line for line in f.readlines()
                if not line.startswith("WAN21_API_URL=") and not line.startswith("ANIMATION_ENGINE_MODE=")
            ]
    existing_lines.append(f"ANIMATION_ENGINE_MODE=COLAB_WAN\n")
    existing_lines.append(f"WAN21_API_URL={url}\n")
    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(existing_lines)

    return {
        "status": "SUCCESS",
        "message": "Connected to Google Colab GPU Worker (Path 1: Wan 2.1)",
        "wan21_api_url": url,
        "animation_engine_mode": "COLAB_WAN"
    }

@api_router.get("/marathons/bible")
async def get_marathon_bible(series_title: str = "The Lost Valley"):
    """Returns the canonical 12-chapter season story arc."""
    from backend.app.services.marathon_engine import MarathonEngine
    return {
        "series": series_title,
        "season": 1,
        "total_chapters": 12,
        "chapters": MarathonEngine.get_season_bible(series_title)
    }

@api_router.post("/marathons/compile")
async def trigger_marathon_compilation(series_title: str = "The Lost Valley", season_number: int = 1):
    """Compiles all season chapters into a single 1-hour full movie marathon with chapters and poster thumbnail."""
    from backend.app.services.marathon_engine import MarathonEngine
    return MarathonEngine.compile_season_marathon(series_title=series_title, season_number=season_number)

# -------------------------------------------------------------
# AUTONOMOUS 2D STICK-FIGURE ANIMATION & SHORTS STUDIO ROUTES
# -------------------------------------------------------------

@api_router.get("/stick/trends")
async def get_stick_trends(geo: str = "US", category: str = None):
    """Fetches global trends, calculates 7-factor Trend Opportunity Scores, and classifies trends."""
    from intelligence.trend_research.trend_intelligence import TrendIntelligenceEngine
    from intelligence.topic_scoring.trend_scorer import TrendScorer
    from intelligence.topic_scoring.trend_classifier import TrendClassifier

    trends = TrendIntelligenceEngine.discover_global_trends(geo=geo, category_filter=category)
    scored_trends = []
    for t in trends[:15]:
        score_res = TrendScorer.calculate_opportunity_score(
            topic=t["topic"],
            category=t["category"],
            volume_numeric=t.get("volume_numeric", 100000)
        )
        opp_score = score_res["opportunity_score"]
        classification = TrendClassifier.classify_trend(
            topic=t["topic"],
            opportunity_score=opp_score,
            volume_numeric=t.get("volume_numeric", 100000)
        )
        tier = "HIGH" if opp_score >= 75 else ("MEDIUM" if opp_score >= 60 else "NORMAL")
        scored_trends.append({
            **t,
            "opportunity_score": opp_score,
            "opportunity_tier": tier,
            "classification": classification,
            "breakdown": score_res["factor_breakdown"]
        })

    # Sort descending by opportunity score
    scored_trends.sort(key=lambda x: x["opportunity_score"], reverse=True)
    return {
        "geo": geo,
        "total_trends": len(scored_trends),
        "trends": scored_trends
    }

@api_router.post("/stick/produce")
async def produce_stick_short(topic: str = None, category: str = None, geo: str = "US"):
    """Triggers the full 14-stage autonomous stick-figure short production pipeline."""
    from orchestrator.autonomous_studio_manager import AutonomousStudioManager
    summary = AutonomousStudioManager.run_production_cycle(
        target_topic=topic,
        target_category=category,
        geo=geo,
        publish_privacy="private"
    )
    return {
        "status": "SUCCESS",
        "production_summary": summary
    }

@api_router.get("/stick/latest")
async def get_latest_stick_short():
    """Returns the most recently rendered stick-figure short and thumbnails."""
    from pathlib import Path
    stick_base = settings.BASE_DIR / "output" / "stick_shorts"
    if not stick_base.exists():
        return {"has_short": False}

    jobs = sorted(list(stick_base.iterdir()), key=lambda p: p.stat().st_mtime, reverse=True)
    for j in jobs:
        master_mp4 = j / f"{j.name}_master.mp4"
        if master_mp4.exists():
            thumb_dir = j / "thumbnails"
            thumbs = [f"/output/stick_shorts/{j.name}/thumbnails/{p.name}" for p in thumb_dir.glob("*.jpg")] if thumb_dir.exists() else []
            return {
                "has_short": True,
                "job_id": j.name,
                "video_url": f"/output/stick_shorts/{j.name}/{j.name}_master.mp4",
                "thumbnails": thumbs,
                "video_path": str(master_mp4)
            }

    return {"has_short": False}
