from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import post_crud
from app.database.database import get_db
from app.schemas import post_schemas

router = APIRouter()


@router.post("/{user_id}", response_model=post_schemas.Post)
def create_post(user_id: int, post: post_schemas.PostCreate, db: Session = Depends(get_db)):
    return post_crud.create_post(db=db, post=post, user_id=user_id)


@router.get("/", response_model=List[post_schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = post_crud.get_posts(db, skip=skip, limit=limit)
    return posts


@router.get("/read_post/{post_id}", response_model=post_schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = post_crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
