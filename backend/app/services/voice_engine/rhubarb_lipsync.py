import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

class LipSyncEngine:
    """
    Computes timestamped visemes (mouth shapes) for 3D facial rigging and blendshapes.
    Supports 9 standard visemes: A, B, C, D, E, F, G, H, X (Rest).
    """

    # Viseme to ARKit/FACS Blendshape mapping weights
    VISEME_TO_BLENDSHAPES = {
        "A": {"jawOpen": 0.05, "mouthClose": 0.80, "mouthPucker": 0.00, "mouthFunnel": 0.00},
        "B": {"jawOpen": 0.25, "mouthSmileLeft": 0.35, "mouthSmileRight": 0.35, "mouthClose": 0.00},
        "C": {"jawOpen": 0.50, "mouthFunnel": 0.20, "mouthClose": 0.00},
        "D": {"jawOpen": 0.85, "mouthFunnel": 0.10, "mouthClose": 0.00},
        "E": {"jawOpen": 0.45, "mouthFunnel": 0.65, "mouthPucker": 0.30},
        "F": {"jawOpen": 0.20, "mouthPucker": 0.85, "mouthFunnel": 0.40},
        "G": {"jawOpen": 0.15, "mouthLowerDownLeft": 0.40, "mouthLowerDownRight": 0.40},
        "H": {"jawOpen": 0.35, "mouthFunnel": 0.15},
        "X": {"jawOpen": 0.00, "mouthClose": 0.00, "mouthPucker": 0.00, "mouthFunnel": 0.00}
    }

    # Simplified English grapheme/phoneme to viseme mapping
    PHONEME_MAP = {
        r'[bmp]': "A",
        r'[iyeéè]': "B",
        r'[eɛ]': "C",
        r'[aɑæ]': "D",
        r'[oɔ]': "E",
        r'[uʊw]': "F",
        r'[fv]': "G",
        r'[l]': "H",
        r'[\s\.\,\!\?]': "X"
    }

    @classmethod
    def generate_visemes_from_text_and_duration(
        cls,
        text: str,
        total_duration_seconds: float,
        output_json_path: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generates timed viseme keyframes across dialogue duration.
        Returns a list of {start: float, end: float, viseme: str, blendshapes: dict}.
        """
        words = text.strip().split()
        if not words or total_duration_seconds <= 0:
            return [{"start": 0.0, "end": max(total_duration_seconds, 0.5), "viseme": "X", "blendshapes": cls.VISEME_TO_BLENDSHAPES["X"]}]

        # Allocate timing per word with realistic pauses
        seconds_per_word = total_duration_seconds / len(words)
        visemes = []
        current_time = 0.0

        for word in words:
            # Clean word
            clean_word = re.sub(r'[^a-zA-Z]', '', word).lower()
            if not clean_word:
                continue

            sub_duration = (seconds_per_word * 0.85) / max(len(clean_word), 1)
            
            for char in clean_word:
                # Map character to viseme
                v = "B"  # default
                if char in "bmp":
                    v = "A"
                elif char in "ae":
                    v = "C"
                elif char in "ai":
                    v = "D"
                elif char in "o":
                    v = "E"
                elif char in "uwq":
                    v = "F"
                elif char in "fv":
                    v = "G"
                elif char in "l":
                    v = "H"
                elif char in "cdgjknrstxyz":
                    v = "B"

                start = round(current_time, 3)
                end = round(current_time + sub_duration, 3)
                visemes.append({
                    "start": start,
                    "end": end,
                    "viseme": v,
                    "blendshapes": cls.VISEME_TO_BLENDSHAPES.get(v, cls.VISEME_TO_BLENDSHAPES["X"])
                })
                current_time += sub_duration

            # Add short inter-word rest
            rest_duration = seconds_per_word * 0.15
            visemes.append({
                "start": round(current_time, 3),
                "end": round(current_time + rest_duration, 3),
                "viseme": "X",
                "blendshapes": cls.VISEME_TO_BLENDSHAPES["X"]
            })
            current_time += rest_duration

        # Ensure final timestamp reaches total_duration
        if current_time < total_duration_seconds:
            visemes.append({
                "start": round(current_time, 3),
                "end": round(total_duration_seconds, 3),
                "viseme": "X",
                "blendshapes": cls.VISEME_TO_BLENDSHAPES["X"]
            })

        if output_json_path:
            with open(output_json_path, 'w', encoding='utf-8') as f:
                json.dump(visemes, f, indent=2)

        return visemes
