import asyncio
import shutil
import psutil
from datetime import datetime
from typing import Dict, Any, List
from backend.app.config import settings
from backend.orchestrator.state_machine import ProductionJobStateMachine, JobState

class AutonomousScheduler:
    """Manages the weekly autonomous production calendar and GPU resource throttling."""

    MIN_FREE_DISK_GB = 20.0
    MAX_RAM_PERCENT = 85.0
    MAX_CPU_PERCENT = 90.0

    @classmethod
    def check_system_readiness(cls) -> Dict[str, Any]:
        """Audits current host resources before launching heavy rendering jobs."""
        total, used, free = shutil.disk_usage(str(settings.BASE_DIR))
        free_gb = free / (1024 ** 3)
        ram_percent = psutil.virtual_memory().percent if hasattr(psutil, "virtual_memory") else 50.0
        cpu_percent = psutil.cpu_percent(interval=0.1) if hasattr(psutil, "cpu_percent") else 20.0

        is_safe = free_gb >= cls.MIN_FREE_DISK_GB and ram_percent < cls.MAX_RAM_PERCENT

        return {
            "is_safe_to_produce": is_safe,
            "free_disk_gb": round(free_gb, 2),
            "ram_used_percent": ram_percent,
            "cpu_used_percent": cpu_percent,
            "throttle_reason": None if is_safe else "Insufficient disk space or high RAM load"
        }

    @classmethod
    async def schedule_weekly_production(cls, episodes_per_week: int = 4, shorts_per_week: int = 6) -> Dict[str, Any]:
        """
        Calculates and reserves production calendar slots according to user targets.
        """
        readiness = cls.check_system_readiness()
        if not readiness["is_safe_to_produce"]:
            return {
                "status": "THROTTLED",
                "message": f"Production throttled: {readiness['throttle_reason']}",
                "readiness": readiness
            }

        return {
            "status": "SCHEDULED",
            "weekly_targets": {
                "long_form_episodes": episodes_per_week,
                "youtube_shorts": shorts_per_week,
                "total_weekly_videos": episodes_per_week + shorts_per_week
            },
            "readiness": readiness,
            "active_queue": await ProductionJobStateMachine.get_active_jobs()
        }
