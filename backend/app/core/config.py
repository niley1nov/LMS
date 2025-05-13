# backend/app/core/config.py
import os
from typing import List, Union, Optional, Any
from pydantic import AnyHttpUrl, field_validator, PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

APP_ENV = os.getenv("APP_ENV", "development").lower()
env_files_to_load_list = []

if APP_ENV == "production":
    if os.path.exists(".env.production"):
        env_files_to_load_list.append(".env.production")
    else:
        print("Warning: APP_ENV is 'production' but .env.production file not found. Relying on shell environment variables.")
elif APP_ENV == "development":
    if os.path.exists(".env.development"):
        env_files_to_load_list.append(".env.development")
    else:
        print("Warning: APP_ENV is 'development' but .env.development file not found.")
else:
    custom_env_file = f".env.{APP_ENV}"
    if os.path.exists(custom_env_file):
        env_files_to_load_list.append(custom_env_file)
    else:
        print(f"Warning: APP_ENV is '{APP_ENV}' but {custom_env_file} not found. Falling back to .env.development if it exists, or shell env vars.")
        if os.path.exists(".env.development"):
            env_files_to_load_list.append(".env.development")


effective_env_files = tuple(env_files_to_load_list) if env_files_to_load_list else None

print(f"--- Config: Effective .env files to be loaded by Pydantic: {effective_env_files} (based on APP_ENV='{APP_ENV}') ---")

class Settings(BaseSettings):
    """
    Application settings.
    Loads values from environment variables and specified .env files.
    """
    # --- Project Information ---
    PROJECT_NAME: str = "LMS Backend"
    PROJECT_VERSION: str = "0.1.0"
    ENV: str = APP_ENV

    # --- API Configuration ---
    API_V1_STR: str = "/api/v1"
    SHOW_DOCS: bool = True

    # --- Security and JWT ---
    JWT_SECRET: str = "JWT_secert"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # --- Frontend URL ---
    FRONTEND_URL: Optional[AnyHttpUrl] = None

    # --- CORS ---
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    BACKEND_CORS_ORIGINS_STR_LIST: List[str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    @classmethod
    def assemble_cors_origins_from_env(cls, v: Any) -> Any:
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            if not v.strip():
                return []
            if not v.strip().startswith('['): # Likely a comma-separated string
                return [item.strip() for item in v.split(',') if item.strip()]
            # If it starts with '[', let Pydantic try to parse it as JSON
        return v
    
    @model_validator(mode='after')
    def process_cors_origins_to_strings(self) -> 'Settings':
        """
        After BACKEND_CORS_ORIGINS is validated (as List[AnyHttpUrl]),
        this validator converts them to a list of strings for the middleware.
        """
        if self.BACKEND_CORS_ORIGINS:
            if isinstance(self.BACKEND_CORS_ORIGINS, list):
                processed_list = []
                for origin_url_obj in self.BACKEND_CORS_ORIGINS:
                    processed_list.append(str(origin_url_obj).rstrip('/'))
                self.BACKEND_CORS_ORIGINS_STR_LIST = processed_list
            else:
                print(f"Warning: BACKEND_CORS_ORIGINS was expected to be a list after validation, but got {type(self.BACKEND_CORS_ORIGINS)}")
                self.BACKEND_CORS_ORIGINS_STR_LIST = []
        else:
            self.BACKEND_CORS_ORIGINS_STR_LIST = []
        return self

    # --- Database Configuration ---
    DB_USER: Optional[str] = "dbuser"
    DB_PASS: Optional[str] = "dbpass"
    DB_HOST: Optional[str] = "127.0.0.1"
    DB_PORT: Optional[str] = "5432"
    DB_NAME: Optional[str] = "dbname"

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @model_validator(mode='after')
    def assemble_db_connection(self) -> 'Settings':
        if self.SQLALCHEMY_DATABASE_URI:
            return self
        dsn_str: Optional[str] = None
        if self.DB_HOST and self.DB_HOST.startswith("/cloudsql/"):
            dsn_str = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@localhost/{self.DB_NAME}?host={self.DB_HOST.strip()}"
        elif self.DB_USER and self.DB_PASS and self.DB_HOST and self.DB_PORT and self.DB_NAME:
            dsn_str = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST.strip()}:{self.DB_PORT}/{self.DB_NAME}"
        if dsn_str:
            try:
                self.SQLALCHEMY_DATABASE_URI = PostgresDsn(dsn_str)
            except Exception as e:
                print(f"Error constructing or validating PostgresDsn for string '{dsn_str}': {e}")
                raise ValueError(f"Invalid DB configuration resulting in DSN error: {e}") from e
        return self

    # --- Google OAuth ---
    GOOGLE_CLIENT_ID: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=effective_env_files,
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )

settings = Settings()

# Debugging output
print(f"--- Config: Loaded settings for effective ENV='{settings.ENV}' ---")
print(f"--- Config: Loaded BACKEND_CORS_ORIGINS='{settings.BACKEND_CORS_ORIGINS}' ---")
print(f"--- Config: Processed BACKEND_CORS_ORIGINS_STR_LIST (List[str]): '{settings.BACKEND_CORS_ORIGINS_STR_LIST}' ---") # New log
print(f"--- Config: Loaded DB_HOST='{settings.DB_HOST}' ---")