"""
Intelligent Topic Formatter & Vernacular Transliteration Engine.
Transforms raw search queries and trending topic tags (e.g. 'sri lanka a vs hong kong')
into natural, grammatically correct spoken vernacular phrases in Marathi, Hindi, and English.
Prevents raw English search queries from being dumped awkwardly into vernacular dialogues.
"""

import re
from typing import Dict, Any

class TopicFormatter:
    """
    Cleans, transliterates, and localizes trending topic titles for screenplays.
    """

    TRANSLITERATION_MAP_MARATHI: Dict[str, str] = {
        "sri lanka": "श्रीलंका",
        "hong kong": "हाँगकाँग",
        "india": "भारत",
        "australia": "ऑस्ट्रेलिया",
        "pakistan": "पाकिस्तान",
        "england": "इंग्लंड",
        "bangladesh": "बांगलादेश",
        "new zealand": "न्यूझीलंड",
        "south africa": "दक्षिण आफ्रिका",
        "west indies": "वेस्ट इंडीज",
        "afghanistan": "अफगाणिस्तान",
        "cricket": "क्रिकेट",
        "world cup": "वर्ल्ड कप",
        "match": "सामना",
        "ai": "एआय (AI)",
        "artificial intelligence": "कृत्रिम बुद्धिमत्ता",
        "quantum computing": "क्वांटम कॉम्प्युटर",
        "black hole": "ब्लॅक होल",
        "mars": "मंगळ ग्रह",
        "moon": "चंद्र",
        "nasa": "नासा",
        "isro": "इस्रो",
        "robot": "रोबोट",
        "iphone": "आयफोन",
        "smartphone": "स्मार्टफोन",
        "electric vehicle": "इलेक्ट्रिक गाडी",
        "cybersecurity": "सायबर सुरक्षा"
    }

    TRANSLITERATION_MAP_HINDI: Dict[str, str] = {
        "sri lanka": "श्रीलंका",
        "hong kong": "हाँगकाँग",
        "india": "भारत",
        "australia": "ऑस्ट्रेलिया",
        "pakistan": "पाकिस्तान",
        "england": "इंग्लैंड",
        "bangladesh": "बांग्लादेश",
        "new zealand": "न्यूजीलैंड",
        "south africa": "दक्षिण अफ्रीका",
        "west indies": "वेस्ट इंडीज",
        "afghanistan": "अफगानिस्तान",
        "cricket": "क्रिकेट",
        "world cup": "वर्ल्ड कप",
        "match": "मैच",
        "ai": "एआई (AI)",
        "artificial intelligence": "आर्टिफिशियल इंटेलिजेंस",
        "quantum computing": "क्वांटम कंप्यूटर",
        "black hole": "ब्लैक होल",
        "mars": "मंगल ग्रह",
        "moon": "चाँद",
        "nasa": "नासा",
        "isro": "इसरो",
        "robot": "रोबोट",
        "iphone": "आईफोन",
        "smartphone": "स्मार्टफोन",
        "electric vehicle": "इलेक्ट्रिक गाड़ी",
        "cybersecurity": "साइबर सुरक्षा"
    }

    @classmethod
    def format_topic_for_script(cls, raw_topic: str, language: str = "mr_rangdi") -> str:
        """
        Transforms raw trend query into a polished, natural vernacular spoken title.
        """
        # 1. Clean query noise
        cleaned = raw_topic.strip()
        cleaned = re.sub(r'^(Why|How|What|Is|Can|When|Where)\s+', '', cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.strip("?!. :,-")

        # 2. Check for sports / match "vs" pattern (e.g. "sri lanka a vs hong kong")
        vs_match = re.search(r'^(.*?)\s+(?:a\s+)?(?:vs\.?|versus)\s+(.*?)$', cleaned, flags=re.IGNORECASE)
        if vs_match:
            team1_raw = vs_match.group(1).strip()
            team2_raw = vs_match.group(2).strip()

            if language.startswith("mr"):
                # Marathi sports match phrasing
                t1 = cls._transliterate(team1_raw, cls.TRANSLITERATION_MAP_MARATHI)
                t2 = cls._transliterate(team2_raw, cls.TRANSLITERATION_MAP_MARATHI)
                return f"{t1} विरुद्ध {t2} सामना"
            elif language.startswith("hi"):
                # Hindi sports match phrasing
                t1 = cls._transliterate(team1_raw, cls.TRANSLITERATION_MAP_HINDI)
                t2 = cls._transliterate(team2_raw, cls.TRANSLITERATION_MAP_HINDI)
                return f"{t1} बनाम {t2} मैच"
            else:
                return f"{team1_raw.title()} vs {team2_raw.title()} Match"

        # 3. General topic transliteration and beautification
        if language.startswith("mr"):
            return cls._transliterate(cleaned, cls.TRANSLITERATION_MAP_MARATHI)
        elif language.startswith("hi"):
            return cls._transliterate(cleaned, cls.TRANSLITERATION_MAP_HINDI)
        else:
            return cleaned.title()

    @classmethod
    def _transliterate(cls, text: str, word_map: Dict[str, str]) -> str:
        """Replaces known phrases or words with vernacular translations."""
        lowered = text.lower()
        # Direct full match
        if lowered in word_map:
            return word_map[lowered]

        # Multi-word substring replacement
        result = lowered
        for k, v in sorted(word_map.items(), key=lambda x: len(x[0]), reverse=True):
            if k in result:
                result = re.sub(r'\b' + re.escape(k) + r'\b', v, result)

        # If unchanged and mostly ascii, return title-cased English
        if result == lowered and not any(ord(c) > 127 for c in result):
            return text.title()

        return result
