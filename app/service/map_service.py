import requests

from app.core.config import settings
from app.dto import base_response_dto, map_response

OPENWEATHERMAP_API_KEY = settings.OPENWEATHERMAP_API_KEY
OPENWEATHERMAP_LOCATION_URL = settings.OPENWEATHERMAP_LOCATION_URL


def get_location_by_city(map_data):
    params = {
        "q": f"{map_data.city},{map_data.country_code}",
        "appid": OPENWEATHERMAP_API_KEY,
    }

    data = requests.get(OPENWEATHERMAP_LOCATION_URL, params=params).json()

    if not data:
        return base_response_dto.BaseResponseDTO(
            status_code=200,
            data=None,
            detail='나라와 도시를 정확히 입력해주세요'
        )
    else:
        data = data[0]

    response_data = map_response.MapResponseDTO(city=data['local_names']['ko'], country=data['country'],
                                                lat=data['lat'], lon=data['lon'])
    return base_response_dto.BaseResponseDTO(
        status_code=200,
        data=response_data.__dict__,
        detail='success'
    )
