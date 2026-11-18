"""
Autonomous AI Cartoon Studio - Universal Humanoid Definition (UHD-54) Standard
Canonical bone hierarchy and standardized role mappings for cross-platform rigging.
"""

# Canonical 54-bone definition
UHD_54_CANONICAL_BONES = [
    # Core Root & Spine
    "Root", "Pelvis", "Spine01", "Spine02", "Spine03", "Neck", "Head", "EyeLeft", "EyeRight", "Jaw",
    # Left Arm
    "ClavicleLeft", "ShoulderLeft", "ArmLeft", "ForearmLeft", "HandLeft",
    "Thumb1Left", "Thumb2Left", "Thumb3Left",
    "Index1Left", "Index2Left", "Index3Left",
    "Middle1Left", "Middle2Left", "Middle3Left",
    "Ring1Left", "Ring2Left", "Ring3Left",
    "Pinky1Left", "Pinky2Left", "Pinky3Left",
    # Right Arm
    "ClavicleRight", "ShoulderRight", "ArmRight", "ForearmRight", "HandRight",
    "Thumb1Right", "Thumb2Right", "Thumb3Right",
    "Index1Right", "Index2Right", "Index3Right",
    "Middle1Right", "Middle2Right", "Middle3Right",
    "Ring1Right", "Ring2Right", "Ring3Right",
    "Pinky1Right", "Pinky2Right", "Pinky3Right",
    # Left Leg
    "UpLegLeft", "LegLeft", "FootLeft", "ToeBaseLeft",
    # Right Leg
    "UpLegRight", "LegRight", "FootRight", "ToeBaseRight"
]

# Standard Mixamo mapping adapter
MIXAMO_TO_UHD54 = {
    "mixamorig:Hips": "Pelvis",
    "mixamorig:Spine": "Spine01",
    "mixamorig:Spine1": "Spine02",
    "mixamorig:Spine2": "Spine03",
    "mixamorig:Neck": "Neck",
    "mixamorig:Head": "Head",
    "mixamorig:LeftShoulder": "ClavicleLeft",
    "mixamorig:LeftArm": "ArmLeft",
    "mixamorig:LeftForeArm": "ForearmLeft",
    "mixamorig:LeftHand": "HandLeft",
    "mixamorig:LeftHandIndex1": "Index1Left",
    "mixamorig:LeftHandIndex2": "Index2Left",
    "mixamorig:LeftHandIndex3": "Index3Left",
    "mixamorig:LeftHandMiddle1": "Middle1Left",
    "mixamorig:LeftHandMiddle2": "Middle2Left",
    "mixamorig:LeftHandMiddle3": "Middle3Left",
    "mixamorig:LeftHandRing1": "Ring1Left",
    "mixamorig:LeftHandRing2": "Ring2Left",
    "mixamorig:LeftHandRing3": "Ring3Left",
    "mixamorig:LeftHandPinky1": "Pinky1Left",
    "mixamorig:LeftHandPinky2": "Pinky2Left",
    "mixamorig:LeftHandPinky3": "Pinky3Left",
    "mixamorig:LeftHandThumb1": "Thumb1Left",
    "mixamorig:LeftHandThumb2": "Thumb2Left",
    "mixamorig:LeftHandThumb3": "Thumb3Left",
    "mixamorig:RightShoulder": "ClavicleRight",
    "mixamorig:RightArm": "ArmRight",
    "mixamorig:RightForeArm": "ForearmRight",
    "mixamorig:RightHand": "HandRight",
    "mixamorig:RightHandIndex1": "Index1Right",
    "mixamorig:RightHandIndex2": "Index2Right",
    "mixamorig:RightHandIndex3": "Index3Right",
    "mixamorig:RightHandMiddle1": "Middle1Right",
    "mixamorig:RightHandMiddle2": "Middle2Right",
    "mixamorig:RightHandMiddle3": "Middle3Right",
    "mixamorig:RightHandRing1": "Ring1Right",
    "mixamorig:RightHandRing2": "Ring2Right",
    "mixamorig:RightHandRing3": "Ring3Right",
    "mixamorig:RightHandPinky1": "Pinky1Right",
    "mixamorig:RightHandPinky2": "Pinky2Right",
    "mixamorig:RightHandPinky3": "Pinky3Right",
    "mixamorig:RightHandThumb1": "Thumb1Right",
    "mixamorig:RightHandThumb2": "Thumb2Right",
    "mixamorig:RightHandThumb3": "Thumb3Right",
    "mixamorig:LeftUpLeg": "UpLegLeft",
    "mixamorig:LeftLeg": "LegLeft",
    "mixamorig:LeftFoot": "FootLeft",
    "mixamorig:LeftToeBase": "ToeBaseLeft",
    "mixamorig:RightUpLeg": "UpLegRight",
    "mixamorig:RightLeg": "LegRight",
    "mixamorig:RightFoot": "FootRight",
    "mixamorig:RightToeBase": "ToeBaseRight"
}
