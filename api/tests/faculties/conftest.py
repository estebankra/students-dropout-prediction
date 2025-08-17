import pytest
from sqlalchemy.orm import Session

from app.faculties import models, schemas
from app.faculties.constants import FACULTIES


@pytest.fixture
def sample_faculty_data():
    return {
        "long_name": "Sample Faculty",
        "short_name": "SAMPLE",
        "active": True
    }


@pytest.fixture
def db_faculty(db: Session, sample_faculty_data):
    # Create a faculty in the database for testing
    faculty = models.Faculty(
        long_name=sample_faculty_data["long_name"],
        short_name=sample_faculty_data["short_name"],
        active=sample_faculty_data["active"]
    )
    db.add(faculty)
    db.commit()
    db.refresh(faculty)

    yield faculty

    # Clean up after the test
    db.delete(faculty)
    db.commit()


@pytest.fixture
def db_faculties(db: Session):
    # Create multiple faculties in the database for testing
    faculties = []
    for faculty_data in FACULTIES:
        faculty = models.Faculty(
            long_name=faculty_data["long_name"],
            short_name=faculty_data["short_name"],
            active=True
        )
        db.add(faculty)
        faculties.append(faculty)

    db.commit()
    for faculty in faculties:
        db.refresh(faculty)

    yield faculties

    # Clean up after the test
    for faculty in faculties:
        db.delete(faculty)
    db.commit()