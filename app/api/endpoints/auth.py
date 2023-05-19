from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.core.config import settings
from app.crud import user_crud
from app.database.database import get_db
from app.dto import signup_res_dto
from app.data_type.token_type import Token
from app.schemas import user_schemas, token_schemas
from app.service.auth_service import verify_token, authenticate_user, create_jwt_token

router = APIRouter()


# status_code=status.HTTP_204_NO_CONTENT
@router.post("/signup", response_model=signup_res_dto.User)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    UserInDB = user_crud.get_user_by_username(db, username=user.username)
    if UserInDB:
        raise HTTPException(status_code=400, detail="username already registered")
    user = user_crud.create_user(db=db, user=user)
    return signup_res_dto.User(id=user.id, username=user.username)


@router.post("/login", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_jwt_token(data={"sub": user.username}, token_type=Token.ACCESS_TOKEN)
    refresh_token = create_jwt_token(data={"sub": user.username}, token_type=Token.REFRESH_TOKEN)
    response = JSONResponse({
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    })
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return response


@router.post("/token", response_model=token_schemas.Token)
def create_access_token(request: Request, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get(Token.REFRESH_TOKEN)
    user = verify_token(refresh_token, Token.get_key(Token.REFRESH_TOKEN), settings.HASH_ALGORITHM, db)
    access_token = create_jwt_token(data={"sub": user.username}, token_type=Token.ACCESS_TOKEN)
    response = JSONResponse({
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    })
    return response
