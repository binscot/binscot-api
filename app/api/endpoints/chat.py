from fastapi import APIRouter, Depends
from fastapi import Request, WebSocket
from sqlalchemy.orm import Session

from app.core import consts
from app.database.database import get_db
from app.schemas import chat_schemas
from app.service import chat_service

router = APIRouter()


@router.websocket("/ws/{room_name}/{username}")
async def subscribe_chat_room(websocket: WebSocket, room_name: str, username: str):
    await chat_service.subscribe_chat_room(websocket, room_name, username)


@router.get("/room")
async def client(request: Request):
    return consts.templates.TemplateResponse("chat.html", {"request": request})


@router.post("/create")
async def client(chat_room: chat_schemas.ChatRoomCreate, db: Session = Depends(get_db)):
    return chat_service.create_chat_room(db, chat_room)


@router.put("/add_user/{room_id}/{user_name}")
def add_user_to_room(room_id: int, user_name: str, db: Session = Depends(get_db)):
    return chat_service.add_user_chat_room(db, room_id, user_name)
