import json
import os
from typing import Dict, Any, List, Optional
from backend.app.schemas.script import (
    GeneratedEpisodeScript, ScriptScene, CameraShotCue,
    CharacterActionCue, DialogueCue, SoundEffectCue
)
from backend.app.config import settings

class ScreenwriterAgent:
    """Generates structured 3D animation scripts with cinematic staging and dialogue."""

    @classmethod
    def generate_script_procedural(
        cls,
        series_title: str,
        episode_number: int,
        episode_title: str,
        format_type: str,
        cast: List[Dict[str, Any]],
        unresolved_mystery: Optional[str] = None
    ) -> GeneratedEpisodeScript:
        """
        Generates a calibrated directorial screenplay with cinematic camera shots,
        character locomotion, facial expressions, and emotional dialogue.
        """
        hero = cast[0] if cast else {"id": "hero_leo", "name": "Leo"}
        partner = cast[1] if len(cast) > 1 else {"id": "sidekick_maya", "name": "Maya"}

        cliffhanger = (
            f"Why did the glowing ancient artifact suddenly display {hero['name']}'s name?"
            if episode_number % 2 == 1 else
            f"Who was hiding behind the shadow at the end of the corridor?"
        )

        scenes = [
            ScriptScene(
                scene_number=1,
                environment="ancient_ruins_courtyard",
                lighting_preset="dramatic_sunset",
                duration_seconds=7.0,
                camera_shots=[
                    CameraShotCue(
                        shot_type="ESTABLISHING_TRACKING",
                        camera_pos=(0.0, -5.0, 2.0),
                        target_focus_pos=(0.0, 0.0, 1.2),
                        focal_length_mm=35.0,
                        shake_intensity=0.05
                    )
                ],
                actions=[
                    CharacterActionCue(
                        character_id=hero["id"],
                        action_name="torch_walk_cautious",
                        start_second=0.0,
                        end_second=6.0,
                        start_pos=(-2.0, -1.0, 0.0),
                        end_pos=(0.0, 0.0, 0.0),
                        facial_expression="focused"
                    )
                ],
                dialogues=[
                    DialogueCue(
                        character_id=hero["id"],
                        character_name=hero["name"],
                        text=f"Stay close, {partner['name']}. These ruins weren't meant to be found.",
                        emotion="whisper",
                        start_second=1.5
                    )
                ],
                sound_effects=[
                    SoundEffectCue(sfx_type="wind_ruins", start_second=0.0, volume=0.4),
                    SoundEffectCue(sfx_type="footsteps_stone", start_second=0.5, volume=0.6)
                ]
            ),
            ScriptScene(
                scene_number=2,
                environment="ancient_ruins_courtyard",
                lighting_preset="mysterious_cyan_glow",
                duration_seconds=9.0,
                camera_shots=[
                    CameraShotCue(
                        shot_type="OVER_SHOULDER",
                        target_character_id=hero["id"],
                        camera_pos=(0.8, -1.2, 1.6),
                        target_focus_pos=(0.0, 0.0, 1.3),
                        focal_length_mm=50.0
                    )
                ],
                actions=[
                    CharacterActionCue(
                        character_id=partner["id"],
                        action_name="point_forward_alarmed",
                        start_second=0.5,
                        end_second=4.0,
                        start_pos=(1.2, -0.5, 0.0),
                        end_pos=(1.0, -0.2, 0.0),
                        facial_expression="scared"
                    ),
                    CharacterActionCue(
                        character_id=hero["id"],
                        action_name="turn_around_shocked",
                        start_second=3.5,
                        end_second=7.5,
                        start_pos=(0.0, 0.0, 0.0),
                        end_pos=(0.0, 0.0, 0.0),
                        facial_expression="shocked"
                    )
                ],
                dialogues=[
                    DialogueCue(
                        character_id=partner["id"],
                        character_name=partner["name"],
                        text="Leo, look at the door! The symbols... they are glowing!",
                        emotion="terrified",
                        start_second=1.0
                    ),
                    DialogueCue(
                        character_id=hero["id"],
                        character_name=hero["name"],
                        text="That's impossible... only the Keymaster could activate this!",
                        emotion="excited",
                        start_second=4.8
                    )
                ],
                sound_effects=[
                    SoundEffectCue(sfx_type="stone_grind_creak", start_second=2.8, volume=0.8),
                    SoundEffectCue(sfx_type="energy_hum", start_second=3.5, volume=0.7)
                ]
            ),
            ScriptScene(
                scene_number=3,
                environment="ancient_ruins_courtyard",
                lighting_preset="dramatic_pulsing_red",
                duration_seconds=7.5,
                camera_shots=[
                    CameraShotCue(
                        shot_type="EXTREME_CLOSE_UP",
                        target_character_id=hero["id"],
                        camera_pos=(0.0, -1.0, 1.5),
                        target_focus_pos=(0.0, 0.0, 1.45),
                        focal_length_mm=85.0,
                        shake_intensity=0.15
                    )
                ],
                actions=[
                    CharacterActionCue(
                        character_id=hero["id"],
                        action_name="recoil_step_back",
                        start_second=0.0,
                        end_second=6.0,
                        start_pos=(0.0, 0.0, 0.0),
                        end_pos=(-0.5, -0.5, 0.0),
                        facial_expression="shocked"
                    )
                ],
                dialogues=[
                    DialogueCue(
                        character_id=hero["id"],
                        character_name=hero["name"],
                        text="Wait... who is that standing in the shadows?",
                        emotion="terrified",
                        start_second=1.0
                    )
                ],
                sound_effects=[
                    SoundEffectCue(sfx_type="dramatic_orchestral_hit", start_second=2.5, volume=0.9)
                ]
            )
        ]

        return GeneratedEpisodeScript(
            series_title=series_title,
            episode_number=episode_number,
            episode_title=episode_title,
            format=format_type,
            synopsis=f"Leo and Maya explore the forbidden ruins and accidentally trigger a dormant mechanism that reveals a terrifying mystery.",
            cliffhanger_question=cliffhanger,
            next_episode_teaser=f"In Episode {episode_number + 1}, the identity of the shadow figure is revealed!",
            scenes=scenes,
            story_memory_updates={
                "ruins_discovered": True,
                "symbols_activated": True,
                "unresolved_figure_in_shadow": True
            }
        )
