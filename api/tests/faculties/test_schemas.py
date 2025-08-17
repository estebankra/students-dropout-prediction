import pytest
from pydantic import ValidationError

from app.faculties.schemas import FacultyBase, FacultyCreate, FacultyUpdate, FacultyRead


def test_faculty_base_schema():
    # Test valid data
    faculty_data = {
        "long_name": "Test Faculty",
        "short_name": "TEST"
    }
    faculty = FacultyBase(**faculty_data)
    assert faculty.long_name == faculty_data["long_name"]
    assert faculty.short_name == faculty_data["short_name"]

    # Test with missing short_name (should be None)
    faculty_data = {"long_name": "Test Faculty"}
    faculty = FacultyBase(**faculty_data)
    assert faculty.long_name == faculty_data["long_name"]
    assert faculty.short_name is None

    # Test with missing long_name (should raise ValidationError)
    faculty_data = {"short_name": "TEST"}
    with pytest.raises(ValidationError):
        FacultyBase(**faculty_data)


def test_faculty_create_schema():
    # Test valid data
    faculty_data = {
        "long_name": "Test Faculty",
        "short_name": "TEST"
    }
    faculty = FacultyCreate(**faculty_data)
    assert faculty.long_name == faculty_data["long_name"]
    assert faculty.short_name == faculty_data["short_name"]


def test_faculty_update_schema():
    # Test valid data
    faculty_data = {
        "long_name": "Updated Faculty",
        "short_name": "UPDT",
        "active": False
    }
    faculty = FacultyUpdate(**faculty_data)
    assert faculty.long_name == faculty_data["long_name"]
    assert faculty.short_name == faculty_data["short_name"]
    assert faculty.active == faculty_data["active"]

    # Test with missing active field (should raise ValidationError)
    faculty_data = {
        "long_name": "Updated Faculty",
        "short_name": "UPDT"
    }
    with pytest.raises(ValidationError):
        FacultyUpdate(**faculty_data)


def test_faculty_read_schema():
    # Test valid data
    faculty_data = {
        "id": 1,
        "long_name": "Test Faculty",
        "short_name": "TEST",
        "active": True
    }
    faculty = FacultyRead(**faculty_data)
    assert faculty.id == faculty_data["id"]
    assert faculty.long_name == faculty_data["long_name"]
    assert faculty.short_name == faculty_data["short_name"]
    assert faculty.active == faculty_data["active"]

    # Test with missing id field (should raise ValidationError)
    faculty_data = {
        "long_name": "Test Faculty",
        "short_name": "TEST",
        "active": True
    }
    with pytest.raises(ValidationError):
        FacultyRead(**faculty_data)

    # Test with missing active field (should raise ValidationError)
    faculty_data = {
        "id": 1,
        "long_name": "Test Faculty",
        "short_name": "TEST"
    }
    with pytest.raises(ValidationError):
        FacultyRead(**faculty_data)