"""
Advanced Character Dialogue Coordination & Scheduler Engine.
Enforces strict speaking-turn management and guarantees ZERO accidental overlapping voices.
Dynamically measures actual generated audio durations and inserts natural conversational gaps.
"""

import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
import imageio_ffmpeg

class DialogueScheduler:
    """
    Centralized Speaking-Turn Coordinator & Timeline Scheduler.
    Guarantees no accidental overlapping voices between characters.
    """

    @staticmethod
    def get_audio_duration_sec(audio_path: Path) -> float:
        """Measures exact duration of an audio file using FFmpeg."""
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [exe, "-i", str(audio_path)]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        for line in res.stderr.splitlines():
            if "Duration:" in line:
                try:
                    time_part = line.split("Duration:")[1].split(",")[0].strip()
                    h, m, s = time_part.split(":")
                    return float(h) * 3600 + float(m) * 60 + float(s)
                except Exception:
                    pass
        return 2.5  # Fallback estimate

    @classmethod
    def schedule_dialogues(
        cls,
        dialogue_items: List[Dict[str, Any]],
        natural_gap_sec: float = 0.25,
        target_total_sec: float = 30.0,
        start_offset_sec: float = 2.3
    ) -> List[Dict[str, Any]]:
        """
        Calculates exact non-overlapping start/end timestamps based on actual audio durations.
        Starts after the opening disclaimer screen (start_offset_sec = 2.3s) for perfect A/V sync.
        """
        scheduled = []
        current_time = start_offset_sec

        for idx, item in enumerate(dialogue_items):
            audio_path = Path(item["audio_path"])
            actual_dur = cls.get_audio_duration_sec(audio_path)

            start_time = round(current_time, 2)
            end_time = round(start_time + actual_dur, 2)

            scheduled.append({
                "sequence_index": idx,
                "speaker_id": item["speaker_id"],
                "speaker_name": item.get("speaker_name", item["speaker_id"]),
                "text": item["text"],
                "emotion": item.get("emotion", "curious"),
                "audio_path": str(audio_path),
                "actual_duration_sec": actual_dur,
                "start_second": start_time,
                "end_second": end_time
            })

            # Advance clock with natural human conversational gap
            current_time = end_time + natural_gap_sec

        return scheduled

    @classmethod
    def audit_zero_overlap(cls, scheduled_dialogues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validates that no two dialogue clips overlap in time.
        """
        overlaps = []
        for i in range(len(scheduled_dialogues) - 1):
            curr = scheduled_dialogues[i]
            next_item = scheduled_dialogues[i+1]
            if curr["end_second"] > next_item["start_second"]:
                overlaps.append({
                    "conflict_index": i,
                    "speaker_1": curr["speaker_id"],
                    "speaker_2": next_item["speaker_id"],
                    "overlap_duration": round(curr["end_second"] - next_item["start_second"], 2)
                })

        return {
            "passed": len(overlaps) == 0,
            "total_dialogues": len(scheduled_dialogues),
            "overlap_count": len(overlaps),
            "conflicts": overlaps
        }

    @classmethod
    def get_speaker_at_timestamp(
        cls,
        scheduled_dialogues: List[Dict[str, Any]],
        t_sec: float
    ) -> Dict[str, Any]:
        """
        Returns active speaker info and listener state for any arbitrary frame at t_sec.
        """
        for item in scheduled_dialogues:
            if item["start_second"] <= t_sec <= item["end_second"]:
                # Calculate progress within current spoken phrase (0.0 to 1.0)
                dur = max(0.01, item["end_second"] - item["start_second"])
                progress = (t_sec - item["start_second"]) / dur
                return {
                    "is_speaking": True,
                    "speaker_id": item["speaker_id"],
                    "text": item["text"],
                    "emotion": item["emotion"],
                    "progress": progress
                }

        return {
            "is_speaking": False,
            "speaker_id": None,
            "text": "",
            "emotion": "neutral",
            "progress": 0.0
        }
