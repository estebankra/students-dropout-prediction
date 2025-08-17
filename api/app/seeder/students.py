import pandas as pd
from faker import Faker
from sqlalchemy.orm import Session

from app.faculties import crud as faculty_crud
from app.predictions import helpers as prediction_helpers
from app.students import models as student_models

fake = Faker("es_ES")


def seed_students(db: Session):
    file_location = "files/data.xlsx"
    df = pd.read_excel(file_location)
    df = prediction_helpers.clean_data(df)

    # Commit changes to the database
    try:
        # Process each student
        for _, row in df.iterrows():
            # Get faculty
            faculty_name = row["facultad"].replace(" ", "")
            faculty = faculty_crud.get_faculty_by_short_name(db, faculty_name)
            if faculty is None:
                print(faculty_name)
                continue

            # Create the student
            student = student_models.Student(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                faculty_id=faculty.id,
                estado=row["estado"],
                fecha_nac=row["fecha_nac"],
                ultimo_semestre_cursado=row["ultimo_semestre_cursado"],
                anio_egreso=row["anio_egreso"],
                cuantos_colegios_secundaria=row["cuantos_colegios_secundaria"],
                nro_hijos=row["nro_hijos"],
                estado_civil=row["estado_civil"],
                promedio_secundaria=row["promedio_secundaria"],
                posee_enfermedad=row["posee_enfermedad"],
                vive_con=row["vive_con"],
                situacion_ocupacional=row["situacion_ocupacional"],
                sustento_economico=row["sustento_economico"],
                formacion_academica_padre=row["formacion_academica_padre"],
                formacion_academica_madre=row["formacion_academica_madre"],
                formacion_academica_hermanos=row["formacion_academica_hermanos"],
            )
            db.add(student)
            db.commit()
            db.refresh(student)

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
