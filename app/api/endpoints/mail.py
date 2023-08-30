from fastapi import APIRouter

from app.dto.response_dto import BaseResponseDTO
from app.schemas import mail_schemas
from app.service import mail_service

router = APIRouter()


@router.post("/send", response_model=BaseResponseDTO)
async def send_email(email_data: mail_schemas.EmailData):
    return mail_service.send_email(email_data)
