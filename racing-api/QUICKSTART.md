# Quick Start Guide

Get your Racing API up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- Betfair account with API access
- App Key from [developer.betfair.com](https://developer.betfair.com/)

## Setup Steps

### 1. Install Dependencies

```bash
cd racing-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Credentials

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
BETFAIR_USERNAME=your_username
BETFAIR_PASSWORD=your_password
BETFAIR_APP_KEY=your_app_key
```

### 3. Start the API

```bash
uvicorn app.main:app --reload
```

The API is now running at http://localhost:8000

### 4. Test It

Open another terminal and run:

```bash
python example_usage.py
```

Or visit the interactive docs: http://localhost:8000/docs

## Quick Examples

### Get Today's Meetings

```bash
curl http://localhost:8000/api/meetings
```

### Search Markets

```bash
curl "http://localhost:8000/api/markets?venue=Flemington&market_type=WIN"
```

### Get Live Odds

```bash
curl "http://localhost:8000/api/odds/1.234567890"
```

Replace `1.234567890` with a real market ID from the meetings response.

## Using Docker

Alternatively, run with Docker:

```bash
docker-compose up
```

## What's Available?

The API provides access to:

- 🏁 **Race meetings** by date and venue
- 🎯 **Market data** (WIN, PLACE) with runner details
- 💰 **Live odds** (back/lay prices, volumes)
- 🐎 **Horse details** (jockey, trainer, form, weight)
- 📊 **Batch operations** for multiple markets

## Common Use Cases

### 1. Monitor a Specific Venue

```python
import requests

venue = "Flemington"
markets = requests.get(
    "http://localhost:8000/api/markets",
    params={"venue": venue, "market_type": "WIN"}
).json()

for market in markets['markets']:
    print(f"{market['market_name']}: {market['runner_count']} runners")
```

### 2. Get Current Odds

```python
import requests

market_id = "1.234567890"
odds = requests.get(f"http://localhost:8000/api/odds/{market_id}").json()

for runner in odds['runners']:
    if runner.get('back_prices'):
        price = runner['back_prices'][0]['price']
        print(f"Selection {runner['selection_id']}: ${price}")
```

### 3. Build Race Card

```python
import requests

event_id = "32614443"
markets = requests.get(
    f"http://localhost:8000/api/event/{event_id}",
    params={"market_types": "WIN"}
).json()

for market in markets['markets']:
    print(f"\n{market['market_name']}")
    for runner in market['runners']:
        print(f"  #{runner['cloth_number']} {runner['runner_name']}")
        print(f"     J: {runner['jockey_name']}, T: {runner['trainer_name']}")
```

## Troubleshooting

**Connection refused?**
- Make sure the API is running: `uvicorn app.main:app --reload`

**Login failed?**
- Check credentials in `.env`
- Verify your Betfair account is active
- Ensure App Key is correct

**No data returned?**
- Check if there are races scheduled today
- Verify venue names (case-sensitive)
- Try a different date: `?date=2025-11-15`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the interactive docs at http://localhost:8000/docs
- Check out [example_usage.py](example_usage.py) for more examples
- Review Betfair's API documentation at [docs.developer.betfair.com](https://docs.developer.betfair.com/)

## Need Help?

- **Betfair API**: See `../src/api/apiPythontutorial.md`
- **Getting App Key**: See `../src/api/apiappkey.md`
- **Data Structure**: See `../src/modelling/springRacingDatathon.md`

Happy racing! 🏇
