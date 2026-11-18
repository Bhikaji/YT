from datetime import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime, Integer, Float, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from backend.app.database import Base

class YouTubePublication(Base):
    __tablename__ = "youtube_publications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    episode_id = Column(String(36), ForeignKey("episodes.id"), nullable=False)
    
    youtube_video_id = Column(String(50), nullable=True, unique=True)
    youtube_url = Column(String(255), nullable=True)
    
    # Upload Metadata
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    tags = Column(JSON, nullable=False, default=list)
    playlist_id = Column(String(100), nullable=True)
    
    # Settings & Compliance
    privacy_status = Column(String(20), nullable=False, default="unlisted")  # private, unlisted, public
    made_for_kids = Column(Boolean, nullable=False, default=False)
    compliance_audit = Column(JSON, nullable=False, default=dict)
    
    # State tracking
    upload_status = Column(String(50), nullable=False, default="PENDING")  # PENDING, UPLOADED, FAILED
    error_message = Column(Text, nullable=True)
    scheduled_publish_time = Column(DateTime, nullable=True)
    uploaded_at = Column(DateTime, nullable=True)
    
    # Relationships
    episode = relationship("Episode", back_populates="publications")
    metrics = relationship("VideoMetricSnapshot", back_populates="publication", cascade="all, delete-orphan")

class ThumbnailCandidate(Base):
    __tablename__ = "thumbnail_candidates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    episode_id = Column(String(36), ForeignKey("episodes.id"), nullable=False)
    
    variant_number = Column(Integer, nullable=False)
    image_path = Column(String(500), nullable=False)
    expression_focus = Column(String(50), nullable=False)  # shock, intrigue, action
    text_overlay = Column(String(100), nullable=True)
    ctr_vision_score = Column(Float, nullable=False, default=0.0)
    is_selected = Column(Boolean, nullable=False, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    episode = relationship("Episode", back_populates="thumbnails")

class VideoMetricSnapshot(Base):
    __tablename__ = "video_metric_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    publication_id = Column(String(36), ForeignKey("youtube_publications.id"), nullable=False)
    
    recorded_at = Column(DateTime, default=datetime.utcnow)
    views = Column(Integer, nullable=False, default=0)
    watch_time_minutes = Column(Float, nullable=False, default=0.0)
    average_view_duration_seconds = Column(Float, nullable=False, default=0.0)
    ctr_percent = Column(Float, nullable=False, default=0.0)
    likes = Column(Integer, nullable=False, default=0)
    comments = Column(Integer, nullable=False, default=0)
    retention_drop_points = Column(JSON, nullable=False, default=list)

    # Relationships
    publication = relationship("YouTubePublication", back_populates="metrics")
