from fastapi import WebSocket


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
