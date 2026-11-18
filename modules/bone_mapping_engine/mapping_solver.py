"""
Universal Skeleton Bone Mapping Solver
Maps external skeleton rigs (Mixamo, Rigify, Unity Humanoid, Unreal Engine 5 Mannequin, Maya HumanIK)
to the canonical UHD-54 standard bone hierarchy.
"""

from typing import Dict, Any, Optional, List
from modules.skeleton_profiles.uhd_standard import UHD_54_CANONICAL_BONES, MIXAMO_TO_UHD54

RIGIFY_TO_UHD54 = {
    "spine": "spine_01",
    "spine.001": "spine_02",
    "spine.002": "spine_03",
    "spine.003": "chest",
    "spine.004": "neck_01",
    "spine.006": "head",
    "shoulder.L": "clavicle_l",
    "shoulder.R": "clavicle_r",
    "upper_arm.L": "upperarm_l",
    "upper_arm.R": "upperarm_r",
    "forearm.L": "lowerarm_l",
    "forearm.R": "lowerarm_r",
    "hand.L": "hand_l",
    "hand.R": "hand_r",
    "thigh.L": "thigh_l",
    "thigh.R": "thigh_r",
    "shin.L": "calf_l",
    "shin.R": "calf_r",
    "foot.L": "foot_l",
    "foot.R": "foot_r",
    "toe.L": "toe_l",
    "toe.R": "toe_r",
}

UNITY_HUMANOID_TO_UHD54 = {
    "Hips": "pelvis",
    "Spine": "spine_01",
    "Chest": "spine_02",
    "UpperChest": "chest",
    "Neck": "neck_01",
    "Head": "head",
    "LeftShoulder": "clavicle_l",
    "RightShoulder": "clavicle_r",
    "LeftUpperArm": "upperarm_l",
    "RightUpperArm": "upperarm_r",
    "LeftLowerArm": "lowerarm_l",
    "RightLowerArm": "lowerarm_r",
    "LeftHand": "hand_l",
    "RightHand": "hand_r",
    "LeftUpperLeg": "thigh_l",
    "RightUpperLeg": "thigh_r",
    "LeftLowerLeg": "calf_l",
    "RightLowerLeg": "calf_r",
    "LeftFoot": "foot_l",
    "RightFoot": "foot_r",
    "LeftToes": "toe_l",
    "RightToes": "toe_r",
}

UNREAL_TO_UHD54 = {
    "root": "root",
    "pelvis": "pelvis",
    "spine_01": "spine_01",
    "spine_02": "spine_02",
    "spine_03": "spine_03",
    "spine_04": "chest",
    "spine_05": "upper_chest",
    "neck_01": "neck_01",
    "neck_02": "neck_02",
    "head": "head",
    "clavicle_l": "clavicle_l",
    "clavicle_r": "clavicle_r",
    "upperarm_l": "upperarm_l",
    "upperarm_r": "upperarm_r",
    "lowerarm_l": "lowerarm_l",
    "lowerarm_r": "lowerarm_r",
    "hand_l": "hand_l",
    "hand_r": "hand_r",
    "thigh_l": "thigh_l",
    "thigh_r": "thigh_r",
    "calf_l": "calf_l",
    "calf_r": "calf_r",
    "foot_l": "foot_l",
    "foot_r": "foot_r",
    "ball_l": "toe_l",
    "ball_r": "toe_r",
}

class BoneMappingSolver:
    """Detects bone nomenclature format and solves bidirectional mapping to UHD-54 standard."""

    @classmethod
    def detect_rig_profile(cls, bone_names: List[str]) -> str:
        names_set = set(bone_names)
        if any("mixamorig" in b for b in names_set):
            return "MIXAMO"
        if any(b.startswith("spine.") or b.startswith("shoulder.") for b in names_set):
            return "RIGIFY"
        if "LeftUpperArm" in names_set or "RightUpperArm" in names_set:
            return "UNITY_HUMANOID"
        if "upperarm_l" in names_set and "calf_l" in names_set:
            return "UNREAL_MANNEQUIN"
        return "UNKNOWN"

    @classmethod
    def solve_to_uhd54(cls, bone_names: List[str]) -> Dict[str, str]:
        profile = cls.detect_rig_profile(bone_names)
        mapping = {}
        if profile == "MIXAMO":
            for b in bone_names:
                if b in MIXAMO_TO_UHD54:
                    mapping[b] = MIXAMO_TO_UHD54[b]
        elif profile == "RIGIFY":
            for b in bone_names:
                if b in RIGIFY_TO_UHD54:
                    mapping[b] = RIGIFY_TO_UHD54[b]
        elif profile == "UNITY_HUMANOID":
            for b in bone_names:
                if b in UNITY_HUMANOID_TO_UHD54:
                    mapping[b] = UNITY_HUMANOID_TO_UHD54[b]
        elif profile == "UNREAL_MANNEQUIN":
            for b in bone_names:
                if b in UNREAL_TO_UHD54:
                    mapping[b] = UNREAL_TO_UHD54[b]
        else:
            # Fuzzy heuristic matching
            for b in bone_names:
                cleaned = b.lower().replace("_", "").replace(".", "").replace("-", "")
                for uhd in UHD_54_CANONICAL_BONES:
                    uhd_clean = uhd.lower().replace("_", "")
                    if cleaned == uhd_clean:
                        mapping[b] = uhd
                        break
        return mapping
