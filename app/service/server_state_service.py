import json

from app.core.config import settings
from app.schemas import mail_schemas
from app.schemas import map_schemas
from app.service import weather_service, mail_service
from app.utils import miscellaneous_util

OWNER_MAIL = settings.OWNER_MAIL


def get_server_state():
    to_email = OWNER_MAIL
    subject = "server state and weather"
    mail_template = "server_state_template.html"
    map_data = map_schemas.MapData(city="seoul", country_code="KR")
    try:
        cat_url = miscellaneous_util.get_random_cat_image()
        weather_seoul = weather_service.get_weather_now(map_data)
        weather_suwon = weather_service.get_weather_now(map_data)

        replacements = {
            "cat_url": cat_url,
            "kst_time": weather_seoul.kst_time.strftime("%m월%d일 %H시%M분"),
            "weather_main_suwon": weather_suwon.weather_main,
            "description_suwon": weather_suwon.description,
            "weather_main_seoul": weather_seoul.weather_main,
            "description_seoul": weather_seoul.description,
            "last_rain_1h_seoul": weather_seoul.last_rain_1h,
            "last_rain_1h_suwon": weather_suwon.last_rain_1h,
            "last_snow_1h_seoul": weather_seoul.last_snow_1h,
            "last_snow_1h_suwon": weather_suwon.last_snow_1h,
            "celsius_seoul": weather_seoul.celsius,
            "celsius_suwon": weather_suwon.celsius,
            "humidity_seoul": weather_seoul.humidity,
            "humidity_suwon": weather_suwon.humidity,
            "sunrise_seoul": weather_seoul.sunrise.strftime("%m월%d일 %H시%M분"),
            "sunset_seoul": weather_seoul.sunset.strftime("%m월%d일 %H시%M분")
        }

        return mail_schemas.EmailData(to_email=to_email, subject=subject, body=json.dumps(replacements),
                                      template=mail_template)
    except Exception as e:
        return e


def send_server_state():
    return mail_service.send_email_server_state(get_server_state())
