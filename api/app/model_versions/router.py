from fastapi import APIRouter, Query
from fastapi_pagination import LimitOffsetPage

from app.api.deps import SessionDep, UserRequired
from app.model_versions import schemas, crud, constants

router = APIRouter(prefix="/models")


@router.get("", response_model=LimitOffsetPage[schemas.ModelVersionRead])
def get_model_versions(
    db: SessionDep,
    _user: UserRequired,
    sort_by: constants.ValidModelVersionSortFields = Query(
        constants.ValidModelVersionSortFields.VERSION, description="Field to sort by"
    ),
    sort_order: str = Query("desc", description="Sort order (asc, desc)"),
    status: constants.ModelVersionStatus | None = None,
):
    return crud.get_model_versions(db, sort_by, sort_order, status)
