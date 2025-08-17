import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    ENVIRONMENT: str
    SECRET_KEY: str
    API_VERSION: str = "/api/v1"

    # Cors
    FRONTEND_URL: str = "http://localhost:4000"
    BACKEND_URL: str = "http://localhost:8000"

    # DB
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = ""

    # Cookie authentication
    ACCESS_EXPIRE_MINUTES: int = 120
    COOKIE_DOMAIN: str
    COOKIE_SAMESITE: str = "strict"
    COOKIE_HTTPONLY: bool = True
    COOKIE_SECURE: bool = True


class DevelopmentSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.development")
    ENVIRONMENT: str = "development"

    # Cookies
    COOKIE_DOMAIN: str | None = None
    COOKIE_SECURE: bool = False


class TestingSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.testing")
    ENVIRONMENT: str = "testing"

    # Cookies
    COOKIE_DOMAIN: str | None = None
    COOKIE_SECURE: bool = False


class ProductionSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.production")
    ENVIRONMENT: str = "production"


@lru_cache()
def get_settings():
    env = os.getenv("ENVIRONMENT", "development")
    if env == "development":
        return DevelopmentSettings()
    if env == "testing":
        return TestingSettings()
    if env == "production":
        return ProductionSettings()
    return Settings()


settings = get_settings()
