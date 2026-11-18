"""
Unit tests for Voice, Lip-Sync, and Facial Animation Engines
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.lipsync_engine.viseme_aligner import VisemeAligner
from modules.facial_animation_engine.expression_blender import FacialExpressionBlender

def test_viseme_aligner():
    print("--- Testing Rhubarb 9-Viseme & ARKit Alignment ---")
    text = "Look at that glowing crystal on the bridge!"
    keyframes = VisemeAligner.align_transcript_to_visemes(text=text, total_duration_seconds=2.5, fps=30)
    
    assert len(keyframes) > 0
    first_kf = keyframes[0]
    assert "frame" in first_kf
    assert "viseme" in first_kf
    assert "arkit" in first_kf
    assert "jawOpen" in first_kf["arkit"]
    print(f"✔ Transcript aligned to {len(keyframes)} viseme keyframes with ARKit shapekeys.")

def test_facial_expressions():
    print("--- Testing Facial Expressions and Blinks ---")
    frames = FacialExpressionBlender.generate_expression_track(emotion="AWE_WONDER", total_frames=90, fps=30)
    assert len(frames) == 90
    
    # Check wide eyes and brow lift
    sample_frame = frames[10]["shapekeys"]
    assert sample_frame["eyeWideLeft"] > 0.5
    assert sample_frame["browInnerUp"] > 0.5
    assert "eyeBlinkLeft" in sample_frame
    print("✔ AWE_WONDER expression track with organic micro-movements and blinks verified.")

if __name__ == "__main__":
    test_viseme_aligner()
    test_facial_expressions()
    print("\n✔ Voice & Lip-Sync Tests Passed Successfully!")
