"""
Multilingual, Dialect, Dialogue Coordination & Voice Engine Database Schema.
Defines all 18 tables required for authentic Rangdi Marathi, Hindi, and International audio production.
"""

from typing import List

MULTILINGUAL_TABLE_DEFINITIONS: List[str] = [
    # 1. Languages Table
    """
    CREATE TABLE IF NOT EXISTS languages (
        code TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        native_name TEXT NOT NULL,
        priority_rank INTEGER DEFAULT 3,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,

    # 2. Language Priorities by Geography
    """
    CREATE TABLE IF NOT EXISTS language_priorities (
        id TEXT PRIMARY KEY,
        geo_region TEXT UNIQUE NOT NULL,
        primary_language TEXT NOT NULL REFERENCES languages(code),
        secondary_language TEXT REFERENCES languages(code),
        multilingual_strategy TEXT DEFAULT 'SINGLE_LANGUAGE'
    );
    """,

    # 3. Regional Dialects Table
    """
    CREATE TABLE IF NOT EXISTS regional_dialects (
        id TEXT PRIMARY KEY,
        language_code TEXT NOT NULL REFERENCES languages(code),
        dialect_name TEXT NOT NULL,
        region TEXT NOT NULL,
        is_colloquial BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,

    # 4. Dialect Vocabulary Database
    """
    CREATE TABLE IF NOT EXISTS dialect_vocabulary (
        id TEXT PRIMARY KEY,
        dialect_id TEXT NOT NULL REFERENCES regional_dialects(id),
        slang_term TEXT NOT NULL,
        standard_meaning TEXT NOT NULL,
        context_usage TEXT,
        humor_weight REAL DEFAULT 1.0,
        category TEXT
    );
    """,

    # 5. Localization Profiles
    """
    CREATE TABLE IF NOT EXISTS localization_profiles (
        id TEXT PRIMARY KEY,
        profile_name TEXT NOT NULL,
        target_geo TEXT NOT NULL,
        language_code TEXT NOT NULL REFERENCES languages(code),
        dialect_id TEXT REFERENCES regional_dialects(id),
        conversational_tone TEXT DEFAULT 'humorous_and_punchy'
    );
    """,

    # 6. Character Voice Profiles
    """
    CREATE TABLE IF NOT EXISTS character_voice_profiles (
        id TEXT PRIMARY KEY,
        character_id TEXT NOT NULL,
        language_code TEXT NOT NULL REFERENCES languages(code),
        voice_id TEXT NOT NULL,
        provider TEXT DEFAULT 'edge_tts',
        gender TEXT NOT NULL,
        vocal_style TEXT NOT NULL,
        pitch_offset TEXT DEFAULT '0Hz',
        speed_offset TEXT DEFAULT '0%',
        texture TEXT DEFAULT 'warm_conversational'
    );
    """,

    # 7. Voice Provider Configurations
    """
    CREATE TABLE IF NOT EXISTS voice_provider_configs (
        id TEXT PRIMARY KEY,
        provider_name TEXT UNIQUE NOT NULL,
        api_key_env TEXT,
        is_active BOOLEAN DEFAULT 1,
        latency_tier TEXT DEFAULT 'LOW',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,

    # 8. Voice Generation Jobs
    """
    CREATE TABLE IF NOT EXISTS voice_generation_jobs (
        id TEXT PRIMARY KEY,
        video_id TEXT NOT NULL,
        language_code TEXT NOT NULL REFERENCES languages(code),
        status TEXT DEFAULT 'PENDING',
        error_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,

    # 9. Voice Assets
    """
    CREATE TABLE IF NOT EXISTS voice_assets (
        id TEXT PRIMARY KEY,
        job_id TEXT NOT NULL REFERENCES voice_generation_jobs(id),
        character_id TEXT NOT NULL,
        audio_path TEXT NOT NULL,
        duration_sec REAL NOT NULL,
        sample_rate INTEGER DEFAULT 24000,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,

    # 10. Dialogue Segments
    """
    CREATE TABLE IF NOT EXISTS dialogue_segments (
        id TEXT PRIMARY KEY,
        scene_id INTEGER NOT NULL,
        speaker_id TEXT NOT NULL,
        text_original TEXT NOT NULL,
        text_localized TEXT NOT NULL,
        language_code TEXT NOT NULL,
        emotion TEXT DEFAULT 'curious',
        sequence_index INTEGER NOT NULL
    );
    """,

    # 11. Dialogue Schedules (Zero Overlap Enforcer)
    """
    CREATE TABLE IF NOT EXISTS dialogue_schedules (
        id TEXT PRIMARY KEY,
        video_id TEXT NOT NULL,
        segment_id TEXT NOT NULL REFERENCES dialogue_segments(id),
        speaker_id TEXT NOT NULL,
        start_sec REAL NOT NULL,
        end_sec REAL NOT NULL,
        gap_to_next_sec REAL DEFAULT 0.3,
        overlap_detected BOOLEAN DEFAULT 0
    );
    """,

    # 12. Speaker Assignments (Speaker vs Listener Status)
    """
    CREATE TABLE IF NOT EXISTS speaker_assignments (
        id TEXT PRIMARY KEY,
        schedule_id TEXT NOT NULL REFERENCES dialogue_schedules(id),
        speaker_id TEXT NOT NULL,
        is_speaking BOOLEAN NOT NULL,
        listener_reaction TEXT DEFAULT 'attentive_nod'
    );
    """,

    # 13. Audio Timeline
    """
    CREATE TABLE IF NOT EXISTS audio_timeline (
        id TEXT PRIMARY KEY,
        video_id TEXT NOT NULL,
        total_duration_sec REAL DEFAULT 30.0,
        dialogue_duration_sec REAL NOT NULL,
        music_ducking_db REAL DEFAULT -14.0,
        sfx_count INTEGER DEFAULT 0
    );
    """,

    # 14. Phoneme Alignments
    """
    CREATE TABLE IF NOT EXISTS phoneme_alignments (
        id TEXT PRIMARY KEY,
        segment_id TEXT NOT NULL REFERENCES dialogue_segments(id),
        phoneme TEXT NOT NULL,
        start_sec REAL NOT NULL,
        end_sec REAL NOT NULL
    );
    """,

    # 15. Viseme Timelines
    """
    CREATE TABLE IF NOT EXISTS viseme_timelines (
        id TEXT PRIMARY KEY,
        segment_id TEXT NOT NULL REFERENCES dialogue_segments(id),
        viseme TEXT NOT NULL,
        mouth_width REAL NOT NULL,
        mouth_height REAL NOT NULL,
        timestamp_sec REAL NOT NULL
    );
    """,

    # 16. Audio Quality Reports
    """
    CREATE TABLE IF NOT EXISTS audio_quality_reports (
        id TEXT PRIMARY KEY,
        video_id TEXT NOT NULL,
        qc_passed BOOLEAN NOT NULL,
        overlap_detected BOOLEAN DEFAULT 0,
        clipping_detected BOOLEAN DEFAULT 0,
        music_masking_detected BOOLEAN DEFAULT 0,
        overall_audio_score REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,

    # 17. Localization Versions
    """
    CREATE TABLE IF NOT EXISTS localization_versions (
        id TEXT PRIMARY KEY,
        source_video_id TEXT NOT NULL,
        target_language TEXT NOT NULL,
        localized_title TEXT NOT NULL,
        video_file_path TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,

    # 18. Language Performance Analytics
    """
    CREATE TABLE IF NOT EXISTS language_performance_analytics (
        id TEXT PRIMARY KEY,
        language_code TEXT NOT NULL REFERENCES languages(code),
        total_views INTEGER DEFAULT 0,
        avg_retention_pct REAL DEFAULT 0.0,
        engagement_score REAL DEFAULT 0.0,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
]
