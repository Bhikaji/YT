"""
Autonomous AI Cartoon Studio - Character Version & DNA Manager (V2.0)
Maintains character identity continuity, seed consistency, wardrobe configs, and versions across episodes.
"""

import json
from pathlib import Path
import sqlite3

DB_PATH = Path(r"E:\YT\database\studio_v2.db")
CHAR_DNA_DIR = Path(r"E:\YT\assets\characters\dna")

class CharacterVersionManager:
    def __init__(self, db_path=DB_PATH, dna_dir=CHAR_DNA_DIR):
        self.db_path = db_path
        self.dna_dir = dna_dir
        self.dna_dir.mkdir(parents=True, exist_ok=True)

    def register_character_dna(self, character_id: str, name: str, archetype: str,
                               voice_profile_id: str, proportions: dict, 
                               wardrobe_palette: dict, bio_lore: str) -> dict:
        dna = {
            "character_id": character_id,
            "name": name,
            "archetype": archetype,
            "voice_profile_id": voice_profile_id,
            "proportions": proportions,
            "wardrobe_palette": wardrobe_palette,
            "bio_lore": bio_lore,
            "version": "2.0.0"
        }
        
        file_path = self.dna_dir / f"{character_id}_dna.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(dna, f, indent=2)

        # Register in SQLite
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO characters (
                character_id, asset_id, name, archetype, voice_profile_id, bio_lore
            ) VALUES (?, ?, ?, ?, ?, ?)
            """, (character_id, f"asset_{character_id}", name, archetype, voice_profile_id, bio_lore))
            conn.commit()

        print(f"[Character Version Manager] Registered DNA for '{name}' ({character_id}).")
        return dna

    def get_character_dna(self, character_id: str) -> dict:
        file_path = self.dna_dir / f"{character_id}_dna.json"
        if not file_path.exists():
            raise FileNotFoundError(f"DNA manifest not found for character: {character_id}")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

if __name__ == "__main__":
    cvm = CharacterVersionManager()
    leo_dna = cvm.register_character_dna(
        "char_leo", "Leo", "hero", "voice_leo_cheerful_boy",
        proportions={"height_meters": 1.25, "eye_scale": 1.35, "head_scale": 1.15},
        wardrobe_palette={"hoodie": "#D92E20", "jeans": "#223B68", "boots": "#332014", "hair": "#422312"},
        bio_lore="A curious, spirited young explorer equipped with a glowing crystal compass and red knitted hoodie."
    )
    lumi_dna = cvm.register_character_dna(
        "char_lumi", "Lumi", "companion", "voice_lumi_magical_fox",
        proportions={"height_meters": 0.45, "tail_fluff_scale": 1.4},
        wardrobe_palette={"fur_primary": "#FF75D8", "fur_tail_tip": "#4DEEEA"},
        bio_lore="A playful bioluminescent fox spirit attuned to the ancient crystal caverns."
    )
    print("Registered Core Characters:", leo_dna["name"], "&", lumi_dna["name"])
