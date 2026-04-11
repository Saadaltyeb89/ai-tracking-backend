from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Tracking API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/aitracking"
    
    # Security
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_HERE"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str = "" # Web Client ID
    GOOGLE_CLIENT_SECRET: str = ""
    
    # OpenAI / Gemini
    AI_MODEL_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
