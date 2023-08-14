from fastapi import APIRouter

from app.service import server_state_service, mail_service

router = APIRouter()


@router.get("/")
async def test():
    email_data = server_state_service.get_server_state()
    return mail_service.send_email(email_data)
