import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import timedelta
import imageio_ffmpeg

from backend.app.config import settings
from backend.app.services.post_production.ffmpeg_compositor import FFmpegCompositor
from backend.app.services.thumbnail_engine.typography_styler import ThumbnailGenerator

class MarathonEngine:
    """
    Orchestrates the 12-Chapter Season Arc and 1-Hour Marathon Movie Compilation.
    Combines episodic chapters into a single master cinematic movie for massive watch time.
    """

    SEASON_1_CHAPTER_BIBLE = [
        {"ep": 1, "title": "The Prehistoric Awakening", "theme": "Discovery of the ancient glowing relic and hidden dino valley"},
        {"ep": 2, "title": "The Whispering Jungle", "theme": "Tracking mysterious colossal footprints through tropical mist"},
        {"ep": 3, "title": "The Stegosaurus Sanctuary", "theme": "First friendly encounter with giant armored herbivores"},
        {"ep": 4, "title": "The Boiling River", "theme": "Navigating geothermal rapids beside active volcanic vents"},
        {"ep": 5, "title": "The Pterodactyl Peak", "theme": "Scaling misty volcanic cliffs and spotting flying reptiles"},
        {"ep": 6, "title": "The Ancient Cavern", "theme": "Deciphering glowing symbols and hieroglyphs inside obsidian caves"},
        {"ep": 7, "title": "The Midnight Roar", "theme": "Surviving a tense stealth encounter with an apex predator"},
        {"ep": 8, "title": "The Crystal Falls", "theme": "Discovering an underground bioluminescent oasis and crystal waters"},
        {"ep": 9, "title": "The Raptor Riddle", "theme": "Outsmarting a pack of curious velociraptors using clever traps"},
        {"ep": 10, "title": "The Volcano's Tremor", "theme": "The earth shakes as the volcano begins its awakening rumble"},
        {"ep": 11, "title": "The Race to the Relic", "theme": "A high-stakes dash across obsidian bridges before lava floods the valley"},
        {"ep": 12, "title": "The Gate of Dawn", "theme": "Unlocking the ancient sanctuary gate in a jaw-dropping season finale"}
    ]

    @classmethod
    def get_season_bible(cls, series_title: str = "The Lost Valley") -> List[Dict[str, Any]]:
        return cls.SEASON_1_CHAPTER_BIBLE

    @classmethod
    def get_video_duration(cls, video_path: str) -> float:
        """Inspects video duration in seconds using FFmpeg."""
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [exe, "-i", video_path]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        for line in res.stderr.splitlines():
            if "Duration:" in line:
                try:
                    time_part = line.split("Duration:")[1].split(",")[0].strip()
                    h, m, s = time_part.split(":")
                    return float(h) * 3600 + float(m) * 60 + float(s)
                except Exception:
                    pass
        return 300.0  # default 5 minutes

    @classmethod
    def compile_season_marathon(
        cls,
        series_title: str = "The Lost Valley",
        season_number: int = 1,
        episode_paths: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Gathers all 12 chapters and compiles them into a seamless 1-Hour Full Season Movie.
        Generates YouTube chapters, timestamps, metadata, and 16:9 movie poster thumbnail.
        """
        output_dir = settings.OUTPUT_DIR / "marathons"
        output_dir.mkdir(parents=True, exist_ok=True)

        episodes_dir = settings.OUTPUT_DIR / "episodes"
        shorts_dir = settings.OUTPUT_DIR / "shorts"

        # Discover or use supplied paths
        resolved_episodes = []
        if episode_paths:
            resolved_episodes = [p for p in episode_paths if os.path.exists(p)]
        else:
            # Look in output/episodes and output/shorts
            for ep_info in cls.SEASON_1_CHAPTER_BIBLE:
                ep_num = ep_info["ep"]
                # Match patterns like ep_1_*.mp4
                candidates = list(episodes_dir.glob(f"ep_{ep_num}_*.mp4")) + list(shorts_dir.glob(f"ep_{ep_num}_*.mp4"))
                if candidates:
                    resolved_episodes.append(str(candidates[0]))

        # If fewer than 12 exist for test, use available episodes or duplicate for simulation
        if not resolved_episodes:
            # Fallback to available demo shorts/episodes
            for f in sorted(shorts_dir.glob("*.mp4")):
                resolved_episodes.append(str(f))
                if len(resolved_episodes) >= 12:
                    break

        print(f"[MarathonEngine] Found {len(resolved_episodes)} chapters for Season {season_number} compilation.")

        # Calculate chapter timestamps
        timestamps = []
        current_second = 0.0
        for i, ep_path in enumerate(resolved_episodes):
            ch_title = cls.SEASON_1_CHAPTER_BIBLE[i]["title"] if i < len(cls.SEASON_1_CHAPTER_BIBLE) else f"Chapter {i+1}"
            td = str(timedelta(seconds=int(current_second)))
            # Format hh:mm:ss or mm:ss
            time_str = td if td.startswith("0:") and len(td) > 4 else td
            timestamps.append(f"{time_str} - Chapter {i+1}: {ch_title}")
            dur = cls.get_video_duration(ep_path)
            current_second += dur

        # Assemble master video
        marathon_file_name = f"{series_title.lower().replace(' ', '_')}_season_{season_number}_full_movie.mp4"
        marathon_video_path = str(output_dir / marathon_file_name)

        print(f"[MarathonEngine] Concatenating {len(resolved_episodes)} chapters into master movie...")
        comp_res = FFmpegCompositor.concatenate_episodes(
            episode_paths=resolved_episodes,
            output_marathon_path=marathon_video_path
        )

        # Generate High-CTR 16:9 Marathon Poster Thumbnail
        hero_thumb = settings.ASSETS_DIR / "thumbnails" / f"season_{season_number}_marathon_movie_thumb.jpg"
        hero_thumb.parent.mkdir(parents=True, exist_ok=True)
        base_frame = None
        for p in resolved_episodes:
            frame_cand = str(Path(p).parent.parent / "renders" / Path(p).stem / "frame_0060.jpg")
            if os.path.exists(frame_cand):
                base_frame = frame_cand
                break
        if not base_frame:
            base_frame = str(settings.BASE_DIR / "output" / "test_preview_frame.jpg")

        if os.path.exists(base_frame):
            ThumbnailGenerator.create_thumbnail(
                base_frame_path=base_frame,
                output_thumbnail_path=str(hero_thumb),
                headline_text="1 HOUR FULL MOVIE",
                emotion_tag="INTENSE",
                format_type="LONG"
            )

        # Build YouTube Metadata
        youtube_title = f"{series_title}: Complete Season {season_number} (1 Hour 3D Animated Movie) [Pixar 4K]"
        youtube_description = (
            f"🎬 Watch the COMPLETE SEASON {season_number} of {series_title} in one epic 1-hour movie marathon!\n\n"
            f"Follow Leo and his golden puppy Lumi as they journey through the perilous prehistoric valley filled with "
            f"living dinosaurs, volcanic eruptions, and ancient mysteries!\n\n"
            f"⏱️ CHAPTER TIMESTAMPS:\n"
            + "\n".join(timestamps) +
            f"\n\n🔔 Subscribe to the channel for upcoming Season 2 adventures!\n"
            f"#TheLostValley #Animation #Dinosaurs #FullMovie #3DAnimation #Cartoon"
        )

        return {
            "status": "COMPLETED",
            "series": series_title,
            "season": season_number,
            "chapters_included": len(resolved_episodes),
            "total_duration_seconds": current_second,
            "marathon_video_path": marathon_video_path,
            "thumbnail_path": str(hero_thumb),
            "youtube_title": youtube_title,
            "youtube_description": youtube_description,
            "timestamps": timestamps
        }
