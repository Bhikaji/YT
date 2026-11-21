from typing import Dict, Any, List

class TrendScorer:
    """
    Computes the Trend Opportunity Score (0 - 100) using the 7-factor weighted model:
    - Search interest growth: 20%
    - Audience interest: 20%
    - Engagement potential: 15%
    - Trend freshness: 15%
    - Competition opportunity: 10%
    - Global relevance: 10%
    - Storytelling potential: 10%
    """

    DEFAULT_WEIGHTS = {
        "search_growth": 0.20,
        "audience_interest": 0.20,
        "engagement_potential": 0.15,
        "trend_freshness": 0.15,
        "competition_opportunity": 0.10,
        "global_relevance": 0.10,
        "storytelling_potential": 0.10
    }

    @classmethod
    def calculate_opportunity_score(
        cls,
        topic: str,
        category: str,
        volume_numeric: int = 100000,
        custom_weights: Dict[str, float] = None
    ) -> Dict[str, Any]:
        weights = custom_weights or cls.DEFAULT_WEIGHTS

        # 1. Search growth (based on volume magnitude)
        search_growth = min(100.0, (volume_numeric / 500000) * 100)

        # 2. Audience interest (topic length & hook trigger keywords)
        hook_triggers = ["why", "how", "secret", "hidden", "mistake", "vs", "new", "truth", "shocking"]
        matches = sum(1 for w in hook_triggers if w in topic.lower())
        audience_interest = min(100.0, 50.0 + (matches * 15.0))

        # 3. Engagement potential (comedy & tech naturally get higher comment velocity)
        category_boost = {
            "comedy_entertainment": 95.0,
            "technology": 90.0,
            "social_media": 88.0,
            "science_discovery": 85.0,
            "business_finance": 82.0,
            "education_knowledge": 80.0,
            "electronics_gadgets": 84.0,
            "shopping_ecommerce": 78.0,
            "lifestyle_society": 76.0,
            "gaming_entertainment": 88.0
        }
        engagement_potential = category_boost.get(category, 75.0)

        # 4. Trend Freshness (defaults high for newly parsed topics)
        trend_freshness = 92.0

        # 5. Competition opportunity (inverse of oversaturation)
        competition_opportunity = 80.0

        # 6. Global relevance
        global_relevance = 90.0 if any(k in topic.lower() for k in ["ai", "space", "smartphone", "boss", "work", "money"]) else 75.0

        # 7. Storytelling potential (can two stick figures debate/act this out?)
        storytelling_potential = 92.0 if any(q in topic.lower() for q in ["why", "how", "when", "vs", "secret"]) else 80.0

        raw_score = (
            search_growth * weights["search_growth"] +
            audience_interest * weights["audience_interest"] +
            engagement_potential * weights["engagement_potential"] +
            trend_freshness * weights["trend_freshness"] +
            competition_opportunity * weights["competition_opportunity"] +
            global_relevance * weights["global_relevance"] +
            storytelling_potential * weights["storytelling_potential"]
        )

        final_score = round(min(100.0, max(10.0, raw_score)), 1)

        return {
            "opportunity_score": final_score,
            "factor_breakdown": {
                "search_growth": round(search_growth, 1),
                "audience_interest": round(audience_interest, 1),
                "engagement_potential": round(engagement_potential, 1),
                "trend_freshness": round(trend_freshness, 1),
                "competition_opportunity": round(competition_opportunity, 1),
                "global_relevance": round(global_relevance, 1),
                "storytelling_potential": round(storytelling_potential, 1)
            }
        }
