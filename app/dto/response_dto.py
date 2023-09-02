from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from app.schemas.chat_schemas import ChatRoomResDTO
from app.schemas.user_schemas import UserResDTO


class MapResDTO(BaseModel):
    city: str
    country: str
    lat: float
    lon: float




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
           List[WeatherWeekResDTO] |
           List[UserResDTO] |
           TokenResDTO |
           List[ChatRoomResDTO]

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
