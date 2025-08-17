from typing import Any
from datetime import datetime, timedelta


from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.security import get_password_hash
from app.users import models, schemas, constants


def get_user(db: Session, email: str) -> models.User | None:
    stmt = select(models.User).where(email == models.User.email)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    stmt = select(models.User).where(user_id == models.User.id)
    return db.execute(stmt).scalar_one_or_none()


def get_users(
    db: Session,
    exclude_user_id: int,
    role: constants.Roles | None = None,
    active: bool | None = None,
):
    stmt = select(models.User).where(exclude_user_id != models.User.id)
    # Filter by role if specified
    if role is not None:
        stmt = stmt.where(role == models.User.role)
    # Filter by active status if specified
    if active is not None:
        stmt = stmt.where(active == models.User.active)

    # Construct the query and exclude the current user
    return paginate(db, stmt)


def create_user(db: Session, form_data: schemas.UserCreate):
    form_data.password = get_password_hash(form_data.password)
    new_user = models.User(**form_data.model_dump(exclude={"confirm_password"}))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, db_user: models.User, form_data: schemas.UserUpdate):
    # Update user attributes
    update_data = form_data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
        del update_data["confirm_password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_stats(db: Session) -> dict[str, Any]:
    """Get user statistics for the dashboard"""
    # Get total users count
    total_users = db.query(func.count(models.User.id)).scalar()

    # Get supervisor count
    supervisor_count = (
        db.query(func.count(models.User.id))
        .filter(constants.Roles.SUPERVISOR == models.User.role)
        .scalar()
    )
    # Get active supervisor count
    active_supervisor_count = (
        db.query(func.count(models.User.id))
        .filter_by(role=constants.Roles.SUPERVISOR, active=True)
        .scalar()
    )

    # Get admin count
    admin_count = (
        db.query(func.count(models.User.id))
        .filter(constants.Roles.ADMIN == models.User.role)
        .scalar()
    )
    # Get active admin count
    active_admin_count = (
        db.query(func.count(models.User.id))
        .filter_by(role=constants.Roles.ADMIN, active=True)
        .scalar()
    )

    # Get recently added users (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    new_users_count = (
        db.query(func.count(models.User.id))
        .filter(models.User.created_at >= thirty_days_ago)
        .scalar()
    )

    return {
        "total_users": total_users,
        "total_supervisors": supervisor_count,
        "total_active_supervisors": active_supervisor_count,
        "total_admins": admin_count,
        "total_active_admins": active_admin_count,
        "new_users_last_30_days": new_users_count,
    }
