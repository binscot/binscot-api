from fastapi import Request, APIRouter, WebSocket

from app.core import consts
from app.service import chat_service

router = APIRouter()


@router.websocket("/ws/{room_id}/{username}")
async def subscribe_chat_room(websocket: WebSocket, room_id: str, username: str):
    await chat_service.subscribe_chat_room(websocket, room_id, username)


@router.get("/room")
async def client(request: Request):
    return consts.templates.TemplateResponse("chat.html", {"request": request})

