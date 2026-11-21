"""
Natural Varhadi & Rangdi Marathi Language Intelligence Engine matching demo.mp4.
Generates authentic, colloquial Varhadi Marathi comedy screenplays with the exact
regional verbal expressions (मा, हो का व, बकऱ्या, तुले, आम्हाले), fast scolding mother dialogue,
and classic multi-character situational cartoon timing.
"""

from typing import Dict, Any, List
from intelligence.script_generation.script_schema import StickFigureScript, ScriptScene, DialogueLine, SceneAction
from intelligence.language_intelligence.gavti_comedy_catalog import GavtiComedyCatalog

class RangdiMarathiEngine:
    """
    Dedicated generator for authentic Varhadi & Rangdi Marathi cartoon screenplays.
    """

    @classmethod
    def generate_rangdi_marathi_script(cls, topic: str = "", category: str = "comedy") -> StickFigureScript:
        """
        Generates a culturally authentic, hilarious Varhadi Marathi Short screenplay.
        Matches the characters, verbals, and environments from demo.mp4.
        """
        scenario = GavtiComedyCatalog.get_scenario_by_id_or_keyword(topic)

        # Characters matching demo.mp4
        char1_id = "stick_bob"          # बब्या (Orange Hair Hero Boy in Red-and-White Stripes)
        char1_name = "बब्या"
        char2_id = "stick_prof"         # गंप्या (Purple Hair Friend in White T-Shirt)
        char2_name = "गंप्या"
        char3_id = "varhadi_mother"     # आई (Mother in Blue Saree)
        char3_name = "आई"

        env = scenario.get("environment", "msrtc_bus_stand")
        scenes: List[ScriptScene] = []

        is_bus_scene = (scenario["id"] == "msrtc_bus_tour_scold")

        # -------------------------------------------------------------
        # SCENE 1: 0–5 sec - POWERFUL HOOK (Stop Scrolling)
        # -------------------------------------------------------------
        scenes.append(ScriptScene(
            scene_id=1,
            environment=env,
            start_second=0.0,
            end_second=5.0,
            description="बब्या चालत येऊन आश्चर्याने मित्राकडे हात करतो." if not is_bus_scene else "बब्या आईपुढे हात पसरून तिकिटाचे पैसे मागतो.",
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
                    action_type="walk" if not is_bus_scene else "slapstick_react",
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
        spk_2 = char3_id if is_bus_scene else char2_id
        spk_2_name = char3_name if is_bus_scene else char2_name
        scenes.append(ScriptScene(
            scene_id=2,
            environment=env,
            start_second=5.0,
            end_second=10.0,
            description="गंप्या हात जोडून/पसरून अपराधी चेहऱ्याने कारण सांगतो." if not is_bus_scene else "आई कंबरेवर हात ठेवून बब्याला जोरात ओरडते.",
            camera_movement="PAN_RIGHT",
            dialogues=[
                DialogueLine(
                    speaker_id=spk_2,
                    speaker_name=spk_2_name,
                    text=scenario["situation"],
                    emotion="angry" if is_bus_scene else "apologetic",
                    start_second=5.2,
                    end_second=9.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=spk_2,
                    action_type="scold" if is_bus_scene else "explain",
                    gesture="plead" if not is_bus_scene else "cross_arms",
                    facial_expression="angry" if is_bus_scene else "fearful",
                    start_second=5.0,
                    end_second=10.0
                )
            ],
            sound_effects=["punchline_impact"]
        ))

        # -------------------------------------------------------------
        # SCENE 3: 10–15 sec - DEVELOPMENT (Create Intrigue)
        # -------------------------------------------------------------
        spk_3 = char2_id if is_bus_scene else char1_id
        spk_3_name = char2_name if is_bus_scene else char1_name
        scenes.append(ScriptScene(
            scene_id=3,
            environment=env,
            start_second=10.0,
            end_second=15.0,
            description="बसच्या दारात उभा गंप्या काकूंना धीर देतो." if is_bus_scene else "बब्या कंबरेवर हात ठेवून बोट दाखवून मित्राला खडसावतो.",
            camera_movement="STATIC",
            dialogues=[
                DialogueLine(
                    speaker_id=spk_3,
                    speaker_name=spk_3_name,
                    text=scenario["intrigue"],
                    emotion="excited" if is_bus_scene else "angry",
                    start_second=10.2,
                    end_second=14.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=spk_3,
                    action_type="wave" if is_bus_scene else "scold",
                    gesture="wave" if is_bus_scene else "point",
                    facial_expression="laughing" if is_bus_scene else "angry",
                    start_second=10.0,
                    end_second=15.0
                )
            ],
            sound_effects=[]
        ))

        # -------------------------------------------------------------
        # SCENE 4: 15–20 sec - CONFLICT / SURPRISE (Twist)
        # -------------------------------------------------------------
        spk_4 = char3_id if is_bus_scene else char2_id
        spk_4_name = char3_name if is_bus_scene else char2_name
        scenes.append(ScriptScene(
            scene_id=4,
            environment=env,
            start_second=15.0,
            end_second=20.0,
            description="आई डोळे मोठे करून धोक्याचा इशारा देते." if is_bus_scene else "गंप्या वेटरकडे बघून घाबरून बोट दाखवतो.",
            camera_movement="SHAKE",
            dialogues=[
                DialogueLine(
                    speaker_id=spk_4,
                    speaker_name=spk_4_name,
                    text=scenario["twist"],
                    emotion="suspicious" if is_bus_scene else "fearful",
                    start_second=15.2,
                    end_second=19.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=spk_4,
                    action_type="point" if is_bus_scene else "shock",
                    gesture="point",
                    facial_expression="angry" if is_bus_scene else "shocked",
                    start_second=15.0,
                    end_second=20.0
                )
            ],
            sound_effects=["punchline_impact"]
        ))

        # -------------------------------------------------------------
        # SCENE 5: 20–25 sec - PAYOFF (Main Value Punchline)
        # -------------------------------------------------------------
        spk_5 = char1_id
        spk_5_name = char1_name
        scenes.append(ScriptScene(
            scene_id=5,
            environment=env,
            start_second=20.0,
            end_second=25.0,
            description="बब्या हसून पोट धरतो आणि भन्नाट युक्ती सांगतो.",
            camera_movement="ZOOM_IN",
            dialogues=[
                DialogueLine(
                    speaker_id=spk_5,
                    speaker_name=spk_5_name,
                    text=scenario["payoff"],
                    emotion="laughing",
                    start_second=20.2,
                    end_second=24.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=spk_5,
                    action_type="laugh",
                    gesture="thumbs_up",
                    facial_expression="laughing",
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
            description="सर्वजण हसतात आणि वऱ्हाडी स्टाईलमध्ये सबस्क्राईब करायला सांगतात.",
            camera_movement="ZOOM_OUT",
            dialogues=[
                DialogueLine(
                    speaker_id=char1_id,
                    speaker_name=char1_name,
                    text=scenario["cta"],
                    emotion="excited",
                    start_second=25.2,
                    end_second=29.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=char1_id,
                    action_type="wave",
                    gesture="wave",
                    facial_expression="laughing",
                    start_second=25.0,
                    end_second=30.0
                )
            ],
            sound_effects=["pop"]
        ))

        cast_list = [
            {"id": char3_id, "name": char3_name, "color": "#1d4ed8"},
            {"id": char1_id, "name": char1_name, "color": "#f97316"}
        ] if is_bus_scene else [
            {"id": char1_id, "name": char1_name, "color": "#f97316"},
            {"id": char2_id, "name": char2_name, "color": "#7c3aed"}
        ]

        return StickFigureScript(
            title=f"वऱ्हाडी कॉमेडी: {scenario['title_marathi']}",
            topic=scenario["title_marathi"],
            category=category or "comedy_entertainment",
            hook=scenario["hook"],
            situation=scenario["situation"],
            development=scenario["intrigue"],
            conflict=scenario["twist"],
            payoff=scenario["payoff"],
            ending_cta=scenario["cta"],
            total_duration=30.0,
            cast=cast_list,
            scenes=scenes
        )
