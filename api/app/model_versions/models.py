from sqlalchemy import Column, Integer, Boolean, String, Float, Text, JSON, Enum
from app.database import Base, TimestampMixin

from app.model_versions import constants


class ModelVersion(Base, TimestampMixin):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=False)
    model_path = Column(String, nullable=False)

    status = Column(
        Enum(constants.ModelVersionStatus),
        default=constants.ModelVersionStatus.PENDING,
        nullable=False,
    )

    # Metrics
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=False)
    confusion_matrix = Column(Text, nullable=True)

    # Model parameters
    hyperparameters = Column(JSON)

    # Training details
    num_samples = Column(Integer, nullable=False)
    num_features = Column(Integer, nullable=False)
    training_time = Column(Float, nullable=True)
