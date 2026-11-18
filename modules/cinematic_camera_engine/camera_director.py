"""
Cinematic Camera & Lighting Director
Configures Hollywood-grade shot composition, lens focal lengths,
depth of field (aperture), and 3-point lighting setups.
"""

from typing import Dict, Any, List, Tuple
import math

class CameraDirector:
    """Computes shot framing, camera movements, and lighting for 3D animation scenes."""

    SHOT_TYPES = {
        "ESTABLISHING": {
            "lens": 28.0,
            "fstop": 5.6,
            "distance": 6.5,
            "height": 2.2,
            "pitch_deg": 75.0,
            "description": "Wide panoramic view establishing environment and scope"
        },
        "MEDIUM_TRACKING": {
            "lens": 42.0,
            "fstop": 2.8,
            "distance": 3.4,
            "height": 1.25,
            "pitch_deg": 84.0,
            "description": "Waist-up framing tracking character movement and gestures"
        },
        "HERO_CLOSEUP": {
            "lens": 65.0,
            "fstop": 1.8,
            "distance": 1.35,
            "height": 1.22,
            "pitch_deg": 92.0,
            "description": "Intimate cinematic close-up with shallow DOF highlighting facial emotion and eyes"
        }
    }

    @classmethod
    def get_shot_parameters(cls, shot_type: str) -> Dict[str, Any]:
        return cls.SHOT_TYPES.get(shot_type.upper(), cls.SHOT_TYPES["MEDIUM_TRACKING"])

    @classmethod
    def get_three_point_lighting(cls, mood: str = "MYSTICAL_FANTASY") -> Dict[str, Any]:
        if mood == "MYSTICAL_FANTASY":
            return {
                "key_light": {
                    "type": "POINT",
                    "energy": 750,
                    "color": (1.0, 0.88, 0.74), # Warm golden
                    "location": (-1.2, -1.6, 2.2)
                },
                "fill_light": {
                    "type": "POINT",
                    "energy": 550,
                    "color": (0.2, 0.82, 1.0), # Bioluminescent cyan
                    "location": (1.5, 0.2, 1.0)
                },
                "rim_light": {
                    "type": "SUN",
                    "energy": 3.0,
                    "color": (1.0, 0.65, 0.35), # Warm rim edge
                    "rotation_euler": (math.radians(45), math.radians(25), math.radians(-115))
                }
            }
        else:
            return {
                "key_light": {"type": "POINT", "energy": 800, "color": (1.0, 1.0, 1.0), "location": (-1.5, -2.0, 2.5)},
                "fill_light": {"type": "POINT", "energy": 400, "color": (0.8, 0.8, 1.0), "location": (1.5, -1.0, 1.5)},
                "rim_light": {"type": "SUN", "energy": 2.5, "color": (1.0, 0.9, 0.8), "rotation_euler": (0.7, 0.4, -2.0)}
            }
