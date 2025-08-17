from pydantic import BaseModel, Field

from datetime import date, datetime
from app.faculties import schemas as faculty_schemas
from app.faculties import constants as faculty_constants
from app.predictions import schemas as prediction_schemas
from app.students import constants


class StudentBase(BaseModel):
    archived: bool = False
    estado: constants.EstadoEnum = constants.EstadoEnum.VIGENTE
    estado_civil: constants.EstadoCivilEnum
    fecha_nac: date = Field(..., description="Fecha de nacimiento del estudiante")
    nro_hijos: int = Field(..., ge=0)
    anio_egreso: int = Field(..., ge=1970, le=date.today().year)
    ultimo_semestre_cursado: int = Field(ge=1, default=1)
    promedio_secundaria: constants.PromedioEnum
    cuantos_colegios_secundaria: int = Field(..., ge=1)
    posee_enfermedad: constants.EnfermedadEnum
    vive_con: constants.ViveConEnum
    situacion_ocupacional: constants.SituacionOcupacionalEnum
    sustento_economico: constants.SustentoEconomicoEnum
    formacion_academica_padre: constants.FormacionEnum
    formacion_academica_madre: constants.FormacionEnum
    formacion_academica_hermanos: constants.FormacionEnum


class Student(StudentBase):
    id: int
    first_name: str = Field(min_length=2, max_length=200)
    last_name: str = Field(min_length=2, max_length=200)
    faculty: faculty_schemas.FacultyRead
    predictions: list[prediction_schemas.PredictionBase]


class CreateOrUpdateStudent(StudentBase):
    faculty_short_name: faculty_constants.FacultiesOptions
    first_name: str = Field(min_length=2, max_length=200)
    last_name: str = Field(min_length=2, max_length=200)


class StudentWithPrediction(StudentBase):
    id: int
    first_name: str = Field(min_length=2, max_length=200)
    last_name: str = Field(min_length=2, max_length=200)
    faculty: faculty_schemas.FacultyRead
    dropout_probability: float
    prediction_id: int
    model_version: str
    prediction_date: datetime
