from app.core.config import settings
from app.schemas import mail_schemas
from app.service import weather_service, mail_service
from app.utils import miscellaneous_util
from app.schemas import map_schemas

OWNER_MAIL = settings.OWNER_MAIL


def get_server_state():
    to_email = OWNER_MAIL
    subject = "server state and weather"
    map_data = map_schemas.MapData(city="seoul", country_code="KR")
    try:
        cat_url = miscellaneous_util.get_random_cat_image()
        weather_seoul = weather_service.get_weather_now(map_data)
        weather_suwon = weather_service.get_weather_now(map_data)
        weather_detail_seoul = weather_seoul.get("weather") + " " + weather_seoul.get("weather_description")
        weather_detail_suwon = weather_suwon.get("weather") + " " + weather_suwon.get("weather_description")

        html_content = miscellaneous_util.read_html_file("./resource/mail.html")

        replacements = {
            r'this_time': weather_seoul.get("dt"),
            r'img_url': cat_url,
            r'weather_detail_seoul': weather_detail_seoul,
            r'weather_detail_suwon': weather_detail_suwon
        }

        replacement_string = miscellaneous_util.multiple_replace(html_content, replacements)

        return mail_schemas.EmailData(to_email=to_email, subject=subject, body=replacement_string)
    except Exception as e:
        return e


def send_server_state():
    email_data = get_server_state()
    return mail_service.send_email(email_data)
