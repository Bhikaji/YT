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
        scene_action_map: Dict[str, str]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Determines gaze direction, primary action, and social reaction for both characters.
        """
        # Default positioning: Char1 on left (x=380), Char2 on right (x=700)
        c1_x, c2_x = 380.0, 700.0

        # Check who is speaking
        c1_speaking = False
        c2_speaking = False
        active_emotion = "curious"

        for d in dialogues:
            if d.get("start_second", 0.0) <= t_sec <= d.get("end_second", 0.0):
                if d.get("speaker_id") == char1_id:
                    c1_speaking = True
                    active_emotion = d.get("emotion", "curious")
                elif d.get("speaker_id") == char2_id:
                    c2_speaking = True
                    active_emotion = d.get("emotion", "curious")

        # Roles: Speaker faces listener; Listener faces speaker and reacts
        if c1_speaking:
            # Char 1 speaking -> faces Char 2 (facing right: 1)
            c1_facing = 1
            # Char 2 listening -> faces Char 1 (facing left: -1)
            c2_facing = -1
            c1_action = scene_action_map.get(char1_id, "point")
            c2_action = "think" if active_emotion in ["confused", "curious"] else "stand"
        elif c2_speaking:
            # Char 2 speaking -> faces Char 1 (facing left: -1)
            c2_facing = -1
            # Char 1 listening -> faces Char 2 (facing right: 1)
            c1_facing = 1
            c2_action = scene_action_map.get(char2_id, "point")
            c1_action = "think" if active_emotion in ["confused", "curious"] else "stand"
        else:
            # Idle / Mutual observation
            c1_facing = 1
            c2_facing = -1
            c1_action = scene_action_map.get(char1_id, "stand")
            c2_action = scene_action_map.get(char2_id, "stand")

        return {
            char1_id: {
                "x": c1_x,
                "y": 1380.0,
                "facing": c1_facing,
                "action": c1_action,
                "is_speaking": c1_speaking
            },
            char2_id: {
                "x": c2_x,
                "y": 1380.0,
                "facing": c2_facing,
                "action": c2_action,
                "is_speaking": c2_speaking
            }
        }
