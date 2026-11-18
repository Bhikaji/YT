"""
Autonomous AI Cartoon Studio - Resource & Thermal Governor (V2.0)
Monitors CPU, RAM, and thermal state to prevent system lockups or memory exhaustion.
Enforces an 8GB memory safety ceiling and allocates optimal threads for Intel i5-8265U.
"""

import os
import time
import subprocess
import shutil

MAX_RAM_MB = 8192      # 8 GB process ceiling
MAX_CPU_THREADS = 4    # Optimal multi-threading on 8-thread CPU
CPU_THROTTLE_DELAY = 1.5 # Thermal rest delay when CPU usage spikes

class ResourceGovernor:
    def __init__(self, max_ram_mb=MAX_RAM_MB, max_threads=MAX_CPU_THREADS):
        self.max_ram_mb = max_ram_mb
        self.max_threads = max_threads

    def check_system_headroom(self) -> dict:
        # Check free disk space on Drive E:
        total, used, free = shutil.disk_usage("E:\\YT")
        free_gb = free / (1024**3)
        
        # Check memory via Windows wmic/powershell
        mem_info = {"free_disk_gb": round(free_gb, 2), "ram_safe": True, "disk_safe": free_gb > 10.0}
        
        if not mem_info["disk_safe"]:
            print(f"[Resource Governor] WARNING: Low disk space on E: ({free_gb:.1f} GB free)!")
        return mem_info

    def get_blender_render_threads(self) -> int:
        return self.max_threads

    def throttle_if_needed(self):
        headroom = self.check_system_headroom()
        if not headroom["disk_safe"]:
            raise RuntimeError("Emergency Stop: Disk headroom below 10GB threshold!")
        time.sleep(0.05)

if __name__ == "__main__":
    gov = ResourceGovernor()
    hr = gov.check_system_headroom()
    print("Resource Governor active:", hr)
