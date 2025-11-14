"""
Example usage of the Racing API.

Start the API server first:
    uvicorn app.main:app --reload

Then run this script:
    python example_usage.py
"""
import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000"


def print_json(data, title=""):
    """Pretty print JSON data."""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print('='*60)
    print(json.dumps(data, indent=2))


def main():
    """Demonstrate API usage."""

    print("🏇 Betfair Racing API - Example Usage\n")

    # 1. Health check
    print("1️⃣  Checking API health...")
    response = requests.get(f"{API_BASE}/health")
    health = response.json()
    print(f"   Status: {health['status']}")
    print(f"   Betfair Connected: {health.get('betfair_connected', False)}")

    # 2. Get today's meetings
    print("\n2️⃣  Getting today's race meetings...")
    response = requests.get(f"{API_BASE}/api/meetings")
    meetings = response.json()
    print(f"   Found {meetings['meeting_count']} meetings on {meetings['date']}")

    if meetings['meetings']:
        for meeting in meetings['meetings'][:3]:  # Show first 3
            print(f"   - {meeting['venue']}: {meeting['market_count']} markets")

        # Store first meeting for later use
        first_meeting = meetings['meetings'][0]
        print_json(first_meeting, "First Meeting Details")

        # 3. Get venues
        print("\n3️⃣  Getting all venues racing today...")
        response = requests.get(f"{API_BASE}/api/venues")
        venues = response.json()
        print(f"   Found {venues['venue_count']} venues:")
        print(f"   {', '.join(venues['venues'][:5])}{'...' if len(venues['venues']) > 5 else ''}")

        # 4. Search markets at first venue
        venue = first_meeting['venue']
        print(f"\n4️⃣  Searching for WIN markets at {venue}...")
        response = requests.get(
            f"{API_BASE}/api/markets",
            params={"venue": venue, "market_type": "WIN"}
        )
        markets = response.json()
        print(f"   Found {markets['market_count']} WIN markets")

        if markets['markets']:
            first_market = markets['markets'][0]
            print(f"   First race: {first_market['market_name']}")
            print(f"   Market ID: {first_market['market_id']}")
            print(f"   Runners: {first_market['runner_count']}")

            # 5. Get detailed market information
            event_id = first_meeting['event_id']
            print(f"\n5️⃣  Getting detailed markets for event {event_id}...")
            response = requests.get(
                f"{API_BASE}/api/event/{event_id}",
                params={"market_types": "WIN"}
            )
            event_markets = response.json()

            if event_markets['markets']:
                market = event_markets['markets'][0]
                print(f"   Market: {market['market_name']}")
                print(f"   Runners: {len(market['runners'])}")

                # Show first 3 runners
                print("\n   First 3 runners:")
                for runner in market['runners'][:3]:
                    print(f"   #{runner.get('cloth_number', '?')} - {runner['runner_name']}")
                    if runner.get('jockey_name'):
                        print(f"      Jockey: {runner['jockey_name']}")
                    if runner.get('trainer_name'):
                        print(f"      Trainer: {runner['trainer_name']}")
                    if runner.get('form'):
                        print(f"      Form: {runner['form']}")

                print_json(market['runners'][0], "Detailed Runner Information")

                # 6. Get live odds
                market_id = first_market['market_id']
                print(f"\n6️⃣  Getting live odds for market {market_id}...")
                response = requests.get(f"{API_BASE}/api/odds/{market_id}")
                odds = response.json()

                print(f"   Market Status: {odds['status']}")
                print(f"   In-Play: {odds['inplay']}")
                print(f"   Total Matched: ${odds['total_matched']:,.2f}")

                print("\n   Current Odds (Top 5 runners):")
                for i, runner in enumerate(odds['runners'][:5], 1):
                    selection_id = runner['selection_id']
                    ltp = runner.get('last_price_traded', 'N/A')

                    back_price = "N/A"
                    lay_price = "N/A"

                    if runner.get('back_prices'):
                        back_price = f"${runner['back_prices'][0]['price']}"

                    if runner.get('lay_prices'):
                        lay_price = f"${runner['lay_prices'][0]['price']}"

                    print(f"   {i}. Selection {selection_id}: Back {back_price} | Lay {lay_price} | LTP: ${ltp}")

                print_json(odds['runners'][0], "Detailed Odds for First Runner")

                # 7. Batch odds (if multiple markets)
                if len(markets['markets']) >= 2:
                    print("\n7️⃣  Getting batch odds for multiple markets...")
                    market_ids = ','.join([m['market_id'] for m in markets['markets'][:3]])
                    response = requests.get(
                        f"{API_BASE}/api/odds/batch",
                        params={"market_ids": market_ids}
                    )
                    batch_odds = response.json()
                    print(f"   Retrieved odds for {batch_odds['market_count']} markets")

        # 8. Get races at venue
        print(f"\n8️⃣  Getting all races at {venue}...")
        response = requests.get(f"{API_BASE}/api/race/{venue}")
        races = response.json()
        print(f"   Found {races['race_count']} races")
        print(f"   Races: {', '.join(list(races['races'].keys())[:3])}")

    else:
        print("\n⚠️  No meetings found today. The examples above require active race meetings.")
        print("   Try running this script on a day with scheduled races.")

    print("\n✅ Example completed!")
    print("\n📚 Visit http://localhost:8000/docs for interactive API documentation")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("   Make sure the API is running:")
        print("   uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
