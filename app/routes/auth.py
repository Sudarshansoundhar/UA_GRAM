from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.database.db import get_db
from app.database.models import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# =========================
# Pydantic Schemas
# =========================

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    username: str
    profile_pic: str | None


# =========================
# Register
# =========================

@router.post("/register")
def register_user(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(
        (User.username == data.username) |
        (User.email == data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        role="USER",
    )

    db.add(user)
    db.commit()

    return {"message": "User registered successfully"}


# =========================
# Login
# =========================

@router.post("/login", response_model=LoginResponse)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token = create_access_token(
        {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username,              # ✅ REQUIRED
        "profile_pic": user.profile_pic,        # ✅ REQUIRED
    }
