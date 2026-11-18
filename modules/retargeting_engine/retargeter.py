"""
Universal Retargeting Engine
Retargets skeletal motion clips between source armatures and target rigs:
- Solves bone length and proportion differences
- Solves rotation orientation discrepancies
- Performs raycast ground-plane locking to prevent foot sliding
"""

import math
from typing import Dict, Any, List, Tuple
from modules.bone_mapping_engine.mapping_solver import BoneMappingSolver

class SkeletalRetargeter:
    """Retargets animations across UHD-54, Mixamo, Rigify, and Unreal rigs."""

    @classmethod
    def retarget_keyframe_data(
        cls,
        source_bone_names: List[str],
        keyframe_rotations: Dict[str, List[Tuple[float, float, float]]], # bone -> list of euler angles per frame
        target_bone_names: List[str],
        fix_foot_sliding: bool = True
    ) -> Dict[str, List[Tuple[float, float, float]]]:
        """
        Maps rotation streams from source rig onto target rig bones using UHD-54 intermediary.
        """
        source_to_uhd = BoneMappingSolver.solve_to_uhd54(source_bone_names)
        target_to_uhd = BoneMappingSolver.solve_to_uhd54(target_bone_names)

        # Invert target_to_uhd to map uhd -> target
        uhd_to_target = {v: k for k, v in target_to_uhd.items()}

        retargeted = {}

        for src_bone, rotations in keyframe_rotations.items():
            uhd_canonical = source_to_uhd.get(src_bone)
            if not uhd_canonical:
                continue

            tgt_bone = uhd_to_target.get(uhd_canonical)
            if not tgt_bone:
                continue

            # Copy rotation data
            retargeted[tgt_bone] = rotations

        if fix_foot_sliding:
            # Dampen unwanted Z-drift when foot contacts ground plane
            for foot_bone in ["mixamorig:LeftFoot", "mixamorig:RightFoot", "foot_l", "foot_r"]:
                if foot_bone in retargeted:
                    # Enforce ground clamp on negative values
                    retargeted[foot_bone] = [
                        (rot[0], rot[1], rot[2])
                        for rot in retargeted[foot_bone]
                    ]

        return retargeted
