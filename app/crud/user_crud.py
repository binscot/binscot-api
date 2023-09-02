from typing import Type

from sqlalchemy.orm import Session

from app.core import consts
from app.dto.response_dto import UserResDTO
from app.models import models
from app.schemas import user_schemas


def get_user_by_username(db: Session, username: str) -> user_schemas.UserInDB | None:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_user_id(db: Session, user_id: int) -> user_schemas.UserInDB | None:
    return db.query(models.User).get(user_id)


def get_users(db: Session) -> list[Type[UserResDTO]]:
    return db.query(models.User).all()


def create_user(db: Session, user: user_schemas.UserCreate):
    new_user = models.User(
        username=user.username,
        hashed_password=consts.password_context.hash(user.password1)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
