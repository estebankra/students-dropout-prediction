import time
from typing import Any

import joblib
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model_versions import models, constants, exceptions, helpers
from app.students import crud as student_crud
from app.predictions import helpers as prediction_helpers


def get_model_versions(
    db: Session,
    sort_by: constants.ValidModelVersionSortFields = constants.ValidModelVersionSortFields.VERSION,
    sort_order: str = "desc",
    status: constants.ModelVersionStatus | None = None,
):
    """
    Get all model versions with optional sorting.

    Args:
        db (Session): Database session
        sort_by (str): Field to sort by (created_at accuracy, precision, recall, f1_score...)
        sort_order (str): Sort order (asc, desc)
        status (str): Filter by (Pending, Training, Completed, Failed)

    Returns:
        Paginated list of model versions
    """
    # Define valid sort fields and their corresponding model attributes
    valid_sort_fields = {
        "version": models.ModelVersion.version,
        "num_samples": models.ModelVersion.num_samples,
        "num_features": models.ModelVersion.num_features,
        "accuracy": models.ModelVersion.accuracy,
        "precision": models.ModelVersion.precision,
        "recall": models.ModelVersion.recall,
        "f1_score": models.ModelVersion.f1_score,
        "created_at": models.ModelVersion.created_at,
    }

    # Use the specified sort field if valid, otherwise default to created_at
    sort_field = valid_sort_fields.get(sort_by.value, models.ModelVersion.created_at)

    # Apply sort order
    if sort_order.lower() == "asc":
        order_by = sort_field.asc()
    else:
        order_by = sort_field.desc()

    stmt = select(models.ModelVersion).order_by(order_by)

    # Filter by status if specified
    if status is not None:
        stmt = stmt.filter(status == models.ModelVersion.status)

    return paginate(db, stmt)


def get_model_version(db: Session, model_id) -> models.ModelVersion | None:
    return db.query(models.ModelVersion).filter_by(id=model_id).first()


def get_model_in_training_status(db: Session) -> models.ModelVersion | None:
    """
    If there's any model in PENDING or TRAINING status means that a model is currently being trained

    Args:
        db (Session): Database session object

    Returns:
        Optional[models.ModelVersion]: First model found in PENDING or TRAINING status,
                                     or None if no such model exists
    """
    return (
        db.query(models.ModelVersion)
        .filter(
            (models.ModelVersion.status == constants.ModelVersionStatus.PENDING)
            | (models.ModelVersion.status == constants.ModelVersionStatus.TRAINING)
        )
        .first()
    )


def get_latest_model_version(db: Session) -> models.ModelVersion | None:
    return (
        db.query(models.ModelVersion)
        .order_by(models.ModelVersion.created_at.desc())
        .first()
    )


def get_previous_model_version(
    db: Session, current_version: int
) -> models.ModelVersion | None:
    # Get the highest version below current
    return (
        db.query(models.ModelVersion)
        .filter(models.ModelVersion.version < current_version)
        .order_by(models.ModelVersion.version.desc())
        .first()
    )


def get_active_model_version(db: Session) -> models.ModelVersion | None:
    return db.query(models.ModelVersion).filter_by(is_active=True).first()


def set_active_model_version(
    db: Session, new_model_version: models.ModelVersion
) -> models.ModelVersion | None:
    """Set a new model version as active"""
    # Deactivate the actual model
    actual_model_version = get_active_model_version(db)
    if actual_model_version is not None:
        actual_model_version.is_active = False

    # Activate the new model
    new_model_version.is_active = True
    db.commit()
    db.refresh(new_model_version)
    return new_model_version


def update_training_status(
    db: Session, model_version: models.ModelVersion
) -> models.ModelVersion | None:
    if model_version.status != constants.ModelVersionStatus.TRAINING:
        return
    model_version.status = constants.ModelVersionStatus.COMPLETED

    db.commit()
    db.refresh(model_version)
    return model_version


def save_model(
    db: Session, model: Any, training_time: time, metrics: dict
) -> models.ModelVersion:
    next_model_version = helpers.get_next_model_version(db)
    # Save the trained model
    model_filename = f"model_v{next_model_version}.pkl"
    joblib.dump(model, f"files/{model_filename}")

    # Save model details to the database
    model_version = models.ModelVersion(
        version=next_model_version,
        model_path=model_filename,
        status=constants.ModelVersionStatus.TRAINING,
        training_time=training_time,
        **metrics,
    )
    db.add(model_version)
    db.commit()
    return model_version


def train_new_model_version(db: Session) -> (models.ModelVersion, dict, str):
    # Check if there is a model being trained
    training_model = get_model_in_training_status(db)
    if training_model:
        raise exceptions.ModelIsCurrentlyUnderTraining()

    # Check if there is new data
    if not helpers.has_new_data(db):
        raise exceptions.NoNewStudentsDataAvailable()

    # Fetch all students from the database
    df = student_crud.get_students_data_for_ia(db, purpose="TRAINING")
    # Convert 'estado' to binary 'desercion' column
    df["desercion"] = df["estado"].apply(lambda x: 1 if x == "A" else 0)
    # Preprocess the data
    df = prediction_helpers.preprocess_data(df, db)

    # Train model
    start_time = time.time()
    model, metrics = helpers.train_model(df)
    training_time = time.time() - start_time

    # Save the trained model
    new_model_version = save_model(db, model, training_time, metrics)

    # Get the current active model from the database
    current_active_model = get_active_model_version(db)
    if current_active_model is not None:
        # Check if the new model improves performance
        improved, comparison_results = helpers.compare_model_versions(
            model1=current_active_model, model2=new_model_version
        )
    else:
        # If there's no active model, the new model is automatically an improvement
        improved = True

    update_training_status(db, new_model_version)

    # If the model improves performance, set it as active
    if improved:
        set_active_model_version(db, new_model_version)
        improvement_message = "El nuevo modelo mejoró el rendimiento por lo que se estableció como activo."
    else:
        improvement_message = "El nuevo modelo no mejoró el rendimiento. La versión anterior se mantiene activa."

    return new_model_version, metrics, improvement_message
