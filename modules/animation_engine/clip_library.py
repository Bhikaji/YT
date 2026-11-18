"""
Animation Clip Library & Procedural Locomotion Generator
Provides programmatic keyframe curves for standard character actions and gestures.
"""

from typing import Dict, Any, List, Optional
import math

class AnimationClipLibrary:
    """Standardized action clips for humanoid and companion character animations."""

    @classmethod
    def get_supported_actions(cls) -> List[str]:
        return [
            "idle_breathing",
            "walk_cycle",
            "run_cycle",
            "jump",
            "fight_punch",
            "fight_dodge",
            "sit_down",
            "talking_questioning",
            "talking_excited",
            "looking_in_awe"
        ]

    @classmethod
    def generate_locomotion_keyframes(cls, action_name: str, total_frames: int, fps: int = 30) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generates sinusoidal bone transform curves for locomotion and gestures.
        Outputs frame-by-frame Euler rotations (pitch, roll, yaw) for key bones.
        """
        curves: Dict[str, List[Dict[str, Any]]] = {
            "hips": [],
            "spine": [],
            "thigh.L": [],
            "thigh.R": [],
            "shin.L": [],
            "shin.R": [],
            "arm.L": [],
            "arm.R": [],
            "head": []
        }

        cycle_duration_frames = int(fps * (0.8 if action_name == "run_cycle" else 1.2))

        for frame in range(1, total_frames + 1):
            phase = (frame % cycle_duration_frames) / cycle_duration_frames * (2 * math.pi)

            if action_name == "walk_cycle":
                # Pelvis bounce & roll
                hips_y = math.sin(2 * phase) * 0.03
                curves["hips"].append({"frame": frame, "loc_z": hips_y, "rot_z": math.sin(phase) * 0.05})
                # Legs alternating swing
                curves["thigh.L"].append({"frame": frame, "rot_x": math.sin(phase) * 0.55})
                curves["thigh.R"].append({"frame": frame, "rot_x": -math.sin(phase) * 0.55})
                curves["shin.L"].append({"frame": frame, "rot_x": max(0.0, -math.sin(phase) * 0.70)})
                curves["shin.R"].append({"frame": frame, "rot_x": max(0.0, math.sin(phase) * 0.70)})
                # Arms swinging counter to legs
                curves["arm.L"].append({"frame": frame, "rot_x": -math.sin(phase) * 0.45})
                curves["arm.R"].append({"frame": frame, "rot_x": math.sin(phase) * 0.45})
                curves["head"].append({"frame": frame, "rot_x": 0.0, "rot_y": 0.0})

            elif action_name == "run_cycle":
                # High energy bounce
                hips_y = math.sin(2 * phase) * 0.08
                curves["hips"].append({"frame": frame, "loc_z": hips_y, "rot_z": math.sin(phase) * 0.10})
                curves["thigh.L"].append({"frame": frame, "rot_x": math.sin(phase) * 0.95})
                curves["thigh.R"].append({"frame": frame, "rot_x": -math.sin(phase) * 0.95})
                curves["shin.L"].append({"frame": frame, "rot_x": max(0.0, -math.sin(phase) * 1.20)})
                curves["shin.R"].append({"frame": frame, "rot_x": max(0.0, math.sin(phase) * 1.20)})
                curves["arm.L"].append({"frame": frame, "rot_x": -math.sin(phase) * 0.85})
                curves["arm.R"].append({"frame": frame, "rot_x": math.sin(phase) * 0.85})
                curves["head"].append({"frame": frame, "rot_x": 0.05})

            elif action_name == "looking_in_awe":
                # Head tilts back, eyes and chest lift up
                tilt = min(1.0, frame / 30.0) * 0.35
                curves["head"].append({"frame": frame, "rot_x": -tilt, "rot_y": math.sin(frame * 0.05) * 0.03})
                curves["spine"].append({"frame": frame, "rot_x": -tilt * 0.3})
                curves["arm.L"].append({"frame": frame, "rot_x": 0.15, "rot_z": 0.10})
                curves["arm.R"].append({"frame": frame, "rot_x": 0.15, "rot_z": -0.10})

            else:  # idle_breathing default
                breath = math.sin(frame * 0.08) * 0.02
                curves["hips"].append({"frame": frame, "loc_z": breath * 0.5})
                curves["spine"].append({"frame": frame, "scale_x": 1.0 + breath, "scale_y": 1.0 + breath})
                curves["head"].append({"frame": frame, "rot_x": breath * 0.3})

        return curves
