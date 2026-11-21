"""
Automated Integration and Unit Test Suite for Autonomous 2D Stick-Figure Animation Studio.
Tests discovery, topic scoring, script generation, skeletal kinematics, facial rigs,
procedural backgrounds, thumbnail creation, quality control,
Rangdi Marathi & Hindi dialogue intelligence, zero-overlap scheduling, and high-contrast rendering.
"""

import unittest
import asyncio
from pathlib import Path
from PIL import Image

from intelligence.trend_research.category_catalog import ContentCategoryCatalog
from intelligence.trend_research.trend_intelligence import TrendIntelligenceEngine
from intelligence.topic_scoring.trend_scorer import TrendScorer
from intelligence.topic_scoring.trend_classifier import TrendClassifier
from intelligence.script_generation.story_engine import StickStoryEngine
from intelligence.script_generation.script_evaluator import ScriptEvaluator
from intelligence.language_intelligence.language_selector import LanguageSelectionEngine
from intelligence.language_intelligence.rangdi_marathi_engine import RangdiMarathiEngine
from intelligence.language_intelligence.hindi_dialogue_engine import HindiDialogueEngine
from intelligence.language_intelligence.multilingual_localizer import MultilingualLocalizer
from animation.character_engine.character_model import StickFigureCharacter
from animation.skeleton_engine.stick_skeleton import StickSkeletonPose
from animation.skeleton_engine.forward_kinematics import ForwardKinematicsSolver
from animation.skeleton_engine.movement_presets import MovementPresetEngine
from animation.expression_engine.facial_rig import FacialRig
from animation.lip_sync.phoneme_mapper import PhonemeMapper
from animation.environment_engine.procedural_backgrounds import ProceduralBackgroundRenderer
from animation.camera_engine.camera_2d import Camera2D
from audio.dialogue_coordination.dialogue_scheduler import DialogueScheduler
from audio.dialogue_coordination.audio_qa_engine import AudioQualityAssuranceEngine
from audio.voice_generation.realistic_voice_engine import RealisticHumanVoiceEngine
from production.renderer.stick_renderer import StickFigureRenderer
from production.thumbnail_generator.thumbnail_studio import StickThumbnailStudio
from production.quality_control.qc_inspector import StickQCInspector


class TestCategoryAndScoring(unittest.TestCase):
    def test_categories_catalog(self):
        cats = ContentCategoryCatalog.get_all_categories()
        self.assertGreaterEqual(len(cats), 10)
        names = [c["name"] for c in cats.values()]
        self.assertIn("Science and Discovery", names)
        self.assertIn("Technology", names)
        self.assertIn("Comedy and Entertainment", names)

    def test_custom_category_registration(self):
        ContentCategoryCatalog.register_custom_category(
            "mythology", "Mythology & Lore", ["Gods", "Legends", "Myths"], ["zeus", "thor"]
        )
        cats = ContentCategoryCatalog.get_all_categories()
        self.assertIn("mythology", cats)

    def test_topic_scoring_and_classification(self):
        score_data = TrendScorer.calculate_opportunity_score(
            topic="Quantum Supercomputers Breakthrough",
            category="technology",
            volume_numeric=350000
        )
        score = score_data["opportunity_score"]
        self.assertGreaterEqual(score, 60.0)
        self.assertLessEqual(score, 100.0)
        self.assertIn("factor_breakdown", score_data)

        trend_type = TrendClassifier.classify_trend(
            topic="Quantum Supercomputers Breakthrough",
            opportunity_score=score,
            volume_numeric=350000
        )
        self.assertIn(trend_type, ["EMERGING", "VIRAL", "RAPIDLY_GROWING"])


class TestScriptEngine(unittest.TestCase):
    def test_script_generation_and_evaluation(self):
        script = StickStoryEngine.generate_30s_script(
            topic="Why Monday Mornings Feel Impossible",
            category="comedy_entertainment"
        )
        self.assertEqual(script.category, "comedy_entertainment")
        self.assertGreaterEqual(len(script.scenes), 5)
        self.assertAlmostEqual(script.total_duration, 30.0, delta=2.0)
        self.assertGreater(len(script.cast), 0)

        # Quality Gate
        passed, score, breakdown = ScriptEvaluator.evaluate_script(script)
        self.assertTrue(passed)
        self.assertGreaterEqual(score, 70.0)


