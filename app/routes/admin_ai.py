from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import AIModerationLog
from app.core.admin_guard import admin_required

router = APIRouter(prefix="/admin/ai", tags=["Admin AI"])


# ===============================
# GET ALL AI LOGS
# ===============================
@router.get("/logs")
def get_logs(
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    logs = db.query(AIModerationLog).order_by(AIModerationLog.id.desc()).all()

    return [
        {
            "id": l.id,
            "content": l.content,
            "score": l.score,
            "reasons": l.reasons.split(",") if l.reasons else [],
            "decision": l.decision
        }
        for l in logs
    ]


# ===============================
# APPROVE AI DECISION
# ===============================
@router.post("/approve/{log_id}")
def approve(
    log_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    log = db.query(AIModerationLog).get(log_id)

    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    log.decision = "approved"
    db.commit()

    return {"status": "approved"}


# ===============================
# REJECT AI DECISION
# ===============================
@router.post("/reject/{log_id}")
def reject(
    log_id: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_required)
):
    log = db.query(AIModerationLog).get(log_id)

    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    log.decision = "rejected"
    db.commit()

    return {"status": "rejected"}
