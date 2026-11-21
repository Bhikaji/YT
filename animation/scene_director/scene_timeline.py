import re
from typing import Dict, Any, List, Optional
from intelligence.script_generation.script_schema import StickFigureScript, ScriptScene
from animation.character_engine.character_model import StickFigureCharacter
from animation.skeleton_engine.movement_presets import MovementPresetEngine
from animation.lip_sync.speech_synchronizer import SpeechSynchronizer
from animation.camera_engine.camera_2d import Camera2D
from animation.scene_director.multi_character_coord import MultiCharacterCoordinator

class AnimationTimelineDirector:
    """
    Directorial Timeline Compiler.
    Transforms a StickFigureScript into 900 frame-by-frame instructions (30s @ 30 FPS).
    Synchronizes audio-measured lip-sync, mutual character gaze, and clean subtitles.
    """

    @classmethod
    def compile_timeline(
        cls,
        script: StickFigureScript,
        fps: int = 30,
        scheduled_dialogues: Optional[List[Dict[str, Any]]] = None,
        width: int = 1280,
        height: int = 720
    ) -> List[Dict[str, Any]]:
        total_frames = int(script.total_duration * fps)
        timeline = []
        camera = Camera2D()

        char1_info = script.cast[0]
        char2_info = script.cast[1]
        c1_id = char1_info["id"]
        c2_id = char2_info["id"]

        # Global list of scheduled dialogues with exact audio timestamps
        if scheduled_dialogues and len(scheduled_dialogues) > 0:
            all_dialogues = scheduled_dialogues
        else:
            all_dialogues = []
            for s in script.scenes:
                for d in s.dialogues:
                    all_dialogues.append(d.model_dump())

        for frame_idx in range(total_frames):
            t_sec = frame_idx / float(fps)

            # Find active scene
            active_scene = script.scenes[0]
            for s in script.scenes:
                if s.start_second <= t_sec <= s.end_second:
                    active_scene = s
                    break

            scene_dur = max(0.1, active_scene.end_second - active_scene.start_second)
            scene_progress = (t_sec - active_scene.start_second) / scene_dur

            # Camera calculation
            zoom, pan_x, pan_y = camera.update(active_scene.camera_movement, scene_progress, t_sec)

            # Scene action map
            act_map = {}
            for a in active_scene.actions:
                act_map[a.character_id] = a.action_type

            # Multi-character coordination with global audio schedule
            coord = MultiCharacterCoordinator.coordinate_roles(
                char1_id=c1_id,
                char2_id=c2_id,
                t_sec=t_sec,
                dialogues=all_dialogues,
                scene_action_map=act_map,
                width=width,
                height=height
            )

            # Accurate Lip-Sync: Synchronized to exact synthesized audio timestamps
            c1_mouth = SpeechSynchronizer.get_mouth_state(c1_id, t_sec, all_dialogues)
            c2_mouth = SpeechSynchronizer.get_mouth_state(c2_id, t_sec, all_dialogues)

            # Determine facial expression
            c1_expr = "curious"
            c2_expr = "curious"
            for a in active_scene.actions:
                if a.character_id == c1_id:
                    c1_expr = a.facial_expression
                elif a.character_id == c2_id:
                    c2_expr = a.facial_expression

            # Sync active speaking emotion from dialogue
            for d in all_dialogues:
                if d.get("start_second", 0.0) <= t_sec <= d.get("end_second", 0.0):
                    if d.get("speaker_id") == c1_id:
                        c1_expr = d.get("emotion", c1_expr)
                    elif d.get("speaker_id") == c2_id:
                        c2_expr = d.get("emotion", c2_expr)

            # Poses from movement presets
            c1_pose = MovementPresetEngine.get_pose_at_time(
                action_name=coord[c1_id]["action"],
                t_sec=t_sec,
                root_x=coord[c1_id]["x"],
                root_y=coord[c1_id]["y"],
                facing_dir=coord[c1_id]["facing"]
            )

            c2_pose = MovementPresetEngine.get_pose_at_time(
                action_name=coord[c2_id]["action"],
                t_sec=t_sec,
                root_x=coord[c2_id]["x"],
                root_y=coord[c2_id]["y"],
                facing_dir=coord[c2_id]["facing"]
            )

            # Active Subtitle & Active Speaker
            current_sub = ""
            active_speaker = ""
            for d in all_dialogues:
                if d.get("start_second", 0.0) <= t_sec <= d.get("end_second", 0.0):
                    raw_text = d.get("text", "")
                    clean_text = re.sub(r'^\s*[\(\[]?[A-Za-z0-9_\u0900-\u097F\s\.\-]+[\)\]]?\s*:\s*', '', raw_text)
                    current_sub = clean_text.strip()
                    active_speaker = d.get("speaker_id", "")
                    break

            # Sound effects triggered around start of scene
            sfx_active = []
            if abs(t_sec - active_scene.start_second) < (1.0 / fps):
                sfx_active = active_scene.sound_effects

            timeline.append({
                "frame": frame_idx,
                "time_sec": t_sec,
                "environment": active_scene.environment,
                "camera": {"zoom": zoom, "pan_x": pan_x, "pan_y": pan_y},
                "active_speaker": active_speaker,
                "char1": {
                    "id": c1_id,
                    "name": char1_info["name"],
                    "pose": c1_pose,
                    "expression": c1_expr,
                    "mouth": c1_mouth,
                    "is_speaking": coord[c1_id]["is_speaking"],
                    "facing": coord[c1_id]["facing"]
                },
                "char2": {
                    "id": c2_id,
                    "name": char2_info["name"],
                    "pose": c2_pose,
                    "expression": c2_expr,
                    "mouth": c2_mouth,
                    "is_speaking": coord[c2_id]["is_speaking"],
                    "facing": coord[c2_id]["facing"]
                },
                "subtitle": current_sub,
                "sfx": sfx_active
            })

        return timeline
