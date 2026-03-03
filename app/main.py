from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database.db import engine
from app.database import models
from app.routes import auth, posts, admin, comments, profile, dm
from app.routes.dm_ws import dm_ws_router
from app.ws.feed_ws import router as feed_ws_router
from app.routes.admin_ai import router as admin_ai_router

# ===============================
# DATABASE INIT
# ===============================
models.Base.metadata.create_all(bind=engine)

# ===============================
# CREATE APP FIRST (IMPORTANT)
# ===============================
app = FastAPI(title="Cyberbullying AI System")

# ===============================
# CORS (SAFE + UPLOAD FRIENDLY)
# ===============================
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ===============================
# ROUTERS (HTTP)
# ===============================
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(profile.router)
app.include_router(comments.router)
app.include_router(dm.router)
app.include_router(admin.router)
app.include_router(admin_ai_router)   # ✅ FIXED POSITION

# ===============================
# WEBSOCKETS
# ===============================
app.include_router(feed_ws_router)
app.include_router(dm_ws_router)

# ===============================
# STATIC FILES
# ===============================
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ===============================
# AI TEST ENDPOINT
# ===============================
@app.get("/test-ai")
def test_ai():
    from app.plugins.ai_moderation.plugin import ai_plugin
    return ai_plugin.process("you are an idiot")
