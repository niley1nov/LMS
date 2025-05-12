# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os # Keep os import for getenv

from app.core.config import settings
from app.api.v1.api_v1 import api_router as api_v1_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.SHOW_DOCS else None,
    docs_url=f"{settings.API_V1_STR}/docs" if settings.SHOW_DOCS else None,
    redoc_url=f"{settings.API_V1_STR}/redoc" if settings.SHOW_DOCS else None,
    version=settings.PROJECT_VERSION,
)

# --- Simplified CORS Middleware for Debugging ---
print("--- CORS Configuration (DEBUG MODE) ---")
# For debugging, allow any origin, method, header.
# This helps isolate if the problem is with specific origin matching
# or something else.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
    # max_age=600, # Optional
)
print("CORS Middleware added with allow_origins=['*'] (DEBUG MODE)")
print("--- End CORS Configuration ---")


@app.on_event("startup")
async def on_startup():
    print(f"Application startup: {settings.PROJECT_NAME} - Version: {settings.PROJECT_VERSION} (ENV: {settings.ENV})")
    # The following print statements from your config.py will still run and show parsed values
    # print(f"--- Config: Loaded settings for effective ENV='{settings.ENV}' ---")
    # print(f"--- Config: Loaded BACKEND_CORS_ORIGINS='{settings.BACKEND_CORS_ORIGINS}' ---")
    # print(f"--- Config: Loaded DB_HOST='{settings.DB_HOST}' ---")
    if not settings.SHOW_DOCS:
        print("API docs are disabled.")
    else:
        print(f"API docs available at: {settings.API_V1_STR}/docs and {settings.API_V1_STR}/redoc")

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": f"{settings.PROJECT_NAME} is healthy!"}

@app.get("/", tags=["Root"], include_in_schema=False)
async def read_root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.PROJECT_VERSION,
        "docs_url": f"{settings.API_V1_STR}/docs" if settings.SHOW_DOCS else "API Docs Disabled",
    }
