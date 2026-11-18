import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from backend.app.config import settings

class RenderManager:
    """Orchestrates genuine 3D rendering with Blender LTS (EEVEE-Next)."""

    @staticmethod
    def find_blender_binary() -> Optional[str]:
        if settings.BLENDER_EXECUTABLE_PATH and os.path.exists(settings.BLENDER_EXECUTABLE_PATH):
            return settings.BLENDER_EXECUTABLE_PATH
        which_blender = shutil.which("blender")
        if which_blender:
            return which_blender
        candidates = [
            r"E:\YT\tools\blender\blender-4.2.16-windows-x64\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
        ]
        tools_blender_dir = Path("E:/YT/tools/blender")
        if tools_blender_dir.exists():
            for p in tools_blender_dir.rglob("blender.exe"):
                if p.is_file():
                    return str(p)

        for c in candidates:
            if os.path.exists(c):
                return c
        return None

    @classmethod
    def execute_blender_render(
        cls,
        bpy_script_path: str,
        timeout_seconds: int = 1800
    ) -> bool:
        """Executes a Blender headless automation script."""
        blender_bin = cls.find_blender_binary()
        if not blender_bin:
            raise RuntimeError("Blender 4.2 LTS binary not found! Please ensure Blender is installed at E:\\YT\\tools\\blender.")

        print(f"[RenderManager] Launching Blender headless: {blender_bin} -b -P {bpy_script_path}")
        result = subprocess.run(
            [blender_bin, "-b", "-P", bpy_script_path],
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )
        if result.returncode != 0:
            print(f"[RenderManager] Blender render error:\n{result.stderr}")
            return False

        print("[RenderManager] Blender headless 3D render completed successfully.")
        return True