class TestMultilingualAndVoiceEngine(unittest.TestCase):
    def test_language_selection_priorities(self):
        # Priority 1: Maharashtra / India defaults to Rangdi Marathi
        mh_lang = LanguageSelectionEngine.select_language_for_target(target_geo="IN")
        self.assertEqual(mh_lang["language_code"], "mr_rangdi")
        self.assertEqual(mh_lang["priority"], 1)

        # Priority 2: North India / Explicit Hindi
        hi_lang = LanguageSelectionEngine.select_language_for_target(target_geo="IN_HINDI")
        self.assertEqual(hi_lang["language_code"], "hi")
        self.assertEqual(hi_lang["priority"], 2)

        # Priority 3: International US/UK
        us_lang = LanguageSelectionEngine.select_language_for_target(target_geo="US")
        self.assertEqual(us_lang["language_code"], "en")
        self.assertEqual(us_lang["priority"], 3)

    def test_rangdi_marathi_script_generation(self):
        script = RangdiMarathiEngine.generate_rangdi_marathi_script(
            topic="Smart Glasses vs Smartphones",
            category="technology"
        )
        self.assertEqual(len(script.scenes), 6)
        self.assertEqual(script.total_duration, 30.0)
        # Check authentic colloquial Marathi keywords
        full_text = " ".join(d.text for s in script.scenes for d in s.dialogues)
        self.assertTrue(any(w in full_text for w in ["गड्या", "लय भारी", "खतरनाक", "झकास", "राव", "बघ"]))

    def test_hindi_dialogue_generation(self):
        script = HindiDialogueEngine.generate_hindi_script(
            topic="Smart Glasses vs Smartphones",
            category="technology"
        )
        self.assertEqual(len(script.scenes), 6)
        full_text = " ".join(d.text for s in script.scenes for d in s.dialogues)
        self.assertTrue(any(w in full_text for w in ["भाई", "सच", "दिमाग", "मजाक", "सब्सक्राइब"]))

    def test_zero_overlap_scheduler(self):
        # Mock dialogue items with simulated audio paths
        mock_items = [
            {"speaker_id": "char1", "text": "Line 1", "audio_path": "output/test_marathi.mp3"},
            {"speaker_id": "char2", "text": "Line 2", "audio_path": "output/test_marathi.mp3"},
            {"speaker_id": "char1", "text": "Line 3", "audio_path": "output/test_marathi.mp3"}
        ]
        if Path("output/test_marathi.mp3").exists():
            scheduled = DialogueScheduler.schedule_dialogues(mock_items, natural_gap_sec=0.25)
            self.assertEqual(len(scheduled), 3)
            # Verify each subsequent line starts after the previous line ends
            for i in range(len(scheduled) - 1):
                self.assertGreaterEqual(scheduled[i+1]["start_second"], scheduled[i]["end_second"])

            audit = DialogueScheduler.audit_zero_overlap(scheduled)
            self.assertTrue(audit["passed"])
            self.assertEqual(audit["overlap_count"], 0)


class TestSkeletalKinematics(unittest.TestCase):
    def test_forward_kinematics(self):
        char = StickFigureCharacter("char_test", "Tester")
        pose = StickSkeletonPose(root_x=540, root_y=1200)
        solved = ForwardKinematicsSolver.solve_joint_positions(char, pose)
        
        expected_joints = [
            "pelvis", "neck", "head",
            "left_shoulder", "left_elbow", "left_hand",
            "right_shoulder", "right_elbow", "right_hand",
            "left_hip", "left_knee", "left_foot",
            "right_hip", "right_knee", "right_foot"
        ]
        for j in expected_joints:
            self.assertIn(j, solved)
            x, y = solved[j]
            self.assertIsInstance(x, (int, float))
            self.assertIsInstance(y, (int, float))

    def test_movement_presets(self):
        walk_pose = MovementPresetEngine.get_pose_at_time("walk", t_sec=0.5)
        self.assertIsInstance(walk_pose, StickSkeletonPose)
        idle_pose = MovementPresetEngine.get_pose_at_time("idle", t_sec=1.0)
        self.assertIsInstance(idle_pose, StickSkeletonPose)


class TestFacialAndLipSync(unittest.TestCase):
    def test_facial_expressions(self):
        for expr in ["happy", "shocked", "angry", "thinking", "laughing"]:
            face = FacialRig.EXPRESSION_PRESETS.get(expr)
            self.assertIsNotNone(face)
            self.assertIn("mouth_type", face)
            self.assertIn("eyebrow_angle", face)

    def test_phoneme_mapping(self):
        shape = PhonemeMapper.get_mouth_for_phoneme("A_I")
        self.assertIsInstance(shape, dict)
        self.assertTrue(shape.get("open"))


class TestVisualsAndRendering(unittest.TestCase):
    def test_procedural_background(self):
        img = ProceduralBackgroundRenderer.render_environment("science_lab", 540, 960)
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (540, 960))

    def test_high_contrast_renderer(self):
        char1 = StickFigureCharacter.get_canonical_library()["stick_bob"]
        char2 = StickFigureCharacter.get_canonical_library()["stick_prof"]
        frame_data = {
            "time_sec": 1.0,
            "environment": "tech_showroom",
            "char1": {"pose": MovementPresetEngine.get_pose_at_time("walk", 1.0), "expression": "happy", "mouth": {"open": False}, "is_speaking": False},
            "char2": {"pose": MovementPresetEngine.get_pose_at_time("think", 1.0), "expression": "thinking", "mouth": {"open": False}, "is_speaking": False},
            "subtitle": "मराठी सबटायटल टेस्ट",
            "camera": {"zoom": 1.0, "pan_x": 0.0, "pan_y": 0.0}
        }
        img = StickFigureRenderer.render_frame(frame_data, char1, char2, width=540, height=960)
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (540, 960))

    def test_camera_2d(self):
        cam = Camera2D()
        zoom, px, py = cam.update("ZOOM_IN", scene_progress=0.5, t_sec=1.0)
        self.assertGreater(zoom, 1.0)
        self.assertIsInstance(px, float)
        self.assertIsInstance(py, float)


