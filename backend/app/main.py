# backend/app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .config import get_origins
from .routes import auth
from .deps import get_current_user
from .database import init_db         # ← import your init helper

app = FastAPI()

# ▶️ Run once on startup to create any missing tables (idempotent)
@app.on_event("startup")
def on_startup():
    init_db()

# ▶️ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_origins(),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# ▶️ Routes
app.include_router(auth.router)

@app.get("/")
def health():
    return {"message": "LMS Backend working"}

@app.get("/protected")
def protected(user=Depends(get_current_user)):
    name = user.get('name') or user.get('email')
    return {"message": f"Hello {name}, you have access!"}
