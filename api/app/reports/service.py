from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.faculties.models import Faculty
from app.predictions.models import Prediction
from app.students.models import Student
from app.students import constants as student_constants
from app.model_versions import crud as model_versions_crud
from app.reports import schemas


class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def __get_predictions_query(
        self, faculty_id: int, model_version_id: int | None = None
    ):
        # Create distribution buckets (0-10%, 10-20%, etc.)
        buckets = {
            "0-10%": 0,
            "10-20%": 0,
            "20-30%": 0,
            "30-40%": 0,
            "40-50%": 0,
            "50-60%": 0,
            "60-70%": 0,
            "70-80%": 0,
            "80-90%": 0,
            "90-100%": 0,
        }

        # If model_version_id is provided, get the model version
        if model_version_id is not None:
            model_version = model_versions_crud.get_model_version(
                self.db, model_version_id
            )
            if model_version is None:
                # If model version not found, use the active model
                model_version = model_versions_crud.get_active_model_version(self.db)
        else:
            # If no model_version_id provided, use the active model
            model_version = model_versions_crud.get_active_model_version(self.db)

        # Get the model version string (e.g., "v1.0")
        model_version_str = f"v{model_version.version}.0" if model_version else None

        # Get the latest prediction for each student with the current model specified
        latest_predictions_subquery = (
            self.db.query(
                Prediction.student_id,
                func.max(Prediction.created_at).label("latest_date"),
            )
            .filter(model_version_str == Prediction.model_version)
            .group_by(Prediction.student_id)
            .subquery()
        )

        # Join with the predictions table to get the actual prediction records
        query = (
            self.db.query(
                Prediction.dropout_probability,
                Faculty.short_name.label("faculty_name"),
            )
            .join(Student, Prediction.student_id == Student.id)
            .join(Faculty, Student.faculty_id == Faculty.id)
            .join(
                latest_predictions_subquery,
                (Prediction.student_id == latest_predictions_subquery.c.student_id)
                & (Prediction.created_at == latest_predictions_subquery.c.latest_date),
            )
            .filter(model_version_str == Prediction.model_version)
        )

        # Apply optional filters
        if faculty_id is not None:
            query = query.filter(faculty_id == Student.faculty_id)

        # Execute query
        query = query.filter(student_constants.EstadoEnum.VIGENTE == Student.estado)
        return query.all(), buckets

    def get_dropout_probability_distribution(
        self, faculty_id: int | None = None, model_version_id: int | None = None
    ) -> dict[str, Any]:
        """
        Get the distribution of dropout probabilities across all students
        """
        results, buckets = self.__get_predictions_query(faculty_id, model_version_id)

        # Populate buckets
        for probability, faculty_name in results:
            # Overall distribution
            bucket_idx = min(int(probability * 10), 9)  # Ensure it's within 0-9 range
            bucket_key = list(buckets.keys())[bucket_idx]
            buckets[bucket_key] += 1

        # Calculate statistics
        total_students = len(results)
        high_risk_count = sum(prob >= 0.7 for prob, _ in results)
        medium_risk_count = sum(0.4 <= prob < 0.7 for prob, _ in results)
        low_risk_count = sum(prob < 0.4 for prob, _ in results)

        # Calculate percentages for the overall distribution
        distribution_percentages = {}
        for bucket, count in buckets.items():
            distribution_percentages[bucket] = (
                round((count / total_students * 100), 1) if total_students > 0 else 0
            )

        return {
            "total_students": total_students,
            "distribution": buckets,
            "distribution_percentages": distribution_percentages,
            "risk_summary": {
                "high_risk": {
                    "count": high_risk_count,
                    "percentage": round((high_risk_count / total_students * 100), 1)
                    if total_students > 0
                    else 0,
                },
                "medium_risk": {
                    "count": medium_risk_count,
                    "percentage": round((medium_risk_count / total_students * 100), 1)
                    if total_students > 0
                    else 0,
                },
                "low_risk": {
                    "count": low_risk_count,
                    "percentage": round((low_risk_count / total_students * 100), 1)
                    if total_students > 0
                    else 0,
                },
            },
        }

    def get_faculty_dropout_distribution(
        self, faculty_id: int | None = None, model_version_id: int | None = None
    ) -> dict[str, Any]:
        """
        Get the distribution of dropout probabilities across all faculties
        """
        results, buckets = self.__get_predictions_query(faculty_id, model_version_id)

        # Faculty-specific distributions
        faculty_distributions = {}

        # Populate buckets
        for probability, faculty_name in results:
            # Overall distribution
            bucket_idx = min(int(probability * 10), 9)  # Ensure it's within 0-9 range
            bucket_key = list(buckets.keys())[bucket_idx]
            buckets[bucket_key] += 1

            # Faculty-specific distribution
            if faculty_name not in faculty_distributions:
                faculty_distributions[faculty_name] = buckets.copy()

            faculty_distributions[faculty_name][bucket_key] += 1

        return {"faculty_distributions": faculty_distributions}

    def get_dropout_factors_impact(
        self, faculty_id: int | None = None, model_version_id: int | None = None
    ) -> dict[str, Any]:
        """
        Get the most impactful factors for student dropout
        """
        # If model_version_id is provided, get the model version
        if model_version_id is not None:
            model_version = model_versions_crud.get_model_version(
                self.db, model_version_id
            )
            if model_version is None:
                # If model version not found, use the active model
                model_version = model_versions_crud.get_active_model_version(self.db)
        else:
            # If no model_version_id provided, use the active model
            model_version = model_versions_crud.get_active_model_version(self.db)

        # Get the model version string (e.g., "v1.0")
        model_version_str = f"v{model_version.version}.0" if model_version else None

        # Get the latest prediction for each student with the current model specified
        latest_predictions_subquery = (
            self.db.query(
                Prediction.student_id,
                func.max(Prediction.created_at).label("latest_date"),
            )
            .filter(model_version_str == Prediction.model_version)
            .group_by(Prediction.student_id)
            .subquery()
        )

        # Base query to get students with their predictions
        query = (
            self.db.query(Student, Prediction.dropout_probability)
            .join(Prediction, Student.id == Prediction.student_id)
            .join(
                latest_predictions_subquery,
                (Prediction.student_id == latest_predictions_subquery.c.student_id)
                & (Prediction.created_at == latest_predictions_subquery.c.latest_date),
            )
            .filter(model_version_str == Prediction.model_version)
            .filter(student_constants.EstadoEnum.VIGENTE == Student.estado)
        )

        # Apply optional filters
        if faculty_id is not None:
            query = query.filter(faculty_id == Student.faculty_id)

        # Execute query
        results = query.all()
        total_students = len(results)

        # Define the factors to analyze
        factors_to_analyze = [
            ("estado_civil", "Estado civil"),
            ("nro_hijos", "Número de hijos"),
            ("posee_enfermedad", "Posee enfermedad"),
            ("vive_con", "Vive con"),
            ("situacion_ocupacional", "Situación ocupacional"),
            ("sustento_economico", "Sustento económico"),
            ("formacion_academica_padre", "Formación académica del padre"),
            ("formacion_academica_madre", "Formación académica de la madre"),
            ("formacion_academica_hermanos", "Formación académica de hermanos"),
            ("ultimo_semestre_cursado", "Último semestre cursado"),
            ("promedio_secundaria", "Promedio de secundaria"),
            ("cuantos_colegios_secundaria", "Cantidad de colegios en secundaria"),
        ]

        # Calculate impact scores for each factor
        factor_impact_scores = []

        for factor_key, factor_name in factors_to_analyze:
            # Group students by factor value and calculate average dropout probability
            factor_values = {}
            for student, probability in results:
                factor_value = getattr(student, factor_key)
                if factor_value is not None:
                    if factor_value not in factor_values:
                        factor_values[factor_value] = []
                    factor_values[factor_value].append(probability)

            # Skip factors with no data
            if not factor_values:
                continue

            # Calculate variance in dropout probability across different factor values
            avg_probabilities = [
                sum(probs) / len(probs) for probs in factor_values.values() if probs
            ]
            if not avg_probabilities:
                continue

            # Higher variance indicates more impact on dropout probability
            variance = sum(
                (p - sum(avg_probabilities) / len(avg_probabilities)) ** 2
                for p in avg_probabilities
            ) / len(avg_probabilities)

            # Find the factor value with highest dropout probability
            highest_risk_value = max(
                factor_values.items(),
                key=lambda x: sum(x[1]) / len(x[1]) if x[1] else 0,
            )
            highest_risk_value_str = str(highest_risk_value[0])
            highest_risk_prob = (
                sum(highest_risk_value[1]) / len(highest_risk_value[1])
                if highest_risk_value[1]
                else 0
            )

            # Create description
            description = f"Los estudiantes con {factor_name.lower()} '{highest_risk_value_str}' tienen una predicción de deserción promedio de {round(highest_risk_prob * 100, 1)}%"

            factor_impact_scores.append(
                {
                    "factor": factor_name,
                    "impact_score": variance,
                    "description": description,
                }
            )

        # Sort factors by impact score (highest first)
        factor_impact_scores.sort(key=lambda x: x["impact_score"], reverse=True)

        # Normalize impact scores to a 0-100 scale
        if factor_impact_scores:
            max_score = max(item["impact_score"] for item in factor_impact_scores)
            for item in factor_impact_scores:
                item["impact_score"] = round(item["impact_score"] / max_score * 100, 1)

        return {
            "factors": [
                schemas.FactorImpactItem(**item) for item in factor_impact_scores
            ],
            "total_students_analyzed": total_students,
        }
