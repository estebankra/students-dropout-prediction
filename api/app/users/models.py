from sqlalchemy import Column, Integer, String, Boolean, Enum

from app.database import Base, TimestampMixin
from app.users import constants


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    picture = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    role = Column(
        Enum(constants.Roles),
        nullable=False,
        default=constants.Roles.SUPERVISOR,
    )
