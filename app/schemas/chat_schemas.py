from typing import Optional

from pydantic import BaseModel


class ChatRoomBase(BaseModel):
    room_name: str
    lock: bool
    hashed_password: Optional[str]
    limit_number_rooms: int
    user_in_room: Optional[str]


class ChatRoom(ChatRoomBase):
    id: int
    room_name: str
    lock: bool
    limit_number_rooms: int
    user_in_room: Optional[str]

    class Config:
        from_attributes = True


class ChatRoomCreate(ChatRoomBase):
    pass
