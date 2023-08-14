from fastapi import APIRouter

from app.service import map_service

router = APIRouter()


@router.post("/city")
async def get_location(city: str, country_code: str):
    return map_service.get_location_by_city(city=city, country_code=country_code)
