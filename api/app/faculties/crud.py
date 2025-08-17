from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.faculties import models, schemas


def get_faculties(db: Session, active: bool | None = None):
    stmt = select(models.Faculty)
    if active is not None:
        stmt = stmt.where(active == models.Faculty.active)
    return paginate(db, stmt)


def get_faculty_by_id(db: Session, faculty_id: int) -> models.Faculty | None:
    stmt = select(models.Faculty).where(faculty_id == models.Faculty.id)
    return db.execute(stmt).scalar_one_or_none()


def get_faculty_by_short_name(db: Session, name: str) -> models.Faculty | None:
    stmt = select(models.Faculty).where(name == models.Faculty.short_name)
    return db.execute(stmt).scalar_one_or_none()


def create_faculty(db: Session, form_data: schemas.FacultyCreate):
    new_faculty = models.Faculty(
        short_name=form_data.short_name, long_name=form_data.long_name
    )
    db.add(new_faculty)
    db.commit()
    db.refresh(new_faculty)
    return new_faculty


def update_faculty(
    db: Session, db_faculty: models.Faculty, form_data: schemas.FacultyUpdate
):
    # Update faculty attributes
    db_faculty.short_name = form_data.short_name
    db_faculty.long_name = form_data.long_name
    db_faculty.active = form_data.active
    db.commit()
    db.refresh(db_faculty)
    return db_faculty
