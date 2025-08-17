from datetime import datetime

from pydantic import BaseModel


class PredictionBase(BaseModel):
    id: int
    student_id: int
    dropout_probability: float
    model_version: str
    created_at: datetime
