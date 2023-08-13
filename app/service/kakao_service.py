import json

import requests
from fastapi import HTTPException

from app.core.config import settings
from app.service import weather_service

KAKAO_TOKEN_URL = settings.KAKAO_TOKEN_URL
KAKAO_CLIENT_ID = settings.KAKAO_CLIENT_ID
KAKAO_SEND_URL = settings.KAKAO_SEND_URL
RANDOM_CAT_URL = settings.RANDOM_CAT_URL


def get_access_token_by_refresh_token():
    with open("resource/kakao_refresh_code.json", "r") as fp:
        loaded_tokens = json.load(fp)

    data = {
        "grant_type": "refresh_token",
        "client_id": KAKAO_CLIENT_ID,
        "refresh_token": loaded_tokens.get("refresh_token")
    }

    response = requests.post(KAKAO_TOKEN_URL, data=data).json()

    if "refresh_token" in response:
        with open("resource/kakao_refresh_code.json", "w") as fp:
            json.dump(response, fp)

        return response.get("access_token")

    if "access_token" in response:
        with open("resource/kakao_access_code.json", "w") as fp:
            json.dump(response, fp)

        return response.get("access_token")

    return None


def send_server_state_kakao_message():
    cat_url = get_random_cat_image()
    weather_seoul = weather_service.get_weather_now(city="seoul", country_code="KR")
    weather_suwon = weather_service.get_weather_now(city="suwon", country_code="KR")
    weather_detail_seoul = weather_seoul.get("weather") + " " + weather_seoul.get("weather_description")
    weather_detail_suwon = weather_suwon.get("weather") + " " + weather_suwon.get("weather_description")

    params = {
        "object_type": "feed",

        "content": {
            "title": "server-1 : OK server-2 : OK",
            "image_url": cat_url,
            "image_width": 640,
            "image_height": 640,
            "link": {
                "web_url": "",
                "mobile_web_url": "",
                "android_execution_params": "",
                "ios_execution_params": ""
            }
        },
        "item_content": {
            "profile_text": "Server Status and Weather",

            "items": [
                {"item": "현재시각", "item_op": weather_seoul.get("dt")},
                {"item": "도시", "item_op": "서울"},
                {"item": "날씨", "item_op": weather_detail_seoul},
                {"item": "도시", "item_op": "수원"},
                {"item": "날씨", "item_op": weather_detail_suwon},

            ]
        }
    }

    access_token = get_access_token_by_refresh_token()

    if access_token is None:
        raise HTTPException(status_code=500, detail="access_token 생성이 실패했습니다.")

    KA_HEADER = {
        "Authorization": "Bearer " + access_token
    }

    payload = {
        "template_object": json.dumps(params)
    }

    response = requests.post(KAKAO_SEND_URL, headers=KA_HEADER, data=payload)

    if response.status_code == 200:
        return {"status_code": 200, "message": "카카오 피드 메시지가 전송되었습니다."}
    else:
        raise HTTPException(status_code=500, detail="카카오 피드 메시지 전송에 실패했습니다.")


def get_random_cat_image():
    response = requests.get(RANDOM_CAT_URL)
    data = response.json()

    if data:
        cat_image_url = data[0]['url']
        return cat_image_url
    else:
        return None
