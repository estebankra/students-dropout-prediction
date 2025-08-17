import joblib
from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep, SupervisorRequired
from app.students import crud as student_crud
from app.predictions import crud, helpers
from app.model_versions import crud as model_version_crud

router = APIRouter(prefix="/predictions")


# Define the prediction endpoint
@router.post("/predict")
def predict(
    _supervisor: SupervisorRequired,
    db: SessionDep,
    model_version_id: int | None = None,
):
    """
    Predict dropout probability for all students.
    Returns probability scores from 0.0 (0%) to 1.0 (100%).
    """
    try:
        # If model_version_id is provided, get the model version
        if model_version_id is not None:
            model_version = model_version_crud.get_model_version(db, model_version_id)
            if model_version is None:
                # If model version not found, use the active model
                model_version = model_version_crud.get_active_model_version(db)
        else:
            # If no model_version_id provided, use the active model
            model_version = model_version_crud.get_active_model_version(db)

        # Fetch all students from the database
        df = student_crud.get_students_data_for_ia(
            db, purpose="PREDICT", model_version=model_version
        )
        # Preprocess the data
        processed_data = helpers.preprocess_data(df, db)
        # Remove extra column
        processed_data = processed_data.drop("desercion", axis=1)
        # Load active model
        model = joblib.load(f"files/{model_version.model_path}")
        # Make probability predictions
        # predict_proba returns probabilities for each class
        prediction_probabilities = model.predict_proba(processed_data)
        # Extract the probability of class 1 (dropout)
        dropout_probabilities = prediction_probabilities[:, 1]
        # Round to 2 decimal places to limit precision
        dropout_probabilities = [round(prob, 2) for prob in dropout_probabilities]
        # Add probability predictions to the original DataFrame (0 to 1 range)
        df["prediction"] = dropout_probabilities
        # Get the results as a list of dictionaries
        student_predictions = df.to_dict(orient="records")

        # Save predictions results
        for student_prediction in student_predictions:
            current_student_id: int | None = student_prediction.get("id", None)
            current_student_prediction: float | None = student_prediction.get(
                "prediction", None
            )

            if current_student_id is None or current_student_prediction is None:
                continue
            student_db = student_crud.get_student(db, current_student_id)
            if not student_db:
                continue
            crud.create_prediction(
                db,
                student_id=current_student_id,
                prediction=current_student_prediction,
                model_version=f"v{model_version.version}.0",
            )
        return student_predictions

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
