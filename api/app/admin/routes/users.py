from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import LimitOffsetPage

from app.users import crud as users_crud
from app.users import constants as user_constants
from app.api.deps import SessionDep, AdminRequired
from app.users import schemas as user_schemas

router = APIRouter(prefix="/users")


@router.get("", response_model=LimitOffsetPage[user_schemas.UserRead])
def get_users(
    admin: AdminRequired,
    db: SessionDep,
    role: user_constants.Roles | None = None,
    active: bool | None = None,
):
    return users_crud.get_users(db, exclude_user_id=admin.id, role=role, active=active)


@router.post("", response_model=user_schemas.UserRead)
async def create_user(
    _admin: AdminRequired,
    db: SessionDep,
    form_data: user_schemas.UserCreate,
):
    try:
        new_user = users_crud.create_user(db, form_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="A user with this email already exists."
        )
    return new_user


@router.put("/{user_id}", response_model=user_schemas.UserRead)
async def update_user(
    _admin: AdminRequired,
    db: SessionDep,
    user_id: int,
    form_data: user_schemas.UserUpdate,
):
    try:
        db_user = users_crud.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )
        updated_user = users_crud.update_user(db, db_user, form_data)
        return updated_user
    except HTTPException as ex:
        raise ex
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="A user with this email already exists."
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user",
        )
