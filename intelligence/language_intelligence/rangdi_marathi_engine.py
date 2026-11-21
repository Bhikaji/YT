"""
Natural Rangdi Marathi Language Intelligence Engine.
Generates authentic, colloquial, conversational Rangdi Marathi dialogue with regional
humor, natural pauses, realistic pronunciation, and comedy timing.
Uses relatable non-educational everyday comedy topics with ZERO English prompts,
ZERO speaker tags in subtitles, and ZERO complex/critical vocabulary.
"""

from typing import Dict, Any, List
from intelligence.script_generation.script_schema import StickFigureScript, ScriptScene, DialogueLine, SceneAction
from intelligence.language_intelligence.gavti_comedy_catalog import GavtiComedyCatalog

class RangdiMarathiEngine:
    """
    Dedicated generator for conversational Rangdi Marathi screenplays.
    """

    @classmethod
    def generate_rangdi_marathi_script(cls, topic: str = "", category: str = "comedy") -> StickFigureScript:
        """
        Generates a culturally authentic, hilarious Rangdi Marathi Short screenplay.
        Follows the strict 6-part YouTube Shorts retention formula.
        Uses pure everyday relatable village comedy (battery dying, bike petrol, tea, borrowed money).
        """
        scenario = GavtiComedyCatalog.get_scenario_by_id_or_keyword(topic)

        # Authentic Marathi Character Cast (No English suffixes in names)
        char1_id = "stick_bob"
        char1_name = "बब्या"
        char2_id = "stick_prof"
        char2_name = "गंप्या"

        env = "village_katta"
        scenes: List[ScriptScene] = []

        # -------------------------------------------------------------
        # SCENE 1: 0–5 sec - POWERFUL HOOK (Stop Scrolling)
        # -------------------------------------------------------------
        scenes.append(ScriptScene(
            scene_id=1,
            environment=env,
            start_second=0.0,
            end_second=5.0,
            description="बब्या डोक्याला हात लावून जोरात ओरडतो.",
            camera_movement="ZOOM_IN",
            dialogues=[
                DialogueLine(
                    speaker_id=char1_id,
                    speaker_name=char1_name,
                    text=scenario["hook"],
                    emotion="shocked",
                    start_second=0.3,
                    end_second=4.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=char1_id,
                    action_type="slapstick_react",
                    gesture="point",
                    facial_expression="shocked",
                    start_second=0.0,
                    end_second=5.0
                )
            ],
            sound_effects=["whoosh"]
        ))

        # -------------------------------------------------------------
        # SCENE 2: 5–10 sec - SITUATION (Introduce Premise)
        # -------------------------------------------------------------
        scenes.append(ScriptScene(
            scene_id=2,
            environment=env,
            start_second=5.0,
            end_second=10.0,
            description="गंप्या कट्ट्यावर बसून हसतो आणि बब्याला विचारतो.",
            camera_movement="PAN_RIGHT",
            dialogues=[
                DialogueLine(
                    speaker_id=char2_id,
                    speaker_name=char2_name,
                    text=scenario["situation"],
                    emotion="laughing",
                    start_second=5.2,
                    end_second=9.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=char2_id,
                    action_type="laugh",
                    gesture="cross_arms",
                    facial_expression="laughing",
                    start_second=5.0,
                    end_second=10.0
                )
            ],
            sound_effects=["pop"]
        ))

        # -------------------------------------------------------------
        # SCENE 3: 10–15 sec - DEVELOPMENT (Create Intrigue)
        # -------------------------------------------------------------
        scenes.append(ScriptScene(
            scene_id=3,
            environment=env,
            start_second=10.0,
            end_second=15.0,
            description="बब्या उत्साहाने आपली अतरंगी आयडिया सांगतो.",
            camera_movement="STATIC",
            dialogues=[
                DialogueLine(
                    speaker_id=char1_id,
                    speaker_name=char1_name,
                    text=scenario["intrigue"],
                    emotion="excited",
                    start_second=10.2,
                    end_second=14.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=char1_id,
                    action_type="dance",
                    gesture="wave",
                    facial_expression="laughing",
                    start_second=10.0,
                    end_second=15.0
                )
            ],
            sound_effects=["ding_lightbulb"]
        ))

        # -------------------------------------------------------------
        # SCENE 4: 15–20 sec - CONFLICT / SURPRISE (Twist)
        # -------------------------------------------------------------
        scenes.append(ScriptScene(
            scene_id=4,
            environment=env,
            start_second=15.0,
            end_second=20.0,
            description="गंप्या धोक्याचा इशारा देतो आणि डोळे मोठे करतो.",
            camera_movement="SHAKE",
            dialogues=[
                DialogueLine(
                    speaker_id=char2_id,
                    speaker_name=char2_name,
                    text=scenario["twist"],
                    emotion="suspicious",
                    start_second=15.2,
                    end_second=19.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=char2_id,
                    action_type="point",
                    gesture="point",
                    facial_expression="angry",
                    start_second=15.0,
                    end_second=20.0
                )
            ],
            sound_effects=["punchline_impact"]
        ))

        # -------------------------------------------------------------
        # SCENE 5: 20–25 sec - PAYOFF (Main Value Punchline)
        # -------------------------------------------------------------
        scenes.append(ScriptScene(
            scene_id=5,
            environment=env,
            start_second=20.0,
            end_second=25.0,
            description="बब्या कॉलर उडवून खरा तोडगा दाखवतो.",
            camera_movement="ZOOM_IN",
            dialogues=[
                DialogueLine(
                    speaker_id=char1_id,
                    speaker_name=char1_name,
                    text=scenario["payoff"],
                    emotion="confident",
                    start_second=20.2,
                    end_second=24.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=char1_id,
                    action_type="slapstick_react",
                    gesture="thumbs_up",
                    facial_expression="confident",
                    start_second=20.0,
                    end_second=25.0
                )
            ],
            sound_effects=["whoosh"]
        ))

        # -------------------------------------------------------------
        # SCENE 6: 25–30 sec - CALL TO ACTION (Engagement)
        # -------------------------------------------------------------
        scenes.append(ScriptScene(
            scene_id=6,
            environment=env,
            start_second=25.0,
            end_second=30.0,
            description="दोघेही हसतात आणि सबस्क्राईब करायला सांगतात.",
            camera_movement="ZOOM_OUT",
            dialogues=[
                DialogueLine(
                    speaker_id=char2_id,
                    speaker_name=char2_name,
                    text=scenario["cta"],
                    emotion="excited",
                    start_second=25.2,
                    end_second=29.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=char2_id,
                    action_type="dance",
                    gesture="wave",
                    facial_expression="laughing",
                    start_second=25.0,
                    end_second=30.0
                )
            ],
            sound_effects=["pop"]
        ))

        return StickFigureScript(
            title=f"गावठी कॉमेडी: {scenario['title_marathi']}",
            topic=scenario["title_marathi"],
            category=category or "comedy_entertainment",
            hook=scenario["hook"],
            situation=scenario["situation"],
            development=scenario["intrigue"],
            conflict=scenario["twist"],
            payoff=scenario["payoff"],
            ending_cta=scenario["cta"],
            total_duration=30.0,
            cast=[
                {"id": char1_id, "name": char1_name, "color": "#0ea5e9"},
                {"id": char2_id, "name": char2_name, "color": "#8b5cf6"}
            ],
            scenes=scenes
        )
