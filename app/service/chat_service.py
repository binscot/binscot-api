import json

import redis
from fastapi import WebSocket, WebSocketDisconnect, HTTPException
from app.crud import chat_room_crud
from app.core.config import settings
from app.utils import websocket_util, miscellaneous_util

REDIS_SERVER = settings.REDIS_SERVER
REDIS_PORT = settings.REDIS_PORT
REDIS_DB = settings.REDIS_DB
REDIS_PASSWORD = settings.REDIS_PASSWORD

redis_server = redis.Redis(host=REDIS_SERVER, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
manager = websocket_util.ConnectionManager()


async def subscribe_chat_room(websocket: WebSocket, room_name: str, username: str):
    await manager.connect(websocket, room_name, username)

    try:
        messages = redis_server.lrange(f"messages:{room_name}", 0, -1)
        for message in messages:
            await manager.broadcast(miscellaneous_util.byte_to_json_str(message))
        while True:
            message = await websocket.receive_text()
            message_data = {
                "author": username,
                "message": json.loads(message)["message"]
            }
            await manager.broadcast(json.dumps(message_data))
            redis_server.lpush(f"messages:{room_name}", json.dumps(message_data))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client {username} disconnected")
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
        manager.disconnect(websocket)


def create_chat_room(db, chat_room):
    chat_room_in_db = chat_room_crud.get_room_by_room_name(db, chat_room_name=chat_room.room_name)
    if chat_room_in_db:
        raise HTTPException(status_code=400, detail="room_name already registered")
    return chat_room_crud.create_chat_room(db, chat_room)


def add_user_to_room(db, room_id, user_name: str):
    user_name = user_name.strip()
    chat_room_in_db = chat_room_crud.get_room_by_room_id(db, room_id)
    if not chat_room_in_db:
        raise HTTPException(status_code=400, detail="Room not found")
    if chat_room_in_db.user_in_room is not None and str('/' + user_name + '/') in chat_room_in_db.user_in_room:
        raise HTTPException(status_code=400, detail="already username in the Room")
    return chat_room_crud.add_user_to_user_in_room(db, chat_room_in_db, user_name)


def remove_user_from_room(db, room_id, user_name: str):
    chat_room_in_db = chat_room_crud.get_room_by_room_id(db, room_id)
    if chat_room_in_db is None:
        raise HTTPException(status_code=400, detail="Room is already empty")
    if str('/' + user_name + '/') in chat_room_in_db.user_in_room:
        return chat_room_crud.remove_user_from_user_in_room(db, chat_room_in_db, user_name)
    else:
        raise HTTPException(status_code=400, detail="user is not in the room")
