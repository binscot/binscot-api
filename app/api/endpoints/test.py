from fastapi import APIRouter

from app.service import server_state_service, mail_service

router = APIRouter()


@router.get("/")
async def test():
    return mail_service.send_email_server_state(server_state_service.get_server_state())
