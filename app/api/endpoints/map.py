from fastapi import APIRouter

from app.service import map_service
from app.schemas import map_schemas
router = APIRouter()


@router.post("/city")
async def get_location(
        map_data: map_schemas.MapData
):
    return map_service.get_location_by_city(map_data)
