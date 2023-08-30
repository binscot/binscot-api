from sqlalchemy.orm import Session
from typing import Type
from app.models import models
from app.schemas import post_schemas
from app.dto.response_dto import PostResponseDTO


def get_posts(db: Session) -> list[Type[PostResponseDTO]]:
    return db.query(models.Post).all()


def get_post(db: Session, post_id: int) -> PostResponseDTO | None:
    return db.query(models.Post).get(post_id)


def create_post(db: Session, post: post_schemas.PostCreate, current_user) -> PostResponseDTO | None:
    db_post = models.Post(**post.__dict__, owner_id=current_user.id, owner_name=current_user.username)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    print(db_post)
    return db_post
