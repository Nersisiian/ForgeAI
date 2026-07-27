import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.redis import redis_client
from app.core.security import decode_token

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, message: dict, user_id: str):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001)
        return
    payload = decode_token(token)
    if not payload:
        await websocket.close(code=4001)
        return
    user_id = payload["sub"]
    await manager.connect(websocket, user_id)
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(f"project:{project_id}")
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await manager.send_personal_message(data, user_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await pubsub.unsubscribe(f"project:{project_id}")
