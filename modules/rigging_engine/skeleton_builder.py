"""
Blender Rigging Engine - Skeleton Generator & Constraint Setup
Supports humanoid bipedal armatures and quadruped companion rigs.
"""

from typing import Dict, Any, List

class SkeletonBuilder:
    """Generates Blender bpy code to assemble standardized humanoid and creature rigs."""

    # Standard bipedal bone mapping matching Rigify and Mixamo standards
    BIPED_BONES = [
        "root", "hips", "spine", "spine.001", "spine.002", "neck", "head",
        # Left Leg
        "thigh.L", "shin.L", "foot.L", "toe.L",
        # Right Leg
        "thigh.R", "shin.R", "foot.R", "toe.R",
        # Left Arm
        "shoulder.L", "upper_arm.L", "forearm.L", "hand.L",
        # Right Arm
        "shoulder.R", "upper_arm.R", "forearm.R", "hand.R"
    ]

    @classmethod
    def generate_armature_script(cls, armature_name: str = "CharacterRig", is_quadruped: bool = False) -> str:
        """
        Generates headless Blender bpy code to build the armature with proper bone hierarchy and roll angles.
        """
        if is_quadruped:
            # Quadruped companion rig for Lumi (Fox)
            return f'''
def create_quadruped_rig_{armature_name}():
    import bpy
    arm_data = bpy.data.armatures.new(name="{armature_name}_data")
    arm_obj = bpy.data.objects.new(name="{armature_name}", object_data=arm_data)
    bpy.context.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='EDIT')

    # Spine & Tail
    root = arm_data.edit_bones.new("root")
    root.head = (0, 0, 0)
    root.tail = (0, 0.1, 0)

    hips = arm_data.edit_bones.new("hips")
    hips.parent = root
    hips.head = (0, -0.2, 0.35)
    hips.tail = (0, 0, 0.35)

    spine = arm_data.edit_bones.new("spine")
    spine.parent = hips
    spine.head = (0, 0, 0.35)
    spine.tail = (0, 0.2, 0.38)

    neck = arm_data.edit_bones.new("neck")
    neck.parent = spine
    neck.head = (0, 0.2, 0.38)
    neck.tail = (0, 0.3, 0.45)

    head = arm_data.edit_bones.new("head")
    head.parent = neck
    head.head = (0, 0.3, 0.45)
    head.tail = (0, 0.35, 0.50)

    tail_01 = arm_data.edit_bones.new("tail.001")
    tail_01.parent = hips
    tail_01.head = (0, -0.2, 0.35)
    tail_01.tail = (0, -0.4, 0.40)

    tail_02 = arm_data.edit_bones.new("tail.002")
    tail_02.parent = tail_01
    tail_02.head = (0, -0.4, 0.40)
    tail_02.tail = (0, -0.6, 0.30)

    bpy.ops.object.mode_set(mode='OBJECT')
    return arm_obj
'''
        else:
            # Humanoid rig for Leo, Aria, Milo
            return f'''
def create_humanoid_rig_{armature_name}():
    import bpy
    arm_data = bpy.data.armatures.new(name="{armature_name}_data")
    arm_obj = bpy.data.objects.new(name="{armature_name}", object_data=arm_data)
    bpy.context.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='EDIT')

    # Root & Pelvis
    root = arm_data.edit_bones.new("root")
    root.head = (0, 0, 0)
    root.tail = (0, 0, 0.1)

    hips = arm_data.edit_bones.new("hips")
    hips.parent = root
    hips.head = (0, 0, 0.70)
    hips.tail = (0, 0, 0.85)

    spine = arm_data.edit_bones.new("spine")
    spine.parent = hips
    spine.head = (0, 0, 0.85)
    spine.tail = (0, 0, 1.05)

    neck = arm_data.edit_bones.new("neck")
    neck.parent = spine
    neck.head = (0, 0, 1.05)
    neck.tail = (0, 0, 1.15)

    head = arm_data.edit_bones.new("head")
    head.parent = neck
    head.head = (0, 0, 1.15)
    head.tail = (0, 0, 1.35)

    # Left Leg
    thigh_l = arm_data.edit_bones.new("thigh.L")
    thigh_l.parent = hips
    thigh_l.head = (0.12, 0, 0.70)
    thigh_l.tail = (0.12, 0, 0.38)

    shin_l = arm_data.edit_bones.new("shin.L")
    shin_l.parent = thigh_l
    shin_l.head = (0.12, 0, 0.38)
    shin_l.tail = (0.12, 0, 0.08)

    foot_l = arm_data.edit_bones.new("foot.L")
    foot_l.parent = shin_l
    foot_l.head = (0.12, 0, 0.08)
    foot_l.tail = (0.12, 0.15, 0.0)

    # Right Leg
    thigh_r = arm_data.edit_bones.new("thigh.R")
    thigh_r.parent = hips
    thigh_r.head = (-0.12, 0, 0.70)
    thigh_r.tail = (-0.12, 0, 0.38)

    shin_r = arm_data.edit_bones.new("shin.R")
    shin_r.parent = thigh_r
    shin_r.head = (-0.12, 0, 0.38)
    shin_r.tail = (-0.12, 0, 0.08)

    foot_r = arm_data.edit_bones.new("foot.R")
    foot_r.parent = shin_r
    foot_r.head = (-0.12, 0, 0.08)
    foot_r.tail = (-0.12, 0.15, 0.0)

    # Left Arm
    shoulder_l = arm_data.edit_bones.new("shoulder.L")
    shoulder_l.parent = spine
    shoulder_l.head = (0.05, 0, 1.02)
    shoulder_l.tail = (0.18, 0, 1.02)

    upper_arm_l = arm_data.edit_bones.new("upper_arm.L")
    upper_arm_l.parent = shoulder_l
    upper_arm_l.head = (0.18, 0, 1.02)
    upper_arm_l.tail = (0.38, 0, 0.80)

    forearm_l = arm_data.edit_bones.new("forearm.L")
    forearm_l.parent = upper_arm_l
    forearm_l.head = (0.38, 0, 0.80)
    forearm_l.tail = (0.55, 0, 0.62)

    hand_l = arm_data.edit_bones.new("hand.L")
    hand_l.parent = forearm_l
    hand_l.head = (0.55, 0, 0.62)
    hand_l.tail = (0.62, 0, 0.58)

    # Right Arm
    shoulder_r = arm_data.edit_bones.new("shoulder.R")
    shoulder_r.parent = spine
    shoulder_r.head = (-0.05, 0, 1.02)
    shoulder_r.tail = (-0.18, 0, 1.02)

    upper_arm_r = arm_data.edit_bones.new("upper_arm.R")
    upper_arm_r.parent = shoulder_r
    upper_arm_r.head = (-0.18, 0, 1.02)
    upper_arm_r.tail = (-0.38, 0, 0.80)

    forearm_r = arm_data.edit_bones.new("forearm.R")
    forearm_r.parent = upper_arm_r
    forearm_r.head = (-0.38, 0, 0.80)
    forearm_r.tail = (-0.55, 0, 0.62)

    hand_r = arm_data.edit_bones.new("hand.R")
    hand_r.parent = forearm_r
    hand_r.head = (-0.55, 0, 0.62)
    hand_r.tail = (-0.62, 0, 0.58)

    bpy.ops.object.mode_set(mode='OBJECT')
    return arm_obj
'''
