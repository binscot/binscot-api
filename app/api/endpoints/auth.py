from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dto.response_dto import BaseResponseDTO
from app.schemas.user_schemas import UserCreateReqDTO
from app.service import auth_service

router = APIRouter()


@router.post("/signup", response_model=BaseResponseDTO)
def create_user(user_create_req_dto: UserCreateReqDTO, db: Session = Depends(get_db)):
    return auth_service.create_user(db, user_create_req_dto)


@router.post("/login", response_model=BaseResponseDTO)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        response: Response,
        db: Session = Depends(get_db)
):
    return auth_service.login(db, form_data, response)


@router.post("/token", response_model=BaseResponseDTO)
def create_access_token(request: Request, db: Session = Depends(get_db)):
    return auth_service.create_access_token(db, request)
