# Betfair Racing API

A personal FastAPI-based REST API for accessing Betfair horse racing data. This API provides clean, structured endpoints for retrieving race meetings, markets, odds, and runner information.

## Features

- 🏇 **Race Discovery** - Find meetings, venues, and races by date
- 📊 **Market Data** - Access WIN and PLACE markets with full runner details
- 💰 **Live Odds** - Get real-time back/lay prices and volumes
- 🔍 **Flexible Filtering** - Search by venue, date, market type, and race type
- 📦 **Batch Operations** - Retrieve odds for multiple markets simultaneously
- 🗄️ **Caching** - SQLite-based caching for improved performance
- 📚 **Auto Documentation** - Interactive API docs with Swagger UI
- 🚀 **Fast & Async** - Built with FastAPI for high performance

## What Data is Available?

### Race Information
- Meeting dates and venues
- Event IDs and names
- Market start times
- Race types (Flat, Hurdle, Steeple)

### Runner/Horse Details
- Horse name and cloth number
- Jockey and trainer names
- Weight, age, sex, and form
- Stall draw position
- Pedigree (sire, dam, damsire)
- Days since last run
- Horse characteristics (bred, colour)

### Market Data
- WIN markets (winner prediction)
- PLACE markets (top 2-3 finishers)
- Market status (open, closed, suspended)
- Total matched volume
- Market start times

### Odds and Pricing
- Best available back prices (top 3)
- Best available lay prices (top 3)
- Price sizes (available liquidity)
- Last traded price
- Traded volumes by price
- In-play status

## Prerequisites

