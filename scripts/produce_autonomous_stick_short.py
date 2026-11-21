import asyncio
import sys
import argparse
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from orchestrator.autonomous_studio_manager import AutonomousStickStudioManager

async def main():
    parser = argparse.ArgumentParser(description="Autonomous AI 2D Stick-Figure Animation & YouTube Shorts Studio")
    parser.add_argument("--topic", type=str, default=None, help="Force a specific topic (or leave empty for autonomous trend discovery)")
    parser.add_argument("--category", type=str, default=None, help="Force a specific category (e.g. science_discovery, technology, comedy_entertainment)")
    parser.add_argument("--geo", type=str, default="IN", help="Target country code: IN, US, GB, CA, AU, WORLDWIDE")
    parser.add_argument("--language", type=str, default="mr_rangdi", choices=["mr_rangdi", "hi", "en"], help="Target language (Default: Priority 1 - Rangdi Marathi)")
    parser.add_argument("--privacy", type=str, default="private", choices=["private", "unlisted", "public"], help="YouTube publishing visibility")

    args = parser.parse_args()

    result = await AutonomousStickStudioManager.produce_autonomous_short(
        geo=args.geo,
        forced_category=args.category,
        forced_topic=args.topic,
        language_override=args.language,
        privacy_status=args.privacy
    )

    print("\n------------------ PRODUCTION SUMMARY ------------------")
    print(f"Title:         {result['script_title']}")
    print(f"Topic:         {result['topic']}")
    print(f"Category:      {result['category']}")
    print(f"Characters:    {' & '.join(result['cast'])}")
    print(f"Video File:    {result['final_video_path']}")
    print(f"Thumbnail:     {result['thumbnail_path']}")
    print(f"YouTube ID:    {result['youtube_publication']['youtube_video_id']} ({result['youtube_publication']['privacy_status']})")
    print(f"QC Score:      {result['qc_audit']['quality_score']}/100")
    print(f"Elapsed Time:  {result['production_time_seconds']}s")
    print("--------------------------------------------------------\n")

if __name__ == "__main__":
    asyncio.run(main())
