import pytest
from sqlalchemy.orm import Session

from app.users import models, schemas, constants
from app.security import get_password_hash


@pytest.fixture
def sample_user_data():
    return {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "active": True,
        "role": constants.Roles.SUPERVISOR
    }


@pytest.fixture
def sample_admin_data():
    return {
        "email": "admin@example.com",
        "password": "password123",
        "first_name": "Admin",
        "last_name": "User",
        "active": True,
        "role": constants.Roles.ADMIN
    }


@pytest.fixture
def db_user(db: Session, sample_user_data):
    # Create a user in the database for testing
    hashed_password = get_password_hash(sample_user_data["password"])
    user = models.User(
        email=sample_user_data["email"],
        password=hashed_password,
        first_name=sample_user_data["first_name"],
        last_name=sample_user_data["last_name"],
        active=sample_user_data["active"],
        role=sample_user_data["role"]
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    yield user

    # Clean up after the test
    db.delete(user)
    db.commit()


@pytest.fixture
def db_admin(db: Session, sample_admin_data):
    # Create an admin user in the database for testing
    hashed_password = get_password_hash(sample_admin_data["password"])
    admin = models.User(
        email=sample_admin_data["email"],
        password=hashed_password,
        first_name=sample_admin_data["first_name"],
        last_name=sample_admin_data["last_name"],
        active=sample_admin_data["active"],
        role=sample_admin_data["role"]
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    yield admin

    # Clean up after the test
    db.delete(admin)
    db.commit()


@pytest.fixture
def db_multiple_users(db: Session):
    # Create multiple users with different roles and statuses
    users = []

    # Create 3 active supervisors
    for i in range(3):
        user = models.User(
            email=f"supervisor{i}@example.com",
            password=get_password_hash("password123"),
            first_name=f"Supervisor{i}",
            last_name="User",
            active=True,
            role=constants.Roles.SUPERVISOR
        )
        db.add(user)
        users.append(user)

    # Create 1 inactive supervisor
    user = models.User(
        email="inactive_supervisor@example.com",
        password=get_password_hash("password123"),
        first_name="Inactive",
        last_name="Supervisor",
        active=False,
        role=constants.Roles.SUPERVISOR
    )
    db.add(user)
    users.append(user)

    # Create 2 active admins
    for i in range(2):
        user = models.User(
            email=f"admin{i}@example.com",
            password=get_password_hash("password123"),
            first_name=f"Admin{i}",
            last_name="User",
            active=True,
            role=constants.Roles.ADMIN
        )
        db.add(user)
        users.append(user)

    # Create 1 inactive admin
    user = models.User(
        email="inactive_admin@example.com",
        password=get_password_hash("password123"),
        first_name="Inactive",
        last_name="Admin",
        active=False,
        role=constants.Roles.ADMIN
    )
    db.add(user)
    users.append(user)

    db.commit()
    for user in users:
        db.refresh(user)

    yield users

    # Clean up after the test
    for user in users:
        db.delete(user)
    db.commit()