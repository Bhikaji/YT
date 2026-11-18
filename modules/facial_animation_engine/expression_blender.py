"""
Facial Expression Blender & Eye Motion Engine
Generates expressive ARKit 52 emotion blendshapes, organic blinks, and micro-saccades.
"""

from typing import Dict, Any, List
import math
import random

class FacialExpressionBlender:
    """Blends emotional FACS blendshapes, blinks, and eye-darts for Pixar-level character performance."""

    EMOTION_PRESETS = {
        "AWE_WONDER": {
            "eyeWideLeft": 0.65, "eyeWideRight": 0.65,
            "browInnerUp": 0.70, "browOuterUpLeft": 0.40, "browOuterUpRight": 0.40,
            "jawOpen": 0.20, "mouthFunnel": 0.15
        },
        "DETERMINED_INTENSE": {
            "browDownLeft": 0.75, "browDownRight": 0.75,
            "eyeSquintLeft": 0.45, "eyeSquintRight": 0.45,
            "mouthFrownLeft": 0.20, "mouthFrownRight": 0.20
        },
        "JOY_LAUGH": {
            "mouthSmileLeft": 0.85, "mouthSmileRight": 0.85,
            "cheekPuff": 0.40, "eyeSquintLeft": 0.50, "eyeSquintRight": 0.50,
            "browInnerUp": 0.30
        },
        "SUSPICIOUS_CURIOUS": {
            "browOuterUpLeft": 0.80, "browDownRight": 0.50,
            "eyeWideLeft": 0.30, "eyeSquintRight": 0.40,
            "mouthSmileLeft": 0.20
        },
        "NEUTRAL": {
            "browInnerUp": 0.05, "mouthSmileLeft": 0.05, "mouthSmileRight": 0.05
        }
    }

    @classmethod
    def generate_expression_track(cls, emotion: str, total_frames: int, fps: int = 30) -> List[Dict[str, Any]]:
        """
        Creates smooth keyframes with natural organic micro-movements, breathing brow twitches, and periodic blinks.
        """
        preset = cls.EMOTION_PRESETS.get(emotion.upper(), cls.EMOTION_PRESETS["NEUTRAL"])
        frames = []

        blink_interval = int(fps * 3.2)  # Blink roughly every 3.2 seconds
        blink_duration = int(fps * 0.15) # 150ms blink

        for f in range(1, total_frames + 1):
            frame_data = dict(preset)
            
            # Subtle micro-movement
            micro_twitch = math.sin(f * 0.12) * 0.03
            for k in frame_data:
                frame_data[k] = max(0.0, min(1.0, frame_data[k] + micro_twitch))

            # Blink calculation
            f_in_cycle = f % blink_interval
            if f_in_cycle < blink_duration:
                blink_phase = f_in_cycle / blink_duration * math.pi
                blink_weight = math.sin(blink_phase)
                frame_data["eyeBlinkLeft"] = blink_weight
                frame_data["eyeBlinkRight"] = blink_weight
            else:
                frame_data["eyeBlinkLeft"] = 0.0
                frame_data["eyeBlinkRight"] = 0.0

            # Eye micro-saccades (subtle gaze shifts)
            frame_data["eyeLookInLeft"] = math.sin(f * 0.08) * 0.08
            frame_data["eyeLookOutRight"] = math.sin(f * 0.08) * 0.08

            frames.append({"frame": f, "shapekeys": frame_data})

        return frames
