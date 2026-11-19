import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.app.services.pipeline_orchestrator import PipelineOrchestrator
from backend.app.repositories import EpisodeRepo

async def main():
    print("==========================================================================")
    print("      AUTONOMOUS AI CARTOON STUDIO: 10-SECOND DEMO EPISODE PRODUCTION      ")
    print("==========================================================================")
    print("Series: The Lost Valley")
    print("Episode 1: The Prehistoric Awakening")
    print("Format: SHORT (1080x1920 9:16 Vertical, 10.0 seconds)")
    print("--------------------------------------------------------------------------")

    result = await PipelineOrchestrator.produce_episode(
        series_title="The Lost Valley",
        series_genre="Adventure / Dinosaur",
        season_number=1,
        episode_number=1,
        episode_title="The Prehistoric Awakening",
        format_type="SHORT"
    )

    print("\n==========================================================================")
    print("PRODUCTION COMPLETED SUCCESSFULLY!")
    print("==========================================================================")
    print(f"Status: {result.get('status')}")
    print(f"Job ID: {result.get('job_id')}")
    print(f"Final Video: {result.get('final_video_path')}")
    print(f"Thumbnail: {result.get('thumbnail_path')}")
    print(f"Duration: {result.get('duration_seconds')}s")
    print(f"Aspect Ratio: {result.get('aspect_ratio')}")
    print(f"Elapsed Time: {result.get('production_time_seconds')}s")

    # Persist episode record
    await EpisodeRepo.create({
        "season_id": "s1",
        "episode_number": 1,
        "title": "The Prehistoric Awakening",
        "format": "SHORT",
        "synopsis": result.get("synopsis", ""),
        "cliffhanger_question": result.get("cliffhanger_question", ""),
        "next_episode_teaser": result.get("next_episode_teaser", ""),
        "final_video_path": result.get("final_video_path", ""),
        "primary_thumbnail_path": result.get("thumbnail_path", ""),
        "status": "COMPLETED"
    })
    print("Episode metadata saved to studio database.")

if __name__ == "__main__":
    asyncio.run(main())
