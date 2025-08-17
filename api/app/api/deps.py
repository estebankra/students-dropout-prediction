from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.auth import schemas as auth_schemas
from app.config import settings
from app.database import SessionLocal
from app.security import ALGORITHM, OAuth2PasswordBearerCookie
from app.users import constants as users_constants
from app.users import crud as user_crud
from app.users import models as users_models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]

oauth2_dependency = OAuth2PasswordBearerCookie(
    tokenUrl=f"{settings.API_VERSION}/auth/login"
)
TokenDep = Annotated[str, Depends(oauth2_dependency)]


def get_current_user_from_token(
    db: SessionDep, token: TokenDep
) -> users_models.User | None:
    try:
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            token_data = auth_schemas.TokenPayload(**payload)
        except (JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        user = user_crud.get_user(db, token_data.sub)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user
    except (HTTPException, Exception):
        return None


UserOrNone = Annotated[users_models.User | None, Depends(get_current_user_from_token)]


def get_current_user_required(user: UserOrNone) -> users_models.User:
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


UserRequired = Annotated[users_models.User, Depends(get_current_user_required)]


def role_required(role: users_constants.Roles):
    def role_checker(user: UserRequired):
        if user.role == role:
            return user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{role.value.title()} role required",
        )

    return role_checker


SupervisorRequired = Annotated[
    users_models.User, Depends(role_required(users_constants.Roles.SUPERVISOR))
]
AdminRequired = Annotated[
    users_models.User, Depends(role_required(users_constants.Roles.ADMIN))
]
