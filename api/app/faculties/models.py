from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.students import models as student_models

from app.database import Base, TimestampMixin


class Faculty(Base, TimestampMixin):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    long_name = Column(String(100), nullable=False)
    short_name = Column(String(25), nullable=False)
    active = Column(Boolean, default=True)

    # Relationships
    students = relationship(student_models.Student, back_populates="faculty")
