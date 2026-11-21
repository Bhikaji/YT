"""
Natural Varhadi & Rangdi Marathi Language Intelligence Engine matching demo.mp4.
Generates authentic, colloquial Varhadi Marathi comedy screenplays with the exact
regional verbal expressions (मा, हो का व, बकऱ्या, तुले, आम्हाले), fast scolding mother dialogue,
hilarious Gavti shivya (भडव्या, मुडद्या, येड्या, काळ्या तोंडाच्या, फुकट्या, मारीन एक मुस्काटात),
and canonical cast: ganya, shanti, rohya, sonya, yogya, aakya.
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

        # Canonical characters matching demo.mp4
        char1_id = scenario.get("char1_id", "ganya")       # गण्या (Orange Hair Hero Boy in Red-and-White Stripes)
        char1_name = scenario.get("char1_name", "गण्या")
        char2_id = scenario.get("char2_id", "shanti")      # शांताबाई (Mother in Blue Saree) or Rohya
        char2_name = scenario.get("char2_name", "शांताबाई")
        char3_id = scenario.get("char3_id", "rohya")       # रोह्या (Purple Hair Friend in White T-Shirt)
        char3_name = scenario.get("char3_name", "रोह्या")

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
            description="गण्या आईपुढे हात पसरून रडवेल्या चेहऱ्याने तिकिटाचे पैसे मागतो." if is_bus_scene else "गण्या चालत येऊन मित्राकडे हात करतो.",
            camera_movement="ZOOM_IN",
            dialogues=[
                DialogueLine(
                    speaker_id=char1_id,
                    speaker_name=char1_name,
                    text=scenario["hook"],
                    emotion="cry" if is_bus_scene else "shocked",
                    start_second=0.3,
                    end_second=4.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=char1_id,
                    action_type="slapstick_react" if is_bus_scene else "walk",
                    gesture="plead" if is_bus_scene else "point",
                    facial_expression="cry" if is_bus_scene else "shocked",
                    start_second=0.0,
                    end_second=5.0
                )
            ],
            sound_effects=["whoosh"]
        ))

        # -------------------------------------------------------------
        # SCENE 2: 5–10 sec - SITUATION (Introduce Premise / Maternal Scold)
        # -------------------------------------------------------------
        spk_2 = char2_id
        spk_2_name = char2_name
        scenes.append(ScriptScene(
            scene_id=2,
            environment=env,
            start_second=5.0,
            end_second=10.0,
            description="शांताबाई कंबरेवर हात ठेवून संतापाने गण्याला ओरडतात." if is_bus_scene else "रोह्या हात पसरून अपराधी चेहऱ्याने कारण सांगतो.",
            camera_movement="PAN_RIGHT",
            dialogues=[
                DialogueLine(
                    speaker_id=spk_2,
                    speaker_name=spk_2_name,
                    text=scenario["situation"],
                    emotion="angry" if is_bus_scene else "fearful",
                    start_second=5.2,
                    end_second=9.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=spk_2,
                    action_type="scold" if is_bus_scene else "explain",
                    gesture="cross_arms" if is_bus_scene else "plead",
                    facial_expression="angry" if is_bus_scene else "fearful",
                    start_second=5.0,
                    end_second=10.0
                )
            ],
            sound_effects=["punchline_impact"]
        ))

        # -------------------------------------------------------------
        # SCENE 3: 10–15 sec - INTRIGUE (Friend steps in with cheeky comment)
        # -------------------------------------------------------------
        spk_3 = char3_id
        spk_3_name = char3_name
        scenes.append(ScriptScene(
            scene_id=3,
            environment=env,
            start_second=10.0,
            end_second=15.0,
            description="रोह्या पुढे येऊन शहाणपणा शिकवतो आणि काकूंना धीर देतो.",
            camera_movement="STATIC",
            dialogues=[
                DialogueLine(
                    speaker_id=spk_3,
                    speaker_name=spk_3_name,
                    text=scenario["intrigue"],
                    emotion="confident",
                    start_second=10.2,
                    end_second=14.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=spk_3,
                    action_type="explain",
                    gesture="point",
                    facial_expression="confident",
                    start_second=10.0,
                    end_second=15.0
                )
            ],
            sound_effects=["ding_lightbulb"]
        ))

        # -------------------------------------------------------------
        # SCENE 4: 15–20 sec - TWIST (Mother roasts the friend!)
        # -------------------------------------------------------------
        spk_4 = char2_id
        spk_4_name = char2_name
        scenes.append(ScriptScene(
            scene_id=4,
            environment=env,
            start_second=15.0,
            end_second=20.0,
            description="शांताबाई रोह्यावर भडकतात आणि हात उगारून दम भरतात.",
            camera_movement="ZOOM_IN",
            dialogues=[
                DialogueLine(
                    speaker_id=spk_4,
                    speaker_name=spk_4_name,
                    text=scenario["twist"],
                    emotion="angry",
                    start_second=15.2,
                    end_second=19.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=spk_4,
                    action_type="scold",
                    gesture="point",
                    facial_expression="angry",
                    start_second=15.0,
                    end_second=20.0
                )
            ],
            sound_effects=["slap_impact"]
        ))

        # -------------------------------------------------------------
        # SCENE 5: 20–25 sec - PAYOFF (Hilarious punchline & laughter)
        # -------------------------------------------------------------
        spk_5 = char3_id
        spk_5_name = char3_name
        scenes.append(ScriptScene(
            scene_id=5,
            environment=env,
            start_second=20.0,
            end_second=25.0,
            description="रोह्या तोंडावर हात ठेवून हसतो आणि पंचलाईन सांगतो.",
            camera_movement="PAN_LEFT",
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
                    action_type="slapstick_react",
                    gesture="wave_arms_frantic",
                    facial_expression="happy",
                    start_second=20.0,
                    end_second=25.0
                )
            ],
            sound_effects=["laughter_punchline"]
        ))

        # -------------------------------------------------------------
        # SCENE 6: 25–30 sec - CALL TO ACTION (CTA & Subscribe)
        # -------------------------------------------------------------
        spk_6 = char1_id
        spk_6_name = char1_name
        scenes.append(ScriptScene(
            scene_id=6,
            environment=env,
            start_second=25.0,
            end_second=30.0,
            description="दोघेही कॅमेऱ्याकडे हात हलवून प्रेक्षकांना सबस्क्राईब करायला सांगतात.",
            camera_movement="STATIC",
            dialogues=[
                DialogueLine(
                    speaker_id=spk_6,
                    speaker_name=spk_6_name,
                    text=scenario["cta"],
                    emotion="happy",
                    start_second=25.2,
                    end_second=29.5
                )
            ],
            actions=[
                SceneAction(
                    character_id=char1_id,
                    action_type="walk",
                    gesture="wave_arms_frantic",
                    facial_expression="happy",
                    start_second=25.0,
                    end_second=30.0
                )
            ],
            sound_effects=["pop"]
        ))

        # Compile final screenplay
        title = scenario.get("title_marathi", "वऱ्हाडी कॉमेडी")
        cast_list = [
            {"id": char1_id, "name": char1_name, "voice_id": "mr-IN-ManoharNeural"},
            {"id": char2_id, "name": char2_name, "voice_id": "mr-IN-AarohiNeural" if "shanti" in char2_id else "mr-IN-ManoharNeural"}
        ]
        if char3_id:
            cast_list.append({"id": char3_id, "name": char3_name, "voice_id": "mr-IN-ManoharNeural"})

        return StickFigureScript(
            title=title,
            topic=topic or scenario.get("title_marathi", "वऱ्हाडी कॉमेडी"),
            category=category,
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
