from fastapi import APIRouter

from app.dto.response_dto import BaseResponseDTO
from app.schemas.map_schemas import MapReqDTO
from app.service import weather_service

router = APIRouter()


@router.get("/week", response_model=BaseResponseDTO)
async def get_weather_week(map_data: MapReqDTO):
    return weather_service.get_weather_week(map_data)


@router.get("/now", response_model=BaseResponseDTO)
async def get_weather_now(map_data: MapReqDTO):
    return weather_service.get_weather_now(map_data)
