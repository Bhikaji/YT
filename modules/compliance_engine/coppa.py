"""
COPPA & YouTube Policy Compliance Engine
Enforces YouTube community guidelines, advertiser-friendly policies, and child safety laws.
"""

from typing import Dict, Any, List

class ComplianceAuditor:
    """Audits episodes for COPPA child safety classification and monetization eligibility."""

    BANNED_KEYWORD_PATTERNS = [
        "violence", "gore", "explicit", "hate", "nsfw"
    ]

    @classmethod
    def audit_episode(
        cls,
        title: str,
        description: str,
        target_audience: str = "Family & Teen",
        is_original_animation: bool = True
    ) -> Dict[str, Any]:
        """
        Validates metadata and ensures proper COPPA declaration ('made_for_kids' = False for general audience).
        """
        text_corpus = (title + " " + description).lower()
        violations = [kw for kw in cls.BANNED_KEYWORD_PATTERNS if kw in text_corpus]

        is_made_for_kids = target_audience.lower() in ["toddler", "preschool", "children_under_13"]
        advertiser_friendly = len(violations) == 0 and is_original_animation

        return {
            "compliant": len(violations) == 0,
            "advertiser_friendly": advertiser_friendly,
            "made_for_kids": is_made_for_kids,
            "target_audience": target_audience,
            "category_id": "1",  # Film & Animation
            "violations_found": violations,
            "original_ip_certified": is_original_animation
        }
