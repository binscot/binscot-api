from typing import Optional

from pydantic import BaseModel


class ChatRoomBase(BaseModel):
    id: int
    room_name: str
    lock: bool
    limit_number_rooms: int
    user_in_room: Optional[str] = None


class ChatRoomInDB(ChatRoomBase):
    pass


class ChatRoomCreateReqDTO(BaseModel):
    room_name: str
    lock: bool
    hashed_password: Optional[str]
    limit_number_rooms: int


class ChatRoomResDTO(ChatRoomBase):
    pass
