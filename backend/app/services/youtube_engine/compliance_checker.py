from typing import Dict, Any, List

class ComplianceChecker:
    """Pre-publication compliance audit for YouTube Monetization & Community Policies."""

    PROHIBITED_KEYWORDS = [
        "hack", "crack", "cheat", "free robux", "violence", "hate"
    ]

    @classmethod
    def audit_publication(
        cls,
        title: str,
        description: str,
        target_audience: str,
        is_original_animation: bool = True
    ) -> Dict[str, Any]:
        """
        Runs comprehensive compliance checks prior to video upload.
        """
        flags = []
        full_text = f"{title} {description}".lower()

        # 1. Prohibited Keywords Check
        for word in cls.PROHIBITED_KEYWORDS:
            if word in full_text:
                flags.append(f"Contains flagged keyword: '{word}'")

        # 2. Made For Kids (COPPA) Assessment
        # If targeted strictly at young children (< 13), COPPA flag MUST be True
        made_for_kids = False
        if "toddler" in target_audience.lower() or "preschool" in target_audience.lower() or "kids" in target_audience.lower():
            made_for_kids = True
        
        # 3. Monetization & Reused Content Guideline
        if not is_original_animation:
            flags.append("Warning: Content must contain original creative animation to qualify for YouTube Partner Program monetization.")

        # 4. Title & Metadata Quality Check
        if len(title.strip()) < 5:
            flags.append("Title too short.")
        if len(title) > 100:
            flags.append("Title exceeds YouTube 100-character limit.")

        is_passed = len(flags) == 0

        return {
            "passed": is_passed,
            "made_for_kids": made_for_kids,
            "flags": flags,
            "advertiser_friendly": is_passed and not made_for_kids,
            "recommendation": "Ready for upload" if is_passed else "Review flags before publishing"
        }
