from app.core.config import settings
from app.dto.response_dto import BaseResponseListDTO

KAKAO_TOKEN_URL = settings.KAKAO_TOKEN_URL
KAKAO_CLIENT_ID = settings.KAKAO_CLIENT_ID
KAKAO_SEND_URL = settings.KAKAO_SEND_URL


def get_access_token_by_refresh_token():
    return BaseResponseListDTO(
        status_code=200,
        data=None,
        detail="서비스 준비중 입니다."
    )


def send_server_state_kakao_message():
    return BaseResponseListDTO(
        status_code=200,
        data=None,
        detail="서비스 준비중 입니다."
    )

