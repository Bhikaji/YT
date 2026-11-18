import os
import aiosqlite
import json
from pathlib import Path
from typing import AsyncGenerator
from backend.app.config import settings

DB_FILE = settings.DATA_DIR / "cartoon_studio.db"

async def get_db_connection() -> AsyncGenerator[aiosqlite.Connection, None]:
    """Dependency for providing an async SQLite connection."""
    conn = await aiosqlite.connect(str(DB_FILE))
    conn.row_factory = aiosqlite.Row
    try:
        yield conn
    finally:
        await conn.close()

async def init_db():
    """Initializes the database tables using aiosqlite."""
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(str(DB_FILE)) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        
        # 1. Series Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS series (
                id TEXT PRIMARY KEY,
                title TEXT UNIQUE NOT NULL,
                description TEXT,
                genre TEXT NOT NULL,
                target_audience TEXT NOT NULL,
                art_style_preset TEXT NOT NULL,
                world_lore TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 2. Seasons Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS seasons (
                id TEXT PRIMARY KEY,
                series_id TEXT NOT NULL REFERENCES series(id) ON DELETE CASCADE,
                season_number INTEGER NOT NULL,
                title TEXT,
                story_arc_summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 3. Characters Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id TEXT PRIMARY KEY,
                series_id TEXT NOT NULL REFERENCES series(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                age_category TEXT NOT NULL,
                personality_summary TEXT NOT NULL,
                speaking_style TEXT NOT NULL,
                background_story TEXT,
                character_relationships TEXT NOT NULL,
                physical_specs TEXT NOT NULL,
                blend_model_path TEXT,
                rig_type TEXT NOT NULL,
                texture_dir_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 4. Character Voices Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS character_voices (
                id TEXT PRIMARY KEY,
                character_id TEXT UNIQUE NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
                provider TEXT NOT NULL,
                voice_identifier TEXT NOT NULL,
                pitch_adjustment TEXT NOT NULL,
                rate_adjustment TEXT NOT NULL,
                volume_adjustment TEXT NOT NULL,
                emotion_presets TEXT NOT NULL,
                reference_audio_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 5. Episodes Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                id TEXT PRIMARY KEY,
                season_id TEXT NOT NULL REFERENCES seasons(id) ON DELETE CASCADE,
                episode_number INTEGER NOT NULL,
                title TEXT NOT NULL,
                format TEXT NOT NULL,
                target_duration_seconds INTEGER NOT NULL,
                status TEXT NOT NULL,
                synopsis TEXT,
                script_structured TEXT,
                cliffhanger_question TEXT NOT NULL,
                next_episode_teaser TEXT,
                rendered_frames_dir TEXT,
                final_video_path TEXT,
                primary_thumbnail_path TEXT,
                production_cost_usd REAL DEFAULT 0.0,
                render_duration_seconds REAL DEFAULT 0.0,
                error_log TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                published_at TIMESTAMP
            );
        """)

        # 6. Story Memories Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS story_memories (
                id TEXT PRIMARY KEY,
                episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
                event_category TEXT NOT NULL,
                summary TEXT NOT NULL,
                character_states TEXT NOT NULL,
                item_states TEXT NOT NULL,
                unresolved_mystery TEXT,
                is_resolved INTEGER DEFAULT 0,
                resolution_episode_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 7. Publications Table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS youtube_publications (
                id TEXT PRIMARY KEY,
                episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
                youtube_video_id TEXT,
                youtube_url TEXT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                tags TEXT NOT NULL,
                playlist_id TEXT,
                privacy_status TEXT NOT NULL,
                made_for_kids INTEGER NOT NULL,
                compliance_audit TEXT NOT NULL,
                upload_status TEXT NOT NULL,
                error_message TEXT,
                scheduled_publish_time TIMESTAMP,
                uploaded_at TIMESTAMP
            );
        """)

        await db.commit()
