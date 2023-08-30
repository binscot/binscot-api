from fastapi import APIRouter

from app.service import kakao_service
from app.dto.response_dto import BaseResponseDTO

router = APIRouter()


@router.get("/send_server_state", response_model=BaseResponseDTO)
async def send_server_state_kakao_message():
    return kakao_service.send_server_state_kakao_message()


@router.post("/token", response_model=BaseResponseDTO)
def get_kakao_token():
    return kakao_service.get_access_token_by_refresh_token()


