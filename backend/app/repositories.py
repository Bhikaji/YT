import uuid
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import aiosqlite
from backend.app.database import DB_FILE

class SeriesRepo:
    @staticmethod
    async def create(data: Dict[str, Any]) -> Dict[str, Any]:
        s_id = str(uuid.uuid4())
        season_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        async with aiosqlite.connect(str(DB_FILE)) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("""
                INSERT INTO series (id, title, description, genre, target_audience, art_style_preset, world_lore, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s_id,
                data["title"],
                data.get("description", ""),
                data.get("genre", "Adventure"),
                data.get("target_audience", "Family & Teen"),
                data.get("art_style_preset", "Pixar_Stylized_3D"),
                json.dumps(data.get("world_lore", {})),
                now, now
            ))
            
            # Create Season 1
            await db.execute("""
                INSERT INTO seasons (id, series_id, season_number, title, story_arc_summary, created_at)
                VALUES (?, ?, 1, 'Season 1', 'Genesis Arc', ?)
            """, (season_id, s_id, now))
            
            await db.commit()
            return await SeriesRepo.get_by_id(s_id)

    @staticmethod
    async def get_by_id(series_id: str) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(str(DB_FILE)) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM series WHERE id = ?", (series_id,))
            row = await cursor.fetchone()
            if not row:
                return None
            res = dict(row)
            res["world_lore"] = json.loads(res["world_lore"])
            return res

    @staticmethod
    async def list_all() -> List[Dict[str, Any]]:
        async with aiosqlite.connect(str(DB_FILE)) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM series ORDER BY created_at DESC")
            rows = await cursor.fetchall()
            result = []
            for r in rows:
                item = dict(r)
                item["world_lore"] = json.loads(item["world_lore"])
                result.append(item)
            return result

class CharacterRepo:
    @staticmethod
    async def create(data: Dict[str, Any]) -> Dict[str, Any]:
        c_id = str(uuid.uuid4())
        v_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        async with aiosqlite.connect(str(DB_FILE)) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("""
                INSERT INTO characters (
                    id, series_id, name, role, age_category, personality_summary,
                    speaking_style, background_story, character_relationships, physical_specs,
                    blend_model_path, rig_type, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                c_id,
                data["series_id"],
                data["name"],
                data.get("role", "PROTAGONIST"),
                data.get("age_category", "TEEN"),
                data.get("personality_summary", ""),
                data.get("speaking_style", "energetic"),
                data.get("background_story", ""),
                json.dumps(data.get("character_relationships", {})),
                json.dumps(data.get("physical_specs", {})),
                data.get("blend_model_path", ""),
                data.get("rig_type", "RIGIFY_ARKit52"),
                now, now
            ))

            if "voice" in data and data["voice"]:
                v = data["voice"]
                await db.execute("""
                    INSERT INTO character_voices (
                        id, character_id, provider, voice_identifier, pitch_adjustment,
                        rate_adjustment, volume_adjustment, emotion_presets, reference_audio_path, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    v_id, c_id,
                    v.get("provider", "edge_tts"),
                    v.get("voice_identifier", "en-US-ChristopherNeural"),
                    v.get("pitch_adjustment", "+0Hz"),
                    v.get("rate_adjustment", "+0%"),
                    v.get("volume_adjustment", "+0%"),
                    json.dumps(v.get("emotion_presets", {})),
                    v.get("reference_audio_path", ""),
                    now
                ))

            await db.commit()
            return await CharacterRepo.get_by_id(c_id)

    @staticmethod
    async def get_by_id(char_id: str) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(str(DB_FILE)) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM characters WHERE id = ?", (char_id,))
            row = await cursor.fetchone()
            if not row:
                return None
            res = dict(row)
            res["character_relationships"] = json.loads(res["character_relationships"])
            res["physical_specs"] = json.loads(res["physical_specs"])
            return res

    @staticmethod
    async def list_by_series(series_id: str) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(str(DB_FILE)) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM characters WHERE series_id = ?", (series_id,))
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

class EpisodeRepo:
    @staticmethod
    async def create(data: Dict[str, Any]) -> Dict[str, Any]:
        ep_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        async with aiosqlite.connect(str(DB_FILE)) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("""
                INSERT INTO episodes (
                    id, season_id, episode_number, title, format, target_duration_seconds,
                    status, synopsis, script_structured, cliffhanger_question, next_episode_teaser,
                    final_video_path, primary_thumbnail_path, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ep_id,
                data.get("season_id", "s1"),
                data.get("episode_number", 1),
                data["title"],
                data.get("format", "SHORT"),
                data.get("target_duration_seconds", 45),
                data.get("status", "COMPLETED"),
                data.get("synopsis", ""),
                json.dumps(data.get("script_structured", {})),
                data.get("cliffhanger_question", ""),
                data.get("next_episode_teaser", ""),
                data.get("final_video_path", ""),
                data.get("primary_thumbnail_path", ""),
                now, now
            ))
            await db.commit()
            return await EpisodeRepo.get_by_id(ep_id)

    @staticmethod
    async def get_by_id(ep_id: str) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(str(DB_FILE)) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM episodes WHERE id = ?", (ep_id,))
            row = await cursor.fetchone()
            if not row:
                return None
            res = dict(row)
            if res.get("script_structured"):
                res["script_structured"] = json.loads(res["script_structured"])
            return res
