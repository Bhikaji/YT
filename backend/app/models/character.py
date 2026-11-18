from datetime import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    series_id = Column(String(36), ForeignKey("series.id"), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False, default="PROTAGONIST")  # PROTAGONIST, ANTAGONIST, SIDEKICK, RECURRING
    age_category = Column(String(50), nullable=False, default="TEEN")
    
    # Narrative & Identity
    personality_summary = Column(Text, nullable=False)
    speaking_style = Column(String(255), nullable=False)
    background_story = Column(Text, nullable=True)
    character_relationships = Column(JSON, nullable=False, default=dict)
    
    # 3D Physical Specifications
    physical_specs = Column(JSON, nullable=False, default=dict)
    # {
    #   "face_structure": "round_stylized",
    #   "eye_shape": "large_anime_stylized",
    #   "eye_color": "emerald_green",
    #   "hair_style": "spiky_messy",
    #   "hair_color": "chestnut_brown",
    #   "body_proportions": "stylized_hero_slender",
    #   "outfit": "blue_leather_vest_cargo_pants"
    # }

    # 3D Asset Anchors
    blend_model_path = Column(String(500), nullable=True)
    rig_type = Column(String(50), nullable=False, default="RIGIFY_ARKit52")
    texture_dir_path = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    series = relationship("Series", back_populates="characters")
    voice = relationship("CharacterVoice", back_populates="character", uselist=False, cascade="all, delete-orphan")

class CharacterVoice(Base):
    __tablename__ = "character_voices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    character_id = Column(String(36), ForeignKey("characters.id"), nullable=False, unique=True)
    
    provider = Column(String(50), nullable=False, default="edge_tts")  # 'edge_tts', 'elevenlabs', 'xtts'
    voice_identifier = Column(String(100), nullable=False)  # e.g. 'en-US-ChristopherNeural', 'en-US-AnaNeural'
    pitch_adjustment = Column(String(20), nullable=False, default="+0Hz")
    rate_adjustment = Column(String(20), nullable=False, default="+0%")
    volume_adjustment = Column(String(20), nullable=False, default="+0%")
    
    # Emotional tone presets
    emotion_presets = Column(JSON, nullable=False, default=dict)
    # {
    #   "angry": {"pitch": "+5Hz", "rate": "+15%"},
    #   "scared": {"pitch": "+10Hz", "rate": "+20%"},
    #   "whisper": {"pitch": "-5Hz", "rate": "-10%"}
    # }
    
    reference_audio_path = Column(String(500), nullable=True)  # For voice cloning / XTTS
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    character = relationship("Character", back_populates="voice")
