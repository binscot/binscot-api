import json

import redis
from fastapi import WebSocket, WebSocketDisconnect

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
