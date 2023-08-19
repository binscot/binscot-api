import json
import redis
from fastapi import Request, APIRouter, WebSocket, WebSocketDisconnect
from app.core import consts
from app.core.config import settings

REDIS_SERVER = settings.REDIS_SERVER
REDIS_PORT = settings.REDIS_PORT
REDIS_DB = settings.REDIS_DB
REDIS_PASSWORD = settings.REDIS_PASSWORD

router = APIRouter()

redis_server = redis.Redis(host=REDIS_SERVER, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket, room_id: str, username: str):
        await websocket.accept()
        self.active_connections.append((websocket, room_id, username))

    def disconnect(self, websocket: WebSocket):
        connection = next((c for c in self.active_connections if c[0] == websocket), None)
        if connection:
            self.active_connections.remove(connection)

    async def send_chat_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection, _, _ in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{room_id}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, username: str):
    await manager.connect(websocket, room_id, username)

    try:
        messages = redis_server.lrange(f"messages:{room_id}", 0, -1)
        for message in messages:
            await manager.send_chat_message(message, websocket)

        while True:
            message = await websocket.receive_text()
            message_content = json.loads(message)["message"]
            message_data = {
                "author": username,
                "message": message_content
            }

            await manager.broadcast(json.dumps(message_data))
            redis_server.lpush(f"messages:{room_id}", json.dumps(message_data))

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client {username} disconnected")
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
        manager.disconnect(websocket)


@router.get("/chat")
async def client(request: Request):
    return consts.templates.TemplateResponse("chat.html", {"request": request})

