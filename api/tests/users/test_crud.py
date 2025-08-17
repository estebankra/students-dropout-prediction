from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.users import crud, schemas, constants, models
from app.security import verify_password


def test_get_user(db: Session, db_user):
    # Test retrieving a user by email
    user = crud.get_user(db, email=db_user.email)
    assert user is not None
    assert user.id == db_user.id
    assert user.email == db_user.email
    assert user.first_name == db_user.first_name
    assert user.last_name == db_user.last_name
    assert user.role == db_user.role


def test_get_user_not_found(db: Session):
    # Test retrieving a non-existent user
    user = crud.get_user(db, email="nonexistent@example.com")
    assert user is None


def test_get_user_by_id(db: Session, db_user):
    # Test retrieving a user by ID
    user = crud.get_user_by_id(db, user_id=db_user.id)
    assert user is not None
    assert user.id == db_user.id
    assert user.email == db_user.email


def test_get_user_by_id_not_found(db: Session):
    # Test retrieving a non-existent user by ID
    user = crud.get_user_by_id(db, user_id=999)
    assert user is None


def test_create_user(db: Session, sample_user_data):
    # Create a new user schema
    user_create = schemas.UserCreate(
        email=sample_user_data["email"],
        password=sample_user_data["password"],
        confirm_password=sample_user_data["password"],
        first_name=sample_user_data["first_name"],
        last_name=sample_user_data["last_name"],
        role=sample_user_data["role"]
    )

    # Delete any existing user with the same email to avoid conflicts
    existing_user = crud.get_user(db, email=sample_user_data["email"])
    if existing_user:
        db.delete(existing_user)
        db.commit()

    # Create the user
    user = crud.create_user(db, form_data=user_create)

    # Verify the user was created correctly
    assert user.id is not None
    assert user.email == sample_user_data["email"]
    assert user.first_name == sample_user_data["first_name"]
    assert user.last_name == sample_user_data["last_name"]
    assert user.role == sample_user_data["role"]
    assert user.active is True  # Default value
    assert verify_password(sample_user_data["password"], user.password)

    # Clean up
    db.delete(user)
    db.commit()


def test_update_user(db: Session, db_user):
    # Create an update schema
    user_update = schemas.UserUpdate(
        email="updated@example.com",
        first_name="Updated",
        last_name="Name",
        picture="new_picture.jpg",
        role=constants.Roles.ADMIN,
        active=True,
        password="newpassword123",
        confirm_password="newpassword123"
    )

    # Update the user
    updated_user = crud.update_user(db, db_user=db_user, form_data=user_update)

    # Verify the user was updated correctly
    assert updated_user.id == db_user.id
    assert updated_user.email == "updated@example.com"
    assert updated_user.first_name == "Updated"
    assert updated_user.last_name == "Name"
    assert updated_user.picture == "new_picture.jpg"
    assert updated_user.role == constants.Roles.ADMIN
    assert updated_user.active is True
    assert verify_password("newpassword123", updated_user.password)


def test_get_user_stats(db: Session, db_multiple_users):
    # Test getting user statistics
    stats = crud.get_user_stats(db)

    # Verify the statistics
    assert stats["total_users"] == 9

    # Count supervisors in the test data
    assert stats["total_supervisors"] == 5
    assert stats["total_active_supervisors"] == 4

    # Count admins in the test data
    assert stats["total_admins"] == 4
    assert stats["total_active_admins"] == 3

    # Since we just created these users, they should all be counted as new
    assert stats["new_users_last_30_days"] == 9


def test_get_user_stats_with_old_users(db: Session):
    # Create some users with creation dates older than 30 days
    old_users = []
    for i in range(3):
        user = models.User(
            email=f"old_user{i}@example.com",
            password="hashed_password",
            first_name=f"Old{i}",
            last_name="User",
            active=True,
            role=constants.Roles.SUPERVISOR,
            created_at=datetime.now() - timedelta(days=60)  # 60 days old
        )
        db.add(user)
        old_users.append(user)

    # Create some recent users
    new_users = []
    for i in range(2):
        user = models.User(
            email=f"new_user{i}@example.com",
            password="hashed_password",
            first_name=f"New{i}",
            last_name="User",
            active=True,
            role=constants.Roles.SUPERVISOR,
            created_at=datetime.now() - timedelta(days=15)  # 15 days old
        )
        db.add(user)
        new_users.append(user)

    db.commit()

    # Get the stats
    stats = crud.get_user_stats(db)

    # Verify the new users count
    assert stats["new_users_last_30_days"] == 4

    # Clean up
    for user in old_users + new_users:
        db.delete(user)
    db.commit()