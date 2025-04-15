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

[Example Submission Template](../assets/submission_template_2025-04-15.csv)

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
df = df[df['event_open_date'].dt.time >= time(18, 0)]
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

Registrants will be provided with a link for a historic dataset from the Topaz API. Updates will be posted here weekly leading up to the competition and daily during the competition.

Registrants with a Topaz API key can utilise the code below:

### Data Download Code

```py
import pandas as pd
from tqdm import tqdm
import time
from datetime import datetime, timedelta
from topaz import TopazAPI
import requests
import os

# Insert your TOPAZ API key 
TOPAZ_API_KEY = ''

# Define the states you require
JURISDICTION_CODES = ['VIC','NSW','QLD','SA','NZ','TAS','NT','WA']

'''
It is pythonic convention to define hard-coded variables (like credentials) in all caps. Variables whose value may change in use should be defined in lowercase with underscore spacing
'''

# Define the start and end date for the historic data download
start_date = datetime(2025,2,1)
end_date = datetime(2025,3,20)

def generate_date_range(start_date, end_date):
    ''' 
    Here we generate our date range for passing into the Topaz API.
    This is necessary due to the rate limits implemented in the Topaz API. 
    Passing a start date and end date 12 months apart in the API call will cause significant amounts of data to be omitted, so we need to generate a range to pass much smaller date ranges in the Topaz API calls
    '''
    # Initialise the date_range list
    date_range = []

    current_date = start_date

    while current_date <= end_date:
        date_range.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return date_range

def define_topaz_api(api_key):
    '''
    This is where we define the Topaz API and pass our credentials
    '''
    topaz_api = TopazAPI(api_key)

    return topaz_api

def download_topaz_data(topaz_api,date_range,codes,datatype,number_of_retries,sleep_time):
    '''
    The parameters passed here are:
        1. The TopazAPI instance with our credentials
        2. Our date range that we generated which is in the format of a list of strings
        3. Our list of JURISDICTION_CODES
        4. Our datatype (either 'HISTORICAL' or 'UPCOMING'). 
            It is important to separate these in our database to ensure that the upcoming races with lots of empty fields (like margin) do not contaminate our historical dataset.
    '''

    # Iterate over 10-day blocks
    for i in range(0, len(date_range), 10):
        start_block_date = date_range[i]
        print(start_block_date)
        end_block_date = date_range[min(i + 9, len(date_range) - 1)]  # Ensure the end date is within the range

        
        for code in codes:
            # initialise the race list
            all_races = []

            print(code)

            retries = number_of_retries  # Number of retries
            '''
            In this code block we are attempting to download a list of raceIds by passing our JURISDICTION_CODES and date range.
            The sleep functions are included to allow time for the rate limits to reset and any other errors to clear.
            The Topaz API does not return much detail in error messages and through extensive trial and error, we have found the best way to resolve errors is simply to pause for a short time and then try again.
            After 10 retries, the function will move to the next block. This will usually only occur if there actually were zero races for that JURISDICTION_CODE and date_range or there is a total Topaz API outage.
            '''
            while retries > 0:
                try:
                    races = topaz_api.get_races(from_date=start_block_date, to_date=end_block_date, owning_authority_code=code)
                    all_races.append(races)
                    break  # Break out of the loop if successful
                except requests.HTTPError as http_err:
                    if http_err.response.status_code == 429:
                        retries -= 1
                        if retries > 0:
                            print(f"Rate limited. Retrying in {sleep_time * 4/60} minutes...")
                            time.sleep(sleep_time * 4)
                        else:
                            print("Max retries reached. Moving to the next block.")
                    else:
                        print(f"Error fetching races for {code}: {http_err.response.status_code}")
                        retries -= 1
                        if retries > 0:
                            print(f"Retrying in {sleep_time} seconds...")
                            time.sleep(sleep_time)
                        else:
                            print("Max retries reached. Moving to the next block.")

            try:
                all_races_df = pd.concat(all_races, ignore_index=True)
            except ValueError:
                continue

            # Extract unique race IDs
            race_ids = list(all_races_df['raceId'].unique())

            # Define the file path
            file_path = code + '_DATA_'+datatype+'.csv'
            
            # Use tqdm to create a progress bar
            for race_id in tqdm(race_ids, desc="Processing races", unit="race"):
                result_retries = number_of_retries
                '''
                Here we utilise the retries function again to maximise the chances of our data being complete.
                We spend some time here gathering the splitPosition and splitTime. While these fields are not utilised in the completed model, the process to extract this data has been included here for the sake of completeness only, as it is not straightforward.
                
                '''
                while result_retries > 0:
                    # Check if we already have a file for this jurisdiction
                    file_exists = os.path.isfile(file_path)
                    # Set the header_param to the opposite Bool
                    header_param = not file_exists
                    
                    try:                        
                        # Get the race result data
                        race_result_json = topaz_api.get_race_result(race_id=race_id)

                        # Flatten the JSON response into a dataframe
                        race_result = pd.json_normalize(race_result_json)

                        race_run_df = pd.DataFrame(race_result['runs'].tolist(),index=race_result.index)
                        race_run = race_run_df.T.stack().to_frame()
                        race_run.reset_index(drop=True, inplace= True)
                        race_run_normalised = pd.json_normalize(race_run[0])

                        # Separate the split times and flatten them
                        split_times_df = pd.DataFrame(race_result['splitTimes'].tolist(),index=race_result.index)
                        splits_dict = split_times_df.T.stack().to_frame()
                        splits_dict.reset_index(drop=True, inplace= True)
                        splits_normalised = pd.json_normalize(splits_dict[0])
                        
                        if len(splits_normalised) > 0:
                            
                            # Create a dataframe from the first split
                            first_split = splits_normalised[splits_normalised['splitTimeMarker'] == 1]
                            first_split = first_split[['runId','position','time']]
                            first_split = first_split.rename(columns={'position':'firstSplitPosition','time':'firstSplitTime'})

                            # Create a dataframe from the second split
                            second_split = splits_normalised[splits_normalised['splitTimeMarker'] == 2]
                            second_split = second_split[['runId','position','time']]
                            second_split = second_split.rename(columns={'position':'secondSplitPosition','time':'secondSplitTime'})

                            # Create a dataframe from the runIds, then merge the first and second split dataframes
                            split_times = splits_normalised[['runId']]
                            split_times = pd.merge(split_times,first_split,how='left',on=['runId'])
                            split_times = pd.merge(split_times,second_split,how='left',on=['runId'])

                        try:
                            # Attach the split times to the original race_run dataframe
                            race_run = pd.merge(race_run_normalised,split_times,how='left',on=['runId'])
                        except Exception:
                            race_run=race_run_normalised   

                    except requests.HTTPError as http_err:
                        if http_err.response.status_code == 404:
                            break

                    except Exception as e:
                        print(f"Error {e}")
                        result_retries -= 1
                        if result_retries > 0:
                            time.sleep(sleep_time)
                        else:
                            break
                    
                    finally:
                        race_run.drop_duplicates(inplace=True)
                        race_run.to_csv(file_path, mode='a', header=header_param, index=False)
                        break

def collect_topaz_data(api_key,codes,start_date,end_date,datatype,number_of_retries,sleep_time):
    '''
    This function here combines our three previously defined functions into one neat function in the correct order of execution.
    As the data is written to csv files, we do not need to return anything at the end of the function. This also means that it is not necessary to define a variable as the output of a function
    '''
    date_range = generate_date_range(start_date,end_date)

    topaz_api = define_topaz_api(api_key)
    
    download_topaz_data(topaz_api,date_range,codes,datatype,number_of_retries,sleep_time)

collect_topaz_data(TOPAZ_API_KEY,JURISDICTION_CODES,start_date,end_date,'HISTORICAL',10,30)

```

## Leaderboard

Leaderboards will be published here throughout the competition

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

### What happens if a race is not run (abandoned) or is declared a no-race?

- That race will be excluded from scoring

### What happens if there is a scratching?

 - The runner will be removed and the remaining prices will be normalised so that the overround sums to 1

### What happens if there is a deadheat?

 - The result will be recorded as 1 divided by the number of winners

---

### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.
