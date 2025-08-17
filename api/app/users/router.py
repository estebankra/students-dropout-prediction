from fastapi import APIRouter

from app.api.deps import UserOrNone
from app.users import schemas as user_schemas

router = APIRouter(prefix="/users")


@router.get("/me", response_model=user_schemas.UserRead | None)
def get_current_user(current_user: UserOrNone):
    return current_user
