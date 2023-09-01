from fastapi import APIRouter

from app.dto.response_dto import WeatherWeekListResDTO, WeatherNowResDTO
from app.schemas import map_schemas
from app.service import weather_service

router = APIRouter()


@router.get("/week", response_model=WeatherWeekListResDTO)
async def get_weather_week(map_data: map_schemas.MapData):
    return weather_service.get_weather_week(map_data)


@router.get("/now", response_model=WeatherNowResDTO)
async def get_weather_now(map_data: map_schemas.MapData):
    return weather_service.get_weather_now(map_data)
