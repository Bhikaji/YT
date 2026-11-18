import os
from pathlib import Path
from typing import List, Dict, Any

class SubtitleEngine:
    """Generates SRT and formatted ASS subtitle files for video encoding."""

    @staticmethod
    def format_timestamp_srt(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    @classmethod
    def generate_srt(cls, dialogue_events: List[Dict[str, Any]], output_srt_path: str) -> str:
        """
        dialogue_events: List of {speaker: str, text: str, start: float, duration: float}
        """
        lines = []
        for idx, event in enumerate(dialogue_events, start=1):
            start_str = cls.format_timestamp_srt(event["start"])
            end_str = cls.format_timestamp_srt(event["start"] + event["duration"])
            
            lines.append(str(idx))
            lines.append(f"{start_str} --> {end_str}")
            lines.append(f"{event['speaker'].upper()}: {event['text']}")
            lines.append("")

        with open(output_srt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return output_srt_path
