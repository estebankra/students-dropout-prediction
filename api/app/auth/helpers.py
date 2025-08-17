from fastapi.responses import Response

from app.config import settings
from app.security import COOKIE_AUTHORIZATION_NAME


def set_authorization_cookie(response: Response, access_token: str):
    response.set_cookie(
        key=COOKIE_AUTHORIZATION_NAME,
        value=f"Bearer {access_token}",
        max_age=settings.ACCESS_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_EXPIRE_MINUTES * 60,
        domain=settings.COOKIE_DOMAIN,
        secure=settings.COOKIE_SECURE,
        httponly=settings.COOKIE_HTTPONLY,
        samesite=settings.COOKIE_SAMESITE,
    )


def delete_authorization_cookie(response: Response):
    response.delete_cookie(
        key=COOKIE_AUTHORIZATION_NAME,
        domain=settings.COOKIE_DOMAIN,
        secure=settings.COOKIE_SECURE,
        httponly=settings.COOKIE_HTTPONLY,
        samesite=settings.COOKIE_SAMESITE,
    )