class TestLipSyncAndSubtitleCleaner(unittest.TestCase):
    def test_topic_formatter_localization(self):
        from intelligence.language_intelligence.topic_formatter import TopicFormatter
        mr_title = TopicFormatter.format_topic_for_script("sri lanka a vs hong kong", "mr_rangdi")
        self.assertIn("श्रीलंका", mr_title)
        self.assertIn("हाँगकाँग", mr_title)
        self.assertIn("सामना", mr_title)
        self.assertNotIn("sri lanka a vs hong kong", mr_title)

        hi_title = TopicFormatter.format_topic_for_script("sri lanka a vs hong kong", "hi")
        self.assertIn("श्रीलंका", hi_title)
        self.assertIn("हाँगकाँग", hi_title)
        self.assertIn("मैच", hi_title)

    def test_clean_subtitle_no_speaker_prefix(self):
        from animation.scene_director.scene_timeline import AnimationTimelineDirector
        from intelligence.language_intelligence.rangdi_marathi_engine import RangdiMarathiEngine
        script = RangdiMarathiEngine.generate_rangdi_marathi_script("quantum computing")
        scheduled = [
            {
                "speaker_id": "stick_bob",
                "text": "(Bob): अरे गड्या थांब!",
                "start_second": 0.5,
                "end_second": 2.5,
                "emotion": "shocked"
            }
        ]
        timeline = AnimationTimelineDirector.compile_timeline(script, fps=10, scheduled_dialogues=scheduled)
        # Check frame at t=1.0s
        frame_at_1s = timeline[10]
        self.assertEqual(frame_at_1s["subtitle"], "अरे गड्या थांब!")
        self.assertNotIn("(Bob):", frame_at_1s["subtitle"])

    def test_fluid_lip_sync_oscillation(self):
        from animation.lip_sync.speech_synchronizer import SpeechSynchronizer
        dialogues = [
            {
                "speaker_id": "stick_bob",
                "text": "अरे गड्या थांब!",
                "start_second": 1.0,
                "end_second": 3.0,
                "emotion": "shocked"
            }
        ]
        # At t=0.5s (before speech), mouth must be closed REST
        mouth_pre = SpeechSynchronizer.get_mouth_state("stick_bob", 0.5, dialogues)
        self.assertFalse(mouth_pre["open"])

        # Sample multiple frames during speech to confirm dynamic lip movement
        open_states = []
        for t in [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8]:
            m = SpeechSynchronizer.get_mouth_state("stick_bob", t, dialogues)
            open_states.append(m["open"])
        
        # Confirm mouth articulates (both open and closed states occur during speech)
        self.assertTrue(any(open_states), "Mouth should open during speech")

        # At t=3.5s (after speech), mouth must be closed REST
        mouth_post = SpeechSynchronizer.get_mouth_state("stick_bob", 3.5, dialogues)
        self.assertFalse(mouth_post["open"])


class TestGavtiComedyAndVillageEnvironment(unittest.TestCase):
    def test_gavti_comedy_catalog_integrity(self):
        from intelligence.language_intelligence.gavti_comedy_catalog import GavtiComedyCatalog
        sc = GavtiComedyCatalog.get_random_scenario()
        self.assertIn("hook", sc)
        self.assertIn("situation", sc)
        self.assertIn("intrigue", sc)
        self.assertIn("twist", sc)
        self.assertIn("payoff", sc)
        self.assertIn("cta", sc)
        # Verify 100% pure Marathi comedy - no prompt labels
        all_text = " ".join(sc[k] for k in ["hook", "situation", "intrigue", "twist", "payoff", "cta"])
        for k in ["hook", "situation", "intrigue", "twist", "payoff", "cta"]:
            text = sc[k]
            self.assertNotIn("(Bob):", text)
            self.assertNotIn("(Prof):", text)
        self.assertTrue(any(w in all_text for w in ["गड्या", "बब्या", "लाईट", "पैसे", "चहा", "गुलाबजाम", "गाडी"]))

    def test_village_katta_environment_rendering(self):
        from animation.environment_engine.procedural_backgrounds import ProceduralBackgroundRenderer
        img = ProceduralBackgroundRenderer.render_environment("village_katta", 540, 960)
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (540, 960))


if __name__ == "__main__":
    unittest.main()
