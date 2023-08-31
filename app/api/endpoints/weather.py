from fastapi import APIRouter

from app.service import weather_service
from app.schemas import map_schemas, weather_schemas
router = APIRouter()


@router.get("/week")
async def get_weather_week(map_data: map_schemas.MapData):
    return weather_service.get_weather_week(map_data)


@router.get("/now")
async def get_weather_now(map_data: map_schemas.MapData):
    return weather_service.get_weather_now(map_data)
