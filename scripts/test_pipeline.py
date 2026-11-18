import asyncio
import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.database import init_db
from backend.app.services.pipeline_orchestrator import PipelineOrchestrator

async def run_e2e_studio_test():
    print("=================================================================")
    print("      AUTONOMOUS AI CARTOON STUDIO – FULL E2E VALIDATION         ")
    print("=================================================================")
    
    # 1. Initialize SQLite Database Schema
    print("\n[TEST 1/4] Initializing Database Schema...")
    await init_db()
    print("✔ Database schema created successfully.")

    # 2. Define Permanent Cast
    cast = [
        {"id": "hero_leo", "name": "Leo", "voice_id": "en-US-ChristopherNeural"},
        {"id": "sidekick_maya", "name": "Maya", "voice_id": "en-US-AnaNeural"}
    ]

    # 3. Produce Episode 1 (Pilot Short)
    print("\n[TEST 2/4] Producing Episode 1 (YouTube Short)...")
    ep1_result = await PipelineOrchestrator.produce_episode(
        series_title="The Mystery of Shadow Island",
        series_genre="Adventure / Mystery",
        season_number=1,
        episode_number=1,
        episode_title="The Secret Map",
        format_type="SHORT",
        cast=cast
    )

    print("\n✔ EPISODE 1 PRODUCTION SUMMARY:")
    print(f"  • Video: {ep1_result['final_video_path']}")
    print(f"  • Thumbnail: {ep1_result['thumbnail_path']}")
    print(f"  • Subtitles: {ep1_result['subtitles_path']}")
    print(f"  • Cliffhanger: \"{ep1_result['cliffhanger_question']}\"")
    print(f"  • Production Time: {ep1_result['elapsed_seconds']:.2f}s")
    print(f"  • Compliance Check: {ep1_result['compliance']['recommendation']}")

    # 4. Produce Episode 2 (Continues from Ep 1 Cliffhanger)
    print("\n[TEST 3/4] Producing Episode 2 (Connected Continuous Episode)...")
    ep2_result = await PipelineOrchestrator.produce_episode(
        series_title="The Mystery of Shadow Island",
        series_genre="Adventure / Mystery",
        season_number=1,
        episode_number=2,
        episode_title="The Whispering Cavern",
        format_type="SHORT",
        cast=cast,
        prior_cliffhanger=ep1_result["cliffhanger_question"]
    )

    print("\n✔ EPISODE 2 PRODUCTION SUMMARY:")
    print(f"  • Video: {ep2_result['final_video_path']}")
    print(f"  • Thumbnail: {ep2_result['thumbnail_path']}")
    print(f"  • Cliffhanger: \"{ep2_result['cliffhanger_question']}\"")
    print(f"  • Teaser: \"{ep2_result['next_episode_teaser']}\"")

    # 5. Verification
    print("\n[TEST 4/4] Verifying Media Files on Disk...")
    assert os.path.exists(ep1_result["final_video_path"]), "Ep 1 video file missing!"
    assert os.path.exists(ep1_result["thumbnail_path"]), "Ep 1 thumbnail file missing!"
    assert os.path.exists(ep2_result["final_video_path"]), "Ep 2 video file missing!"
    
    ep1_size_mb = os.path.getsize(ep1_result["final_video_path"]) / (1024 * 1024)
    ep2_size_mb = os.path.getsize(ep2_result["final_video_path"]) / (1024 * 1024)
    print(f"✔ Episode 1 MP4 size: {ep1_size_mb:.2f} MB")
    print(f"✔ Episode 2 MP4 size: {ep2_size_mb:.2f} MB")

    print("\n=================================================================")
    print("      ALL ACCEPTANCE CRITERIA VERIFIED & PASSED!               ")
    print("=================================================================")

if __name__ == "__main__":
    asyncio.run(run_e2e_studio_test())
