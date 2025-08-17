import joblib
import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from app.faculties import models as faculty_models

model_columns = joblib.load("files/model_columns.pkl")


def clean_data(df: pd.DataFrame):
    # Data preprocessing
    df.replace("-", np.nan, inplace=True)
    df.replace("", np.nan, inplace=True)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    # Remove string spaces from string columns
    columns_to_clean = [
        "facultad",
        "sustento_economico",
        "promedio_secundaria",
        "vive_con",
        "formacion_academica_padre",
        "formacion_academica_hermanos",
        "formacion_academica_madre",
        "situacion_ocupacional",
        "posee_enfermedad",
    ]
    df[columns_to_clean] = df[columns_to_clean].apply(lambda x: x.str.rstrip())

    # Drop extra columns
    df = df.drop("person_id", axis=1)
    return df


# Helper function to preprocess data
def preprocess_data(df: pd.DataFrame, db: Session | None = None) -> pd.DataFrame:
    # Transform 'fecha_nac' to 'edad'
    if "fecha_nac" in df.columns:
        df["fecha_nac"] = pd.to_datetime(df["fecha_nac"])
        fecha_datos = pd.to_datetime("2019-12-31")
        df["edad"] = fecha_datos.year - df["fecha_nac"].dt.year
        df.loc[df["edad"] < 17, "edad"] = 17
        df = df.drop("fecha_nac", axis=1)

    faculty_mapping = {
        faculty.id: faculty.short_name
        for faculty in db.query(faculty_models.Faculty).all()
    }
    df["facultad"] = df["faculty_id"].map(faculty_mapping)

    # Drop extra columns
    columns_to_drop = [
        "id",
        "archived",
        "estado",
        "first_name",
        "last_name",
        "faculty_id",
        "ultimo_semestre_cursado",
        "created_at",
        "updated_at",
    ]
    df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

    # One-hot encoding for categorical variables
    categorical_columns = [
        "facultad",
        "estado_civil",
        "promedio_secundaria",
        "posee_enfermedad",
        "vive_con",
        "situacion_ocupacional",
        "sustento_economico",
        "formacion_academica_padre",
        "formacion_academica_madre",
        "formacion_academica_hermanos",
    ]
    for col in categorical_columns:
        if col in df.columns:
            df = pd.get_dummies(df, columns=[col], drop_first=True)

    # Ensure all columns match the model's expected input
    for col in model_columns:
        if col not in df.columns:
            df[col] = False  # Add missing columns with default value False

    return df
