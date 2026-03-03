from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.ai_guard import moderate_text
from app.database.db import get_db
from app.database.models import Comment, Post
from app.core.deps import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])


# ===============================
# ADD COMMENT (SAFE + AI FIX)
# ===============================
@router.post("/{post_id}")
def add_comment(
    post_id: int,
    content: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return {"error": "Post not found"}  # kept for compatibility

    # ================= AI MODERATION =================
    ai = moderate_text(content)

    if ai["level"] == "block":
        raise HTTPException(
            400,
            detail={
                "message": "Comment blocked by AI",
                "score": ai["score"],
                "reasons": ai["reasons"],
            },
        )

    if ai["level"] == "warn":
        return {"warning": True, "ai": ai}

    # ================= SAVE COMMENT =================
    comment = Comment(
        content=content,
        post_id=post_id,
        owner_id=user.id
    )

    db.add(comment)
    db.commit()

    return {"message": "Comment added"}  # unchanged


# ===============================
# GET COMMENTS (UNCHANGED)
# ===============================
@router.get("/{post_id}")
def get_comments(
    post_id: int,
    db: Session = Depends(get_db),
):
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()

    return [
        {
            "id": c.id,
            "content": c.content,
            "owner": c.owner.username,
        }
        for c in comments
    ]


# ===============================
# 🗑 DELETE COMMENT (UNCHANGED)
# ===============================
@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # 🔐 Only comment owner can delete
    if comment.owner_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed to delete this comment"
        )

    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted successfully"}