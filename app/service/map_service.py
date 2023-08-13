from fastapi import APIRouter, HTTPException, status
import requests

from app.core.config import settings

router = APIRouter()

OPENWEATHERMAP_API_KEY = settings.OPENWEATHERMAP_API_KEY
OPENWEATHERMAP_LOCATION_URL = settings.OPENWEATHERMAP_LOCATION_URL


def get_location_by_city(city, country_code):
    params = {
        "q": f"{city},{country_code}",
        "appid": OPENWEATHERMAP_API_KEY,
    }

    response = requests.get(OPENWEATHERMAP_LOCATION_URL, params=params)
    data = response.json()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="나라와 도시를 정확히 입력해주세요"
        )
    else:
        data = data[0]
    map_data = {
        "country": data['country'],
        "city": data['local_names']['ko'],
        "lat": data['lat'],
        "lon": data['lon']
    }

    return map_data
