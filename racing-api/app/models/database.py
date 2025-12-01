"""Database models for caching racing data."""
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.config import settings

Base = declarative_base()


class RaceMeeting(Base):
    """Race meeting/event cache."""

    __tablename__ = "race_meetings"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True)
    event_name = Column(String)
    venue = Column(String, index=True)
    country = Column(String, index=True)
    timezone = Column(String)
    open_date = Column(DateTime)
    market_count = Column(Integer)
    cached_at = Column(DateTime, default=datetime.utcnow)


class Market(Base):
    """Market cache."""

    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(String, unique=True, index=True)
    event_id = Column(String, index=True)
    market_name = Column(String)
    market_type = Column(String, index=True)
    venue = Column(String, index=True)
    market_start_time = Column(DateTime, index=True)
    total_matched = Column(Float)
    race_type = Column(String)
    runner_count = Column(Integer)
    runners_data = Column(JSON)  # Store full runner details as JSON
    cached_at = Column(DateTime, default=datetime.utcnow)


class MarketOdds(Base):
    """Market odds cache (short-lived)."""

    __tablename__ = "market_odds"

    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(String, index=True)
    status = Column(String)
    inplay = Column(Boolean)
    total_matched = Column(Float)
    total_available = Column(Float)
    last_match_time = Column(DateTime)
    odds_data = Column(JSON)  # Store all odds as JSON
    cached_at = Column(DateTime, default=datetime.utcnow, index=True)


class Runner(Base):
    """Runner/horse details cache."""

    __tablename__ = "runners"

    id = Column(Integer, primary_key=True, index=True)
    selection_id = Column(Integer, unique=True, index=True)
    runner_name = Column(String, index=True)
    cloth_number = Column(Integer)
    stall_draw = Column(Integer)
    jockey_name = Column(String, index=True)
    trainer_name = Column(String, index=True)
    weight_value = Column(Float)
    age = Column(Integer)
    sex_type = Column(String)
    form = Column(String)
    days_since_last_run = Column(Integer)
    sire_name = Column(String)
    dam_name = Column(String)
    colour_type = Column(String)
    bred = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)


# Database engine and session
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Get database session."""
    async with async_session() as session:
        yield session
