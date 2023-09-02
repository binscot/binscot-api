from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dto.response_dto import BaseResponseDTO, BaseResponseListDTO
from app.schemas import post_schemas
from app.schemas.user_schemas import UserInDB
from app.service import auth_service
from app.service import post_service

router = APIRouter()


@router.post("/create", response_model=BaseResponseDTO)
def create_post(
        current_user: Annotated[UserInDB, Depends(auth_service.get_current_active_user)],
        post: post_schemas.PostCreate,
        db: Session = Depends(get_db)
):
    return post_service.create_post(db, post, current_user)


@router.get("/",  response_model=BaseResponseListDTO)
def read_posts(db: Session = Depends(get_db)):
    return post_service.get_post_list(db)


@router.get("/read_post", response_model=BaseResponseDTO)
def read_post(post_id: int, db: Session = Depends(get_db)):
    return post_service.read_post(db, post_id=post_id)
