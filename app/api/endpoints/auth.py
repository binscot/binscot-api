from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.data_type.token_type import Token
from app.database.database import get_db
from app.dto import signup_res_dto
from app.schemas import user_schemas, token_schemas
from app.service import auth_service

router = APIRouter()


@router.post("/signup", response_model=signup_res_dto.User)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    return auth_service.create_user(db, user)


@router.post("/login", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    return auth_service.login(db, form_data)


@router.post("/token", response_model=token_schemas.Token)
def create_access_token(request: Request, db: Session = Depends(get_db)):
    return auth_service.create_access_token(db, request)

