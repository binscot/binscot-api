from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from app.schemas.post_schemas import Post
from app.schemas.user_schemas import User


class MapResDTO(BaseModel):
    city: str
    country: str
    lat: float
    lon: float


class ChatRoomResDTO(BaseModel):
    id: int
    room_name: str
    lock: bool
    limit_number_rooms: int
    user_in_room: Optional[str]


class PostResDTO(BaseModel):
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


class WeatherNowResDTO(BaseModel):
    kst_time: datetime
    city: str
    country: str
    lon: Optional[float]
    lat: Optional[float]
    weather_main: str
    description: str
    icon: str
    last_rain_3h: Optional[str]
    last_rain_1h: Optional[str]
    last_snow_3h: Optional[str]
    last_snow_1h: Optional[str]
    celsius: float
    feels_like: float
    celsius_min: float
    celsius_max: float
    humidity: str
    wind: str
    sunrise: datetime
    sunset: datetime


class WeatherWeekResDTO(BaseModel):
    kst_time: datetime
    celsius: float
    feels_like: float
    celsius_min: float
    celsius_max: float
    icon: str
    wind: str
    last_rain_3h: Optional[str]
    last_snow_3h: Optional[str]
    humidity: str
    weather_main: str
    weather_description: str
    pop: str


class WeatherWeekListResDTO(BaseModel):
    data: List[WeatherWeekResDTO] = None


class UserResDTO(BaseModel):
    id: int
    username: EmailStr
    disabled: bool | None = None
    posts: List[Post] = []


class UserListResDTO(BaseModel):
    user_list: List[User]


class TokenResDTO(BaseModel):
    access_token: str
    token_type: str
    username: EmailStr


class BaseResponseDTO(BaseModel):
    status_code: int
    data: (Optional[dict] |
           MapResDTO |
           ChatRoomResDTO |
           PostResDTO |
           TranslationResDTO |
           SensingResDTO |
           WeatherWeekResDTO |
           WeatherNowResDTO |
           WeatherWeekListResDTO |
           UserResDTO |
           UserListResDTO |
           List[WeatherWeekResDTO] |
           List[UserResDTO] |
           TokenResDTO
           ) = None
    detail: str

    class Config:
        validate_assignment = True


class BaseResponseListDTO(BaseModel):
    status_code: int
    data: Optional[List] = None
    detail: str

    class Config:
        validate_assignment = True
