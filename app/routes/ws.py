from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
from app.database.models import Message
from app.database.db import SessionLocal

connections = {}

async def websocket_endpoint(websocket: WebSocket, chat_id: int, user_id: int):
    await websocket.accept()
    connections.setdefault(chat_id, []).append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            db = SessionLocal()
            msg = Message(
                chat_id=chat_id,
                sender_id=user_id,
                content=data,
                timestamp=datetime.utcnow().isoformat()
            )
            db.add(msg)
            db.commit()
            db.close()

            for ws in connections[chat_id]:
                await ws.send_text(data)

    except WebSocketDisconnect:
        connections[chat_id].remove(websocket)
