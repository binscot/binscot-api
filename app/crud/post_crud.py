from typing import Type

from sqlalchemy.orm import Session

from app.dto.response_dto import PostResDTO
from app.models.models import Post
from app.schemas.post_schemas import PostCreateReqDTO


def get_posts(db: Session) -> list[Type[PostResDTO]]:
    return db.query(Post).all()


def get_post(db: Session, post_id: int) -> PostResDTO | None:
    return db.query(Post).get(post_id)


def create_post(db: Session, post_create_req_dto: PostCreateReqDTO, current_user) -> PostResDTO | None:
    db_post = Post(**post_create_req_dto.__dict__, owner_id=current_user.id, owner_name=current_user.username)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
