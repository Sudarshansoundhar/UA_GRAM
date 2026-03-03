from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.database.models import Post
from app.core.auth_bearer import admin_only

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.put("/posts/{post_id}/approve")
def approve_post(
    post_id: int,
    admin=Depends(admin_only),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.status = "APPROVED"
    post.is_flagged = False

    db.commit()

    return {"message": "Post approved successfully"}


@router.put("/posts/{post_id}/remove")
def remove_post(
    post_id: int,
    admin=Depends(admin_only),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.status = "REMOVED"

    db.commit()

    return {"message": "Post removed successfully"}
