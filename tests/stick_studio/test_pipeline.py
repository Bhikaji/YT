"""
Automated Integration and Unit Test Suite for Autonomous 2D Stick-Figure Animation Studio.
Tests discovery, topic scoring, script generation, skeletal kinematics, facial rigs,
procedural backgrounds, thumbnail creation, and quality control.
"""

import unittest
from pathlib import Path
from PIL import Image

from intelligence.trend_research.category_catalog import ContentCategoryCatalog
from intelligence.trend_research.trend_intelligence import TrendIntelligenceEngine
from intelligence.topic_scoring.trend_scorer import TrendScorer
from intelligence.topic_scoring.trend_classifier import TrendClassifier
from intelligence.script_generation.story_engine import StickStoryEngine
from intelligence.script_generation.script_evaluator import ScriptEvaluator
from animation.character_engine.character_model import StickFigureCharacter
from animation.skeleton_engine.stick_skeleton import StickSkeletonPose
from animation.skeleton_engine.forward_kinematics import ForwardKinematicsSolver
from animation.skeleton_engine.movement_presets import MovementPresetEngine
from animation.expression_engine.facial_rig import FacialRig
from animation.lip_sync.phoneme_mapper import PhonemeMapper
from animation.environment_engine.procedural_backgrounds import ProceduralBackgroundRenderer
from animation.camera_engine.camera_2d import Camera2D
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

    def test_camera_2d(self):
        cam = Camera2D()
        zoom, px, py = cam.update("ZOOM_IN", scene_progress=0.5, t_sec=1.0)
        self.assertGreater(zoom, 1.0)
        self.assertIsInstance(px, float)
        self.assertIsInstance(py, float)

    def test_qc_audit_on_rendered_short(self):
        video_path = Path("output/stick_shorts/stick_2c4d068f/stick_2c4d068f_master.mp4")
        thumb_path = Path("output/stick_shorts/stick_2c4d068f/thumbnails/thumb_concept_1.jpg")
        if video_path.exists() and thumb_path.exists():
            report = StickQCInspector.audit_short(video_path, thumb_path)
            self.assertTrue(report["passed"])
            self.assertEqual(report["quality_score"], 100.0)


if __name__ == "__main__":
    unittest.main()
