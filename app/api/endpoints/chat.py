from fastapi import Request, APIRouter, WebSocket

from app.core import consts
from app.service import chat_service

router = APIRouter()


@router.websocket("/ws/{room_name}/{username}")
async def subscribe_chat_room(websocket: WebSocket, room_name: str, username: str):
    await chat_service.subscribe_chat_room(websocket, room_name, username)


@router.get("/room")
async def client(request: Request):
    return consts.templates.TemplateResponse("chat.html", {"request": request})

