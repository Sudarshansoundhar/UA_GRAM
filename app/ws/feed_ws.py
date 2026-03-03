from fastapi import WebSocket, WebSocketDisconnect, APIRouter

router = APIRouter()

active_connections: list[WebSocket] = []

@router.websocket("/ws/feed")
async def feed_socket(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast_feed_event(data: dict):
    for ws in active_connections:
        await ws.send_json(data)
