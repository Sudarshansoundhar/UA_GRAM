import os
from fastapi import Depends, HTTPException
from dotenv import load_dotenv
from app.core.deps import get_current_user

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

def admin_required(current_user=Depends(get_current_user)):
    if current_user.username != ADMIN_USERNAME:
        raise HTTPException(status_code=403, detail="Admin access only")
    return current_user
