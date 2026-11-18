from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from backend.app.repositories import SeriesRepo, CharacterRepo, EpisodeRepo
from backend.app.schemas.series import SeriesCreate
from backend.app.schemas.character import CharacterCreate
from backend.app.services.pipeline_orchestrator import PipelineOrchestrator
from backend.app.services.blender_engine.render_manager import RenderManager
from backend.app.services.voice_engine.audio_processor import AudioProcessor
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
