# Betfair’s 2025 Greyhound Racing Datathon

![Greyhound Datathon Banner](../img/GREYHOUND_DATATHON_BANNER.png)

## Registration

[Register Here!](https://forms.office.com/r/VbxSUYXjsi)

Registrations are open until May 16th 2025. Only entrants who have registered through the link will be eligible to win a prize

---

## The Competition

Think you’ve got what it takes to price up a Greyhound market? Now’s your chance to showcase your data modeling skills in Betfair’s 2025 Greyhound Racing Datathon!

With **$5,000 in prizes** on offer, this is your opportunity to create a predictive model for Greyhound racing on the Betfair Exchange. Whether you're a seasoned pro or new to greyhound modeling, we encourage you to get creative—adapt your skills from other fields, improve an existing model, or start fresh!

This year’s Greyhound Racing Datathon runs across 2 weeks, and we challenge you to test your skills against others for both **prizes** and **ultimate bragging rights**.

- Leaderboard updates will be posted here throughout the competition, so check back often.
- Join the conversation in the Quants Discord server (#datathon channel), where you can discuss models with fellow participants.
- Don't forget to complete the [registration form](https://forms.office.com/r/ZG9ea1xQj1) to join the Discord Server.

For questions and submissions, contact [datathon@betfair.com.au](mailto:datathon@betfair.com.au).

---

## The Specifics

Review the full Terms and Conditions for the 2025 Greyhound Racing Datathon [here](../assets/Greyhound_Datathon_2025_TCs.pdf).

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

### Competition Rules

The aim of this competition is to generate a **rated price** for every runner in every race across a set of meetings during the competition period (**WIN** markets only)

The competition period is May 19th, 2025 - May, 30th 2025

The specific meetings will meet the following criteria:

 - The meeting will occur in Australia 
 - The meeting will NOT occur at a venue in Western Australia
 - The meeting will occur on a weekday (Monday to Friday)
 - The meeting will commence after 5pm AEST (Evening meeting)

Submissions are by due by 4:59pm AEST each day

---

### Submission Process

Submission templates will be provided here by 12:00pm AEST each day

 - [Example Submission Template](../assets/submission_template_2025-04-15.csv)
 - [May 19th Submission](../assets/submission_template_2025-05-19.csv)
 - [May 20th Submission](../assets/submission_template_2025-05-20.csv)
 - [May 21st Submission](../assets/submission_template_2025-05-21.csv)
 - [May 22nd Submission](../assets/submission_template_2025-05-22.csv)
 - [May 23rd Submission](../assets/submission_template_2025-05-23.csv)
 - [May 26th Submission](../assets/submission_template_2025-05-26.csv)
 - [May 27th Submission](../assets/submission_template_2025-05-27.csv)
 - [May 28th Submission](../assets/submission_template_2025-05-28.csv)
 - [May 29th Submission](../assets/submission_template_2025-05-29.csv)
 - [May 30th Submission](../assets/submission_template_2025-05-30.csv)

Entrants should not edit the template in any way except to add the rated price for each runner.

```py title='Generate Submission Template'

import betfairlightweight
from betfairlightweight import filters
import pandas as pd
import dateutil.tz
from datetime import datetime, timedelta, time
import json
from tqdm import tqdm

local_tz = dateutil.tz.tzlocal()
now = datetime.now(dateutil.tz.tzlocal())

with open("credentials.json") as f:
    cred = json.load(f)
    my_username = cred["username"]
    my_password = cred["password"]
    my_app_key = cred["app_key"]

trading = betfairlightweight.APIClient(username=my_username,
                                    password=my_password,
                                    app_key=my_app_key
                                    )

trading.login_interactive()

# Define the market filter
market_filter = filters.market_filter(
    bsp_only=True,
    event_type_ids=[4339],  # For greyhound racing
    market_countries=['AU'],  # For Australia
    market_type_codes=['WIN']  # For win markets
)

def process_runner_books(runner_books):
    '''
    This function processes the runner books and returns a DataFrame with the best back/lay prices + vol for each runner
    :param runner_books:
    :return:
    '''
    
    selection_ids = [runner_book.selection_id for runner_book in runner_books]
    statuses = [runner_book.status for runner_book in runner_books]

    df = pd.DataFrame({
        'selection_id': selection_ids,
        'status': statuses,
    })
    return df

# Get a list of all markets that match the filter
market_catalogues = trading.betting.list_market_catalogue(
    filter=market_filter,
    market_projection=['RUNNER_DESCRIPTION', 'EVENT', 'MARKET_START_TIME'],
    max_results='1000')

print(f"Found {len(market_catalogues)} markets.")

data = pd.DataFrame(columns=[
        'event_start_date',
        'market_start',
        'venue', 
        'race_no',
        'race_type',
        'win_market_id',
        'selection_id',
        'tab_number',
        'runner_name',
        'status',
    ])

runner_dataframes = []

for market_catalogue in tqdm(market_catalogues, desc="Processing markets"):
    market_id = market_catalogue.market_id
    market_name = market_catalogue.market_name
    event_name = market_catalogue.event.name
    venue = market_catalogue.event.venue
    market_start_time = market_catalogue.market_start_time
    event_open_date = market_catalogue.event.open_date

    market_books = trading.betting.list_market_book(market_ids=[market_id])
    runner_catalogues = market_catalogue.runners

    for market_book in market_books:
        runners_df = process_runner_books(market_book.runners)
        #get the runner catalogue
        for runner in market_book.runners:
            runner_catalogue = next((rd for rd in runner_catalogues if rd.selection_id == runner.selection_id), None)

            if runner_catalogue is not None:
                runner_name = runner_catalogue.runner_name
                near_price = runner_catalogue
                runners_df.loc[runners_df['selection_id'] == runner.selection_id, 'runner_name'] = runner_name
        #process some of the data to more helpful values
        runners_df['event_open_date'] = event_open_date
        runners_df['event_open_date'] = runners_df['event_open_date'] + timedelta(hours=10)
        runners_df['win_market_id'] = market_id
        runners_df['market_name'] = market_name
        runners_df['event_name'] = event_name
        runners_df['market_start'] = market_start_time
        runners_df['market_start'] = runners_df['market_start'] + timedelta(hours=10)
        runners_df['venue']=venue
        runners_df['race_no']=runners_df['market_name'].str.split(r' ').str[0]
        runners_df['race_no']=runners_df['race_no'].str.split('R').str[1]
        runners_df['race_type']=runners_df['market_name'].str.split(r'm ').str[1]
        runners_df['tab_number']=runners_df['runner_name'].str.split(r'. ').str[0]
        runners_df['runner_name']=runners_df['runner_name'].str.split(r'\. ').str[1]
        #reorder the columns
        runners_df=runners_df[[
        'event_open_date',
        'market_start',
        'venue',
        'race_no',
        'race_type',
        'win_market_id',
        'selection_id',
        'tab_number',
        'runner_name',
        'status',
        ]]
        #join the dataframes together
        runner_dataframes.append(runners_df)

df = pd.concat(runner_dataframes, ignore_index=True)

#remove scratched runners, WA Tracks and meetings starting before 6pm
df=df[~(df['status'] == 'REMOVED')]
df = df[~df['venue'].isin(['Cannington', 'Mandurah', 'Northam'])]
df = df[df['event_open_date'].dt.time >= time(17, 0)]
df = df.drop(columns=['event_open_date'])

#sort columns
df['race_no'] = df['race_no'].astype(int)
df['tab_number'] = df['tab_number'].astype(int)
df = df.sort_values(by=['venue', 'race_no', 'tab_number'])

#initiate rated price column
df['rated_price'] = None

today = datetime.today().strftime('%Y-%m-%d')
filename = f'submission_template_{today}.csv'
df.to_csv(filename, index=False)

# Logout from your Betfair account
trading.logout()

```

**Missed submissions?**

 - You’ll be assigned the median log loss of all other entrants for that race.

---

### Judging

Submissions will be evaluated based on the [Log Loss Method](https://towardsdatascience.com/intuition-behind-log-loss-score-4e0c9979680a/). 

The log loss score for each runner in a race will be added together and entrants will be marked on their average log loss per race

The entrant with the lowest average log loss per race will be declared the winner.

---

### Historic Data

Registrants will be provided with a link for a historic dataset from the Topaz API. Updates will be added to the folder provided in the registration email


Registrants with a Topaz API key can utilise the code below:

### Data Download Code

```py
import pandas as pd
from tqdm import tqdm
import time
from datetime import datetime, timedelta
from topaz import TopazAPI
from sklearn.preprocessing import MinMaxScaler 
import numpy as np
import requests
import os
import itertools
from dateutil.relativedelta import relativedelta

# Constants
TOPAZ_API_KEY = ''

JURISDICTION_CODES = ['NSW', 'QLD', 'WA', 'TAS', 'NT', 'NZ', 'VIC', 'SA']

START_DATE = '2025-01-01'
today = datetime.today()
END_DATE = (today - timedelta(days=7)).strftime('%Y-%m-%d')
first_of_this_month = today.replace(day=1).strftime('%Y-%m-%d')
first_of_last_month = (today.replace(day=1) - relativedelta(months=1)).strftime('%Y-%m-%d')

def define_topaz_api(api_key):
    return TopazAPI(api_key)

topaz_api = define_topaz_api(TOPAZ_API_KEY)

'''
It is pythonic convention to define hard-coded variables (like credentials) in all caps. Variables whose value may change in use should be defined in lowercase with underscore spacing
'''

def generate_month_year_range(start_date, end_date):

    dates = pd.date_range(start=start_date, end=end_date, freq='MS')
    return [(date.year, date.month) for date in dates]

def generate_day_range(start_date, end_date):

    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    return [(date.year, date.month, date.day) for date in dates]

def get_existing_bulk_data(csv_path):

    if not os.path.isfile(csv_path):
        return set(), set()

    try:
        # Extract owning authority code from filename
        base_name = os.path.basename(csv_path)
        owning_authority_code = base_name.split('_')[0]

        # Read and parse meetingDate
        df = pd.read_csv(csv_path, usecols=['meetingDate'], parse_dates=['meetingDate'])

        # Create year, month, and day columns
        df['year'] = df['meetingDate'].dt.year
        df['month'] = df['meetingDate'].dt.month
        df['day'] = df['meetingDate'].dt.day

        # Generate sets
        monthly_done = set((owning_authority_code, y, m) for y, m in zip(df['year'], df['month']))
        daily_done = set((owning_authority_code, y, m, d) for y, m, d in zip(df['year'], df['month'], df['day']))

        return monthly_done, daily_done

    except Exception as e:
        print(f"Error reading {csv_path}: {e}")
        return set(), set()

def download_bulk_data(topaz_api, start_date, end_date, jurisdiction_codes):
    for code in jurisdiction_codes:
        csv_path = f"{code}_bulk_runs.csv"
        file_exists = os.path.isfile(csv_path)

        # Track completed months/days
        monthly_done, daily_done = get_existing_bulk_data(csv_path)

        # --- Monthly ---
        for year, month in generate_month_year_range(start_date, first_of_last_month):
            if (code, year, month) in monthly_done:
                print(f"Skipping {code} {year}-{month:02d} (already downloaded)")
                continue

            success = False
            retries = 0
            max_retries = 5

            while not success and retries < max_retries:
                try:
                    data = topaz_api.get_bulk_runs_by_month(
                        owning_authority_code=code,
                        year=year,
                        month=month
                    )
                    if data.empty:
                        print(f"No data for {code} {year}-{month:02d}")
                        break
                    data.to_csv(csv_path, mode='a', index=False, header=not file_exists)
                    file_exists = True
                    print(f"Appended data for {code} {year}-{month:02d}")
                    success = True
                except Exception as e:
                    error_msg = str(e).lower()
                    if '429' in error_msg or 'rate limit' in error_msg or 'timed out' in error_msg or 'timeout' in error_msg:
                        retries += 1
                        print(f"Retryable error for {code} {year}-{month:02d}: {e}. Retrying in 60 seconds... ({retries}/{max_retries})")
                        time.sleep(60)
                    else:
                        print(f"Non-retryable error for {code} {year}-{month:02d}: {e}")
                        break

        # --- Daily ---
        for year, month, day in generate_day_range(first_of_this_month, end_date):
            if (code, year, month, day) in daily_done:
                continue

            success = False
            retries = 0
            max_retries = 5

            while not success and retries < max_retries:
                try:
                    data = topaz_api.get_bulk_runs_by_day(
                        owning_authority_code=code,
                        year=year,
                        month=month,
                        day=day
                    )
                    if data.empty:
                        print(f"No data for {code} {year}-{month:02d}-{day:02d}")
                        break
                    data.to_csv(csv_path, mode='a', index=False, header=not file_exists)
                    file_exists = True
                    print(f"Appended data for {code} {year}-{month:02d}-{day:02d}")
                    success = True
                except Exception as e:
                    error_msg = str(e).lower()
                    if '429' in error_msg or 'rate limit' in error_msg or 'timed out' in error_msg or 'timeout' in error_msg:
                        retries += 1
                        print(f"Retryable error for {code} {year}-{month:02d}-{day:02d}: {e}. Retrying in 60 seconds... ({retries}/{max_retries})")
                        time.sleep(60)
                    else:
                        print(f"Non-retryable error for {code} {year}-{month:02d}-{day:02d}: {e}")
                        break

download_bulk_data(topaz_api, START_DATE, END_DATE, JURISDICTION_CODES)

```

## Leaderboard - 28th May

![Leaderboard](../img/GH_Leaderboard.png)

---

## FAQs

### Can I resubmit my submission if I notice an error?

- Yes, only the final entry received before the deadline will be used for scoring

### What are the guidelines for the rated prices?

- Prices submitted must be greater than 1 **(exactly 1 is not valid)**
- The overround for the market must be 1 (i.e. the sum of the reciprocals of all the rated prices)

### What if my overround isn't 1?

- Rated Prices will be normalised so that the market sums to 1

### What if I want to use a Machine Learning model?

- The algorithm choice doesn’t matter from a competition perspective. However, you should use a classification model, not a regression model.

### What happens if I miss a race?

- You’ll be assigned the median log loss from other entrants for that race.

### How many races can I miss?

- You can miss up to two full days of racing before you will no longer be eligible for a prize

### What happens if a race is not run (abandoned) or is declared a no-race?

- That race will be excluded from scoring

### What happens if there is a scratching?

 - The runner will be removed and the remaining prices will be normalised so that the overround sums to 1

### What happens if there is a deadheat?

 - The result will be recorded as 1 divided by the number of winners

---

### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.
