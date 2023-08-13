from fastapi import APIRouter

from app.service import weather_service

router = APIRouter()


@router.get("/week")
async def get_weather_week(city: str, country_code: str):
    weather_today = weather_service.get_weather_week(city=city, country_code=country_code)
    return weather_today


@router.get("/now")
async def get_weather_now(city: str, country_code: str):
    weather_now = weather_service.get_weather_now(city=city, country_code=country_code)
    return weather_now
