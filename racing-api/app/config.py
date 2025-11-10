"""Configuration management for Racing API."""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings."""

    # API Configuration
    API_TITLE: str = "Betfair Racing API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Personal API for accessing Betfair horse racing data"

    # Betfair Credentials
    BETFAIR_USERNAME: str
    BETFAIR_PASSWORD: str
    BETFAIR_APP_KEY: str
    BETFAIR_CERT_PATH: Optional[str] = None
    BETFAIR_CERT_KEY_PATH: Optional[str] = None

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./racing_data.db"

    # Cache Settings
    CACHE_ODDS_SECONDS: int = 5  # How long to cache live odds
    CACHE_MARKETS_SECONDS: int = 60  # How long to cache market data
    CACHE_MEETINGS_SECONDS: int = 300  # How long to cache meetings

    # Racing Configuration
    DEFAULT_COUNTRY: str = "AU"
    EVENT_TYPE_HORSE_RACING: int = 7

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
