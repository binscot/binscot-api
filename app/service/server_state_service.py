from app.core.config import settings
from app.schemas import mail_schemas
from app.service import weather_service

OWNER_MAIL = settings.OWNER_MAIL


def get_server_state():
    to_email = OWNER_MAIL
    subject = ""
    weather_seoul = weather_service.get_weather_now(city="seoul", country_code="KR")
    weather_suwon = weather_service.get_weather_now(city="suwon", country_code="KR")
    weather_detail_seoul = weather_seoul.get("weather") + " " + weather_seoul.get("weather_description")
    weather_detail_suwon = weather_suwon.get("weather") + " " + weather_suwon.get("weather_description")

    body = "현재시각 :" + weather_seoul.get("dt")
    # params = {
    #     "object_type": "feed",
    #
    #     "content": {
    #         "title": "server-1 : OK server-2 : OK",
    #         "image_url": cat_url,
    #         "image_width": 640,
    #         "image_height": 640,
    #         "link": {
    #             "web_url": "",
    #             "mobile_web_url": "",
    #             "android_execution_params": "",
    #             "ios_execution_params": ""
    #         }
    #     },
    #     "item_content": {
    #         "profile_text": "Server Status and Weather",
    #
    #         "items": [
    #             {"item": "현재시각", "item_op": weather_seoul.get("dt")},
    #             {"item": "도시", "item_op": "서울"},
    #             {"item": "날씨", "item_op": weather_detail_seoul},
    #             {"item": "도시", "item_op": "수원"},
    #             {"item": "날씨", "item_op": weather_detail_suwon},
    #
    #         ]
    #     }
    # }

    #
    # requests.post(KAKAO_SEND_URL, headers=KA_HEADER, data=payload)
    #
    # if response.status_code == 200:
    #     logging.info("카카오 피드 메시지가 전송되었습니다.")
    #     return {"status_code": 200, "message": "카카오 피드 메시지가 전송되었습니다."}
    # else:
    #     logging.info("카카오 피드 메시지 전송에 실패했습니다.")
    #     raise HTTPException(status_code=500, detail="카카오 피드 메시지 전송에 실패했습니다.")

    return mail_schemas.EmailData(to_email=to_email, subject=subject, body=body)
