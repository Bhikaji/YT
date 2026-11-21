import math
from typing import Dict, Tuple, Any

class StickSkeletonPose:
    """
    Skeletal joint angles and root coordinates for a single frame.
    All angles are in degrees:
    - 0 deg points straight downward along the body axis.
    - Positive angles rotate counter-clockwise, negative rotate clockwise.
    """

    def __init__(
        self,
        root_x: float = 540.0,
        root_y: float = 1250.0,
        body_tilt_deg: float = 0.0,
        head_tilt_deg: float = 0.0,
        left_shoulder_deg: float = 15.0,
        left_elbow_deg: float = 10.0,
        right_shoulder_deg: float = -15.0,
        right_elbow_deg: float = -10.0,
        left_hip_deg: float = 10.0,
        left_knee_deg: float = 5.0,
        right_hip_deg: float = -10.0,
        right_knee_deg: float = 5.0,
        left_hand_gesture: str = "open",
        right_hand_gesture: str = "open"
    ):
        self.root_x = root_x
        self.root_y = root_y
        self.body_tilt = body_tilt_deg
        self.head_tilt = head_tilt_deg
        self.left_shoulder = left_shoulder_deg
        self.left_elbow = left_elbow_deg
        self.right_shoulder = right_shoulder_deg
        self.right_elbow = right_elbow_deg
        self.left_hip = left_hip_deg
        self.left_knee = left_knee_deg
        self.right_hip = right_hip_deg
        self.right_knee = right_knee_deg
        self.left_hand_gesture = left_hand_gesture
        self.right_hand_gesture = right_hand_gesture
