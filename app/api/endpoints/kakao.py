from fastapi import APIRouter

from app.service import kakao_service

router = APIRouter()


@router.get("/send_server_state")
async def send_server_state_kakao_message():
    return kakao_service.send_server_state_kakao_message()


@router.post("/token")
def get_kakao_token():
    return kakao_service.get_access_token_by_refresh_token()


