from typing import Type

from sqlalchemy.orm import Session

from app.core import consts
from app.models.models import User
from app.schemas import user_schemas
from app.schemas.user_schemas import UserInDB, UserResDTO


def get_user_by_username(db: Session, username: str) -> UserInDB | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_user_id(db: Session, user_id: int) -> user_schemas.UserInDB | None:
    return db.query(User).get(user_id)


def get_users(db: Session) -> list[Type[UserResDTO]]:
    return db.query(User).all()


def create_user(db: Session, user: user_schemas.UserCreateReqDTO):
    new_user = User(
        username=user.username,
        hashed_password=consts.password_context.hash(user.password1)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
