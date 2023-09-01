from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dto.response_dto import UserResDTO, UserListResDTO
from app.service import auth_service, user_service

router = APIRouter()


@router.get("/", response_model=UserListResDTO)
def read_users(db: Session = Depends(get_db)):
    return user_service.get_user_list(db)


@router.get("/me", response_model=UserResDTO)
async def get_user_me(
        current_user: Annotated[UserResDTO, Depends(auth_service.get_current_active_user)]
):
    return user_service.get_user_me(current_user)
