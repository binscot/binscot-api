from fastapi import APIRouter, HTTPException, status
import requests

from app.core.config import settings

router = APIRouter()

OPENWEATHERMAP_API_KEY = settings.OPENWEATHERMAP_API_KEY
OPENWEATHERMAP_LOCATION_URL = settings.OPENWEATHERMAP_LOCATION_URL


def get_location_by_city(map_data):

    params = {
        "q": f"{map_data.city},{map_data.country_code}",
        "appid": OPENWEATHERMAP_API_KEY,
    }

    data = requests.get(OPENWEATHERMAP_LOCATION_URL, params=params).json()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="나라와 도시를 정확히 입력해주세요"
        )
    else:
        data = data[0]

    return {
        "country": data['country'],
        "city": data['local_names']['ko'],
        "lat": data['lat'],
        "lon": data['lon']
    }
