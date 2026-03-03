from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
from app.core.deps import get_current_user_ws

dm_ws_router = APIRouter(prefix="/ws/dm", tags=["DM WS"])

# chat_id -> list of sockets
active_connections: Dict[int, List[WebSocket]] = {}


# 🔥 REAL-TIME BROADCAST FUNCTION
async def broadcast_to_chat(chat_id: int, data: dict):
    connections = active_connections.get(chat_id, [])
    for ws in connections:
        try:
            await ws.send_json(data)
        except Exception:
            pass  # ignore broken sockets


@dm_ws_router.websocket("/{chat_id}")
async def chat_socket(websocket: WebSocket, chat_id: int):
    # 🔐 Authenticate user from token
    user = await get_current_user_ws(websocket)
    if not user:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    # ➕ Register socket
    active_connections.setdefault(chat_id, []).append(websocket)

    try:
        while True:
            data = await websocket.receive_json()

            # Echo / broadcast typing or live messages if needed
            await broadcast_to_chat(chat_id, {
                "type": "LIVE",
                "sender": user.username,
                "content": data.get("content"),
            })

    except WebSocketDisconnect:
        # ➖ Cleanup
        if chat_id in active_connections:
            if websocket in active_connections[chat_id]:
                active_connections[chat_id].remove(websocket)

            if not active_connections[chat_id]:
                del active_connections[chat_id]  