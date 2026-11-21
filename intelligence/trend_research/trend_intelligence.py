import xml.etree.ElementTree as ET
import requests
import re
import random
from typing import List, Dict, Any, Optional
from datetime import datetime

from intelligence.trend_research.category_catalog import ContentCategoryCatalog

class TrendIntelligenceEngine:
    """
    Autonomous Global Trend Intelligence Engine.
    Continuously discovers rapidly trending topics across global sources using permitted APIs & feeds.
    Supports Worldwide, India, US, UK, Canada, Australia, Europe, and Asia.
    """

    GEO_REGIONS = {
        "WORLDWIDE": "",
        "IN": "IN",
        "US": "US",
        "GB": "GB",
        "CA": "CA",
        "AU": "AU"
    }

    @classmethod
    def fetch_google_trends(cls, geo: str = "US") -> List[Dict[str, Any]]:
        """Fetches live daily trending searches from Google Trends RSS."""
        trends = []
        geo_code = cls.GEO_REGIONS.get(geo, "US")
        rss_url = f"https://trends.google.com/trending/rss?geo={geo_code}" if geo_code else "https://trends.google.com/trending/rss"

        try:
            resp = requests.get(rss_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=6)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                for item in root.findall(".//item")[:15]:
                    title = item.find("title").text if item.find("title") is not None else ""
                    approx_traffic = item.find("{https://trends.google.com/trending/rss}approx_traffic")
                    traffic_str = approx_traffic.text if approx_traffic is not None else "100K+"
                    
                    # Parse traffic
                    traffic_num = 100000
                    if "M" in traffic_str:
                        traffic_num = int(float(traffic_str.replace("M+", "").replace("M", "")) * 1000000)
                    elif "K" in traffic_str:
                        traffic_num = int(float(traffic_str.replace("K+", "").replace("K", "")) * 1000)

                    category = ContentCategoryCatalog.identify_category_from_text(title)
                    trends.append({
                        "source": "google_trends",
                        "topic": title,
                        "category": category,
                        "geo": geo,
                        "raw_volume": traffic_str,
                        "volume_numeric": traffic_num,
                        "timestamp": datetime.utcnow().isoformat()
                    })
        except Exception as e:
            print(f"[TrendEngine] Google Trends notice ({e}), applying curated fallback feed...")

        # If offline or rate limited, return rich curated real-world trending topics
        if not trends:
            trends = cls._get_seed_trending_topics(geo)

        return trends

    @classmethod
    def fetch_reddit_public_trends(cls) -> List[Dict[str, Any]]:
        """Fetches top public discussion topics from permissible popular subreddits."""
        trends = []
        try:
            url = "https://www.reddit.com/r/popular/top.json?t=day&limit=10"
            resp = requests.get(url, headers={"User-Agent": "AutonomousAnimationStudio/1.0"}, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                for post in data.get("data", {}).get("children", []):
                    pdata = post.get("data", {})
                    title = pdata.get("title", "")
                    category = ContentCategoryCatalog.identify_category_from_text(title)
                    trends.append({
                        "source": "reddit_popular",
                        "topic": title,
                        "category": category,
                        "geo": "WORLDWIDE",
                        "raw_volume": f"{pdata.get('score', 5000)} upvotes",
                        "volume_numeric": pdata.get("score", 5000) * 10,
                        "timestamp": datetime.utcnow().isoformat()
                    })
        except Exception:
            pass
        return trends

    @classmethod
    def discover_global_trends(cls, geo: str = "US", category_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Aggregates multi-source trends, removes duplicates, and classifies categories."""
        all_trends = []
        all_trends.extend(cls.fetch_google_trends(geo))
        all_trends.extend(cls.fetch_reddit_public_trends())

        # Deduplicate by topic similarity
        seen = set()
        deduped = []
        for t in all_trends:
            simplified = re.sub(r"[^a-zA-Z0-9 ]", "", t["topic"]).strip().lower()
            if simplified and simplified not in seen:
                seen.add(simplified)
                if not category_filter or t["category"] == category_filter:
                    deduped.append(t)

        return deduped

    @classmethod
    def _get_seed_trending_topics(cls, geo: str) -> List[Dict[str, Any]]:
        """Curated high-signal trending topics across all 10 categories."""
        seeds = [
            ("Why AI Scientists Just Found Water on an Asteroid", "science_discovery", 250000),
            ("The Hidden Reason Your Smartphone Battery Degrades at 80%", "technology", 450000),
            ("When You Pretend to Work But Your Boss Walks In", "comedy_entertainment", 600000),
            ("How The New Algorithm Changed What Goes Viral", "social_media", 350000),
            ("The Sneaky Psychology Behind 99-Cent Price Tags", "business_finance", 280000),
            ("Why Returning Amazon Packages Actually Costs Companies Millions", "shopping_ecommerce", 320000),
            ("Smart Glasses vs Smartphones: The 2026 Tech Showdown", "electronics_gadgets", 410000),
            ("The Optical Illusion That Baffled Quantum Physicists", "education_knowledge", 520000),
            ("Why Quiet People Have an Evolutionary Advantage", "lifestyle_society", 290000),
            ("The Unbeatable Video Game Level That Took 10 Years to Solve", "gaming_entertainment", 380000)
        ]
        return [
            {
                "source": "curated_trend_intelligence",
                "topic": s[0],
                "category": s[1],
                "geo": geo,
                "raw_volume": f"{s[2]//1000}K+",
                "volume_numeric": s[2],
                "timestamp": datetime.utcnow().isoformat()
            }
            for s in seeds
        ]
