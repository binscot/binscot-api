from typing import Optional

from pydantic import BaseModel


class BaseResponseDTO(BaseModel):
    status_code: int
    data: Optional[dict] = None
    detail: str

    class Config:
        validate_assignment = True


class MapResponseDTO(BaseModel):
    city: str
    country: str
    lat: float
    lon: float


class ChatRoomResponseDTO(BaseModel):
    id: int
    room_name: str
    lock: bool
    limit_number_rooms: int
    user_in_room: Optional[str]
