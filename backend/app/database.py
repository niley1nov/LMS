# File: backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

# Build the SQLAlchemy URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
# Build the SQLAlchemy URL.
# If DB_HOST is a Unix socket path (starts with ‘/’), use `?host=` syntax.
if DB_HOST.startswith('/'):
    # Cloud Run will connect over the Unix socket at DB_HOST
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASS}@/{DB_NAME}?host={DB_HOST}"
    )
else:
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# Create engine and session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,   # ensure dropped connections are detected
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Initialize database (create tables)
def init_db():
    """
    Initialize the database by creating all tables.
    Uses SQLAlchemy metadata.create_all which is idempotent.
    """
    # Import models module to register table metadata
    from . import models  # relative import of models
    Base.metadata.create_all(bind=engine)
