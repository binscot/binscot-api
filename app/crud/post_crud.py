from sqlalchemy.orm import Session

from app.models import models
from app.schemas import post_schemas


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def create_post(db: Session, post: post_schemas.PostCreate, current_user):
    db_post = models.Post(**post.__dict__, owner_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
