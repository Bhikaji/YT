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
            leg_swing = math.sin(phase) * 28.0 * facing_dir
            arm_swing = -math.sin(phase) * 32.0 * facing_dir
            bob = abs(math.sin(phase)) * 8.0

            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y - bob,
                body_tilt_deg=4.0 * facing_dir,
                head_tilt_deg=2.0 * facing_dir,
                left_shoulder_deg=arm_swing,
                left_elbow_deg=15.0,
                right_shoulder_deg=-arm_swing,
                right_elbow_deg=15.0,
                left_hip_deg=leg_swing,
                left_knee_deg=max(0.0, -leg_swing * 0.8),
                right_hip_deg=-leg_swing,
                right_knee_deg=max(0.0, leg_swing * 0.8)
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
                right_knee_deg=max(0.0, leg_swing * 1.2)
            )

        elif "jump" in act:
            # Jump cycle: 0.8 sec period
            cycle = (t_sec % 0.8) / 0.8
            if cycle < 0.2:
                # Crouch
                crouch = cycle / 0.2
                return StickSkeletonPose(
                    root_x=root_x,
                    root_y=root_y + 35.0 * crouch,
                    left_hip_deg=-25.0,
                    left_knee_deg=45.0,
                    right_hip_deg=-25.0,
                    right_knee_deg=45.0
                )
            else:
                # In air arc
                air_t = (cycle - 0.2) / 0.8
                h = math.sin(air_t * math.pi) * 80.0
                return StickSkeletonPose(
                    root_x=root_x,
                    root_y=root_y - h,
                    left_shoulder_deg=-70.0,
                    right_shoulder_deg=-70.0,
                    left_hip_deg=15.0,
                    right_hip_deg=-15.0
                )

        elif "point" in act:
            # Extended pointing arm towards facing direction
            arm_angle = -95.0 * facing_dir
            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y,
                body_tilt_deg=2.0 * facing_dir,
                head_tilt_deg=3.0 * facing_dir,
                left_shoulder_deg=10.0,
                left_elbow_deg=15.0,
                right_shoulder_deg=arm_angle,
                right_elbow_deg=5.0,
                left_hip_deg=5.0,
                right_hip_deg=-5.0
            )

        elif "wave" in act:
            wave_phase = math.sin(t_sec * 6.0) * 25.0
            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y,
                left_shoulder_deg=10.0,
                left_elbow_deg=15.0,
                right_shoulder_deg=-140.0 * facing_dir,
                right_elbow_deg=30.0 + wave_phase,
                left_hip_deg=5.0,
                right_hip_deg=-5.0
            )

        elif "think" in act:
            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y,
                body_tilt_deg=-5.0 * facing_dir,
                head_tilt_deg=15.0 * facing_dir,
                left_shoulder_deg=15.0,
                left_elbow_deg=20.0,
                right_shoulder_deg=-120.0 * facing_dir,
                right_elbow_deg=110.0,  # Hand to chin
                left_hip_deg=-5.0,
                right_hip_deg=8.0
            )

        elif "slapstick_react" in act or "shock" in act:
            # Sudden dramatic backward arched torso, flailing arms
            tremble = math.sin(t_sec * 24.0) * 3.0
            return StickSkeletonPose(
                root_x=root_x + tremble,
                root_y=root_y + 10.0,
                body_tilt_deg=-22.0 * facing_dir,
                head_tilt_deg=-15.0 * facing_dir,
                left_shoulder_deg=-120.0 + tremble * 2,
                left_elbow_deg=30.0,
                right_shoulder_deg=-120.0 - tremble * 2,
                right_elbow_deg=30.0,
                left_hip_deg=-20.0,
                left_knee_deg=35.0,
                right_hip_deg=15.0,
                right_knee_deg=20.0
            )

        else:
            # Natural idle breathing
            breath = math.sin(t_sec * 2.0) * 2.5
            return StickSkeletonPose(
                root_x=root_x,
                root_y=root_y - breath,
                body_tilt_deg=0.0,
                head_tilt_deg=math.sin(t_sec * 1.5) * 1.5,
                left_shoulder_deg=12.0 + breath,
                left_elbow_deg=8.0,
                right_shoulder_deg=-12.0 - breath,
                right_elbow_deg=8.0,
                left_hip_deg=6.0,
                left_knee_deg=3.0,
                right_hip_deg=-6.0,
                right_knee_deg=3.0
            )
