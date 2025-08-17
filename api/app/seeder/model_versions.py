from sqlalchemy.orm import Session
from app.helpers import get_now_utc
from app.model_versions import models as model_version_models
from app.model_versions import constants as model_version_constants


def seed_model_versions(db: Session):
    model_version = model_version_models.ModelVersion(
        version=1,
        is_active=True,
        model_path="model_v1.pkl",
        status=model_version_constants.ModelVersionStatus.COMPLETED,
        precision=0.50,
        recall=0.15,
        f1_score=0.25,
        accuracy=0.35,
        confusion_matrix="[[38, 23], [21, 42]]",
        num_samples=50,
        num_features=37,
        training_time=0.047,
        created_at=get_now_utc(),
    )
    db.add(model_version)
    db.commit()
    db.refresh(model_version)
