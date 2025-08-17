import pytest
from sqlalchemy.orm import Session

from app.faculties import crud, schemas, models
from app.faculties.constants import FACULTIES


@pytest.fixture
def faculty_create_data():
    return schemas.FacultyCreate(
        long_name="Test Faculty",
        short_name="TEST"
    )


@pytest.fixture
def faculty_update_data():
    return schemas.FacultyUpdate(
        long_name="Updated Faculty",
        short_name="UPDT",
        active=False
    )

def test_get_faculty_by_short_name(test_client, db: Session):
    # Get a faculty from the constants
    faculty_data = FACULTIES[0]

    # Test getting a faculty by short name
    faculty = crud.get_faculty_by_short_name(db, faculty_data['short_name'])
    assert faculty is not None
    assert faculty.short_name == faculty_data['short_name']
    assert faculty.long_name == faculty_data['long_name']

    # Test getting a non-existent faculty
    non_existent_faculty = crud.get_faculty_by_short_name(db, 'NONEXISTENT')
    assert non_existent_faculty is None


def test_create_faculty(test_client, db: Session, faculty_create_data: schemas.FacultyCreate):
    # Test creating a new faculty
    new_faculty = crud.create_faculty(db, faculty_create_data)
    assert new_faculty is not None
    assert new_faculty.long_name == faculty_create_data.long_name
    assert new_faculty.short_name == faculty_create_data.short_name
    assert new_faculty.active is True  # Default value

    # Verify the faculty was actually added to the database
    db_faculty = crud.get_faculty_by_id(db, new_faculty.id)
    assert db_faculty is not None
    assert db_faculty.id == new_faculty.id


def test_update_faculty(test_client, db: Session, faculty_create_data: schemas.FacultyCreate,
                        faculty_update_data: schemas.FacultyUpdate):
    # First create a faculty to update
    faculty = crud.create_faculty(db, faculty_create_data)

    # Test updating the faculty
    updated_faculty = crud.update_faculty(db, faculty, faculty_update_data)
    assert updated_faculty is not None
    assert updated_faculty.id == faculty.id
    assert updated_faculty.long_name == faculty_update_data.long_name
    assert updated_faculty.short_name == faculty_update_data.short_name
    assert updated_faculty.active == faculty_update_data.active

    # Verify the faculty was actually updated in the database
    db_faculty = crud.get_faculty_by_id(db, faculty.id)
    assert db_faculty is not None
    assert db_faculty.long_name == faculty_update_data.long_name
    assert db_faculty.short_name == faculty_update_data.short_name
    assert db_faculty.active == faculty_update_data.active