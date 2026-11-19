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
