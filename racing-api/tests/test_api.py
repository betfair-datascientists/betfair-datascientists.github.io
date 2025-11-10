"""
Basic tests for the Racing API.

Run with: pytest tests/
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "endpoints" in data


def test_health_check_no_credentials():
    """Test health check endpoint (may fail without credentials)."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


@patch('app.services.betfair_client.betfair_client.get_race_meetings')
def test_get_meetings(mock_get_meetings):
    """Test get meetings endpoint."""
    # Mock the Betfair API response
    mock_get_meetings.return_value = [
        {
            'event_id': '12345',
            'event_name': 'Test Meeting',
            'venue': 'Test Venue',
            'country': 'AU',
            'timezone': 'Australia/Melbourne',
            'open_date': '2025-11-10T00:00:00',
            'market_count': 10
        }
    ]

    response = client.get("/api/meetings")
    assert response.status_code == 200
    data = response.json()
    assert "meeting_count" in data
    assert "meetings" in data
    assert data["meeting_count"] == 1


@patch('app.services.betfair_client.betfair_client.get_venues_for_date')
def test_get_venues(mock_get_venues):
    """Test get venues endpoint."""
    mock_get_venues.return_value = ['Flemington', 'Caulfield', 'Moonee Valley']

    response = client.get("/api/venues")
    assert response.status_code == 200
    data = response.json()
    assert "venue_count" in data
    assert "venues" in data
    assert data["venue_count"] == 3
    assert 'Flemington' in data["venues"]


def test_invalid_date_format():
    """Test that invalid date format returns 400."""
    response = client.get("/api/meetings?date=invalid-date")
    assert response.status_code == 400
    assert "Invalid date format" in response.json()["detail"]


@patch('app.services.betfair_client.betfair_client.search_markets')
def test_search_markets(mock_search):
    """Test market search endpoint."""
    mock_search.return_value = [
        {
            'market_id': '1.234567',
            'market_name': 'R1 1200m',
            'market_type': 'WIN',
            'venue': 'Flemington',
            'event_name': 'Flemington 10th Nov',
            'market_start_time': '2025-11-10T01:00:00',
            'runner_count': 12
        }
    ]

    response = client.get("/api/markets?venue=Flemington&market_type=WIN")
    assert response.status_code == 200
    data = response.json()
    assert "market_count" in data
    assert "markets" in data
    assert data["market_count"] == 1


@patch('app.services.betfair_client.betfair_client.get_market_odds')
def test_get_odds(mock_get_odds):
    """Test get odds endpoint."""
    mock_get_odds.return_value = [
        {
            'market_id': '1.234567',
            'status': 'OPEN',
            'inplay': False,
            'total_matched': 10000.0,
            'total_available': 50000.0,
            'last_match_time': None,
            'runners': [
                {
                    'selection_id': 12345,
                    'status': 'ACTIVE',
                    'last_price_traded': 5.5,
                    'total_matched': 1000.0,
                    'back_prices': [{'price': 5.5, 'size': 100.0}],
                    'lay_prices': [{'price': 5.6, 'size': 150.0}]
                }
            ]
        }
    ]

    response = client.get("/api/odds/1.234567")
    assert response.status_code == 200
    data = response.json()
    assert data['market_id'] == '1.234567'
    assert data['status'] == 'OPEN'
    assert len(data['runners']) == 1


def test_batch_odds_limit():
    """Test batch odds endpoint enforces limit."""
    # Create 51 market IDs (over the limit of 50)
    market_ids = ','.join([f"1.{i}" for i in range(51)])
    response = client.get(f"/api/odds/batch?market_ids={market_ids}")
    assert response.status_code == 400
    assert "Maximum 50 markets" in response.json()["detail"]
