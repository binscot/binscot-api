from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import post_crud
from app.database.database import get_db
from app.schemas import post_schemas
from app.service import post_service

router = APIRouter()


@router.post("/{user_id}", response_model=post_schemas.Post)
def create_post(user_id: int, post: post_schemas.PostCreate, db: Session = Depends(get_db)):
    return post_crud.create_post(db=db, post=post, user_id=user_id)


@router.get("/", response_model=List[post_schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return post_crud.get_posts(db, skip=skip, limit=limit)


@router.get("/read_post/{post_id}", response_model=post_schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    return post_service.read_post(db, post_id)
