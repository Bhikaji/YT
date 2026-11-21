import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from animation.character_engine.character_model import StickFigureCharacter
from animation.skeleton_engine.movement_presets import MovementPresetEngine
from production.renderer.stick_renderer import StickFigureRenderer

def test():
    chars = StickFigureCharacter.get_canonical_library()
    bob = chars["stick_bob"]
    gampya = chars["stick_prof"]

    p_bob = MovementPresetEngine.get_pose_at_time("point", 1.5, root_x=450.0, root_y=450.0, facing_dir=1)
    p_gampya = MovementPresetEngine.get_pose_at_time("explain", 1.5, root_x=900.0, root_y=450.0, facing_dir=-1)

    frame_data = {
        "time_sec": 3.0,
        "environment": "night_terrace_ferris_wheel",
        "show_disclaimer": False,
        "char1": {
            "pose": p_bob,
            "expression": "shocked",
            "mouth": {"width": 24, "height": 18, "open": True, "shape": "oval_vertical"}
        },
        "char2": {
            "pose": p_gampya,
            "expression": "apologetic",
            "mouth": {"width": 18, "height": 2, "open": False, "shape": "neutral_line"}
        },
        "subtitle": "अर्रर्र गड्या! एवढ्या मोठ्या हॉटेलमध्ये आणून बसवलं आणि आता म्हणतो खिशात पाकीटच नाही!",
        "camera": {"zoom": 1.0, "pan_x": 0.0, "pan_y": 0.0}
    }

    img = StickFigureRenderer.render_frame(frame_data, bob, gampya, 1280, 720)
    out_path = Path("C:/Users/Mr.Scientist/.gemini/antigravity/brain/1ff6e728-5386-415c-b67c-5b2db0481163/test_night_terrace_frame.png")
    img.save(out_path)
    print("Saved test frame to:", out_path)

if __name__ == "__main__":
    test()
