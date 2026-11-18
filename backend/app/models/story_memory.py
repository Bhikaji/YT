from datetime import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from backend.app.database import Base

class StoryMemory(Base):
    __tablename__ = "story_memories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    episode_id = Column(String(36), ForeignKey("episodes.id"), nullable=False)
    
    event_category = Column(String(50), nullable=False)  # 'PLOT_TWIST', 'CHARACTER_DISCOVERY', 'RELATIONSHIP_SHIFT', 'ITEM_ACQUIRED'
    summary = Column(Text, nullable=False)
    
    # State changes
    character_states = Column(JSON, nullable=False, default=dict)
    # e.g., {"hero_leo": {"knows_secret": True, "trusts_maya": False}}
    
    item_states = Column(JSON, nullable=False, default=dict)
    # e.g., {"golden_compass": {"holder": "hero_leo", "location": "lost_cave"}}
    
    unresolved_mystery = Column(String(500), nullable=True)
    is_resolved = Column(Boolean, nullable=False, default=False)
    resolution_episode_id = Column(String(36), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    episode = relationship("Episode", back_populates="memories")
