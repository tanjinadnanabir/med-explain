import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    image_path: str
    question: str | None
    prediction: str | None
    confidence: float | None
    model_version: str | None
    created_at: datetime