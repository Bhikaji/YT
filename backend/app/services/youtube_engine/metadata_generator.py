from typing import List, Dict, Any

class MetadataGenerator:
    """Generates high-CTR, SEO-optimized YouTube titles, descriptions, and tags."""

    @staticmethod
    def generate_metadata(
        series_title: str,
        episode_number: int,
        episode_title: str,
        cliffhanger_question: str,
        synopsis: str,
        format_type: str = "SHORT"
    ) -> Dict[str, Any]:
        
        if format_type == "SHORT":
            title = f"{episode_title} 😱 | {series_title} Ep.{episode_number} #shorts #animation"
            if len(title) > 95:
                title = f"{episode_title} 😱 Ep.{episode_number} #shorts"
        else:
            title = f"{series_title} - Episode {episode_number}: {episode_title} (3D Animated Series)"

        description = (
            f"{synopsis}\n\n"
            f"❓ BURNING QUESTION: {cliffhanger_question}\n"
            f"What do you think happens next? Tell us in the comments below!\n\n"
            f"🎬 Series: {series_title}\n"
            f"📅 Episode: #{episode_number}\n\n"
            f"Subscribe and ring the notification bell to see what happens in the next episode!\n\n"
            f"#3Danimation #cartoon #storytime #animation #blender #animatedseries"
        )

        tags = [
            series_title.lower(),
            "3d animation",
            "animated series",
            "cartoon",
            "blender animation",
            "mystery cartoon",
            "shorts",
            f"episode {episode_number}"
        ]

        return {
            "title": title,
            "description": description,
            "tags": tags,
            "category_id": "1"  # Film & Animation
        }
