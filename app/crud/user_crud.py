from typing import Type

from sqlalchemy.orm import Session

from app.models import models
from app.models.models import User
from app.schemas.user_schemas import UserInDB, UserCreate
from app.core import consts


def get_user_by_username(db: Session, username: str) -> UserInDB | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_user_id(db: Session, user_id: int) -> UserInDB | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[Type[UserInDB]]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    new_user = User(
        username=user.username,
        hashed_password=consts.password_context.hash(user.password1)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
