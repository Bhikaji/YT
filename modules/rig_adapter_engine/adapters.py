"""
Rig Adapter Engine
Handles rest pose normalizations, T-Pose to A-Pose adjustments,
and axis coordinate conversions (Blender Z-Up to Maya/Unity Y-Up, Unreal Left-Handed).
"""

import math
from typing import Dict, Any, Tuple, List

class RigAdapter:
    """Adapts disparate 3D rest poses and rotational axes to Blender standard."""

    @staticmethod
    def tpose_to_apose_angles() -> Dict[str, Tuple[float, float, float]]:
        """Returns standard bone angular offsets to convert a strict T-Pose into an ergonomic A-Pose."""
        return {
            "upperarm_l": (0.0, 0.0, math.radians(-45.0)),
            "upperarm_r": (0.0, 0.0, math.radians(45.0)),
            "lowerarm_l": (0.0, 0.0, math.radians(-10.0)),
            "lowerarm_r": (0.0, 0.0, math.radians(10.0)),
            "thigh_l": (0.0, 0.0, math.radians(6.0)),
            "thigh_r": (0.0, 0.0, math.radians(-6.0)),
        }

    @staticmethod
    def maya_to_blender_rotation_matrix() -> List[List[float]]:
        """Rotates Maya FBX coordinates (-90 deg around X-axis) to align with Blender's Z-Up convention."""
        return [
            [1.0, 0.0, 0.0],
            [0.0, 0.0, -1.0],
            [0.0, 1.0, 0.0]
        ]

    @staticmethod
    def unity_to_blender_coords(x: float, y: float, z: float) -> Tuple[float, float, float]:
        """Converts Unity Y-Up left-handed coordinates to Blender Z-Up right-handed coordinates."""
        return (x, z, y)

    @staticmethod
    def unreal_to_blender_coords(x: float, y: float, z: float) -> Tuple[float, float, float]:
        """Converts Unreal centimeters Z-Up to Blender meters Z-Up."""
        return (x / 100.0, y / 100.0, z / 100.0)
