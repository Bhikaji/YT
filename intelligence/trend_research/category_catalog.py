from typing import List, Dict, Any, Optional

class ContentCategoryCatalog:
    """
    Modular Global Content Category Catalog.
    Supports all 10 major categories and enables dynamic registration of new domains.
    """

    CATEGORIES: Dict[str, Dict[str, Any]] = {
        "science_discovery": {
            "name": "Science and Discovery",
            "icon": "flask-conical",
            "subcategories": [
                "Space exploration", "NASA and astronomy", "Black holes",
                "Artificial intelligence research", "Human biology", "Medical discoveries",
                "Physics and chemistry", "Scientific experiments", "Robotics",
                "Future technologies", "Environmental science", "Climate discoveries"
            ],
            "keywords": ["science", "space", "discovery", "astronomy", "biology", "physics", "quantum", "robotics", "experiment"],
            "target_tone": "wonder_and_insight"
        },
        "technology": {
            "name": "Technology",
            "icon": "cpu",
            "subcategories": [
                "Artificial intelligence", "Machine learning", "Robotics",
                "Smartphones", "Computers and laptops", "Software development",
                "Cybersecurity", "Gaming technology", "Electric vehicles",
                "Smart devices", "Future inventions", "Emerging startups"
            ],
            "keywords": ["tech", "ai", "software", "gadget", "cybersecurity", "ev", "hardware", "apps", "coding"],
            "target_tone": "futuristic_and_smart"
        },
        "comedy_entertainment": {
            "name": "Comedy and Entertainment",
            "icon": "smile",
            "subcategories": [
                "Funny everyday situations", "Office comedy", "School and college comedy",
                "Family comedy", "Relationship humour", "Situational comedy",
                "Unexpected reactions", "Funny misunderstandings", "Character-based comedy", "Clever visual jokes"
            ],
            "keywords": ["funny", "comedy", "hilarious", "meme", "relatable", "joke", "prank", "awkward"],
            "target_tone": "humorous_and_punchy"
        },
        "social_media": {
            "name": "Social Media",
            "icon": "share-2",
            "subcategories": [
                "Instagram trends", "YouTube trends", "Facebook trends",
                "TikTok trends", "Viral challenges", "Influencer culture",
                "Social media behaviour", "Online scams", "Digital privacy",
                "Social media algorithms", "Creator economy"
            ],
            "keywords": ["viral", "instagram", "tiktok", "youtube", "algorithm", "influencer", "challenge", "scam"],
            "target_tone": "trendy_and_alert"
        },
        "shopping_ecommerce": {
            "name": "Shopping and E-commerce",
            "icon": "shopping-cart",
            "subcategories": [
                "Amazon shopping trends", "Flipkart shopping trends", "Online shopping mistakes",
                "Product comparisons", "Shopping hacks", "Consumer behaviour",
                "Fashion trends", "Trending gadgets", "Budget shopping",
                "Unusual products", "Customer experiences"
            ],
            "keywords": ["shopping", "amazon", "haul", "review", "discount", "deal", "unboxing", "budget"],
            "target_tone": "relatable_and_practical"
        },
        "electronics_gadgets": {
            "name": "Electronics and Gadgets",
            "icon": "smartphone",
            "subcategories": [
                "Smartphones", "Smart TVs", "Headphones", "Smartwatches",
                "Cameras", "Home appliances", "Gaming consoles",
                "Electronic innovations", "Hidden gadget features", "Future electronics"
            ],
            "keywords": ["gadgets", "phone", "iphone", "android", "console", "specs", "features", "hardware"],
            "target_tone": "informative_and_enthusiastic"
        },
        "business_finance": {
            "name": "Business and Finance",
            "icon": "trending-up",
            "subcategories": [
                "Startups", "Entrepreneurship", "Business success stories",
                "Business failures", "Marketing psychology", "Stock market education",
                "Cryptocurrency education", "Personal finance education",
                "Consumer economics", "Future business opportunities"
            ],
            "keywords": ["money", "business", "startup", "finance", "investing", "crypto", "marketing", "stocks"],
            "target_tone": "sharp_and_valuable"
        },
        "education_knowledge": {
            "name": "Education and Knowledge",
            "icon": "book-open",
            "subcategories": [
                "Interesting facts", "History", "Geography", "Mathematics",
                "Psychology", "General knowledge", "Human behaviour",
                "Communication skills", "Career guidance", "Learning techniques"
            ],
            "keywords": ["facts", "history", "psychology", "didyouknow", "knowledge", "curiosity", "mindblowing"],
            "target_tone": "curious_and_educational"
        },
        "lifestyle_society": {
            "name": "Lifestyle and Society",
            "icon": "heart",
            "subcategories": [
                "Family life", "Relationships", "Workplace behaviour",
                "Social problems", "Daily life challenges", "Human psychology",
                "Cultural differences", "Public awareness", "Environmental responsibility"
            ],
            "keywords": ["lifestyle", "habits", "relationships", "culture", "work", "wellness", "life"],
            "target_tone": "empathetic_and_observational"
        },
        "gaming_entertainment": {
            "name": "Gaming and Pop Culture",
            "icon": "gamepad-2",
            "subcategories": [
                "Trending games", "Gamer problems", "Retro gaming", "Esports",
                "Game mechanics", "Movies and cinema", "Anime culture", "Easter eggs"
            ],
            "keywords": ["gaming", "gamer", "games", "playstation", "xbox", "nintendo", "pc", "eastereggs"],
            "target_tone": "playful_and_energetic"
        }
    }

    @classmethod
    def get_all_categories(cls) -> Dict[str, Dict[str, Any]]:
        return cls.CATEGORIES

    @classmethod
    def get_category_by_id(cls, cat_id: str) -> Optional[Dict[str, Any]]:
        return cls.CATEGORIES.get(cat_id)

    @classmethod
    def identify_category_from_text(cls, text: str) -> str:
        """Determines best-matching category for a given text or headline."""
        text_lower = text.lower()
        scored = {}
        for cat_id, data in cls.CATEGORIES.items():
            score = 0
            for kw in data["keywords"]:
                if kw in text_lower:
                    score += 2
            for sub in data["subcategories"]:
                if sub.lower() in text_lower:
                    score += 5
            scored[cat_id] = score
        
        best = max(scored.items(), key=lambda x: x[1])
        return best[0] if best[1] > 0 else "education_knowledge"

    @classmethod
    def register_custom_category(cls, cat_id: str, name: str, subcategories: List[str], keywords: List[str], icon: str = "sparkles"):
        cls.CATEGORIES[cat_id] = {
            "name": name,
            "icon": icon,
            "subcategories": subcategories,
            "keywords": keywords,
            "target_tone": "engaging"
        }
