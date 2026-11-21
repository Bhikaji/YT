import math
from animation.skeleton_engine.stick_skeleton import StickSkeletonPose

class MovementPresetEngine:
    """
    Parametric procedural movement generator for 2D stick figures.
    Produces continuous, organic keyframes with zero sudden snaps or broken joints.
    """

    @classmethod
    def get_pose_at_time(
        cls,
        action_name: str,
        t_sec: float,
        root_x: float = 540.0,
        root_y: float = 1250.0,
        facing_dir: int = 1  # 1 for right, -1 for left
    ) -> StickSkeletonPose:
        """Computes joint angles for the given action at timestamp t_sec."""
        act = action_name.lower()

        if "walk" in act:
            # Frequency: 1.8 steps per second
            freq = 1.8
            phase = t_sec * freq * 2.0 * math.pi
            leg_swing = math.sin(phase) * 32.0 * facing_dir
            arm_swing = -math.sin(phase) * 36.0 * facing_dir
            bob = abs(math.sin(phase)) * 8.0

            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y - bob,
                body_tilt_deg=5.0 * facing_dir,
                head_tilt_deg=2.0 * facing_dir,
                left_shoulder_deg=arm_swing,
                left_elbow_deg=18.0,
                right_shoulder_deg=-arm_swing,
                right_elbow_deg=18.0,
                left_hip_deg=leg_swing,
                left_knee_deg=max(0.0, -leg_swing * 0.9),
                right_hip_deg=-leg_swing,
                right_knee_deg=max(0.0, leg_swing * 0.9),
                left_hand_gesture="relaxed",
                right_hand_gesture="relaxed"
            )

        elif "run" in act:
            # Frequency: 3.0 steps per second
            freq = 3.0
            phase = t_sec * freq * 2.0 * math.pi
            leg_swing = math.sin(phase) * 45.0 * facing_dir
            arm_swing = -math.sin(phase) * 55.0 * facing_dir
            bob = abs(math.sin(phase)) * 16.0

            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y - bob,
                body_tilt_deg=14.0 * facing_dir,
                head_tilt_deg=5.0 * facing_dir,
                left_shoulder_deg=arm_swing,
                left_elbow_deg=40.0,
                right_shoulder_deg=-arm_swing,
                right_elbow_deg=40.0,
                left_hip_deg=leg_swing,
                left_knee_deg=max(0.0, -leg_swing * 1.2),
                right_hip_deg=-leg_swing,
                right_knee_deg=max(0.0, leg_swing * 1.2),
                left_hand_gesture="fist",
                right_hand_gesture="fist"
            )

        elif "scold" in act or "finger_wag" in act:
            # Mother / friend scolding: Hand on hip, sharp staccato index finger wagging
            wag = math.sin(t_sec * 12.0) * 18.0
            head_nod = math.sin(t_sec * 8.0) * 7.0
            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y,
                body_tilt_deg=8.0 * facing_dir,
                head_tilt_deg=(6.0 + head_nod) * facing_dir,
                left_shoulder_deg=-32.0 * facing_dir,
                left_elbow_deg=85.0,  # Hand on hip
                right_shoulder_deg=-96.0 * facing_dir,
                right_elbow_deg=18.0 + wag,
                left_hip_deg=6.0,
                left_knee_deg=4.0,
                right_hip_deg=-6.0,
                right_knee_deg=4.0,
                left_hand_gesture="fist",
                right_hand_gesture="pointing"
            )

        elif "explain" in act or "plead" in act or "shrug" in act:
            # Pleading / explaining: both open hands raised, shrugging shoulders
            shrug = math.sin(t_sec * 6.5) * 12.0
            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y,
                body_tilt_deg=-5.0 * facing_dir,
                head_tilt_deg=-6.0 * facing_dir,
                left_shoulder_deg=-65.0 * facing_dir + shrug * 0.4,
                left_elbow_deg=75.0 + shrug,
                right_shoulder_deg=-72.0 * facing_dir - shrug * 0.4,
                right_elbow_deg=75.0 + shrug,
                left_hip_deg=-4.0,
                left_knee_deg=6.0,
                right_hip_deg=6.0,
                right_knee_deg=6.0,
                left_hand_gesture="palms_up",
                right_hand_gesture="palms_up"
            )

        elif "laugh" in act:
            # Punchline belly laughter: rocking back and forth, slapping knees/belly
            laugh_phase = t_sec * 14.0
            rock = math.sin(laugh_phase) * 14.0
            bounce = abs(math.sin(laugh_phase)) * 9.0
            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y - bounce,
                body_tilt_deg=-10.0 + rock,
                head_tilt_deg=-15.0 + rock * 0.8,
                left_shoulder_deg=-45.0,
                left_elbow_deg=90.0 + math.sin(laugh_phase) * 15.0,
                right_shoulder_deg=-45.0,
                right_elbow_deg=90.0 - math.sin(laugh_phase) * 15.0,
                left_hip_deg=-6.0,
                left_knee_deg=8.0,
                right_hip_deg=6.0,
                right_knee_deg=8.0,
                left_hand_gesture="fist",
                right_hand_gesture="open_palm"
            )

        elif "slapstick_react" in act or "shock" in act:
            # Sudden dramatic backward arched torso, trembling hands on cheeks/head
            tremble = math.sin(t_sec * 26.0) * 3.5
            return StickSkeletonPose(
                root_x=root_x + tremble,
                root_y=root_y + 8.0,
                body_tilt_deg=-20.0 * facing_dir,
                head_tilt_deg=-14.0 * facing_dir,
                left_shoulder_deg=-130.0 + tremble * 2.0,
                left_elbow_deg=105.0,
                right_shoulder_deg=-130.0 - tremble * 2.0,
                right_elbow_deg=105.0,
                left_hip_deg=-20.0,
                left_knee_deg=35.0,
                right_hip_deg=15.0,
                right_knee_deg=20.0,
                left_hand_gesture="open_palm",
                right_hand_gesture="open_palm"
            )

        elif "point" in act or "talk" in act or "gestur" in act:
            # Dynamic vocal gesticulation: dominant hand pulses with speech syllables, other hand on hip
            cadence = t_sec * 6.5 * 2.0 * math.pi
            pulse = math.sin(cadence) * 14.0
            lean = math.sin(t_sec * 4.5) * 4.0
            nod = math.sin(t_sec * 6.0) * 7.0
            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y,
                body_tilt_deg=(4.0 + lean) * facing_dir,
                head_tilt_deg=(3.0 + nod) * facing_dir,
                left_shoulder_deg=-28.0 * facing_dir,
                left_elbow_deg=75.0,  # Resting hand on hip/side
                right_shoulder_deg=(-85.0 + pulse * 0.5) * facing_dir,
                right_elbow_deg=25.0 + pulse,
                left_hip_deg=5.0,
                left_knee_deg=3.0,
                right_hip_deg=-5.0,
                right_knee_deg=3.0,
                left_hand_gesture="fist",
                right_hand_gesture="pointing" if math.sin(cadence) > 0 else "open_palm"
            )

        elif "wave" in act:
            wave_phase = math.sin(t_sec * 7.5) * 26.0
            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y,
                body_tilt_deg=2.0 * facing_dir,
                head_tilt_deg=4.0 * facing_dir,
                left_shoulder_deg=-25.0 * facing_dir,
                left_elbow_deg=75.0,
                right_shoulder_deg=-145.0 * facing_dir,
                right_elbow_deg=25.0 + wave_phase,
                left_hip_deg=5.0,
                left_knee_deg=3.0,
                right_hip_deg=-5.0,
                right_knee_deg=3.0,
                left_hand_gesture="fist",
                right_hand_gesture="wave"
            )

        elif "think" in act:
            scratch = math.sin(t_sec * 9.0) * 12.0
            nod = math.sin(t_sec * 2.5) * 6.0
            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y,
                body_tilt_deg=-4.0 * facing_dir,
                head_tilt_deg=(12.0 + nod) * facing_dir,
                left_shoulder_deg=15.0,
                left_elbow_deg=20.0,
                right_shoulder_deg=-122.0 * facing_dir,
                right_elbow_deg=115.0 + scratch,  # Hand scratching chin/cheek
                left_hip_deg=-5.0,
                left_knee_deg=4.0,
                right_hip_deg=8.0,
                right_knee_deg=4.0,
                left_hand_gesture="relaxed",
                right_hand_gesture="pointing"
            )

        else:
            # Alive listener / idle breathing with subtle head tilt and weight shift
            breath = math.sin(t_sec * 2.2) * 2.5
            head_look = math.sin(t_sec * 1.8) * 4.0
            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y - breath,
                body_tilt_deg=math.sin(t_sec * 1.2) * 1.5 * facing_dir,
                head_tilt_deg=head_look * facing_dir,
                left_shoulder_deg=-20.0 * facing_dir + breath,
                left_elbow_deg=65.0,
                right_shoulder_deg=-20.0 * facing_dir - breath,
                right_elbow_deg=65.0,
                left_hip_deg=5.0,
                left_knee_deg=3.0,
                right_hip_deg=-5.0,
                right_knee_deg=3.0,
                left_hand_gesture="relaxed",
                right_hand_gesture="relaxed"
            )
