"""
Master Test Suite Runner
Executes all unit, integration, and quality control tests for Autonomous AI Cartoon Studio.
"""

import sys
import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def run_suite():
    print("=================================================================")
    print("        AUTONOMOUS AI CARTOON STUDIO - MASTER TEST SUITE         ")
    print("=================================================================")

    test_files = [
        "tests/unit/test_state_machine.py",
        "tests/unit/test_character_engine.py",
        "tests/unit/test_animation_and_rigging.py",
        "tests/unit/test_voice_and_lipsync.py",
        "tests/unit/test_scene_and_camera.py",
        "tests/unit/test_quality_control_gates.py"
    ]

    all_passed = True
    for test in test_files:
        print(f"\n[RUNNING] {test}...")
        res = subprocess.run([sys.executable, str(PROJECT_ROOT / test)], capture_output=True, text=True)
        print(res.stdout)
        if res.returncode != 0:
            print(f"✖ FAILED: {test}")
            print(res.stderr)
            all_passed = False
        else:
            print(f"✔ PASSED: {test}")

    print("\n=================================================================")
    if all_passed:
        print("    ALL 6 TEST MODULES PASSED WITH 100% SUCCESS! (READY)        ")
    else:
        print("    ONE OR MORE TESTS FAILED! CHECK OUTPUT ABOVE.              ")
    print("=================================================================")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(run_suite())
