# backend/app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from app.core.config import settings # Import your Pydantic settings

# Create an asynchronous SQLAlchemy engine
# The SQLALCHEMY_DATABASE_URI is now constructed and validated in your Settings model
# in app/core/config.py
async_engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), # Ensure it's a string
    pool_pre_ping=True,  # Check connections before use
    # echo=True, # Set to True for debugging SQL queries (can be noisy)
    # pool_recycle=3600, # Optional: recycle connections after 1 hour
    # connect_args={"options": "-c timezone=utc"} # Example: set timezone for connection
)

# Create an asynchronous session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession, # Use AsyncSession for asynchronous operations
    expire_on_commit=False, # Good default for FastAPI to prevent issues with detached objects
    autocommit=False,
    autoflush=False,
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an SQLAlchemy asynchronous database session.
    Ensures the session is closed after the request.
    """
    async with AsyncSessionLocal() as session:
        try:
            print('yielding db session')
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
