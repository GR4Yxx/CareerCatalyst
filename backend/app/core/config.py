import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # MongoDB settings
    MONGO_URI: str = Field(
        default="mongodb://localhost:27017/",
        env="MONGO_URI"
    )
    DATABASE_NAME: str = Field(
        default="career_catalyst",
        env="DATABASE_NAME"
    )
    
    # JWT settings
    SECRET_KEY: str = Field(
        default="your-secret-key-for-jwt-please-change-in-production",
        env="SECRET_KEY"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # App settings
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="production", env="ENVIRONMENT")
    
    # Upload settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_UPLOAD_TYPES: list = ["application/pdf", "application/msword", 
                                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    
    # Gemini API settings
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    
    # CORS settings
    FRONTEND_URL: str = Field(default="http://localhost:3000", env="FRONTEND_URL")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

settings = Settings() 