import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.auth import helpers
from app.security import authenticate_user, create_access_token

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

router = APIRouter(prefix="/auth")


@router.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)],
    db: Session = Depends(get_db),
) -> JSONResponse:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.email)
    token = jsonable_encoder(access_token)
    content = {"message": "Inicio de sesión exitosa"}
    response = JSONResponse(content=content)
    helpers.set_authorization_cookie(response, token)
    return response


@router.get("/logout")
async def logout_and_remove_cookie() -> JSONResponse:
    content = {"detail": "Cierre de sesión exitoso"}
    response = JSONResponse(content)
    helpers.delete_authorization_cookie(response)
    return response
