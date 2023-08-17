from typing import List, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import post_crud
from app.database.database import get_db
from app.schemas import post_schemas
from app.service import post_service
from app.schemas.user_schemas import User
from app.service import auth_service

router = APIRouter()


@router.post("/create", response_model=post_schemas.Post)
def create_post(
        current_user: Annotated[User, Depends(auth_service.get_current_active_user)],
        post: post_schemas.PostCreate,
        db: Session = Depends(get_db)
):
    return post_crud.create_post(db, post, current_user)


@router.get("/", response_model=List[post_schemas.Post])
def read_posts(
        db: Session = Depends(get_db)
):
    return post_crud.get_posts(db)


@router.get("/read_post/{post_id}", response_model=post_schemas.Post)
def read_post(
        post_id: int,
        db: Session = Depends(get_db)
):
    return post_service.read_post(db, post_id)
