from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    ENCRYPTION_KEY: str
    JWT_SECRET_KEY: str = "mkpro-neon-2025-super-secret-key-change-in-production"
    REDIS_URL: str = "redis://default:your-redis-password@your-redis-host:6379"
    POSTGRES_URL: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