1. **Betfair Account** with API access
2. **App Key** from [Betfair Developer Portal](https://developer.betfair.com/)
3. **Python 3.8+**

## Installation

### 1. Clone or Download

```bash
cd racing-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Credentials

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your Betfair credentials:

```env
BETFAIR_USERNAME=your_username
BETFAIR_PASSWORD=your_password
BETFAIR_APP_KEY=your_app_key
```

**Getting API Credentials:**
- Follow the guide at: `../src/api/apiappkey.md`
- Or visit: https://developer.betfair.com/

### 5. Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Quick Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/api/meetings` | GET | Get race meetings for a date |
| `/api/venues` | GET | Get venues racing on a date |
| `/api/markets` | GET | Search markets with filters |
| `/api/event/{event_id}` | GET | Get markets for specific event |
| `/api/market/{market_id}` | GET | Get market details |
| `/api/odds/{market_id}` | GET | Get live odds for market |
| `/api/odds/batch` | GET | Get odds for multiple markets |
| `/api/race/{venue}` | GET | Get races at specific venue |

## Usage Examples

### 1. Get Today's Meetings

```bash
curl "http://localhost:8000/api/meetings"
```

Response:
```json
{
  "date": "2025-11-10",
  "country": "AU",
  "meeting_count": 8,
  "meetings": [
    {
      "event_id": "32614443",
      "event_name": "Flemington 10th Nov",
      "venue": "Flemington",
      "country": "AU",
      "timezone": "Australia/Melbourne",
      "open_date": "2025-11-10T00:00:00",
      "market_count": 20
    }
  ]
}
```

### 2. Get Venues for Specific Date

```bash
curl "http://localhost:8000/api/venues?date=2025-11-10&country=AU"
```

### 3. Search Markets at Venue

```bash
curl "http://localhost:8000/api/markets?venue=Flemington&market_type=WIN"
```

Response:
```json
{
  "filters": {
    "venue": "Flemington",
    "date": "2025-11-10",
    "market_type": "WIN",
    "race_type": null
  },
  "market_count": 10,
  "markets": [
    {
      "market_id": "1.234567890",
      "market_name": "R1 1200m Mdn",
      "market_type": "WIN",
      "venue": "Flemington",
      "event_name": "Flemington 10th Nov",
      "market_start_time": "2025-11-10T01:00:00",
      "runner_count": 12
    }
  ]
}
```

### 4. Get Event Markets with Runners

```bash
curl "http://localhost:8000/api/event/32614443?market_types=WIN,PLACE"
```

Response includes full runner details:
```json
{
  "event_id": "32614443",
  "market_count": 2,
  "markets": [
    {
      "market_id": "1.234567890",
      "market_name": "R1 1200m Mdn",
      "market_type": "WIN",
      "market_start_time": "2025-11-10T01:00:00",
      "total_matched": 125000.50,
      "race_type": "Flat",
      "runners": [
        {
          "selection_id": 12345678,
          "runner_name": "Thunder Bolt",
          "cloth_number": 1,
          "stall_draw": 5,
          "jockey_name": "J Smith",
          "trainer_name": "P Jones",
          "weight_value": 58.0,
          "age": 3,
          "sex_type": "g",
          "form": "4-2-1",
          "days_since_last_run": 14,
          "sire_name": "Lightning Strike",
          "dam_name": "Storm Queen",
          "colour_type": "Bay",
          "bred": "AUS"
        }
      ]
    }
  ]
}
```

### 5. Get Live Odds

```bash
curl "http://localhost:8000/api/odds/1.234567890?include_volumes=true"
```

Response:
```json
{
  "market_id": "1.234567890",
  "status": "OPEN",
  "inplay": false,
  "total_matched": 125000.50,
  "total_available": 450000.00,
  "last_match_time": "2025-11-10T00:45:00",
  "runners": [
    {
      "selection_id": 12345678,
      "status": "ACTIVE",
      "last_price_traded": 5.5,
      "total_matched": 15000.00,
      "back_prices": [
        {"price": 5.5, "size": 250.00},
        {"price": 5.4, "size": 150.00},
        {"price": 5.3, "size": 100.00}
      ],
      "lay_prices": [
        {"price": 5.6, "size": 300.00},
        {"price": 5.7, "size": 200.00},
        {"price": 5.8, "size": 150.00}
      ]
    }
  ]
}
```

### 6. Batch Odds Retrieval

Monitor multiple races simultaneously:

```bash
curl "http://localhost:8000/api/odds/batch?market_ids=1.234567890,1.234567891,1.234567892"
```

### 7. Get All Races at Venue

```bash
curl "http://localhost:8000/api/race/Flemington?date=2025-11-10"
```

## Python Client Examples

### Basic Usage

```python
import requests
from datetime import datetime

API_BASE = "http://localhost:8000"

# Get today's meetings
response = requests.get(f"{API_BASE}/api/meetings")
meetings = response.json()

print(f"Found {meetings['meeting_count']} meetings today")
for meeting in meetings['meetings']:
    print(f"- {meeting['venue']}: {meeting['market_count']} markets")
```

### Get Odds for All Races at a Venue

```python
import requests

def get_venue_odds(venue: str):
    """Get odds for all races at a venue."""

    # Get markets at venue
    markets_response = requests.get(
        f"http://localhost:8000/api/markets",
        params={"venue": venue, "market_type": "WIN"}
    )
    markets = markets_response.json()['markets']

    # Get odds for each market
    for market in markets:
        market_id = market['market_id']
        odds_response = requests.get(
            f"http://localhost:8000/api/odds/{market_id}"
        )
        odds = odds_response.json()

        print(f"\n{market['market_name']}")
        for runner in odds['runners']:
            if runner.get('back_prices'):
                best_back = runner['back_prices'][0]['price']
                print(f"  Selection {runner['selection_id']}: ${best_back}")

# Example usage
get_venue_odds("Flemington")
```

### Monitor Live Odds

```python
import requests
import time

def monitor_market(market_id: str, interval: int = 5):
    """Monitor odds for a market at regular intervals."""

    while True:
        response = requests.get(f"http://localhost:8000/api/odds/{market_id}")
        odds = response.json()

        print(f"\n{odds['market_id']} - Status: {odds['status']}")
        print(f"Total Matched: ${odds['total_matched']:,.2f}")

        for runner in odds['runners']:
            if runner.get('back_prices'):
                best_back = runner['back_prices'][0]['price']
                best_lay = runner['lay_prices'][0]['price'] if runner.get('lay_prices') else None
                print(f"  {runner['selection_id']}: Back ${best_back} | Lay ${best_lay}")

        time.sleep(interval)

# Monitor a market every 5 seconds
monitor_market("1.234567890", interval=5)
```

### Build a Data Collection Pipeline

```python
import requests
import pandas as pd
from datetime import datetime

def collect_race_data(date: str = None):
    """Collect all race and odds data for analysis."""

    # Get meetings
    params = {"date": date} if date else {}
    meetings = requests.get(
        "http://localhost:8000/api/meetings",
        params=params
    ).json()

    all_data = []

    for meeting in meetings['meetings']:
        event_id = meeting['event_id']

        # Get markets for event
        markets = requests.get(
            f"http://localhost:8000/api/event/{event_id}",
            params={"market_types": "WIN"}
        ).json()

        for market in markets['markets']:
            market_id = market['market_id']

            # Get odds
            odds = requests.get(
                f"http://localhost:8000/api/odds/{market_id}"
            ).json()

            # Combine data
            for runner_market, runner_odds in zip(
                market['runners'], odds['runners']
            ):
                record = {
                    'timestamp': datetime.now(),
                    'venue': meeting['venue'],
                    'market_id': market_id,
                    'market_name': market['market_name'],
                    'runner_name': runner_market['runner_name'],
                    'cloth_number': runner_market.get('cloth_number'),
                    'jockey': runner_market.get('jockey_name'),
                    'trainer': runner_market.get('trainer_name'),
                    'back_price': runner_odds.get('back_prices', [{}])[0].get('price'),
                    'lay_price': runner_odds.get('lay_prices', [{}])[0].get('price'),
                    'total_matched': runner_odds.get('total_matched')
                }
                all_data.append(record)

    return pd.DataFrame(all_data)

# Collect data
df = collect_race_data()
print(df.head())

# Save to CSV
df.to_csv('racing_data.csv', index=False)
```

## Interactive API Documentation

Visit http://localhost:8000/docs for full interactive documentation where you can:

- Browse all endpoints
- See request/response schemas
- Test API calls directly in the browser
- View parameter descriptions
- Download OpenAPI specification

## Configuration

Edit `.env` to customize settings:

```env
# Cache duration (seconds)
CACHE_ODDS_SECONDS=5          # Live odds cache
CACHE_MARKETS_SECONDS=60      # Market data cache
CACHE_MEETINGS_SECONDS=300    # Meetings cache

# Default settings
DEFAULT_COUNTRY=AU            # Default country code
```

## Database

The API uses SQLite for caching to reduce Betfair API calls:

- **Location**: `racing_data.db`
- **Tables**:
  - `race_meetings` - Cached meeting data
  - `markets` - Cached market information
  - `market_odds` - Short-lived odds cache
  - `runners` - Runner details cache

To reset the database:

```bash
rm racing_data.db
# Database will be recreated on next API start
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Structure

```
racing-api/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py            # SQLAlchemy models
│   └── services/
│       ├── __init__.py
│       └── betfair_client.py      # Betfair API wrapper
├── tests/                         # Test files
├── .env                           # Configuration (not in git)
├── .env.example                   # Template
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

## Troubleshooting

### Authentication Issues

If you get login errors:

1. Verify credentials in `.env`
2. Check your Betfair account is active
3. Ensure your App Key is for the correct environment (Production vs. Delayed)
4. For Australia/NZ, you may need certificate-based authentication

### No Data Returned

- Check the date format (YYYY-MM-DD)
- Verify venues are spelled correctly (case-sensitive)
- Ensure markets exist for the specified date/venue
- Some venues may have limited markets on certain days

### Rate Limiting

Betfair has API rate limits. If you hit limits:

- Increase cache durations in `.env`
- Reduce polling frequency
- Use batch endpoints instead of individual calls

## Betfair API Resources

- [Developer Documentation](https://docs.developer.betfair.com/)
- [API Visualiser](https://docs.developer.betfair.com/visualisers/api-ng-sports-operations/)
- [Getting Started Guide](../src/api/apiappkey.md)
- [Python Tutorial](../src/api/apiPythontutorial.md)

## Betfair Data Fields

For detailed information about all available data fields, see:
- Historical data structure: `../src/data/assets/ANZ_Thoroughbreds_2025_10.csv`
- Competition format: `../src/modelling/springRacingDatathon.md`

## License

Personal use only. Comply with Betfair's [Terms and Conditions](https://www.betfair.com.au/aboutUs/Terms.and.Conditions/).

## Next Steps

1. **Add WebSocket Support** for real-time streaming
2. **Historical Data Storage** - Store results for analysis
3. **Enhanced Caching** - Redis for distributed caching
4. **Authentication** - Add API key protection
5. **Rate Limiting** - Implement request throttling
6. **Data Enrichment** - Add form analysis and statistics
7. **Alerting** - Price movement notifications

## Support

For issues with:
- **This API**: Check logs and review configuration
- **Betfair API**: Visit [Betfair Developer Forum](https://forum.developer.betfair.com/)
- **Credentials**: See [API Application Keys Guide](../src/api/apiappkey.md)
