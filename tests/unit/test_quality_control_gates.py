"""
Unit tests for Quality Control (9 Gates), Compliance, and Analytics Engines
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.quality_control.inspector import QualityControlInspector
from modules.compliance_engine.coppa import ComplianceAuditor
from modules.analytics_engine.collector import AnalyticsFeedbackEngine

def test_quality_control_9_gates():
    print("--- Testing Quality Control 9 Inspection Gates ---")
    mock_script = {
        "scenes": [{"scene_id": 1}],
        "cliffhanger_question": "Will Leo escape the glowing cavern?"
    }
    # Test video path
    video_path = str(PROJECT_ROOT / "output" / "shorts" / "demo_pixar_characters.mp4")
    audio_path = str(PROJECT_ROOT / "assets" / "audio" / "voices" / "ep_1_8644659358034629307" / "master_dialogue.mp3")
    thumb_path = str(PROJECT_ROOT / "assets" / "thumbnails" / "demo_pixar_characters_thumb.jpg")
    
    mock_meta = {
        "title": "Shadow Island: The Whispering Cavern #Shorts",
        "description": "Leo and Lumi explore the mysterious bioluminescent cave."
    }

    result = QualityControlInspector.audit_episode(
        script_data=mock_script,
        video_path=video_path,
        audio_path=audio_path,
        thumbnail_path=thumb_path,
        metadata=mock_meta,
        format_type="SHORT"
    )

    assert result["total_gates"] == 9
    assert result["gates_passed"] == 9
    assert result["overall_status"] == "PASSED"
    assert result["ready_for_publish"] is True
    print(f"✔ All {result['gates_passed']}/{result['total_gates']} Quality Control Gates passed.")

def test_compliance():
    print("--- Testing COPPA & YouTube Compliance ---")
    res = ComplianceAuditor.audit_episode(
        title="The Mystery of Shadow Island",
        description="Epic 3D animated adventure following Leo and Lumi.",
        target_audience="Family & Teen",
        is_original_animation=True
    )
    assert res["compliant"] is True
    assert res["made_for_kids"] is False  # General family/teen audience
    assert res["category_id"] == "1"
    print("✔ Compliance audit validated COPPA and advertiser-friendly status.")

def test_analytics_feedback():
    print("--- Testing Analytics Drop-off Detector ---")
    mock_retention = [
        {"timestamp_s": 0.0, "retention_pct": 100.0},
        {"timestamp_s": 5.0, "retention_pct": 92.0},
        {"timestamp_s": 10.0, "retention_pct": 89.0},
        {"timestamp_s": 15.0, "retention_pct": 72.0},  # 17% drop
        {"timestamp_s": 20.0, "retention_pct": 68.0}
    ]
    analysis = AnalyticsFeedbackEngine.analyze_retention_curve(mock_retention)
    assert analysis["has_pacing_issues"] is True
    assert analysis["drop_off_count"] == 1
    assert "Shorten dialogue pauses" in analysis["feedback_for_showrunner"]
    print("✔ Audience retention drop-off successfully flagged pacing feedback.")

if __name__ == "__main__":
    test_quality_control_9_gates()
    test_compliance()
    test_analytics_feedback()
    print("\n✔ Quality Control, Compliance & Analytics Tests Passed Successfully!")
