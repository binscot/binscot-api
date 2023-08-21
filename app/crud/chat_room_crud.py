from sqlalchemy.orm import Session

from app.models import models
from app.schemas import chat_schemas


def create_chat_room(db: Session, chat_room: chat_schemas.ChatRoomCreate):
    new_room = models.ChatRoom(**chat_room.__dict__)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    db.close()
    return new_room


def get_chat_room(db: Session, room_id: int):
    return db.query(models.ChatRoom).get(room_id)


def add_user_to_user_in_room(db, chat_room, username: str):
    new_username = str('/' + username + '/')
    if chat_room.user_in_room is None:
        chat_room.user_in_room = new_username
    else:
        chat_room.user_in_room = chat_room.user_in_room + new_username
    db.commit()
    db.refresh(chat_room)
    db.close()
    return chat_room


def get_room_by_room_name(db: Session, chat_room_name: str):
    return db.query(models.ChatRoom).filter(models.ChatRoom.room_name == chat_room_name).first()


def get_room_by_room_id(db: Session, chat_room_id: int) -> chat_schemas.ChatRoom | None:
    return db.query(models.ChatRoom).filter(models.ChatRoom.id == chat_room_id).first()
