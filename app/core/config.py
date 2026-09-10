import os
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "English for Kids API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # Database Configuration
    DATABASE_URL: str = "postgresql://kids_user:kids_password_123@localhost:5432/english_kids_db"

    # Security & JWT
    SECRET_KEY: str = "super_secret_jwt_key_english_for_kids_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days (10080 minutes)

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    # TTS / Audio Configuration
    AUDIO_CACHE_DIR: str = "static/audio"
    DEFAULT_TTS_VOICE: str = "en-US-AnaNeural"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
