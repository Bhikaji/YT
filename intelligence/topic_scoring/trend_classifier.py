class TrendClassifier:
    """
    Classifies trends into:
    - EMERGING: Early acceleration, high upside
    - RAPIDLY_GROWING: Fast breakout phase
    - VIRAL: Peak mass attention
    - EVERGREEN: Consistent baseline interest
    - SEASONAL: Holiday/calendar recurring
    - DECLINING: Fading momentum
    - OVERSATURATED: High competition, low originality potential
    """

    @classmethod
    def classify_trend(cls, topic: str, opportunity_score: float, volume_numeric: int) -> str:
        t_lower = topic.lower()

        if any(w in t_lower for w in ["ai", "quantum", "2026", "breakthrough", "discovery"]):
            return "EMERGING"
        elif opportunity_score >= 85.0 and volume_numeric >= 400000:
            return "VIRAL"
        elif opportunity_score >= 75.0:
            return "RAPIDLY_GROWING"
        elif any(w in t_lower for w in ["why", "how to", "psychology", "money", "battery"]):
            return "EVERGREEN"
        elif any(w in t_lower for w in ["christmas", "summer", "black friday", "new year"]):
            return "SEASONAL"
        elif volume_numeric < 50000:
            return "DECLINING"
        else:
            return "RAPIDLY_GROWING"
