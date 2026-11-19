import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.app.services.marathon_engine import MarathonEngine

def main():
    print("==========================================================================")
    print("      SEASON 1 MARATHON COMPILER: 12 CHAPTERS -> 1-HOUR FULL MOVIE        ")
    print("==========================================================================")

    bible = MarathonEngine.get_season_bible("The Lost Valley")
    print("Season 1 Story Arc (12 Chapters):")
    for ch in bible:
        print(f"  Chapter {ch['ep']:02d}: {ch['title']} — {ch['theme']}")
    print("--------------------------------------------------------------------------")

    res = MarathonEngine.compile_season_marathon(
        series_title="The Lost Valley",
        season_number=1
    )

    print("\n==========================================================================")
    print("MARATHON MOVIE SUCCESSFULLY COMPILED!")
    print("==========================================================================")
    print(f"Master Video: {res['marathon_video_path']}")
    print(f"Movie Poster: {res['thumbnail_path']}")
    print(f"Chapters Included: {res['chapters_included']} chapters")
    print(f"Total Duration: {res['total_duration_seconds']:.1f}s")
    print("\nYouTube Title:")
    print(res["youtube_title"])
    print("\nYouTube Description with Timestamps:")
    print(res["youtube_description"][:450] + "...\n")

if __name__ == "__main__":
    main()
