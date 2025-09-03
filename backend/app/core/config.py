from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    SECRET_KEY: str = "change_me_now"
    ACCESS_TOKEN_EXPIRES_MIN: int = 15
    REFRESH_TOKEN_EXPIRES_DAYS: int = 7
    AUTH_COOKIES: bool = True
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173"
    DB_URL: str = "sqlite+aiosqlite:///./app.db"
    DEMO_SEED: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
ALLOWED_ORIGINS: List[str] = [o.strip() for o in settings.BACKEND_CORS_ORIGINS.split(",") if o.strip()]
