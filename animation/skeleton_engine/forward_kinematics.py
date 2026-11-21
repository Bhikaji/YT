import math
from typing import Dict, Tuple
from animation.character_engine.character_model import StickFigureCharacter
from animation.skeleton_engine.stick_skeleton import StickSkeletonPose

class ForwardKinematicsSolver:
    """
    Computes exact 2D world coordinates for every joint in the stick figure skeleton.
    Prevents disconnected limbs and preserves anatomical constraints.
    """

    @staticmethod
    def _deg_to_rad(deg: float) -> float:
        return deg * (math.pi / 180.0)

    @classmethod
    def solve_joint_positions(
        cls,
        character: StickFigureCharacter,
        pose: StickSkeletonPose
    ) -> Dict[str, Tuple[float, float]]:
        """Calculates (x, y) world coordinates for all 14 body joints."""
        # Pelvis / Root
        px, py = pose.root_x, pose.root_y

        # Torso extends upward from pelvis at body_tilt angle
        torso_angle_rad = cls._deg_to_rad(pose.body_tilt - 90.0)  # -90 is straight up
        neck_x = px + character.torso_length * math.cos(torso_angle_rad)
        neck_y = py + character.torso_length * math.sin(torso_angle_rad)

        # Head center
        head_angle_rad = cls._deg_to_rad(pose.body_tilt + pose.head_tilt - 90.0)
        head_x = neck_x + (character.head_radius + 10) * math.cos(head_angle_rad)
        head_y = neck_y + (character.head_radius + 10) * math.sin(head_angle_rad)

        # Shoulders (offset slightly left & right of neck)
        shoulder_span = 18.0
        sh_perp_angle = torso_angle_rad + (math.pi / 2.0)
        left_sh_x = neck_x - shoulder_span * math.cos(sh_perp_angle)
        left_sh_y = neck_y - shoulder_span * math.sin(sh_perp_angle)
        right_sh_x = neck_x + shoulder_span * math.cos(sh_perp_angle)
        right_sh_y = neck_y + shoulder_span * math.sin(sh_perp_angle)

        # Left Arm (Upper arm + Forearm)
        l_arm1_rad = cls._deg_to_rad(90.0 + pose.left_shoulder + pose.body_tilt)
        left_elbow_x = left_sh_x + character.upper_arm_length * math.cos(l_arm1_rad)
        left_elbow_y = left_sh_y + character.upper_arm_length * math.sin(l_arm1_rad)

        l_arm2_rad = l_arm1_rad + cls._deg_to_rad(pose.left_elbow)
        left_hand_x = left_elbow_x + character.forearm_length * math.cos(l_arm2_rad)
        left_hand_y = left_elbow_y + character.forearm_length * math.sin(l_arm2_rad)

        # Right Arm (Upper arm + Forearm)
        r_arm1_rad = cls._deg_to_rad(90.0 + pose.right_shoulder + pose.body_tilt)
        right_elbow_x = right_sh_x + character.upper_arm_length * math.cos(r_arm1_rad)
        right_elbow_y = right_sh_y + character.upper_arm_length * math.sin(r_arm1_rad)

        r_arm2_rad = r_arm1_rad + cls._deg_to_rad(pose.right_elbow)
        right_hand_x = right_elbow_x + character.forearm_length * math.cos(r_arm2_rad)
        right_hand_y = right_elbow_y + character.forearm_length * math.sin(r_arm2_rad)

        # Hips (offset slightly left & right of pelvis)
        hip_span = 14.0
        left_hip_x = px - hip_span
        left_hip_y = py
        right_hip_x = px + hip_span
        right_hip_y = py

        # Left Leg (Thigh + Calf)
        l_leg1_rad = cls._deg_to_rad(90.0 + pose.left_hip)
        left_knee_x = left_hip_x + character.thigh_length * math.cos(l_leg1_rad)
        left_knee_y = left_hip_y + character.thigh_length * math.sin(l_leg1_rad)

        l_leg2_rad = l_leg1_rad + cls._deg_to_rad(pose.left_knee)
        left_foot_x = left_knee_x + character.calf_length * math.cos(l_leg2_rad)
        left_foot_y = left_knee_y + character.calf_length * math.sin(l_leg2_rad)

        # Right Leg (Thigh + Calf)
        r_leg1_rad = cls._deg_to_rad(90.0 + pose.right_hip)
        right_knee_x = right_hip_x + character.thigh_length * math.cos(r_leg1_rad)
        right_knee_y = right_hip_y + character.thigh_length * math.sin(r_leg1_rad)

        r_leg2_rad = r_leg1_rad + cls._deg_to_rad(pose.right_knee)
        right_foot_x = right_knee_x + character.calf_length * math.cos(r_leg2_rad)
        right_foot_y = right_knee_y + character.calf_length * math.sin(r_leg2_rad)

        return {
            "pelvis": (px, py),
            "neck": (neck_x, neck_y),
            "head": (head_x, head_y),
            "left_shoulder": (left_sh_x, left_sh_y),
            "left_elbow": (left_elbow_x, left_elbow_y),
            "left_hand": (left_hand_x, left_hand_y),
            "right_shoulder": (right_sh_x, right_sh_y),
            "right_elbow": (right_elbow_x, right_elbow_y),
            "right_hand": (right_hand_x, right_hand_y),
            "left_hip": (left_hip_x, left_hip_y),
            "left_knee": (left_knee_x, left_knee_y),
            "left_foot": (left_foot_x, left_foot_y),
            "right_hip": (right_hip_x, right_hip_y),
            "right_knee": (right_knee_x, right_knee_y),
            "right_foot": (right_foot_x, right_foot_y)
        }
