"""Core configuration for the application."""
from typing import Any, Dict, List, Optional
from pydantic import PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = "Mój Portfel 2026"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_HASH_ALGORITHM: str = "bcrypt"
    BCRYPT_ROUNDS: int = 12
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:8000", "http://localhost:80"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database
    POSTGRES_SERVER: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "portfel"
    POSTGRES_PASSWORD: str = "portfel_password"
    POSTGRES_DB: str = "portfel_db"
    DATABASE_URL: Optional[PostgresDsn] = None
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> Any:
        if isinstance(v, str):
            return v
        values = info.data
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )
    
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    REDIS_URL: Optional[RedisDsn] = None
    
    @field_validator("REDIS_URL", mode="before")
    @classmethod
    def assemble_redis_connection(cls, v: Optional[str], info: Any) -> Any:
        if isinstance(v, str):
            return v
        values = info.data
        password = values.get("REDIS_PASSWORD")
        auth = f":{password}@" if password else ""
        return f"redis://{auth}{values.get('REDIS_HOST')}:{values.get('REDIS_PORT')}/{values.get('REDIS_DB')}"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    AUTH_RATE_LIMIT_PER_MINUTE: int = 5
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@mojportfel.pl"
    SMTP_FROM_NAME: str = "Mój Portfel 2026"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Frontend
    FRONTEND_URL: str = "http://localhost"
    
    # Default monthly goals
    DEFAULT_MONTHLY_INCOME_GOAL: int = 20000  # PLN
    DEFAULT_MONTHLY_GOLD_GOAL: int = 10  # grams
    DEFAULT_MONTHLY_SILVER_GOAL: int = 500  # grams
    DEFAULT_MONTHLY_INVESTMENT_GOAL: int = 5100  # PLN


settings = Settings()
