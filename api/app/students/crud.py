import pandas as pd
from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, desc, func, not_, exists
from sqlalchemy.orm import Session

from app.faculties import constants as faculty_constants
from app.faculties import crud as faculty_crud
from app.model_versions import crud as model_versions_crud
from app.model_versions import models as model_version_models
from app.predictions.models import Prediction
from app.students import models, schemas, constants


def get_students(
    db: Session,
    faculty: faculty_constants.FacultiesOptions | None = None,
    min_probability: int | None = None,
    max_probability: int | None = None,
    search: str | None = None,
    estado: constants.EstadoEnum = constants.EstadoEnum.VIGENTE,
    model_version_id: int | None = None,
    archived: bool = False,
):
    # If model_version_id is provided, get the model version
    if model_version_id is not None:
        model_version = model_versions_crud.get_model_version(db, model_version_id)
        if model_version is None:
            # If model version not found, use the active model
            model_version = model_versions_crud.get_active_model_version(db)
    else:
        # If no model_version_id provided, use the active model
        model_version = model_versions_crud.get_active_model_version(db)

    # Get the model version string (e.g., "v1.0")
    model_version_str = f"v{model_version.version}.0" if model_version else None

    # First, create a subquery to get the latest prediction for each student
    # Use a window function to get the most recent prediction per student
    latest_prediction_subq = (
        select(
            Prediction.student_id,
            Prediction.dropout_probability,
            Prediction.model_version,
            func.row_number()
            .over(
                partition_by=Prediction.student_id, order_by=desc(Prediction.created_at)
            )
            .label("rn"),
        )
        .where(model_version_str == Prediction.model_version)
        .subquery()
    )

    # Filter to only get the most recent prediction for each student
    latest_prediction = (
        select(
            latest_prediction_subq.c.student_id,
            latest_prediction_subq.c.dropout_probability.label("latest_probability"),
        )
        .where(latest_prediction_subq.c.rn == 1)
        .subquery()
    )

    stmt = (
        select(models.Student)
        .filter(estado == models.Student.estado)
        .outerjoin(
            latest_prediction, models.Student.id == latest_prediction.c.student_id
        )
    )

    # Filter by faculty if specified
    if faculty:
        db_faculty = faculty_crud.get_faculty_by_short_name(db, name=faculty.value)
        if db_faculty:
            stmt = stmt.where(db_faculty.id == models.Student.faculty_id)

    if archived is True:
        stmt = stmt.where(True == models.Student.archived)

    # Filter by dropout probability range if specified
    if min_probability is not None:
        min_value = min_probability / 100.0  # Convert percentage to decimal
        # Only include students with predictions that meet the minimum threshold
        stmt = stmt.where(latest_prediction.c.latest_probability >= min_value)

    if max_probability is not None:
        max_value = max_probability / 100.0  # Convert percentage to decimal
        # Only include students with predictions that meet the maximum threshold
        stmt = stmt.where(latest_prediction.c.latest_probability <= max_value)

    # Filter by search term if specified
    if search:
        search_term = f"%{search}%"
        stmt = stmt.where(
            (models.Student.first_name.ilike(search_term))
            | (models.Student.last_name.ilike(search_term))
        )

    if min_probability is not None and max_probability is not None:
        # Order by dropout probability in descending order, placing NULL values last
        stmt = stmt.order_by(
            latest_prediction.c.latest_probability.is_(None).asc(),
            desc(latest_prediction.c.latest_probability),
        )
    else:
        stmt = stmt.filter(latest_prediction.c.latest_probability.is_(None))

    return paginate(db, stmt)


def get_students_data_for_ia(
    db: Session,
    purpose: str | None = None,
    model_version: model_version_models.ModelVersion | None = None,
) -> pd.DataFrame:
    if purpose == "TRAINING":
        stmt = (
            select(models.Student)
            .filter(
                models.Student.estado.in_(
                    [constants.EstadoEnum.ABANDONO, constants.EstadoEnum.EGRESADO]
                )
            )
            .filter_by(archived=False)
        )
    elif model_version is not None:
        predictions_exists = exists().where(
            (Prediction.student_id == models.Student.id)
            & (Prediction.model_version == f"v{model_version.version}.0")
        )
        stmt = select(models.Student).where(not_(predictions_exists))
    else:
        stmt = select(models.Student)

    result = db.execute(stmt).scalars().all()
    # Convert the result to a list of dictionaries
    students = [
        {k: v for k, v in student.__dict__.items() if not k.startswith("_")}
        for student in result
    ]

    if not students:
        raise HTTPException(
            status_code=400,
            detail="No se encontraron estudiantes sin predicciones con el modelo actual",
        )

    # Convert the students to a Pandas DataFrame
    df = pd.DataFrame(students)
    return df


def get_student(db: Session, student_id: int) -> models.Student | None:
    return db.execute(
        select(models.Student).filter_by(id=student_id)
    ).scalar_one_or_none()


def create_student(db: Session, data: schemas.CreateOrUpdateStudent) -> models.Student:
    student = models.Student(**data.model_dump(exclude={"faculty_short_name"}))

    # Set faculty
    faculty = faculty_crud.get_faculty_by_short_name(db, data.faculty_short_name.value)
    if faculty is not None:
        student.faculty_id = faculty.id

    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(
    db: Session, student: models.Student, data: schemas.CreateOrUpdateStudent
) -> models.Student:
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)

    # Set faculty
    faculty = faculty_crud.get_faculty_by_short_name(db, data.faculty_short_name.value)
    if faculty is not None:
        student.faculty_id = faculty.id

    db.commit()
    db.refresh(student)
    return student
