from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.students import schemas, crud

router = APIRouter(prefix="/students")


@router.post("/register", response_model=schemas.Student)
async def register(db: SessionDep, student: schemas.CreateOrUpdateStudent):
    try:
        student = crud.create_student(db, data=student)
        return student
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
