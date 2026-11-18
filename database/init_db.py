"""
Autonomous AI Cartoon Studio - Database Initializer & Migration Tool (V2.0)
Initializes data/studio_v2.db with WAL mode, foreign keys, and complete relational tables.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(r"E:\YT\database\studio_v2.db")
SCHEMA_FILE = Path(r"E:\YT\docs\DATABASE_SCHEMA_V2.md")

def init_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable WAL mode and foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("PRAGMA journal_mode = WAL;")
    
    # 1. Assets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        asset_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT,
        format TEXT NOT NULL,
        file_path TEXT NOT NULL,
        thumbnail_path TEXT,
        preview_3d_path TEXT,
        polygon_count INTEGER DEFAULT 0,
        vertex_count INTEGER DEFAULT 0,
        has_armature BOOLEAN DEFAULT 0,
        rig_family TEXT,
        license_type TEXT NOT NULL,
        commercial_permitted BOOLEAN NOT NULL DEFAULT 1,
        attribution_required BOOLEAN DEFAULT 0,
        version TEXT DEFAULT '1.0.0',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 2. Skeletons & Bone Mappings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skeletons (
        skeleton_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        family TEXT NOT NULL,
        bone_count INTEGER NOT NULL,
        root_bone_name TEXT NOT NULL,
        definition_json TEXT NOT NULL,
        is_canonical_standard BOOLEAN DEFAULT 0
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bone_mappings (
        mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_skeleton_id TEXT NOT NULL,
        canonical_bone_role TEXT NOT NULL,
        source_bone_name TEXT NOT NULL,
        rotation_offset_euler TEXT DEFAULT '(0,0,0)',
        FOREIGN KEY(source_skeleton_id) REFERENCES skeletons(skeleton_id) ON DELETE CASCADE
    );
    """)
    
    # 3. Characters
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        character_id TEXT PRIMARY KEY,
        asset_id TEXT NOT NULL,
        name TEXT NOT NULL,
        archetype TEXT NOT NULL,
        voice_profile_id TEXT NOT NULL,
        bio_lore TEXT,
        personality_prompt TEXT,
        facial_blendshape_standard TEXT DEFAULT 'arkit_52',
        FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
    );
    """)
    
    # 4. Animations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS animations (
        animation_id TEXT PRIMARY KEY,
        asset_id TEXT NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        target_rig_family TEXT NOT NULL,
        duration_frames INTEGER NOT NULL,
        fps INTEGER DEFAULT 30,
        is_looping BOOLEAN DEFAULT 0,
        has_root_motion BOOLEAN DEFAULT 0,
        file_path TEXT NOT NULL,
        FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
    );
    """)
    
    # 5. Series & Episodes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS series (
        series_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        genre TEXT NOT NULL,
        art_style TEXT DEFAULT 'Pixar_Cinematic_3D',
        target_audience TEXT DEFAULT 'All_Ages_Family',
        synopsis TEXT NOT NULL,
        active_season INTEGER DEFAULT 1
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS episodes (
        episode_id TEXT PRIMARY KEY,
        series_id TEXT NOT NULL,
        season_number INTEGER NOT NULL,
        episode_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        format TEXT NOT NULL,
        status TEXT NOT NULL,
        target_duration_seconds REAL NOT NULL,
        master_video_path TEXT,
        thumbnail_path TEXT,
        youtube_video_id TEXT,
        FOREIGN KEY(series_id) REFERENCES series(series_id)
    );
    """)
    
    # 6. Render Jobs & QA Inspections
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS render_jobs (
        job_id TEXT PRIMARY KEY,
        episode_id TEXT NOT NULL,
        stage TEXT NOT NULL,
        status TEXT NOT NULL,
        assigned_engine TEXT NOT NULL,
        allocated_vram_mb INTEGER DEFAULT 0,
        allocated_cpu_threads INTEGER DEFAULT 4,
        retry_count INTEGER DEFAULT 0,
        error_message TEXT,
        started_at TIMESTAMP,
        completed_at TIMESTAMP,
        FOREIGN KEY(episode_id) REFERENCES episodes(episode_id)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qa_inspections (
        inspection_id TEXT PRIMARY KEY,
        job_id TEXT NOT NULL,
        gate_name TEXT NOT NULL,
        passed BOOLEAN NOT NULL,
        metric_value REAL,
        rejection_reason TEXT,
        corrective_action_taken TEXT,
        inspected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(job_id) REFERENCES render_jobs(job_id)
    );
    """)
    
    # 7. YouTube Publications
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS youtube_publications (
        publication_id TEXT PRIMARY KEY,
        episode_id TEXT NOT NULL,
        youtube_video_id TEXT NOT NULL,
        privacy_status TEXT DEFAULT 'private',
        published_at TIMESTAMP,
        view_count INTEGER DEFAULT 0,
        like_count INTEGER DEFAULT 0,
        comment_count INTEGER DEFAULT 0,
        retention_percent REAL DEFAULT 0.0,
        FOREIGN KEY(episode_id) REFERENCES episodes(episode_id)
    );
    """)
    
    conn.commit()
    conn.close()
    print(f"Database successfully initialized at {DB_PATH}")

if __name__ == "__main__":
    init_database()
