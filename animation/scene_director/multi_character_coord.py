from typing import Dict, Any, List, Tuple

class MultiCharacterCoordinator:
    """
    Coordinates interactions, mutual gaze, and turn-taking between multiple stick figures.
    Guarantees characters do not perform random conflicting actions simultaneously.
    """

    @classmethod
    def coordinate_roles(
        cls,
        char1_id: str,
        char2_id: str,
        t_sec: float,
        dialogues: List[Dict[str, Any]],
        scene_action_map: Dict[str, str],
        width: int = 1280,
        height: int = 720
    ) -> Dict[str, Dict[str, Any]]:
        """
        Determines gaze direction, primary action, and social reaction for both characters.
        Dynamically adapts positioning for both 16:9 widescreen and 9:16 vertical resolutions.
        """
        # Widescreen 16:9 (1280x720) or Vertical 9:16 (1080x1920)
        if height <= 800:
            target_c1_x = float(int(width * 0.36))
            c2_x = float(int(width * 0.74))
            root_y = float(int(height * 0.62))
        else:
            target_c1_x, c2_x = 380.0, 700.0
            root_y = 1380.0

        # Walking entrance in the opening seconds (if scene action is walk or t_sec < 2.2)
        if "walk" in str(scene_action_map.get(char1_id, "")).lower() and t_sec < 2.8:
            walk_prog = min(1.0, max(0.0, t_sec / 2.5))
            c1_x = float(int(width * 0.12 + (target_c1_x - width * 0.12) * walk_prog))
            c1_walking = True
        else:
            c1_x = target_c1_x
            c1_walking = False

        # Check who is speaking
        c1_speaking = False
        c2_speaking = False
        active_emotion = "curious"

        for d in dialogues:
            if d.get("start_second", 0.0) <= t_sec <= d.get("end_second", 0.0):
                if d.get("speaker_id") == char1_id:
                    c1_speaking = True
                    active_emotion = d.get("emotion", "curious").lower()
                elif d.get("speaker_id") == char2_id:
                    c2_speaking = True
                    active_emotion = d.get("emotion", "curious").lower()

        # Call to Action (Climax finale: both waving to camera)
        if t_sec > 25.5:
            return {
                char1_id: {"x": c1_x, "y": root_y, "facing": 1, "action": "wave", "is_speaking": c1_speaking},
                char2_id: {"x": c2_x, "y": root_y, "facing": -1, "action": "wave", "is_speaking": c2_speaking}
            }

        # Roles: Speaker gesticulates with dialogue rhythm; Listener reacts with lively social response
        if c1_speaking:
            c1_facing = 1
            c2_facing = -1
            if c1_walking:
                c1_action = "walk"
            else:
                base_c1 = scene_action_map.get(char1_id, "point").lower()
                if base_c1 in ["slapstick_react", "shock"]:
                    c1_action = "slapstick_react"
                elif base_c1 in ["scold", "finger_wag"] or active_emotion in ["angry", "suspicious"]:
                    c1_action = "scold"
                elif base_c1 in ["laugh"] or active_emotion in ["confident", "laughing"]:
                    c1_action = "laugh"
                elif base_c1 in ["explain", "plead", "shrug"]:
                    c1_action = "explain"
                else:
                    c1_action = "point"  # Dynamic vocal gesticulation in MovementPresetEngine

            if active_emotion in ["angry"]:
                c2_action = "explain"  # Listener pleading / shrugging
            elif active_emotion in ["shocked", "fearful"]:
                c2_action = "slapstick_react"
            elif active_emotion in ["confident", "laughing"]:
                c2_action = "laugh"
            else:
                c2_action = "think"

        elif c2_speaking:
            c2_facing = -1
            c1_facing = 1
            base_c2 = scene_action_map.get(char2_id, "point").lower()
            if base_c2 in ["slapstick_react", "shock"]:
                c2_action = "slapstick_react"
            elif base_c2 in ["scold", "finger_wag"] or active_emotion in ["angry", "suspicious"]:
                c2_action = "scold"
            elif base_c2 in ["laugh"] or active_emotion in ["confident", "laughing"]:
                c2_action = "laugh"
            elif base_c2 in ["explain", "plead", "shrug"] or active_emotion in ["apologetic", "fearful"]:
                c2_action = "explain"
            else:
                c2_action = "point"

            if active_emotion in ["angry"]:
                c1_action = "explain"
            elif active_emotion in ["shocked", "fearful"]:
                c1_action = "slapstick_react"
            elif active_emotion in ["confident", "laughing"]:
                c1_action = "laugh"
            else:
                c1_action = "think"

        else:
            # Mutual observation & idle breathing
            c1_facing = 1
            c2_facing = -1
            c1_action = "walk" if c1_walking else scene_action_map.get(char1_id, "stand")
            c2_action = scene_action_map.get(char2_id, "stand")

        return {
            char1_id: {
                "x": c1_x,
                "y": root_y,
                "facing": c1_facing,
                "action": c1_action,
                "is_speaking": c1_speaking
            },
            char2_id: {
                "x": c2_x,
                "y": root_y,
                "facing": c2_facing,
                "action": c2_action,
                "is_speaking": c2_speaking
            }
        }
