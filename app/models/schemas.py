from pydantic import BaseModel, Field
from typing import List

class PairItem(BaseModel):
    en: str = Field(..., description="English subtitle text")
    si: str = Field(..., description="Sinhala subtitle text")
    start: float = Field(..., description="pair start time (seconds)")
    end: float = Field(..., description="pair end time (seconds)")
    overlap_ms: int = Field(..., description="time overlap used for alignment (ms)")
    confidence: float = Field(..., ge=0, le=1, description="simple confidence score")

class CorpusResponse(BaseModel):
    language_source: str = "en"
    language_target: str = "si"
    count: int
    items: List[PairItem]
