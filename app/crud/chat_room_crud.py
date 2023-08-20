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


def add_user_to_user_in_room(db, chat_room, new_username: str):
    chat_room.user_in_room.append(new_username)
    db.commit()
    return chat_room
