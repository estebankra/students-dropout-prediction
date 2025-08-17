from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.database import Base, TimestampMixin


class Prediction(Base, TimestampMixin):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    dropout_probability = Column(Float, nullable=False)
    model_version = Column(String, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="predictions")
