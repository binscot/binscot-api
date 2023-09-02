from fastapi import APIRouter

from app.dto.response_dto import BaseResponseDTO
from app.schemas.map_schemas import MapReqDTO
from app.service import map_service

router = APIRouter()


@router.post("/city", response_model=BaseResponseDTO)
async def get_location(map_data: MapReqDTO):
    return map_service.get_location_by_city(map_data)
