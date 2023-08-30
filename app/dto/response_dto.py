from typing import Optional, List

from pydantic import BaseModel


class BaseResponseDTO(BaseModel):
    status_code: int
    data: Optional[dict] = None
    detail: str

    class Config:
        validate_assignment = True


class BaseResponseListDTO(BaseModel):
    status_code: int
    data: Optional[List] = None
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


class PostResponseDTO(BaseModel):
    id: int
    title: str
    content: str
    image: str
    owner_id: int
    owner_name: str


class TranslationResDTO(BaseModel):
    source_lang: str
    target_lang: str
    translated_text: str


class SensingResDTO(BaseModel):
    detected_language: str
