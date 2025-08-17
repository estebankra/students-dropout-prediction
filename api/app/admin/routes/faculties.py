from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import LimitOffsetPage

from app.api.deps import SessionDep, AdminRequired
from app.faculties import crud as faculties_crud
from app.faculties import schemas as faculties_schemas

router = APIRouter(prefix="/faculties")


@router.get("", response_model=LimitOffsetPage[faculties_schemas.FacultyRead])
def get_faculties(
    _admin: AdminRequired,
    db: SessionDep,
    active: bool | None = None,
):
    return faculties_crud.get_faculties(db, active)


@router.post("", response_model=faculties_schemas.FacultyRead)
async def create_faculty(
    _admin: AdminRequired,
    db: SessionDep,
    form_data: faculties_schemas.FacultyCreate,
):
    try:
        new_faculty = faculties_crud.create_faculty(db, form_data)
        return new_faculty
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create faculty",
        )


@router.put("/{faculty_id}", response_model=faculties_schemas.FacultyRead)
async def update_faculty(
    _admin: AdminRequired,
    db: SessionDep,
    faculty_id: int,
    form_data: faculties_schemas.FacultyUpdate,
):
    try:
        db_faculty = faculties_crud.get_faculty_by_id(db, faculty_id)
        if not db_faculty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Faculty with id {faculty_id} not found",
            )
        updated_faculty = faculties_crud.update_faculty(db, db_faculty, form_data)
        return updated_faculty
    except HTTPException as ex:
        raise ex
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update faculty",
        )
