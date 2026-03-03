from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from sqlalchemy.orm import Session
import uuid, os, shutil

from app.database.db import get_db
from app.database.models import Chat, Message, User, AIModerationLog
from app.core.deps import get_current_user
from app.plugins.ai_moderation.plugin import ai_plugin

router = APIRouter(prefix="/dm", tags=["DM"])

UPLOAD_DIR = "uploads/dm"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ================= CREATE / GET CHAT =================
@router.post("/{username}")
def create_or_get_chat(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    other = db.query(User).filter(User.username == username).first()
    if not other:
        raise HTTPException(status_code=404, detail="User not found")

    chat = (
        db.query(Chat)
        .filter(
            ((Chat.user1_id == current_user.id) & (Chat.user2_id == other.id)) |
            ((Chat.user1_id == other.id) & (Chat.user2_id == current_user.id))
        )
        .first()
    )

    if not chat:
        chat = Chat(user1_id=current_user.id, user2_id=other.id)
        db.add(chat)
        db.commit()
        db.refresh(chat)

    return {"chat_id": chat.id}


# ================= SEND MESSAGE =================
@router.post("/{chat_id}/send")
def send_message(
    chat_id: int,
    bypass_ai: bool = Query(False),
    content: str = Form(None),
    media: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    filename = None

    # SAVE MEDIA
    if media:
        ext = media.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        path = os.path.join(UPLOAD_DIR, filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(media.file, buffer)

    # AI MODERATION
    if content and not bypass_ai:
        ai_result = ai_plugin.process(content=content)
        score = ai_result.get("score", 0)
        reasons = ai_result.get("reasons", [])

        if score > 0.75:
            log = AIModerationLog(
                content=content,
                score=score,
                reasons=",".join(reasons),
                decision="blocked"
            )
            db.add(log)
            db.commit()

            return {"level": "block", "score": score, "reasons": reasons}

        if score > 0.5:
            log = AIModerationLog(
                content=content,
                score=score,
                reasons=",".join(reasons),
                decision="warned"
            )
            db.add(log)
            db.commit()

            return {"level": "warn", "score": score, "reasons": reasons}

    # SAVE MESSAGE
    message = Message(
        chat_id=chat_id,
        sender_id=user.id,
        content=content,
        media_url=filename,
        status="SENT",
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return {
        "id": message.id,  # 👈 IMPORTANT (for delete)
        "sender": user.username,
        "content": message.content,
        "media": message.media_url,
        "status": message.status,
    }


# ================= LOAD HISTORY =================
@router.get("/{chat_id}")
def get_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    messages = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.id)
        .all()
    )

    return [
        {
            "id": m.id,  # 👈 needed for delete
            "sender": m.sender.username if m.sender else None,
            "content": m.content,
            "media": m.media_url,
            "status": m.status,
        }
        for m in messages
    ]


# ================= 🗑 DELETE MESSAGE =================
@router.delete("/message/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    message = db.query(Message).filter(Message.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    # 🔐 Only sender can delete
    if message.sender_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Delete media file if exists
    if message.media_url:
        file_path = os.path.join(UPLOAD_DIR, message.media_url)
        if os.path.exists(file_path):
            os.remove(file_path)

    db.delete(message)
    db.commit()

    return {"message": "Message deleted successfully"}