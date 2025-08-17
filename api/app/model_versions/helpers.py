from typing import Any

from pandas import DataFrame
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.model_versions import models, crud
from app.students import models as student_models
from app.students import constants as student_constants


def has_new_data(db: Session) -> bool:
    """Check if there is new data to train a new model"""
    # Get the latest version of the model
    latest_model = crud.get_latest_model_version(db)
    if not latest_model:
        # If no previous model exists, any data is new.
        return db.query(student_models.Student).count() > 0

    # Count students added or updated after the creation of the last model
    new_students_count = (
        db.query(student_models.Student)
        .filter(
            False == student_models.Student.archived,
            student_models.Student.estado.in_(
                [
                    student_constants.EstadoEnum.ABANDONO,
                    student_constants.EstadoEnum.EGRESADO,
                ]
            ),
            or_(
                student_models.Student.created_at > latest_model.created_at,
                student_models.Student.updated_at > latest_model.created_at,
            ),
        )
        .count()
    )
    return new_students_count > 0


def get_model_metrics(model_version: models.ModelVersion) -> dict:
    return {
        "precision": model_version.precision,
        "recall": model_version.recall,
        "f1_score": model_version.f1_score,
        "accuracy": model_version.accuracy,
    }


def compare_model_versions(model1: models.ModelVersion, model2: models.ModelVersion):
    """
    Compare two trained model versions

    Metrics used to compare the models are:
         - precision (float)
         - recall (float)
         - f1_score (float)
         - accuracy (float)

    Returns:
        tuple: (improved (bool), comparison_results (dict))
               - improved: True if the new model performs better, False otherwise
               - comparison_results: Dictionary with detailed comparison metrics
    """
    # Extract metrics from models
    model1_metrics = get_model_metrics(model1)
    model2_metrics = get_model_metrics(model2)

    # Calculate differences and percentage improvements
    differences = {
        metric: model1_metrics[metric] - model2_metrics[metric]
        for metric in model1_metrics.keys()
        if model1_metrics[metric] is not None and model2_metrics[metric] is not None
    }
    percentage_improvements = {
        metric: (diff / model2_metrics[metric] * 100)
        if model2_metrics[metric] and model2_metrics[metric] > 0
        else float("inf")
        if diff > 0
        else float("-inf")
        for metric, diff in differences.items()
    }

    # Primary decision metric: F1 score (balances precision and recall)
    primary_metric = "f1_score"
    improved = model2_metrics[primary_metric] > model1_metrics[primary_metric]

    # Prepare detailed comparison results
    comparison_results = {
        "model1": {
            "id": model1.id,
            "version": model1.version,
            "metrics": model1_metrics,
        },
        "model2": {
            "id": model2.id,
            "version": model2.version,
            "metrics": model2_metrics,
        },
        "improvement": {
            "differences": differences,
            "percentage": percentage_improvements,
            "improved": improved,
            "primary_metric": primary_metric,
        },
    }
    return improved, comparison_results


def get_next_model_version(db: Session) -> int:
    # Query the highest version from the database
    last_version = db.query(func.max(models.ModelVersion.version)).scalar()

    # If no models exist, start with version 1
    if last_version is None:
        return 1

    # Increment the version by 1
    return last_version + 1


def train_model(df: DataFrame) -> (Any, dict):
    # Define features (X) and target (y)
    X = df.drop("desercion", axis=1)
    y = df["desercion"]

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train a logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    metrics = {
        "precision": float(precision_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "f1_score": float(f1_score(y_test, y_pred)),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "confusion_matrix": str(confusion_matrix(y_test, y_pred).tolist()),
        "num_samples": len(X),
        "num_features": X.shape[1],
        "hyperparameters": model.get_params(),
    }

    return model, metrics
