from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field

class DialogueLineBase(BaseModel):
    character_id: str
    line_index: int
    text: str
    emotion: str = "neutral"
    start_second: float = 0.0
    duration_seconds: float = 0.0
    audio_file_path: Optional[str] = None
    viseme_file_path: Optional[str] = None

class DialogueLineResponse(DialogueLineBase):
    id: str
    scene_id: str

    class Config:
        from_attributes = True

class SceneBase(BaseModel):
    scene_index: int
    environment_preset: str = "generic_stage"
    lighting_mood: str = "cinematic_daylight"
    duration_seconds: float = 5.0
    camera_shots: List[Dict[str, Any]] = Field(default_factory=list)
    action_cues: List[Dict[str, Any]] = Field(default_factory=list)
    sound_effects: List[Dict[str, Any]] = Field(default_factory=list)

class SceneResponse(SceneBase):
    id: str
    episode_id: str
    dialogues: List[DialogueLineResponse] = []

    class Config:
        from_attributes = True

class EpisodeBase(BaseModel):
    episode_number: int
    title: str
    format: str = "SHORT"  # SHORT or LONG_FORM
    target_duration_seconds: int = 45
    synopsis: Optional[str] = None
    cliffhanger_question: str
    next_episode_teaser: Optional[str] = None

class EpisodeCreate(EpisodeBase):
    season_id: str

class EpisodeResponse(EpisodeBase):
    id: str
    season_id: str
    status: str
    final_video_path: Optional[str] = None
    primary_thumbnail_path: Optional[str] = None
    production_cost_usd: float
    created_at: datetime
    published_at: Optional[datetime] = None
    scenes: List[SceneResponse] = []

    class Config:
        from_attributes = True
