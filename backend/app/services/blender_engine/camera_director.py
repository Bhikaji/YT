from typing import Tuple, Dict, Any

class CameraDirector:
    """Calculates cinematic 3D camera coordinates, focal lengths, and tracking constraints."""

    @staticmethod
    def get_shot_config(
        shot_type: str,
        target_pos: Tuple[float, float, float] = (0.0, 0.0, 1.4)
    ) -> Dict[str, Any]:
        tx, ty, tz = target_pos

        if shot_type == "ESTABLISHING":
            return {
                "camera_pos": (tx, ty - 5.5, tz + 0.8),
                "target_pos": target_pos,
                "focal_length": 28.0,
                "dof_distance": 5.5,
                "fstop": 5.6
            }
        elif shot_type == "MEDIUM_TWO_SHOT":
            return {
                "camera_pos": (tx + 0.5, ty - 3.2, tz + 0.2),
                "target_pos": target_pos,
                "focal_length": 45.0,
                "dof_distance": 3.2,
                "fstop": 3.5
            }
        elif shot_type == "OVER_SHOULDER":
            return {
                "camera_pos": (tx + 0.6, ty - 1.4, tz + 0.3),
                "target_pos": (tx - 0.2, ty + 1.2, tz + 0.1),
                "focal_length": 50.0,
                "dof_distance": 2.2,
                "fstop": 2.8
            }
        elif shot_type == "CLOSE_UP":
            return {
                "camera_pos": (tx, ty - 1.8, tz + 0.05),
                "target_pos": target_pos,
                "focal_length": 70.0,
                "dof_distance": 1.8,
                "fstop": 2.0
            }
        elif shot_type == "EXTREME_CLOSE_UP":
            return {
                "camera_pos": (tx, ty - 1.1, tz + 0.08),
                "target_pos": target_pos,
                "focal_length": 85.0,
                "dof_distance": 1.1,
                "fstop": 1.8
            }
        else:  # default tracking
            return {
                "camera_pos": (tx, ty - 3.5, tz + 0.4),
                "target_pos": target_pos,
                "focal_length": 35.0,
                "dof_distance": 3.5,
                "fstop": 4.0
            }

class LightingManager:
    """Generates procedural 3-point cinematic lighting setups."""

    @staticmethod
    def get_preset_lighting(preset_name: str) -> Dict[str, Any]:
        if preset_name == "dramatic_sunset":
            return {
                "key_light": {"color": (1.0, 0.55, 0.2), "energy": 1200, "pos": (3.0, -3.0, 4.0)},
                "fill_light": {"color": (0.3, 0.4, 0.8), "energy": 400, "pos": (-3.0, -2.0, 2.5)},
                "rim_light": {"color": (1.0, 0.8, 0.5), "energy": 1600, "pos": (0.0, 4.0, 3.5)},
                "ambient_world": (0.05, 0.03, 0.08)
            }
        elif preset_name == "mysterious_cyan_glow":
            return {
                "key_light": {"color": (0.1, 0.8, 0.9), "energy": 1000, "pos": (-2.5, -2.5, 3.0)},
                "fill_light": {"color": (0.05, 0.1, 0.3), "energy": 250, "pos": (3.0, -1.5, 2.0)},
                "rim_light": {"color": (0.2, 1.0, 0.8), "energy": 1400, "pos": (0.5, 3.5, 3.0)},
                "ambient_world": (0.01, 0.03, 0.05)
            }
        elif preset_name == "dramatic_pulsing_red":
            return {
                "key_light": {"color": (1.0, 0.1, 0.1), "energy": 1500, "pos": (2.0, -2.5, 2.0)},
                "fill_light": {"color": (0.2, 0.0, 0.0), "energy": 300, "pos": (-2.0, -2.0, 1.5)},
                "rim_light": {"color": (1.0, 0.4, 0.1), "energy": 1800, "pos": (0.0, 3.0, 4.0)},
                "ambient_world": (0.03, 0.01, 0.01)
            }
        else:  # daylight default
            return {
                "key_light": {"color": (1.0, 0.95, 0.85), "energy": 1000, "pos": (3.0, -4.0, 5.0)},
                "fill_light": {"color": (0.6, 0.7, 0.9), "energy": 450, "pos": (-3.5, -3.0, 3.0)},
                "rim_light": {"color": (1.0, 1.0, 1.0), "energy": 1200, "pos": (1.0, 4.0, 4.0)},
                "ambient_world": (0.15, 0.18, 0.22)
            }
