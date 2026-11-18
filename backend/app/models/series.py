from datetime import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Series(Base):
    __tablename__ = "series"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    genre = Column(String(100), nullable=False, default="Adventure / Comedy")
    target_audience = Column(String(100), nullable=False, default="Family & Teen")
    art_style_preset = Column(String(100), nullable=False, default="Pixar_Stylized_3D")
    world_lore = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    seasons = relationship("Season", back_populates="series", cascade="all, delete-orphan")
    characters = relationship("Character", back_populates="series", cascade="all, delete-orphan")

class Season(Base):
    __tablename__ = "seasons"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    series_id = Column(String(36), ForeignKey("series.id"), nullable=False)
    season_number = Column(Integer, nullable=False, default=1)
    title = Column(String(255), nullable=True)
    story_arc_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    series = relationship("Series", back_populates="seasons")
    episodes = relationship("Episode", back_populates="season", cascade="all, delete-orphan")
