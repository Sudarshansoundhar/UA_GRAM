from fastapi import Depends, HTTPException, WebSocket, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import User
from app.core.security import oauth2_scheme
from app.core.config import settings


# 🔐 REST AUTH
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401)

    return user


# 🔥 WEBSOCKET AUTH
async def get_current_user_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return None

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return type("User", (), payload)
    except JWTError:
        await websocket.close(code=1008)
        return None
