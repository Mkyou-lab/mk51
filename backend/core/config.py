from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "MK PRO"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    ENCRYPTION_KEY: str  # For MT5 credentials
    
    # Push Notifications
    ONESIGNAL_APP_ID: str = ""
    ONESIGNAL_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()