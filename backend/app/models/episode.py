from datetime import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime, Integer, Float, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Episode(Base):
    __tablename__ = "episodes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    season_id = Column(String(36), ForeignKey("seasons.id"), nullable=False)
    episode_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    format = Column(String(20), nullable=False, default="SHORT")  # 'SHORT' (9:16) or 'LONG_FORM' (16:9)
    target_duration_seconds = Column(Integer, nullable=False, default=45)
    
    # Lifecycle Status
    status = Column(String(50), nullable=False, default="CONCEPT")
    # 'CONCEPT', 'SCRIPT_DRAFTED', 'CONTINUITY_APPROVED', 'AUDIO_GENERATED',
    # 'ANIMATION_RENDERED', 'POST_PROCESSED', 'READY_FOR_APPROVAL', 'PUBLISHED', 'FAILED'
    
    # Story Content
    synopsis = Column(Text, nullable=True)
    script_structured = Column(JSON, nullable=True)
    cliffhanger_question = Column(String(500), nullable=False)
    next_episode_teaser = Column(String(500), nullable=True)
    
    # Output Media Paths
    rendered_frames_dir = Column(String(500), nullable=True)
    final_video_path = Column(String(500), nullable=True)
    primary_thumbnail_path = Column(String(500), nullable=True)
    
    # Analytics & Metrics
    production_cost_usd = Column(Float, nullable=False, default=0.0)
    render_duration_seconds = Column(Float, nullable=False, default=0.0)
    error_log = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)

    # Relationships
    season = relationship("Season", back_populates="episodes")
    scenes = relationship("Scene", back_populates="episode", cascade="all, delete-orphan", order_by="Scene.scene_index")
    memories = relationship("StoryMemory", back_populates="episode", cascade="all, delete-orphan")
    publications = relationship("YouTubePublication", back_populates="episode", cascade="all, delete-orphan")
    thumbnails = relationship("ThumbnailCandidate", back_populates="episode", cascade="all, delete-orphan")

class Scene(Base):
    __tablename__ = "scenes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    episode_id = Column(String(36), ForeignKey("episodes.id"), nullable=False)
    scene_index = Column(Integer, nullable=False)
    environment_preset = Column(String(100), nullable=False, default="generic_stage")
    lighting_mood = Column(String(100), nullable=False, default="cinematic_daylight")
    duration_seconds = Column(Float, nullable=False, default=5.0)
    
    # Directorial Setup
    camera_shots = Column(JSON, nullable=False, default=list)
    action_cues = Column(JSON, nullable=False, default=list)
    sound_effects = Column(JSON, nullable=False, default=list)

    # Relationships
    episode = relationship("Episode", back_populates="scenes")
    dialogues = relationship("DialogueLine", back_populates="scene", cascade="all, delete-orphan", order_by="DialogueLine.line_index")

class DialogueLine(Base):
    __tablename__ = "dialogue_lines"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scene_id = Column(String(36), ForeignKey("scenes.id"), nullable=False)
    character_id = Column(String(36), ForeignKey("characters.id"), nullable=False)
    line_index = Column(Integer, nullable=False)
    
    text = Column(Text, nullable=False)
    emotion = Column(String(50), nullable=False, default="neutral")  # angry, whisper, excited, scared, etc.
    start_second = Column(Float, nullable=False, default=0.0)
    duration_seconds = Column(Float, nullable=False, default=0.0)
    
    audio_file_path = Column(String(500), nullable=True)
    viseme_file_path = Column(String(500), nullable=True)

    # Relationships
    scene = relationship("Scene", back_populates="dialogues")
    character = relationship("Character")
