from datetime import timedelta
from typing import Any
from typing import Optional

from app.helpers import get_now_utc

from fastapi.requests import HTTPConnection
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import get_authorization_scheme_param
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.users import crud as user_crud
from app.users import models as user_models

COOKIE_AUTHORIZATION_NAME = "Authorization"
ALGORITHM = "HS256"


class OAuth2PasswordBearerCookie(OAuth2PasswordBearer):
    async def __call__(self, conn: HTTPConnection) -> Optional[str]:
        authorization = conn.cookies.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            return None
        return param


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: str | Any) -> str:
    access_token_expires = timedelta(minutes=settings.ACCESS_EXPIRE_MINUTES)
    expire = get_now_utc() + access_token_expires
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(
    db: Session, email: str, password: str
) -> user_models.User | None:
    user = user_crud.get_user(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
