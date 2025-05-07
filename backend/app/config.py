# backend/app/config.py
import os
from dotenv import load_dotenv

# Load .env based on ENV
env = os.getenv("ENV", "development")
load_dotenv(f".env.{env}", override=True)

GOOGLE_CLIENT_ID  = os.getenv("GOOGLE_CLIENT_ID")
JWT_SECRET        = os.getenv("JWT_SECRET", "supersecret")
JWT_ALGORITHM     = os.getenv("JWT_ALGORITHM", "HS256")
FRONTEND_URL      = os.getenv("FRONTEND_URL")

# ─── Add this block ─────────────────────────────────────────────────────────────
# Database configuration
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
# ────────────────────────────────────────────────────────────────────────────────


def get_origins():
    """
    Return CORS origins: allow both HTTP and HTTPS localhost in dev,
    and the production FRONTEND_URL when set.
    """
    # Local development origins
    dev_http  = "http://localhost:3000"
    dev_https = "https://localhost:3000"
    dev_origins = [dev_http, dev_https]

    # Production frontend origin
    prod_origins = [FRONTEND_URL] if FRONTEND_URL else []

    return dev_origins + prod_origins
