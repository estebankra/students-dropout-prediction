import pytest
from sqlalchemy.orm import Session

from app.faculties.models import Faculty


def test_faculty_model_creation(db: Session):
    # Create a new faculty instance
    faculty = Faculty(
        long_name="Test Faculty Model",
        short_name="TFM"
    )

    # Add it to the database
    db.add(faculty)
    db.commit()
    db.refresh(faculty)

    # Check if the faculty was created with the correct attributes
    assert faculty.id is not None
    assert faculty.long_name == "Test Faculty Model"
    assert faculty.short_name == "TFM"
    assert faculty.active is True  # Default value

    # Check if created_at and updated_at are set (from TimestampMixin)
    assert faculty.created_at is not None
    assert faculty.updated_at is None


def test_faculty_model_relationships(db: Session):
    # Create a new faculty instance
    faculty = Faculty(
        long_name="Faculty with Relationships",
        short_name="FWR"
    )

    # Add it to the database
    db.add(faculty)
    db.commit()
    db.refresh(faculty)

    # Check if the students relationship is initialized as an empty list
    assert hasattr(faculty, 'students')
    assert isinstance(faculty.students, list)
    assert len(faculty.students) == 0