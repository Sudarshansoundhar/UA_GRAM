from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
import uuid, os, shutil
from app.services.ai_guard import moderate_text
from app.database.db import get_db
from app.database.models import Post, Like, Comment
from app.core.deps import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ===============================
# CREATE POST (AI ENABLED)
# ===============================
@router.post("/create")
def create_post(
    caption: str = Form(...),
    media: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # ================= AI MODERATION =================
    ai = moderate_text(caption)

    if ai["level"] == "block":
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Post blocked by AI",
                "score": ai["score"],
                "reasons": ai["reasons"],
            },
        )

    if ai["level"] == "warn":
        return {"warning": True, "ai": ai}

    # ================= FILE VALIDATION =================
    if media.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    filename = f"{uuid.uuid4()}.{media.filename.split('.')[-1]}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(media.file, buffer)

    post = Post(
        content=caption,
        media_url=filename,
        owner_id=user.id,
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return {"message": "Post created successfully"}


# ===============================
# GET POSTS (UNCHANGED)
# ===============================
@router.get("/")
def get_posts(db: Session = Depends(get_db), user=Depends(get_current_user)):
    posts = db.query(Post).order_by(Post.id.desc()).all()

    return [
        {
            "id": p.id,
            "content": p.content,
            "media_url": p.media_url,
            "owner": p.owner.username,
            "likes": len(p.likes),
            "comments": [
                {
                    "id": c.id,
                    "content": c.content,
                    "owner": c.owner.username,
                }
                for c in p.comments
            ],
        }
        for p in posts
    ]


# ===============================
# LIKE / UNLIKE (UNCHANGED)
# ===============================
@router.post("/{post_id}/like")
def like_post(post_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == user.id,
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"action": "unlike"}

    db.add(Like(user_id=user.id, post_id=post_id))
    db.commit()
    return {"action": "like"}


# ===============================
# ADD COMMENT (AI ENABLED)
# ===============================
@router.post("/{post_id}/comment")
def add_comment(
    post_id: int,
    content: str = Form(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # ================= AI MODERATION =================
    ai = moderate_text(content)

    if ai["level"] == "block":
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Comment blocked by AI",
                "score": ai["score"],
                "reasons": ai["reasons"],
            },
        )

    if ai["level"] == "warn":
        return {"warning": True, "ai": ai}

    comment = Comment(
        content=content,
        post_id=post_id,
        owner_id=user.id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return {
        "id": comment.id,
        "content": comment.content,
        "owner": user.username,
    }


# ===============================
# 🗑 DELETE POST (UNCHANGED)
# ===============================
@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this post")

    if post.media_url:
        file_path = os.path.join(UPLOAD_DIR, post.media_url)
        if os.path.exists(file_path):
            os.remove(file_path)

    db.query(Like).filter(Like.post_id == post_id).delete()
    db.query(Comment).filter(Comment.post_id == post_id).delete()

    db.delete(post)
    db.commit()

    return {"message": "Post deleted successfully"}