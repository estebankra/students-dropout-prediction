from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base, TimestampMixin
from app.predictions import models as prediction_models


class Student(Base, TimestampMixin):
    __tablename__ = "students"

    # Basic information
    id = Column(Integer, primary_key=True, autoincrement=True)
    archived = Column(Boolean, default=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    estado = Column(String, nullable=True, default="V")

    # Dropout factors
    ultimo_semestre_cursado = Column(Integer, nullable=True)
    estado_civil = Column(String, nullable=True)
    fecha_nac = Column(Date, nullable=True)
    nro_hijos = Column(Integer, nullable=True)
    anio_egreso = Column(Integer, nullable=True)
    promedio_secundaria = Column(String, nullable=True)
    cuantos_colegios_secundaria = Column(Integer, nullable=True)
    posee_enfermedad = Column(String, nullable=True)
    vive_con = Column(String, nullable=True)
    situacion_ocupacional = Column(String, nullable=True)
    sustento_economico = Column(String, nullable=True)
    formacion_academica_padre = Column(String, nullable=True)
    formacion_academica_madre = Column(String, nullable=True)
    formacion_academica_hermanos = Column(String, nullable=True)

    # Relationships
    faculty = relationship("Faculty", back_populates="students")
    predictions = relationship(prediction_models.Prediction, back_populates="student")
