from typing import List

from pydantic import BaseModel

from app.schemas.chat_schemas import ChatRoomResDTO
from app.schemas.map_schemas import MapResDTO
from app.schemas.post_schemas import PostResDTO
from app.schemas.token_schemas import TokenResDTO
from app.schemas.translator_schemas import TranslationResDTO, SensingResDTO
from app.schemas.user_schemas import UserResDTO
from app.schemas.weather_schemas import WeatherWeekResDTO, WeatherNowResDTO


class BaseResponseDTO(BaseModel):
    status_code: int
    data: (
           MapResDTO |
           ChatRoomResDTO |
           TranslationResDTO |
           SensingResDTO |
           WeatherNowResDTO |
           UserResDTO |
           TokenResDTO |
           PostResDTO |
           List[ChatRoomResDTO] |
           List[WeatherWeekResDTO] |
           List[UserResDTO] |
           List[PostResDTO]
           ) = None
    detail: str

    class Config:
        validate_assignment = True
