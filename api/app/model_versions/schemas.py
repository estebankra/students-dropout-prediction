from datetime import datetime

from app.model_versions import constants
from pydantic import BaseModel, field_validator, field_serializer


class ModelMetrics(BaseModel):
    precision: float
    recall: float
    f1_score: float
    accuracy: float

    # Custom field validator to round floats to 4 decimal places
    @field_validator("accuracy", "precision", "recall", "f1_score", mode="before")
    def round_floats(cls, value):
        return round(value, 2)


class ModelVersionRead(ModelMetrics):
    id: int
    version: int
    is_active: bool
    num_samples: int
    num_features: int
    created_at: datetime
    status: constants.ModelVersionStatus

    # Serialize the version as "vX.0"
    @field_serializer("version", when_used="json")
    def format_version(self, value):
        return f"v{value}.0"
