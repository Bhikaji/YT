"""
YouTube Retention Analytics & Feedback Engine
Collects viewer retention metrics, drop-off points, and provides feedback to Showrunner.
"""

from typing import Dict, Any, List, Optional
import json

class AnalyticsFeedbackEngine:
    """Tracks audience retention curves and adjusts future episode pacing."""

    @classmethod
    def analyze_retention_curve(cls, retention_data: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Analyzes percentage of viewers watching at timestamp points.
        Identifies critical drop-off locations (e.g. > 15% drop in 3 seconds).
        """
        if not retention_data:
            return {"status": "NO_DATA", "recommendation": "Maintain high hook intensity in first 5s."}

        drop_offs = []
        for i in range(1, len(retention_data)):
            prev_pct = retention_data[i-1]["retention_pct"]
            curr_pct = retention_data[i]["retention_pct"]
            drop = prev_pct - curr_pct
            if drop >= 12.0:
                drop_offs.append({
                    "timestamp_s": retention_data[i]["timestamp_s"],
                    "drop_percentage": round(drop, 2),
                    "reason": "Pacing lull or scene transition delay"
                })

        return {
            "has_pacing_issues": len(drop_offs) > 0,
            "drop_off_count": len(drop_offs),
            "drop_offs": drop_offs,
            "feedback_for_showrunner": "Shorten dialogue pauses and increase visual action cuts." if drop_offs else "Optimal audience engagement curve."
        }
