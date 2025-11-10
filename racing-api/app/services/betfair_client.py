"""Betfair API client wrapper."""
import betfairlightweight
from betfairlightweight import filters
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class BetfairClient:
    """Wrapper for betfairlightweight API client."""

    def __init__(self):
        """Initialize Betfair client."""
        self.trading = betfairlightweight.APIClient(
            username=settings.BETFAIR_USERNAME,
            password=settings.BETFAIR_PASSWORD,
            app_key=settings.BETFAIR_APP_KEY,
            certs=settings.BETFAIR_CERT_PATH if settings.BETFAIR_CERT_PATH else None,
        )
        self._logged_in = False

    def login(self) -> bool:
        """Login to Betfair API."""
        try:
            if not self._logged_in:
                self.trading.login()
                self._logged_in = True
                logger.info("Successfully logged into Betfair API")
            return True
        except Exception as e:
            logger.error(f"Failed to login to Betfair: {e}")
            raise

    def get_race_meetings(
        self,
        date: Optional[datetime] = None,
        country: str = "AU"
    ) -> List[Dict[str, Any]]:
        """
        Get all race meetings for a specific date.

        Args:
            date: Date to get meetings for (defaults to today)
            country: Country code (defaults to AU)

        Returns:
            List of race events with venue and time information
        """
        self.login()

        if date is None:
            date = datetime.utcnow()

        # Create time range for the day
        start_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(days=1)

        market_filter = filters.market_filter(
            event_type_ids=[settings.EVENT_TYPE_HORSE_RACING],
            market_countries=[country],
            market_start_time={
                'from': start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                'to': end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        )

        events = self.trading.betting.list_events(filter=market_filter)

        return [
            {
                'event_id': event.event.id,
                'event_name': event.event.name,
                'venue': event.event.venue,
                'country': event.event.country_code,
                'timezone': event.event.timezone,
                'open_date': event.event.open_date.isoformat() if event.event.open_date else None,
                'market_count': event.market_count
            }
            for event in events
        ]

    def get_markets_for_event(
        self,
        event_id: str,
        market_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all markets for a specific event (race).

        Args:
            event_id: Betfair event ID
            market_types: List of market types (WIN, PLACE, etc.)

        Returns:
            List of market catalogues with runner information
        """
        self.login()

        if market_types is None:
            market_types = ['WIN', 'PLACE']

        market_filter = filters.market_filter(
            event_ids=[event_id],
            market_type_codes=market_types
        )

        market_catalogues = self.trading.betting.list_market_catalogue(
            filter=market_filter,
            market_projection=[
                'RUNNER_DESCRIPTION',
                'RUNNER_METADATA',
                'EVENT',
                'MARKET_DESCRIPTION',
                'MARKET_START_TIME'
            ],
            max_results=100
        )

        markets = []
        for market in market_catalogues:
            market_data = {
                'market_id': market.market_id,
                'market_name': market.market_name,
                'market_type': market.description.market_type,
                'market_start_time': market.market_start_time.isoformat() if market.market_start_time else None,
                'total_matched': market.total_matched,
                'race_type': market.description.race_type if hasattr(market.description, 'race_type') else None,
                'runners': []
            }

            # Extract runner information
            for runner in market.runners:
                runner_data = {
                    'selection_id': runner.selection_id,
                    'runner_name': runner.runner_name,
                    'handicap': runner.handicap,
                    'sort_priority': runner.sort_priority,
                }

                # Add metadata if available
                if hasattr(runner, 'metadata'):
                    metadata = runner.metadata
                    runner_data.update({
                        'cloth_number': getattr(metadata, 'CLOTH_NUMBER', None),
                        'stall_draw': getattr(metadata, 'STALL_DRAW', None),
                        'jockey_name': getattr(metadata, 'JOCKEY_NAME', None),
                        'trainer_name': getattr(metadata, 'TRAINER_NAME', None),
                        'weight_value': getattr(metadata, 'WEIGHT_VALUE', None),
                        'age': getattr(metadata, 'AGE', None),
                        'sex_type': getattr(metadata, 'SEX_TYPE', None),
                        'form': getattr(metadata, 'FORM', None),
                        'days_since_last_run': getattr(metadata, 'DAYS_SINCE_LAST_RUN', None),
                        'sire_name': getattr(metadata, 'SIRE_NAME', None),
                        'dam_name': getattr(metadata, 'DAM_NAME', None),
                        'colour_type': getattr(metadata, 'COLOUR_TYPE', None),
                        'bred': getattr(metadata, 'BRED', None),
                    })

                market_data['runners'].append(runner_data)

            markets.append(market_data)

        return markets

    def get_market_odds(
        self,
        market_ids: List[str],
        include_volumes: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get current odds for specified markets.

        Args:
            market_ids: List of market IDs to get odds for
            include_volumes: Whether to include volume data

        Returns:
            List of market books with current odds
        """
        self.login()

        price_data = ['EX_BEST_OFFERS']
        if include_volumes:
            price_data.append('EX_TRADED')

        price_filter = filters.price_projection(
            price_data=price_data
        )

        market_books = self.trading.betting.list_market_book(
            market_ids=market_ids,
            price_projection=price_filter
        )

        odds_data = []
        for book in market_books:
            market_odds = {
                'market_id': book.market_id,
                'status': book.status,
                'inplay': book.inplay,
                'total_matched': book.total_matched,
                'total_available': book.total_available,
                'last_match_time': book.last_match_time.isoformat() if book.last_match_time else None,
                'runners': []
            }

            for runner in book.runners:
                runner_odds = {
                    'selection_id': runner.selection_id,
                    'status': runner.status,
                    'last_price_traded': runner.last_price_traded,
                    'total_matched': runner.total_matched,
                }

                # Best available back prices
                if runner.ex and runner.ex.available_to_back:
                    runner_odds['back_prices'] = [
                        {'price': p.price, 'size': p.size}
                        for p in runner.ex.available_to_back[:3]
                    ]

                # Best available lay prices
                if runner.ex and runner.ex.available_to_lay:
                    runner_odds['lay_prices'] = [
                        {'price': p.price, 'size': p.size}
                        for p in runner.ex.available_to_lay[:3]
                    ]

                # Traded volumes
                if include_volumes and runner.ex and runner.ex.traded_volume:
                    runner_odds['traded_volume'] = [
                        {'price': p.price, 'size': p.size}
                        for p in runner.ex.traded_volume
                    ]

                market_odds['runners'].append(runner_odds)

            odds_data.append(market_odds)

        return odds_data

    def get_venues_for_date(
        self,
        date: Optional[datetime] = None,
        country: str = "AU"
    ) -> List[str]:
        """
        Get list of unique venues racing on a specific date.

        Args:
            date: Date to get venues for
            country: Country code

        Returns:
            List of venue names
        """
        meetings = self.get_race_meetings(date=date, country=country)
        venues = sorted(list(set(m['venue'] for m in meetings if m['venue'])))
        return venues

    def search_markets(
        self,
        venue: Optional[str] = None,
        date: Optional[datetime] = None,
        market_types: Optional[List[str]] = None,
        race_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for markets with various filters.

        Args:
            venue: Venue name to filter by
            date: Date to search (defaults to today)
            market_types: Market type codes (WIN, PLACE, etc.)
            race_types: Race types (Flat, Hurdle, Steeple)

        Returns:
            List of matching markets
        """
        self.login()

        if date is None:
            date = datetime.utcnow()

        start_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(days=1)

        filter_params = {
            'event_type_ids': [settings.EVENT_TYPE_HORSE_RACING],
            'market_countries': [settings.DEFAULT_COUNTRY],
            'market_start_time': {
                'from': start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                'to': end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }

        if venue:
            filter_params['venues'] = [venue]

        if market_types:
            filter_params['market_type_codes'] = market_types

        if race_types:
            filter_params['race_types'] = race_types

        market_filter = filters.market_filter(**filter_params)

        market_catalogues = self.trading.betting.list_market_catalogue(
            filter=market_filter,
            market_projection=[
                'RUNNER_DESCRIPTION',
                'EVENT',
                'MARKET_DESCRIPTION',
                'MARKET_START_TIME'
            ],
            max_results=200
        )

        return [
            {
                'market_id': m.market_id,
                'market_name': m.market_name,
                'market_type': m.description.market_type,
                'venue': m.event.venue if m.event else None,
                'event_name': m.event.name if m.event else None,
                'market_start_time': m.market_start_time.isoformat() if m.market_start_time else None,
                'runner_count': len(m.runners) if m.runners else 0
            }
            for m in market_catalogues
        ]


# Singleton instance
betfair_client = BetfairClient()
