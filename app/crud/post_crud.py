from sqlalchemy.orm import Session

from app.models import models
from app.schemas import post_schemas


def get_posts(db: Session):
    return db.query(models.Post).all()


def get_post(db: Session, post_id: int):
    return db.query(models.Post).get(post_id)


def create_post(db: Session, post: post_schemas.PostCreate, current_user):
    db_post = models.Post(**post.__dict__, owner_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
