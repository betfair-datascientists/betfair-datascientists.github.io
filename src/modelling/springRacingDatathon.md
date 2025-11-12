# Betfair’s 2025 Spring Racing Datathon

![Spring Racing Datathon Banner](../img/RACING_DATATHON.png)

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/QnQVkCqtd7)

---

## The Competition

Think you’ve got what it takes to model **Thoroughbred Racing** markets? Now’s your chance to showcase your data modeling skills in **Betfair’s 2025 Spring Racing Datathon!**  

With **$5,000 in prizes** on offer, this is your opportunity to create a predictive model that accurately **prices up Place markets** across Victorian Thoroughbred racing. Whether you're a seasoned pro or new to racing analytics, we encourage you to get creative — adapt your skills from other fields, improve an existing model, or start fresh!  

This year’s Datathon takes place over **3 weeks**, featuring a curated selection of **real Thoroughbred races**. Participants will be challenged to produce **probabilities for each runner in the Place market**, with performance measured against real-world outcomes to determine model accuracy and leaderboard rankings.

- **Leaderboard updates** will be posted here throughout the competition, so check back often.  
- Join the conversation in the Quants Discord server (**#datathon** channel), where you can discuss models with fellow participants.  
- Don’t forget to complete the [registration form](https://forms.office.com/r/ZG9ea1xQj1) to join the Discord Server.  

For questions and submissions, contact [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

---

## The Specifics

Review the full Terms and Conditions for the 2025 Spring Racing Datathon [here](../assets/Spring_Racing_Datathon_2025_TCs.pdf).

The competition will run from **10 November** 2025 until **29 November** 2025 (**excluding Sundays**) and will cover **all** Victorian Thoroughbred Racing

### Prizes

**$5,000 in prizes** are up for grabs! Here's the breakdown of the prize pool:

| Place | Prize     |
|-------|-----------|
| 1     | $2,500.00 |
| 2     | $1,000.00 |
| 3     | $500.00   |
| 4     | $250.00   |
| 5     | $250.00   |
| 6     | $100.00   |
| 7     | $100.00   |
| 8     | $100.00   | 
| 9     | $100.00   | 
| 10    | $100.00   |
| **Total Prize Pool** | **$5,000.00** |

Winners will be announced at the end of the competition, with prizes distributed shortly afterward.

---
 
### Competition Rules

Entrants will receive a bespoke set of thoroughbred racing data from a variety of sources and **this will be updated daily.**

Your goal is create a model or a set of models to generate a probability for each horse to place. The sum of the probabilities for all horses in each race must equal the number of winners in the **PLACE** market on the Betfair Exchange. If the number of runners at the time of market loading is **less than 8**, then the PLACE market will pay **two winners, otherwise three winners will be paid.** In the event of scratchings that reduce the number of runners to less than 8, the initial number of winners in the PLACE market will remain unchanged.

How you build your model is entirely up to you—whether it's an Elo model, regression, Machine Learning, or something else, the creativity is in your hands.

Submit your predictions by **60 minutes prior to the first race of the day.**

See the full Terms and Conditions for more competition rules.

---

### Submission Process

Submissions will be evaluated based on the [Log Loss method](https://en.wikipedia.org/wiki/Cross-entropy#Cross-entropy_loss_function_and_logistic_regression). The entrant with the lowest average log loss per race will be declared the winner.

All submissions should be emailed to datathon@betfair.com.au

- [Submission File 10th November](../assets/Spring_Racing_Datathon_2025_Submission_Model-Name_20251110.csv)
- [Submission File 11th November](../assets/Spring_Racing_Datathon_2025_Submission_Model-Name_20251111.csv)
- [Submission File 12th November](../assets/Spring_Racing_Datathon_2025_Submission_Model-Name_20251112.csv)
- [Submission File 13th November](../assets/Spring_Racing_Datathon_2025_Submission_Model-Name_20251113.csv)

**Code to generate submission file**

```py title="Code to generate submission file"

import os
import json
from datetime import timedelta
import dateutil.tz
import pandas as pd
import betfairlightweight
from betfairlightweight import filters

# ======================================
# ======= GLOBAL SETTINGS ==============
# ======================================

LOCAL_TZ = dateutil.tz.tzlocal()

DEFAULT_COLUMNS = [
    "market_start",
    "venue",
    "race_no",
    "race_type",
    "win_market_id",
    "place_market_id",
    "cloth_number",
    "selection_id",
    "runner_name",
    "places_paid",
    "stall_draw",
    "jockey_name",
    "trainer_name",
    "form",
    "weight_carried",
    "days_since_last_run",
    "sex_type",
    "age",
    "bred",
    "colour_type",
    "dam_name",
    "dam_bred",
    "damsire_name",
    "damsire_bred",
    "sire_name",
    "sire_bred",
    "place_probability"
]

VIC_TRACKS = [
            'Ararat',
            'Avoca',
            'Bairnsdale',
            'Ballarat',
            'Benalla',
            'Bendigo',
            'Burrumbeet',
            'Camperdown',
            'Casterton',
            'Caulfield',
            'Colac',
            'Coleraine',
            'Cranbourne',
            'Donald',
            'Dunkeld',
            'Echuca',
            'Edenhope',
            'Flemington',
            'Geelong',
            'Great Western',
            'Gunbower',
            'Hamilton',
            'Hanging Rock',
            'Horsham',
            'Kerang',
            'Kilmore',
            'Kyneton',
            'Manangatang',
            'Mildura',
            'Moe',
            'Moonee Valley',
            'Mornington',
            'Mortlake',
            'Murtoa',
            'Nhill',
            'Pakenham',
            'Penshurst',
            'Sale',
            'Sandown',
            'Seymour',
            'St Arnaud',
            'Stawell',
            'Stony Creek',
            'Swan Hill',
            'Tatura',
            'Terang',
            'Towong',
            'Traralgon',
            'Wangaratta',
            'Warracknabeal',
            'Warrnambool',
            'Werribee',
            'Wodonga',
            'Wycheproof',
            'Yarra Valley'
            ]

# ======================================
# ======= UTILITY FUNCTIONS ============
# ======================================

def load_credentials(file_path: str) -> tuple[str, str, str]:
    """
    Load Betfair API credentials from a JSON file.

    Expected JSON structure:
        {
            "username": "your_username",
            "password": "your_password",
            "app_key": "your_app_key"
        }
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Credentials file not found: {file_path}")

    with open(file_path, "r") as f:
        data = json.load(f)

    required_keys = ["username", "password", "app_key"]
    missing = [k for k in required_keys if k not in data]
    if missing:
        raise KeyError(f"Missing keys in credentials file: {', '.join(missing)}")

    return data["username"], data["password"], data["app_key"]


def create_api_client(username: str, password: str, app_key: str):
    """Initialize and return a Betfair API client."""
    client = betfairlightweight.APIClient(username, password, app_key=app_key)
    client.login_interactive()
    return client


def process_runner_catalogue(runner_catalogue_list) -> pd.DataFrame:
    """Extract detailed runner information from market catalogue."""
    rows = []
    for runner in runner_catalogue_list:
        meta = runner.metadata or {}
        runner_name = getattr(runner, "runner_name", None)
        cloth_number = meta.get("CLOTH_NUMBER") or (
            runner_name.split(".")[0] if runner_name else None
        )

        rows.append({
            "selection_id": runner.selection_id,
            "runner_name": runner_name,
            "stall_draw": meta.get("STALL_DRAW"),
            "cloth_number": cloth_number,
            "jockey_name": meta.get("JOCKEY_NAME"),
            "trainer_name": meta.get("TRAINER_NAME"),
            "form": meta.get("FORM"),
            "weight_carried": meta.get("WEIGHT_VALUE"),
            "days_since_last_run": meta.get("DAYS_SINCE_LAST_RUN"),
            "sex_type": meta.get("SEX_TYPE"),
            "age": meta.get("AGE"),
            "bred": meta.get("BRED"),
            "colour_type": meta.get("COLOUR_TYPE"),
            "dam_name": meta.get("DAM_NAME"),
            "dam_bred": meta.get("DAM_BRED"),
            "damsire_name": meta.get("DAMSIRE_NAME"),
            "damsire_bred": meta.get("DAMSIRE_BRED"),
            "sire_name": meta.get("SIRE_NAME"),
            "sire_bred": meta.get("SIRE_BRED"),
        })
    return pd.DataFrame(rows)


def process_runner_books(runner_books) -> pd.DataFrame:
    """Extract basic status info from the market book."""
    return pd.DataFrame([
        {"selection_id": rb.selection_id, "status": rb.status}
        for rb in runner_books
    ])


def get_markets(trading, market_type_code: str):
    """Fetch markets of a specific type (e.g., WIN or PLACE)."""
    market_filter = filters.market_filter(
        event_type_ids=[7],
        venues=VIC_TRACKS,
        market_countries=["AU"],
        market_type_codes=[market_type_code],
        race_types=["Flat", "Hurdle", "Steeple"],
    )

    return trading.betting.list_market_catalogue(
        filter=market_filter,
        market_projection=[
            "RUNNER_DESCRIPTION",
            "EVENT",
            "MARKET_DESCRIPTION",
            "RUNNER_METADATA",
        ],
        max_results="200",
    )

def build_win_dataframe(trading, win_markets) -> pd.DataFrame:
    """Construct DataFrame containing WIN market data."""
    all_rows = []
    price_filter = filters.price_projection(price_data=["EX_BEST_OFFERS"])

    for market in win_markets:
        market_id = market.market_id
        market_name = market.market_name
        event_name = market.event.name
        market_start = market.description.market_time + timedelta(hours=11)

        books = trading.betting.list_market_book([market_id], price_projection=price_filter)
        if not books:
            continue

        book = books[0]
        runners_df = process_runner_books(book.runners)
        catalogue_df = process_runner_catalogue(market.runners)

        df = pd.merge(runners_df, catalogue_df, on="selection_id", how="left")
        df["win_market_id"] = market_id
        df["win_market_id"] = df["win_market_id"].astype(str).str.replace("1.", "", regex=False).astype(int)
        df["market_start"] = market_start
        df["venue"] = event_name.split(" (")[0]
        df["race_no"] = market_name.split(" ")[0].replace("R", "")
        df["race_type"] = market_name.split("m ")[-1] if "m " in market_name else None
        df["runner_name"] = df["runner_name"].str.split(". ",n=1).str[-1]

        all_rows.append(df)

    win_df = pd.concat(all_rows, ignore_index=True)
    return win_df[win_df["status"] != "REMOVED"]


def build_place_dataframe(trading, place_markets) -> pd.DataFrame:
    """Construct DataFrame containing PLACE market data including number_of_winners."""
    rows = []

    for market in place_markets:
        market_id = market.market_id
        market_start = market.description.market_time + timedelta(hours=11)
        event_name = market.event.name

        # Fetch MarketBook to get number_of_winners
        books = trading.betting.list_market_book([market_id])
        num_winners = books[0].number_of_winners if books else None

        # Clean numeric market_id
        numeric_market_id = int(str(market_id).replace("1.", ""))

        for runner in market.runners:
            rows.append({
                "venue": event_name.split(" (")[0],
                "place_market_id": numeric_market_id,
                "market_start": market_start,
                "selection_id": runner.selection_id,
                "places_paid": num_winners,
            })

    return pd.DataFrame(rows)


def merge_win_place(win_df: pd.DataFrame, place_df: pd.DataFrame) -> pd.DataFrame:
    """Join WIN and PLACE market dataframes."""
    merged = pd.merge(
        win_df,
        place_df,
        on=["venue", "market_start", "selection_id"],
        how="left",
    )

    merged["cloth_number"] = merged["cloth_number"].astype(int)

    merged.sort_values(["venue", "race_no", "cloth_number"], inplace=True)
    return merged


# ======================================
# =============== MAIN =================
# ======================================

def main():
    """Main workflow for Betfair WIN and PLACE market extraction."""
    credentials_path = (
        "credentials.json"
    )

    username, password, app_key = load_credentials(credentials_path)
    trading = create_api_client(username, password, app_key)

    print("Fetching WIN markets...")
    win_markets = get_markets(trading, "WIN")
    print(f"Found {len(win_markets)} WIN markets.\n")

    win_df = build_win_dataframe(trading, win_markets)

    print("Fetching PLACE markets...")
    place_markets = get_markets(trading, "PLACE")
    print(f"Found {len(place_markets)} PLACE markets.\n")

    place_df = build_place_dataframe(trading, place_markets)

    print("Merging WIN and PLACE data...")
    combined_df = merge_win_place(win_df, place_df)
    combined_df['place_probability'] = None
    combined_df = combined_df[DEFAULT_COLUMNS]

    output_file = "betfair_data_with_place.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"\n✅ Data saved to {output_file} ({len(combined_df)} rows).")

    trading.logout()
    print("Logged out successfully.")

if __name__ == "__main__":
    main()

```

---
 
### Judging

 - Entrants will be ranked in ascending order on their average log loss per race

---

### Historic Data

The dataset for the competition will be provided to participants in the registration email and daily updates will be provided here

 - [October Dataset](../assets/Datathon_Dataset_2025-10.csv)
 - [01-Nov-2025](../assets/Datathon_Dataset_2025-11-01.csv)
 - [02-Nov-2025](../assets/Datathon_Dataset_2025-11-02.csv)
 - [03-Nov-2025](../assets/Datathon_Dataset_2025-11-03.csv)
 - [04-Nov-2025](../assets/Datathon_Dataset_2025-11-04.csv)
 - [05-Nov-2025](../assets/Datathon_Dataset_2025-11-05.csv)
 - [06-Nov-2025](../assets/Datathon_Dataset_2025-11-06.csv)
 - [07-Nov-2025](../assets/Datathon_Dataset_2025-11-07.csv)
 - [08-Nov-2025](../assets/Datathon_Dataset_2025-11-08.csv)
 - [09-Nov-2025](../assets/Datathon_Dataset_2025-11-09.csv)
 - [10-Nov-2025](../assets/Datathon_Dataset_2025-11-10.csv)
 - [11-Nov-2025](../assets/Datathon_Dataset_2025-11-11.csv)
---
 
## Leaderboard

**Check Back Later**
---

## FAQs

### Can I resubmit my submission if I notice an error?

- Yes, only the last submitted file before the submission deadline will be considered for marking

### What are the guidelines for the rated prices?

- For each match, the sum of the reciprocals for all horses must sum to the number of winners in the PLACE market (either 2 or 3)
- Each probability must be between 0 and 1, exclusive
- Any probability of 0 will be adjusted to 0.001 (equivalent to maximum Betfair Price of $1000)
- Any probability of 1 will be adjusted to 0.99 (equivalent to minimum Betfair Price of $1.01)
- No truncation of decimal points is required

### What happens for races that are abandoned or postponed?

- These races will not be considered for scoring

### What happens in the event of a scratching?

- That runner will be removed from the race, and all remaining probabilities will be normalised

### What happens in the event of a dead heat?

- If there is a dead heat, such that the number of actual winners exceeds the market number of winners, the binary result will be divided by the number of runners for the final place.
- e.g. If there is a dead heat for 3rd place between 2 runners, the horses placed 1st and 2nd will be assigned 1, the two runners in 3rd will be assigned a result of 0.5 and all other runners will receive 0. This replicates the process used for market settlement on the Betfair Exchange

### What if I want to use a Machine Learning model?

- The algorithm choice doesn’t matter from a competition perspective. However, you should use a classification model, not a regression model.

### What happens if I miss a race?

- The entrant will be assigned the median value of all other participants for the race. You must submit at least 90% of races to remain eligible for a prize.

---

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/QnQVkCqtd7)