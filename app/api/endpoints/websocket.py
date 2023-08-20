from fastapi import Request, APIRouter, WebSocket

from app.core import consts
from app.service import websocket_service

router = APIRouter()


@router.websocket("/ws/{room_id}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, username: str):
    await websocket_service.websocket_endpoint(websocket, room_id, username)


@router.get("/chat")
async def client(request: Request):
    return consts.templates.TemplateResponse("chat.html", {"request": request})

