from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class CharacterVoiceBase(BaseModel):
    provider: str = "edge_tts"
    voice_identifier: str = "en-US-ChristopherNeural"
    pitch_adjustment: str = "+0Hz"
    rate_adjustment: str = "+0%"
    volume_adjustment: str = "+0%"
    emotion_presets: Dict[str, Any] = Field(default_factory=dict)
    reference_audio_path: Optional[str] = None

class CharacterVoiceCreate(CharacterVoiceBase):
    pass

class CharacterVoiceResponse(CharacterVoiceBase):
    id: str
    character_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class CharacterBase(BaseModel):
    name: str = Field(..., max_length=100)
    role: str = "PROTAGONIST"
    age_category: str = "TEEN"
    personality_summary: str
    speaking_style: str
    background_story: Optional[str] = None
    character_relationships: Dict[str, Any] = Field(default_factory=dict)
    physical_specs: Dict[str, Any] = Field(default_factory=dict)
    blend_model_path: Optional[str] = None
    rig_type: str = "RIGIFY_ARKit52"

class CharacterCreate(CharacterBase):
    series_id: str
    voice: Optional[CharacterVoiceCreate] = None

class CharacterResponse(CharacterBase):
    id: str
    series_id: str
    created_at: datetime
    updated_at: datetime
    voice: Optional[CharacterVoiceResponse] = None

    class Config:
        from_attributes = True
