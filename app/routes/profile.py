from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import uuid, os, shutil

from app.database.db import get_db
from app.database.models import User, Post, Follow
from app.core.deps import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])

PROFILE_DIR = "uploads/profile"
os.makedirs(PROFILE_DIR, exist_ok=True)

# ===============================
# 🔹 GET USER PROFILE
# ===============================
@router.get("/{username}")
def get_profile(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    posts = db.query(Post).filter(Post.owner_id == user.id).all()

    is_following = (
        db.query(Follow)
        .filter(
            Follow.follower_id == current_user.id,
            Follow.following_id == user.id,
        )
        .first()
        is not None
    )

    return {
    "username": user.username,
    "bio": user.bio,
    "profile_pic": user.profile_pic,
    "followers": len(user.followers),
    "following": len(user.following),
    "is_following": is_following,
    "is_self": user.id == current_user.id,   # ✅ IMPORTANT
    "posts": [
        {
            "id": p.id,
            "media_url": p.media_url,
        }
        for p in posts
    ],
}



# ===============================
# 🔹 EDIT PROFILE (BIO + PIC)
# ===============================
@router.put("/edit")
def edit_profile(
    bio: str = Form(""),
    profile_pic: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = db.query(User).filter(User.id == current_user.id).first()

    if bio is not None:
        user.bio = bio

    if profile_pic:
        if profile_pic.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid image type")

        ext = profile_pic.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        path = os.path.join(PROFILE_DIR, filename)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(profile_pic.file, buffer)

        user.profile_pic = filename

    db.commit()

    return {
        "message": "Profile updated successfully",
        "bio": user.bio,
        "profile_pic": user.profile_pic,
    }


# ===============================
# 🔹 FOLLOW / UNFOLLOW USER
# ===============================
@router.post("/{username}/follow")
def follow_unfollow_user(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    target = db.query(User).filter(User.username == username).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    if target.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    existing = (
        db.query(Follow)
        .filter(
            Follow.follower_id == current_user.id,
            Follow.following_id == target.id,
        )
        .first()
    )

    if existing:
        db.delete(existing)
        db.commit()
        return {"following": False}

    follow = Follow(
        follower_id=current_user.id,
        following_id=target.id,
    )
    db.add(follow)
    db.commit()

    return {"following": True} 