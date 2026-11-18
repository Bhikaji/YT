from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field

class SeasonBase(BaseModel):
    season_number: int = 1
    title: Optional[str] = None
    story_arc_summary: Optional[str] = None

class SeasonCreate(SeasonBase):
    pass

class SeasonResponse(SeasonBase):
    id: str
    series_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class SeriesBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    genre: str = "Adventure / Mystery"
    target_audience: str = "Family & Teen"
    art_style_preset: str = "Pixar_Stylized_3D"
    world_lore: Dict[str, Any] = Field(default_factory=dict)

class SeriesCreate(SeriesBase):
    pass

class SeriesResponse(SeriesBase):
    id: str
    created_at: datetime
    updated_at: datetime
    seasons: List[SeasonResponse] = []

    class Config:
        from_attributes = True
