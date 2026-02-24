# Betfair’s 2026 Greyhound Racing Datathon

![Greyhound Racing Datathon Banner](../img/RACING_DATATHON.png)

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/mUmj35mFHb)

Note – only existing customers of Betfair, as at 18 February 2026, can participate in the Competition.

---

## The Competition

Think you’ve got what it takes to model **Greyhound Racing** H2H markets? Now’s your chance to showcase your data modelling skills in **Betfair’s 2026 Greyhound Racing Datathon!**  

With **$5,000 in prizes** on offer, this is your opportunity to create a predictive model that accurately **prices up Head-To-Head markets** across Australian Greyhound racing. Whether you're a seasoned pro or new to racing analytics, we encourage you to get creative — adapt your skills from other fields, improve an existing model, or start fresh!  

This year’s Datathon takes place over **3 weeks**, featuring a curated selection of **real Greyhound races**. Participants will be challenged to produce **probabilities for each runner in every possible head to head combination**, with performance measured against real-world outcomes to determine model accuracy and leaderboard rankings.

- **Leaderboard updates** will be posted here throughout the competition, so check back often.  
- Join the conversation in the Quants Discord server (**#datathon** channel), where you can discuss models with fellow participants.  
- Don’t forget to complete the [registration form](https://forms.office.com/r/ZG9ea1xQj1) to join the Discord Server.  

For questions and submissions, contact [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

---

## The Specifics

Review the full Terms and Conditions for the 2026 Greyhound Racing Datathon [here](../assets/Greyhound_Racing_Datathon_2026_TCs.pdf).

The competition will run from **10 March** 2026 until **25 March** 2026 (**excluding weekends**) and will cover **all** Australian Greyhound Racing (excluding WA) where the first race at the meeting is scheduled to occur after 5:00pm AEDT.

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

Entrants must have been provided a Topaz API key by the Betfair Australia Automation Team to access the historic dataset.

Your goal is create a model or a set of models to generate the probability that one dog will finish ahead of another dog in the race, repeated for all possible combinations in the race (up to 56 combinations per race). The sum of the probabilities for both dogs in each head-to-head match up must equal 1 and must be between 0 and 1, excluding 0 and 1. If either runner is scratched or if both runners fail to finish the race, then that match up will be excluded from scoring.

How you build your model is entirely up to you—whether it's an Elo model, regression, Machine Learning, or something else, the creativity is in your hands.

Submit your predictions by **4:59 AEDT on the day of the race**

See the full Terms and Conditions for more competition rules.

---

### Submission Process

Submissions will be evaluated based on the [Log Loss method](https://en.wikipedia.org/wiki/Cross-entropy#Cross-entropy_loss_function_and_logistic_regression). The entrant with the lowest average log loss per race will be declared the winner.

All submissions should be emailed to datathon@betfair.com.au

**Code to generate submission file will be provided**

---
 
### Judging

 - Entrants will be ranked in ascending order on their average log loss per race

---

### Historic Data

Participants are required to utilise their Topaz API key to download the historic dataset. A temporary Topaz key may be provided upon request.

---

### Submission Files

[Example Submission File](../assets/submission-template_model-name_2026-02-24.csv)

```py title="Code"

import json
from datetime import datetime
from zoneinfo import ZoneInfo
from itertools import combinations

import pandas as pd
from tqdm import tqdm
import betfairlightweight
from betfairlightweight import filters


# ===========================
# Configuration
# ===========================

CREDENTIAL_PATH = "credentials.json"
EVENT_TYPE_ID = 4339  # Horse Racing
COUNTRY = "AU"
MARKET_TYPES = ["WIN"]
MAX_RESULTS = 1000

# ===========================
# Authentication
# ===========================

def load_credentials(path):
    with open(path) as f:
        return json.load(f)


def login():
    cred = load_credentials(CREDENTIAL_PATH)

    client = betfairlightweight.APIClient(
        username=cred["username"],
        password=cred["password"],
        app_key=cred["app_key"],
    )
    client.login_interactive()
    return client


# ===========================
# Market Fetching
# ===========================

def build_market_filter():
    return filters.market_filter(
        event_type_ids=[EVENT_TYPE_ID],
        market_countries=[COUNTRY],
        market_type_codes=MARKET_TYPES,
    )


def get_market_catalogues(client):
    return client.betting.list_market_catalogue(
        filter=build_market_filter(),
        market_projection=[
            "RUNNER_DESCRIPTION",
            "EVENT",
            "MARKET_START_TIME"
        ],
        max_results=MAX_RESULTS,
    )


# ===========================
# Data Processing
# ===========================

def process_market(client, market_catalogue):

    market_start = (
        market_catalogue.market_start_time
        .replace(tzinfo=ZoneInfo("UTC"))
        .astimezone(ZoneInfo("Australia/Sydney"))
    )

    event_open_date = (
        market_catalogue.event.open_date
        .replace(tzinfo=ZoneInfo("UTC"))
        .astimezone(ZoneInfo("Australia/Sydney"))
    )

    runner_lookup = {
        r.selection_id: r.runner_name
        for r in market_catalogue.runners
    }

    market_books = client.betting.list_market_book(
        market_ids=[market_catalogue.market_id]
    )

    records = []

    for market_book in market_books:
        for runner in market_book.runners:

            runner_name = runner_lookup.get(runner.selection_id)

            if not runner_name:
                continue

            rug_number = runner_name.split(". ")[0]
            runner_name_trunc = runner_name.split(". ")[-1]

            records.append({
                "venue": market_catalogue.event.venue,
                "event_id": market_catalogue.event.id,
                "event_open_date": event_open_date,
                "market_name": market_catalogue.market_name,
                "market_start": market_start,
                "market_id": market_catalogue.market_id,
                "selection_id": runner.selection_id,
                "runner_name": runner_name,
                "runner_name_trunc": runner_name_trunc,
                "rug_number": rug_number,
                "runner_status": runner.status,
            })
    
    today_5pm = datetime.now(ZoneInfo("Australia/Sydney")).replace(hour=17, minute=0, second=0, microsecond=0)
    excluded_venues = ["Cannington", "Mandurah", "Northam"]

    df = pd.DataFrame(records)

    # Filter the DataFrame
    df = df[
        (df['event_open_date'] >= today_5pm) & 
        (~df['venue'].isin(excluded_venues))
    ]
    
    return df


# ===========================
# H2H Construction
# ===========================

def build_h2h_markets(df):

    df_clean = df[df["runner_status"] != "REMOVED"].copy()

    # Ensure numeric ordering
    df_clean["rug_number"] = pd.to_numeric(
        df_clean["rug_number"], errors="coerce"
    )

    h2h_rows = []

    for (venue, win_market_name), group in df_clean.groupby(["venue", "market_name"]):

        group = group.sort_values("rug_number")

        for r1, r2 in combinations(group.itertuples(index=False), 2):

            h2h_rows.append({
                "date" : datetime.today().strftime('%d/%m/%Y'),
                "venue": venue,
                "race_number" : int(win_market_name[1:].split(' ')[0]),
                "win_market_name": win_market_name,
                "h2h_market_name": f"{r1.runner_name_trunc} v {r2.runner_name_trunc}",
                "selection_id_1": r1.selection_id,
                "runner_name_1": r1.runner_name,
                "selection_id_2": r2.selection_id,
                "runner_name_2": r2.runner_name,
                "runner_1_win_probability": None,
                "runner_2_win_probability": None,
            })

    # Create DataFrame
    h2h_df = pd.DataFrame(h2h_rows)

    # Sort by venue then race_number (race_number is already int)
    h2h_df = h2h_df.sort_values(["venue", "race_number"]).reset_index(drop=True)

    return h2h_df

# ===========================
# Main Execution
# ===========================

def main():

    client = login()

    try:
        catalogues = get_market_catalogues(client)
        print(f"Found {len(catalogues)} markets.")

        market_dfs = []

        for market_catalogue in tqdm(catalogues, desc="Processing markets"):
            market_df = process_market(client, market_catalogue)

            if not market_df.empty:
                market_dfs.append(market_df)

        if not market_dfs:
            print("No runner data found.")
            return

        df = pd.concat(market_dfs, ignore_index=True)

        h2h_df = build_h2h_markets(df)

        today = datetime.today().strftime("%Y-%m-%d")
        filename = f"submission-template_model-name_{today}.csv"

        h2h_df.to_csv(filename, index=False)
        print(f"Saved {filename}")

    finally:
        client.logout()

if __name__ == "__main__":
    main()

```
---
 
## Leaderboard

Check back later

---

## FAQs

### Can I resubmit my submission if I notice an error?

- Yes, only the last submitted file before the submission deadline will be considered for marking

### What are the guidelines for the probabilities?

- For each match up the probability of both dogs must sum to 1
- Each dog must have a probability between 0 and 1, excluding 0 and 1
- Any probability of 0 will be adjusted to 0.001, corresponding to a price of $1000
- Any probability of 1 will be adjusted to 0.99, corresponding to a price of $1.01

### What happens for races that are abandoned or postponed?

- These races will not be considered for scoring

### What happens in the event of a scratching?

- That runner will be removed from the race, and all combinations relating to that runner will be removed from scoring

### What happens if one or both dogs fail to complete the race?

- If one dog fails to complete the race and other dog completes the race, then the latter will be assigned the winner
- If both dogs fail to complete the race, then the match up will be excluded from scoring

### What happens in the event of a dead heat?

- If there is a dead heat, the result for both runners will be assigned as 0.5 and log loss calculated accordingly

### Why are WA races excluded?

- Due to the later loading times of the WA markets, it is necessary to exclude them to allow the submission templates to be loaded and available by 12pm daily

### What if I want to use a Machine Learning model?

- The algorithm choice doesn’t matter from a competition perspective. However, you should use a classification model, not a regression model.

### What happens if I miss a race?

- The entrant will be assigned the median value of all other participants for the race. You must submit at least 90% of races to remain eligible for a prize.

---

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/QnQVkCqtd7)