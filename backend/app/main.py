# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from contextlib import asynccontextmanager
from app.api.v1.api_v1 import api_router as api_v1_router

@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    print(f"--- Lifespan Event: Application Startup ---")
    print(f"Application Name: {settings.PROJECT_NAME} - Version: {settings.PROJECT_VERSION} (ENV: {settings.ENV})")
    if not settings.SHOW_DOCS:
        print("API docs are disabled.")
    else:
        print(f"API docs available at: {settings.API_V1_STR}/docs and {settings.API_V1_STR}/redoc")
    
    print(f"--- Lifespan Event: Startup Complete. Application is ready. ---")
    yield # This is where the application runs
    
    print(f"--- Lifespan Event: Application Shutdown ---")
    print(f"--- Lifespan Event: Shutdown Complete. ---")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.SHOW_DOCS else None,
    docs_url=f"{settings.API_V1_STR}/docs" if settings.SHOW_DOCS else None,
    redoc_url=f"{settings.API_V1_STR}/redoc" if settings.SHOW_DOCS else None,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)


if settings.BACKEND_CORS_ORIGINS_STR_LIST:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS_STR_LIST,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=[
            "Accept", "Accept-Language", "Content-Language", "Content-Type",
            "Authorization", "X-Requested-With",
        ],
        expose_headers=["Content-Disposition"],
        max_age=600,
    )
else:
    print("CORS: No specific origins configured. CORSMiddleware not added with specific origins.")

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
