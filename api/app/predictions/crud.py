from sqlalchemy.orm import Session

from app.predictions import models as prediction_models


def create_prediction(
    db: Session, student_id: int, prediction: float, model_version: str
):
    """
    Create a prediction record with dropout probability (0.0 to 1.0).

    Args:
        db: Database session
        student_id: ID of the student
        prediction: Dropout probability as a float between 0.0 (0%) and 1.0 (100%)
        model_version: Version of the model used to generate the predictions
    """
    prediction = prediction_models.Prediction(
        student_id=student_id,
        dropout_probability=prediction,
        model_version=model_version,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction
