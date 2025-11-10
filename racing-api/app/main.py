"""FastAPI application for Betfair Racing API."""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import List, Optional
import logging

from app.config import settings
from app.services.betfair_client import betfair_client
from app.models.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info("Starting Racing API...")
    await init_db()
    logger.info("Database initialized")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "description": settings.API_DESCRIPTION,
        "docs": "/docs",
        "endpoints": {
            "meetings": "/api/meetings",
            "venues": "/api/venues",
            "markets": "/api/markets",
            "odds": "/api/odds/{market_id}"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        betfair_client.login()
        return {"status": "healthy", "betfair_connected": True}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}


@app.get("/api/meetings")
async def get_meetings(
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format (defaults to today)"),
    country: str = Query("AU", description="Country code (AU, NZ, GB, etc.)")
):
    """
    Get all race meetings for a specific date.

    Returns list of meetings with venue, time, and event information.
    """
    try:
        # Parse date if provided
        meeting_date = None
        if date:
            try:
                meeting_date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

        meetings = betfair_client.get_race_meetings(date=meeting_date, country=country)

        return {
            "date": (meeting_date or datetime.utcnow()).strftime("%Y-%m-%d"),
            "country": country,
            "meeting_count": len(meetings),
            "meetings": meetings
        }

    except Exception as e:
        logger.error(f"Error getting meetings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/venues")
async def get_venues(
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    country: str = Query("AU", description="Country code")
):
    """
    Get list of venues racing on a specific date.

    Returns sorted list of venue names.
    """
    try:
        meeting_date = None
        if date:
            try:
                meeting_date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

        venues = betfair_client.get_venues_for_date(date=meeting_date, country=country)

        return {
            "date": (meeting_date or datetime.utcnow()).strftime("%Y-%m-%d"),
            "country": country,
            "venue_count": len(venues),
            "venues": venues
        }

    except Exception as e:
        logger.error(f"Error getting venues: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/markets")
async def search_markets(
    venue: Optional[str] = Query(None, description="Venue name to filter by"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    market_type: Optional[str] = Query(None, description="Market type (WIN, PLACE, etc.)"),
    race_type: Optional[str] = Query(None, description="Race type (Flat, Hurdle, Steeple)")
):
    """
    Search for markets with various filters.

    Returns list of markets matching the criteria.
    """
    try:
        search_date = None
        if date:
            try:
                search_date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

        market_types = [market_type] if market_type else None
        race_types = [race_type] if race_type else None

        markets = betfair_client.search_markets(
            venue=venue,
            date=search_date,
            market_types=market_types,
            race_types=race_types
        )

        return {
            "filters": {
                "venue": venue,
                "date": (search_date or datetime.utcnow()).strftime("%Y-%m-%d"),
                "market_type": market_type,
                "race_type": race_type
            },
            "market_count": len(markets),
            "markets": markets
        }

    except Exception as e:
        logger.error(f"Error searching markets: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/event/{event_id}")
async def get_event_markets(
    event_id: str,
    market_types: Optional[str] = Query(None, description="Comma-separated market types (WIN,PLACE)")
):
    """
    Get all markets for a specific event (race).

    Returns detailed market information including runners with metadata.
    """
    try:
        market_type_list = None
        if market_types:
            market_type_list = [mt.strip() for mt in market_types.split(',')]

        markets = betfair_client.get_markets_for_event(
            event_id=event_id,
            market_types=market_type_list
        )

        if not markets:
            raise HTTPException(status_code=404, detail="No markets found for this event")

        return {
            "event_id": event_id,
            "market_count": len(markets),
            "markets": markets
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting event markets: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market/{market_id}")
async def get_market_details(market_id: str):
    """
    Get detailed information for a specific market.

    Returns market catalogue with full runner details and metadata.
    """
    try:
        # We need to get market via event lookup
        # This is a simplified version - in production you might cache market->event mapping
        markets = betfair_client.get_market_odds(market_ids=[market_id])

        if not markets:
            raise HTTPException(status_code=404, detail="Market not found")

        return markets[0]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting market details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/odds/{market_id}")
async def get_market_odds(
    market_id: str,
    include_volumes: bool = Query(True, description="Include traded volume data")
):
    """
    Get current odds for a specific market.

    Returns live back/lay prices and optional volume data.
    """
    try:
        odds = betfair_client.get_market_odds(
            market_ids=[market_id],
            include_volumes=include_volumes
        )

        if not odds:
            raise HTTPException(status_code=404, detail="Market not found or no odds available")

        return odds[0]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting market odds: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/odds/batch")
async def get_batch_odds(
    market_ids: str = Query(..., description="Comma-separated market IDs"),
    include_volumes: bool = Query(False, description="Include traded volume data")
):
    """
    Get odds for multiple markets in a single request.

    Useful for monitoring multiple races simultaneously.
    """
    try:
        market_id_list = [mid.strip() for mid in market_ids.split(',')]

        if len(market_id_list) > 50:
            raise HTTPException(
                status_code=400,
                detail="Maximum 50 markets per request"
            )

        odds = betfair_client.get_market_odds(
            market_ids=market_id_list,
            include_volumes=include_volumes
        )

        return {
            "market_count": len(odds),
            "markets": odds
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting batch odds: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/race/{venue}")
async def get_races_at_venue(
    venue: str,
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format")
):
    """
    Get all races at a specific venue for a date.

    Returns markets and detailed runner information.
    """
    try:
        search_date = None
        if date:
            try:
                search_date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

        markets = betfair_client.search_markets(
            venue=venue,
            date=search_date,
            market_types=['WIN']  # Get WIN markets for each race
        )

        # Group by event
        events = {}
        for market in markets:
            event_name = market.get('event_name')
            if event_name not in events:
                events[event_name] = []
            events[event_name].append(market)

        return {
            "venue": venue,
            "date": (search_date or datetime.utcnow()).strftime("%Y-%m-%d"),
            "race_count": len(events),
            "races": events
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting races at venue: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
