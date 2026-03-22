"""
Application Configuration
Centralized configuration management using Pydantic Settings
"""
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # App Info
    APP_NAME: str = "Pregnancy Safety Radar API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./pregnancy_safety.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # AI APIs
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # Security — MUST override via SECRET_KEY env var in production
    SECRET_KEY: str = "dev-secret-key-change-in-production"

    # CORS — additional allowed origins (comma-separated)
    CORS_ORIGINS: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # Stripe Payments
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_PRICE_ID: Optional[str] = None  # Pro tier ($9.99/mo)
    STRIPE_PRICE_ID_PRO_PLUS: Optional[str] = None  # Pro+ tier ($29.99/mo)
    FRONTEND_URL: str = "http://localhost:8000"

    # Monitoring
    SENTRY_DSN: Optional[str] = None

    # Google Cloud (OCR)
    GOOGLE_CLOUD_PROJECT_ID: Optional[str] = None
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance
    Returns the same Settings object on subsequent calls
    """
    return Settings()


# Global settings instance
settings = get_settings()
