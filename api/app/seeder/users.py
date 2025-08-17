from sqlalchemy.orm import Session

from app.users import constants as user_constants
from app.users import models as user_models
from app.security import get_password_hash


def seed_users(db: Session):
    hashed_password = get_password_hash("Secret12345")
    admin_user = user_models.User(
        email="admin@admin.com",
        first_name="Admin",
        last_name="Test",
        password=hashed_password,
        role=user_constants.Roles.ADMIN,
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    supervisor_user = user_models.User(
        email="supervisor@supervisor.com",
        first_name="Supervisor",
        last_name="Test",
        password=hashed_password,
        role=user_constants.Roles.SUPERVISOR,
    )
    db.add(supervisor_user)
    db.commit()
    db.refresh(supervisor_user)
