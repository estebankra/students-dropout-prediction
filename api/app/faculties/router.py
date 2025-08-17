from fastapi import APIRouter
from fastapi_pagination import LimitOffsetPage

from app.api.deps import SessionDep
from app.faculties import schemas, crud

router = APIRouter(prefix="/faculties")


@router.get("", response_model=LimitOffsetPage[schemas.FacultyRead])
def get_faculties(db: SessionDep):
    return crud.get_faculties(db, active=True)
