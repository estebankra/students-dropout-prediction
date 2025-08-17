from fastapi import Depends

from app.api.deps import SessionDep
from app.students import models, crud, exceptions
from typing import Annotated


def valid_student_id(db: SessionDep, student_id: int) -> models.Student:
    student = crud.get_student(db, student_id)
    if not student:
        raise exceptions.StudentNotFound()

    return student


StudentDep = Annotated[models.Student, Depends(valid_student_id)]
