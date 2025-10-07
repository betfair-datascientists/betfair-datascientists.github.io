A common struggle shared by many a user of Betfair is how to build a database of results from the Betfair Exchange.

There are many different sources of data available, each with its own limitations and lag times.
These sources include:

 - [Daily CSV Files](https://promo.betfair.com/betfairsp/prices) 
 - [Monthly CSV Blocks](https://betfair-datascientists.github.io/data/dataListing/)
 - [Hub Results Graphical UI](https://www.betfair.com.au/hub/racing/horse-racing/racing-results/)
 - [Historical Stream Files](https://historicdata.betfair.com/#/mydata)

However, as is often said, the most accurate and valuable source of data that you can use for modelling is data that you collect yourself.
Collecting your own data ensures that data leakage is excluded from your database, as is always a danger when using someone else's data.

The challenge with collecting your own data is, of course, patience. And the fewer events that take place for your chosen sport or racing code, the longer you need to wait to collect a meaningful data set.
Greyhound Racing, sometimes with 150+ Australian races per day, won't take long, maybe 3 months, to collect a meaningful dataset, whereas Thoroughbred racing might be 12 months, and sport data even longer.
And for events like the Olympics, well you'll need to have the patience of a saint.

There goes a saying of unknown origin that states **"The best time to plant a tree is twenty years ago. The second best time is now."**
Well let's look at how we plant the seed of building a database of recordings from the Betfair Streaming and Polling APIs as well as a template for sending alerts to an external service like Discord

!!! info "Read-Only"
    Read-only access to the live Betfair API is not allowed, so any results recording bot should be supplemented with betting activity to maintain live access

## Coding Principles

As I'm sure many self-taught coders started out, my early python code consisted of one long script with less than 5 defined functions. This code tended to be a nightmare to maintain, debug and little to no reusability or compartmentalisation. Thankfully, I'm now older and (somewhat) wiser, and I've learned some basic principles of coding that have helped to make code more logical and maintainable.

**"Write your code as though the person who has to maintain it is a violent psychopath who knows where you live (and that someone might be you)" - Unknown**

Here's a short list of tips to improve the quality of your code

 - Break your code into functions — each function should do one clear job.
 - Use meaningful names for variables and functions so the code explains itself.
 - Add comments for “why”, not “what” (the code should show what it’s doing).
 - Keep your code consistent in style (indentation, naming, spacing).
 - Test your code in small pieces and use print/logging to trace issues.
 - Where possible, utilise multiple files to reduce the number of lines in each file

This tutorial will be written utilising the flumine python wrapper and using the Visual Studio Code IDE

## Structure

This bot is setup with 5 files to reduce the size of each file:

 - main.py
 - utils.py
 - placing_helpers.py
 - racing_logger.py
 - discord_helper.py

We'll run the main.py file only, and it will import all the other files to assist the process. You could further compartmentalise this to have a config.py file and only ever need to change that file.

The live API key being used to run this bot has a market subscription limit of 1000 for the streaming API, if you need an increased limit please email automation@betfair.com.au (upon application)

## Main.py

```py title="main.py"

# Import Libraries
from flumine import Flumine, clients
from betfairlightweight.filters import streaming_market_filter
from betfairlightweight.filters import streaming_market_data_filter
import logging

# Import Flumine Class and Util
from racing_logger import RacingLogger
from utils import bflw_trading

logging.basicConfig(filename = 'results_logger.log', level=logging.CRITICAL, format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    # Credentials to login and logging in 
    trading = bflw_trading()
    client = clients.BetfairClient(trading, interactive_login=True) # Not using certificates

    # Define the framework
    framework = Flumine(client=client)

    # Define the flumine strategy
    market_monitoring = RacingLogger(
        market_filter=streaming_market_filter(
            event_type_ids=["4339"], # Greyhound Markets
            market_types=['WIN','PLACE','EXACTA','QUINELLA','FORECAST','REV_FORECAST'],
        ),
        market_data_filter=streaming_market_data_filter(fields=[
        "EX_BEST_OFFERS_DISP", # This imports cross-matching or virtual bets
        "EX_TRADED",
        "EX_TRADED_VOL",
        "EX_LTP",
        "EX_MARKET_DEF",
        "SP_TRADED",
        "SP_PROJECTED"], ladder_levels=3),
        streaming_timeout = 1,
    )

    framework.add_strategy(market_monitoring)

    framework.run()

```

## Cross-Matching

Cross-matching bets are bets automatically placed by an engine within the Betfair infrastructure to extend the reach of bets being offered on the Exchange.

An example of this would be a customer offering a lay bet to lose $50 at a price of $10 on the outcome "Under 0.5 Goals" in the market type "OVER_UNDER_05" for a soccer match.
The opposing customer would then see a back bet available to take of $50 at a price of $10. 
The cross-matching engine could, in theory, offer this bet on the following equivalent selections within the same event:

| Market Type         | Selection            | Side | Price | Size  |
|---------------------|----------------------|------|-------|-------|
|CORRECT_SCORE        |0 - 0                 |BACK  |$10.00 |$50.00 |
|OVER_UNDER_05        |Over 0.5 Goals        |LAY   |$1.11  |$454.54|
|MATCH_ODDS_AND_BTTS  |Draw/No               |BACK  |$10.00 |$50.00 |

These prices and stakes are calculated as **1 / (1 - 1 / (Price))** with the price then rounded down to the nearest tick for back and up for lay.

This logic covers all 2 selection markets like Over/Under markets, but **how is it calculated for markets of 3 or more selections?**.
As the number of runners increase in a market, the calculations become more complex but the cross-matching does help in closing the gap between back and lay prices.

Let's consider a racing win market with 5 runners.

| Runner | BATB | Prob  |100%-SUM_OTHER_RUNNERS|XM Unrounded Lay|XM Rounded Lay|
|--------|------|-------|----------------------|----------------|--------------|
|1       |$7.00 |14.28% |13.49%                |$7.41           |$7.50         |
|2       |$9.20 |10.87% |10.08%                |$9.92           |$10.00        |
|3       |$2.50 |40.00% |39.21%                |$2.55           |$2.56         |
|2       |$3.90 |25.64% |24.85%                |$4.02           |$4.10         |
|3       |$10.00|10.00% |9.21%                 |$10.86          |$11.00        |

The column **100%-SUM_OTHER_RUNNERS** indicates how much market percentage is remaining if you took the current best available back prices for each runner excluding the current runner.
Using the fact that backing all other runners is the same as laying just one, the cross-matcher is able to calculate the price to offer on that one runner.

In the event that someone takes the cross-matcher price, then the cross-matcher would take all other back bets to ensure an even position. Obviously it can only offer
valid Betfair ticks, so it will round up the prices where it is backing (a lay bet for someone else to take) and round down lay bets. If someone were to take one of the back
bets available, then the cross matcher price would be invalid and then recalculated.

By default, Flumine does not return the cross-matching bets (also called virtual bets) so we must explicitly call it. These bets are available to take, so it makes sense to call them.
To do this we call **"EX_BEST_OFFERS_DISP"** in the streaming_market_data_filter.

## utils.py

'Utils' is a common name for a file where helper functions are defined. These are functions used multiple times and compartmentalising them in another .py file improves readability of the main code.

```py title='utils.py'

import json
import betfairlightweight
import pandas as pd

'''
This function defines our API login credentials
We are using the interactive login which doesn't use certificates
'''

def bflw_trading():

    with open('credentials.json') as f:
        cred = json.load(f)
        username = cred['username']
        password = cred['password']
        app_key = cred['app_key']

    # Define the betfairlightweight client
    trading = betfairlightweight.APIClient(username, password, app_key=app_key)

    return trading

'''
This function here is used with our Discord webhook
We can decide which channel to send the notification to if we want separate out different codes and countries
'''

def pick_webhook(sport_name,race_type,event_country):

    if sport_name == 'Greyhound Racing':
        return 'Greyhounds'
    elif sport_name == 'Horse Racing' and event_country not in ['AU','NZ']:
        return 'ROW Horse Racing'
    elif sport_name == 'Horse Racing' and event_country in ['AU','NZ'] and race_type != 'Harness':
        return 'ANZ Thoroughbred Racing'
    elif sport_name == 'Horse Racing' and event_country in ['AU'] and race_type == 'Harness':
        return 'AUS Harness Racing'
    else:
        return

'''
This function is used to fetch the runner metadata from the runner catalogue
We use the line m.get to gracefully retrieve data from the metadata dictionary
This method does not raise an error where a default value is set

e.g. m.get('CLOTH_NUMBER', None) will set CLOTH_NUMBER to None if it does not exist

It's good practice to collect as much data as possible here, as the data generally doesn't persist
'''

def process_runner_catalogue(runner_catalogue):

    rows = []

    for r in runner_catalogue:

        m = r.metadata
        runner_name = getattr(r, 'runner_name', None)

        cloth_number = m.get('CLOTH_NUMBER', None)
        if cloth_number is None and runner_name:
            cloth_number = runner_name.split('.')[0]

        row = {
            'selection_id': r.selection_id,
            'runner_name': runner_name,
            'runner_id' : m.get('runnerId', None),
            'stall_draw': m.get('STALL_DRAW', None),
            'cloth_number': cloth_number,
            'cloth_number_alpha': m.get('CLOTH_NUMBER_ALPHA', None),
            'official_rating': m.get('OFFICIAL_RATING', None),
            'forecast_price': int(m.get('FORECASTPRICE_NUMERATOR') or 0) / int(m.get('FORECASTPRICE_DEMONINATOR') or 1),
            'jockey_name': m.get('JOCKEY_NAME', None),
            'jockey_claim': m.get('JOCKEY_CLAIM', None),
            'trainer_name': m.get('TRAINER_NAME', None),
            'owner_name': m.get('OWNER_NAME', None),
            'form': m.get('FORM', None),
            'weight_carried': m.get('WEIGHT_VALUE', None),
            'weight_value': m.get('WEIGHT_UNITS', None),
            'days_since_last_run': m.get('DAYS_SINCE_LAST_RUN', None),
            'wearing': m.get('WEARING', None),
            'sex_type': m.get('SEX_TYPE', None),
            'age': m.get('AGE', None),
            'bred': m.get('BRED', None),
            'colour_type': m.get('COLOUR_TYPE', None),
            'dam_year_born': m.get('DAM_YEAR_BORN', None),
            'dam_name': m.get('DAM_NAME', None),
            'dam_bred': m.get('DAM_BRED', None),
            'damsire_year_born': m.get('DAMSIRE_YEAR_BORN', None),
            'damsire_name': m.get('DAMSIRE_NAME', None),
            'damsire_bred': m.get('DAMSIRE_BRED', None),
            'sire_year_born': m.get('SIRE_YEAR_BORN', None),
            'sire_name': m.get('SIRE_NAME', None),
            'sire_bred': m.get('SIRE_BRED', None),
        }

        rows.append(row)

    return pd.DataFrame(rows)

'''
This function may not make a whole of sense now but it's useful in our clean-up
'''

def clean_dataframe_dict_if_all_settled(dataframe_dict,market_groups,key):
    """
    Checks if all non-None market_ids in self.market_groups[key] are settled.
    If so, removes corresponding entries from self.dataframe_dict.
    """
    try:
        group = market_groups.get(key)
        if not group:
            return

        # Step 1–2: Get all _id keys with non-None values
        active_ids = [v for k, v in group.items() if k.endswith('_id') and v is not None]

        # Step 3: Get all _settled keys with value True
        settled_flags = [v for k, v in group.items() if k.endswith('_settled') and v is True]

        # Step 4: Check if counts match
        if len(active_ids) == len(settled_flags):
            # Step 5: Remove corresponding entries from self.dataframe_dict
            for market_id in active_ids:
                try:
                    if market_id in dataframe_dict:
                        del dataframe_dict[market_id]
                except Exception:
                    return
    except Exception:
        return

'''
This helper function helps us to group markets together in a dictionary based on the number of winners.
More information about why we use this dictionary can be found in the next section
'''
    
def set_market_id(market_groups, key, market_type, number_of_winners, market_id):

    if market_type == 'WIN':
        market_groups[key]['win_market_id'] = market_id
    elif market_type in ['PLACE', 'OTHER_PLACE']:
        tbp_key = f"{number_of_winners}tbp_market_id"
        if number_of_winners in [2, 3, 4]:
            market_groups[key][tbp_key] = market_id
    elif market_type in ['EXACTA', 'FORECAST']:
        market_groups[key]['exacta_market_id'] = market_id
    elif market_type in ['QUINELLA', 'REV_FORECAST']:
        market_groups[key]['quinella_market_id'] = market_id

```

### Inferring placings from market results

**"How do I figure out what position a runner finished in the race?"**

Placing information is not something that can be easily inferred from the Betfair API as the runner status only returns whether a runner (or runner/handicap combination) is a winner in a specific market.
While it is possible to get placing info from another source, this can be time consuming and/or costly. So I'll explain how we can do this with the Betfair API and you can decide for yourself whether the resulting information is complete enough for your use case.

An Event ID for a race meeting will cover all markets offered on a race card for all races. This is helpful but not quite enough. All markets concerned with a single race will have a unique event ID / market start time combination. To utilise this information we will set our key for the race to be the set of these two variables, and we'll work to define which markets will help to infer which places.

The dictionary will be in the format:

```
market_groups[key] = {'win_market_id': market_type == 'WIN',
                      '2tbp_market_id': market_type in ['PLACE','OTHER_PLACE'] and number_of_winners == 2,
                      '3tbp_market_id': market_type in ['PLACE','OTHER_PLACE'] and number_of_winners == 3,
                      '4tbp_market_id': market_type in ['PLACE','OTHER_PLACE'] and number_of_winners == 4,
                      'quinella_market_id': market_type in ['QUINELLA','REV_FORECAST'],
                      'exacta_market_id': market_type in ['EXACTA','FORECAST']
                      }
```
Not every race will have all of these markets, but we will use the data we do have to great effect.

Notes:

 - 'OTHER_PLACE' refers to alternate place markets with a differing number of winners from the main place market. (BSP may not be offered on these markets).
 - Both Exacta and Quinella markets are used as redundancies in case one is present and not the other, or 'Any Other Result' is the result of one of them.

The logic used to infer placings is as follows (assuming all markets are present and settled):

 - 4th Place = 'WINNER' in 4TBP market and 'LOSER' in 3TBP market
 - 3rd Place = 'WINNER' in 3TBP market and 'LOSER' in 2TBP market OR cloth number not part of winning selection in Quinella/Exacta market
 - 2nd Place = ('WINNER' in 2TBP market or cloth number part of winning selection in Quinella/Exacta market) and 'LOSER' in WIN market
 - 1st Place = 'WINNER' in Win Market

It can occur that the 2nd and 3rd place runners' order cannot be determined due to the 2TBP not being offered or the Quinella/Exacta markets being voided/not offered or 'Any Other Result' being the winning selection in those markets.
In these instances we will define the result as 'P' instead of the numerical value. This is common for Harness markets where 'OTHER_PLACE' is not commonly offered and no exotics are normally offered.

## racing_logger.py

Now let's outline our custom flumine class. While this code could be refactored further, keeping the process_market_book function as flat as possible enables better readability.

```py title="Imports and Global Variables"

# Import libraries
from flumine import BaseStrategy 
from flumine.markets.market import Market
from betfairlightweight.resources import MarketBook
from datetime import datetime, timezone
import pytz
import pandas as pd
import os

# Import custom functions
from placing_helpers import save_with_placings, save_market_csv, determine_placings, merge_place_into_win
from discord_helpers import discord_placings_report, run_all_discord_alerts, send_market_void_alert
from utils import process_runner_catalogue, clean_dataframe_dict_if_all_settled, set_market_id, pick_webhook

# Set Global Variables
DISCORD_ALERTS_WEBHOOK = 'INSERT WEBHOOK URL'

DISCORD_WEBHOOKS = {
    'ANZ Thoroughbred Racing':'INSERT WEBHOOK URL',
    'AUS Harness Racing':'INSERT WEBHOOK URL',
    'ROW Horse Racing':'INSERT WEBHOOK URL',
    'Greyhounds':'INSERT WEBHOOK URL'
    }

MARKET_TYPES = ['win', '2tbp', '3tbp', '4tbp', 'exacta', 'quinella']

# Columns for Metadata CSV Files
METADATA_COLUMNS = [
    'event_name',
    'event_date_local',
    'event_timezone',
    'event_country',
    'event_id',
    'track',
    'market_id',
    'market_name',
    'market_time',
    'selection_id',
    'runner_name',
    'runner_id',
    'stall_draw',
    'cloth_number',
    'cloth_number_alpha',
    'official_rating',
    'forecast_price',
    'jockey_name',
    'jockey_claim',
    'trainer_name',
    'owner_name',
    'form',
    'weight_carried',
    'weight_value',
    'days_since_last_run',
    'wearing',
    'sex_type',
    'age',
    'bred',
    'colour_type',
    'dam_year_born',
    'dam_name',
    'dam_bred',
    'damsire_year_born',
    'damsire_name',
    'damsire_bred',
    'sire_year_born',
    'sire_name',
    'sire_bred']

# Columns for CSV Output Files
MARKET_COLUMNS = [
    'sport_id',
    'sport_name',
    'event_date_local',
    'event_timezone',
    'event_country',
    'event_name',
    'event_id',
    'track',
    'market_id',
    'market_name',
    'total_runners',
    'number_of_winners',
    'clarifications',
    'market_base_rate',
    'market_time',
    'inplay_time_local',
    'market_type',
    'race_type',
    'selection_id',
    'cloth_number',
    'runner_name',
    'runner_status',
    'runner_removal_date',
    'runner_adjustment_factor',
    'runner_traded_before_scheduled_off',
    'runner_max_price_traded_before_scheduled_off',
    'runner_min_price_traded_before_scheduled_off',
    'runner_wap_traded_before_scheduled_off',
    'runner_ltp_at_scheduled_off',
    'runner_batb_at_scheduled_off',
    'runner_batl_at_scheduled_off',
    'runner_sp_back_available_at_scheduled_off',
    'runner_sp_lay_available_at_scheduled_off',
    'runner_spf_at_scheduled_off',
    'runner_spn_at_scheduled_off',
    'runner_bsp',
    'runner_sp_traded',
    'runner_traded_volume_total',
    'runner_max_price_total',
    'runner_min_price_total',
    'runner_wap_traded_total',
    'runner_final_traded_price'
]

```

So we've defined everything, now lets launch straight into the flumine class. There are four main flumine base methods that we will customise in this bot:

 - __init___
 - check_market_book
 - process_market_book
 - process_closed_market

```py title="Custom Flumine Class"

class RacingLogger(BaseStrategy):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._market_expiration = self.context.get("market_expiration", 3600) # Increases the default time
        self.market_info_gathered = {} # Logging which markets we have gathered the initial info (including metadata)
        self.scheduled_off_info_gathered = {} # Logging Markets at the scheduled start time
        self.bsp_info_gathered = {} # Logging BSP reconciliation
        self.final_volume_info_gathered = {} # Logging final traded volume info
        self.market_results = {} # Logging closed markets
        self.dataframe_dict = {} # Holding dataframes in memory
        self.market_groups = {} # Grouping markets together
        self.win_markets_written = {} # Logging markets written to the CSV Files

        '''
        The reason we log all these completed items is to prevent processes being run repeatedly and 
        potentially causing KeyErrors further down the line
        '''

    def check_market_book(self, market: Market, market_book: MarketBook) -> bool:
        ''' 
        Flumine has a default worker to fetch the market catalogue as it needs to call the polling API.
        This means that it will run for the first minute or so with no market_catalogue.
        Pausing until the market_catalogue is not None removes a host of errors
        '''
        if market.market_catalogue is None: 
            return False
        elif market.race_type == 'Harness' and market.country_code == 'NZ': # BSP is not offered on NZ Harness
            return False
        elif market.market_id in self.market_results:
            return False
        else:
            return True
        
    def process_market_book(self, market: Market, market_book: MarketBook) -> None:

        if market.seconds_to_start < 300:

            # Pull dataframe or initialise dataframe for this market
            market_dataframe = self.dataframe_dict.setdefault(market.market_id, pd.DataFrame())

            # Define key for this race
            key = (market.event_id, market.market_start_datetime)

            if key not in self.market_groups:

                self.market_groups[key] = {
                    'event_id': market.event_id,
                    'market_time': market.market_start_datetime,
                    'win_market_id': None,
                    '2tbp_market_id': None,
                    '3tbp_market_id': None,
                    '4tbp_market_id': None,
                    'exacta_market_id': None,
                    'quinella_market_id': None,
                    'win_settled': False,
                    '2tbp_settled': False,
                    '3tbp_settled': False,
                    '4tbp_settled': False,
                    'exacta_settled': False,
                    'quinella_settled': False,
                }
                
            set_market_id(self.market_groups, key, market.market_type, market_book.number_of_winners, market.market_id)

            # --- BASIC MARKET INFO ---
            if market.market_id not in self.market_info_gathered:
                
                # --- Event Info ---
                event_data = {
                    'sport_id': market.market_catalogue.event_type.id,
                    'sport_name': market.market_catalogue.event_type.name,
                    'event_date': market.market_catalogue.event.open_date,
                    'event_name' : market.market_catalogue.event.name,
                    'event_timezone': market.market_catalogue.event.time_zone,
                    'event_date_local': pytz.utc.localize(market.market_catalogue.event.open_date).astimezone(pytz.timezone(market.market_catalogue.event.time_zone)).replace(tzinfo=None).strftime("%d-%m-%y %H:%M:%S"),
                    'event_country': market.market_catalogue.event.country_code,
                    'event_id': market.market_catalogue.event.id,
                    'track': market.market_catalogue.event.venue if market.market_catalogue.event.venue else market.market_catalogue.event.name.split(r' (')[0],
                }

                # --- Market Info ---
                market_data = {
                    'market_id': market_book.market_id,
                    'market_name': market.market_catalogue.market_name,
                    'total_runners': market_book.number_of_runners,
                    'number_of_winners': market_book.number_of_winners,
                    'runners_voidable': market_book.runners_voidable,
                    'bsp_market': market.market_catalogue.description.bsp_market,
                    'clarifications': market.market_catalogue.description.clarifications if market.market_catalogue.description.clarifications else None,
                    'market_base_rate': market.market_catalogue.description.market_base_rate,
                    'market_time': pytz.utc.localize(market.market_catalogue.market_start_time).astimezone(pytz.timezone(market.market_catalogue.event.time_zone)).replace(tzinfo=None).strftime("%d-%m-%y %H:%M:%S"),
                    'market_type': market.market_catalogue.description.market_type,
                    'inplay_market': market.market_catalogue.description.turn_in_play_enabled,
                    'race_type': market.market_catalogue.description.race_type if market.market_catalogue.description.race_type else None,
                }

                # Combine event and market info into a one-row DataFrame
                event_market_df = pd.DataFrame([{**event_data, **market_data}])

                # Process runners
                runners_df = process_runner_catalogue(market.market_catalogue.runners)

                # Broadcast the event/market info across all runners (same length as runners_df)
                repeated_info_df = pd.concat([event_market_df]*len(runners_df), ignore_index=True)

                # Concatenate horizontally
                market_dataframe = pd.concat([repeated_info_df, runners_df.reset_index(drop=True)], axis=1)

                # Extract values (only one expected)
                country_code = market_dataframe['event_country'].iloc[0]
                today_str = datetime.today().strftime('%Y-%m-%d')

                # This safely avoids Key Errors
                for col in METADATA_COLUMNS:
                    if col not in market_dataframe.columns:
                        market_dataframe[col] = None

                # Define and write metadata dataframe (Metadata only available for Throughbred Racing)
                if market.event_type_id == '7' and market.market_catalogue.description.race_type != 'Harness' and market.market_type == 'WIN':

                    metadata_dataframe = market_dataframe[METADATA_COLUMNS]

                    metadata_filename = f"metadata-{country_code}-{today_str}.csv"
                    file_exists = os.path.isfile(metadata_filename)

                    metadata_dataframe.to_csv(
                        metadata_filename,
                        mode='a',
                        index=False,
                        header=not file_exists
                    )
                    print(f"Saved Runner Metadata Info for {market.venue} - {market.market_catalogue.market_name}")

                self.market_info_gathered[market.market_id] = True
                self.dataframe_dict[market.market_id] = market_dataframe
                print(f"Added Market Data for {market.venue} - {market.market_catalogue.market_name}")

        # --- MARKET_BOOK INFO AT SCHEDULED OFF TIME ---
        if market.market_id not in self.scheduled_off_info_gathered and (market.seconds_to_start < 0 or market_book.bsp_reconciled == True):

            runners_at_scheduled_off = []

            for runner in market_book.runners:

                runner_data = {
                    'selection_id': runner.selection_id,
                    'runner_removal_date': (pytz.utc.localize(runner.removal_date).astimezone(pytz.timezone(market.market_catalogue.event.time_zone)).replace(tzinfo=None).strftime("%d-%m-%y %H:%M:%S") if runner.removal_date else None),
                    'runner_adjustment_factor': round(runner.adjustment_factor, 2) if runner.adjustment_factor is not None else None,
                    'runner_traded_before_scheduled_off': sum(ps['size'] for ps in runner.ex.traded_volume) if runner.ex.traded_volume else 0,
                    'runner_max_price_traded_before_scheduled_off': max(ps['price'] for ps in runner.ex.traded_volume) if runner.ex.traded_volume else None,
                    'runner_min_price_traded_before_scheduled_off': min(ps['price'] for ps in runner.ex.traded_volume) if runner.ex.traded_volume else None,
                    'runner_wap_traded_before_scheduled_off': (
                        round(
                            sum(ps['price'] * ps['size'] for ps in runner.ex.traded_volume if ps['price'] is not None and ps['size'] is not None) /
                            sum(ps['size'] for ps in runner.ex.traded_volume if ps['size'] is not None),
                            2
                        )
                        if runner.ex.traded_volume and sum(ps['size'] for ps in runner.ex.traded_volume if ps['size'] is not None) > 0
                        else None
                    ),
                    'runner_ltp_at_scheduled_off': runner.last_price_traded or None,
                    'runner_batb_at_scheduled_off': [(o['price'], o['size']) for o in runner.ex.available_to_back] if runner.ex.available_to_back else None,
                    'runner_batl_at_scheduled_off': [(o['price'], o['size']) for o in runner.ex.available_to_lay] if runner.ex.available_to_lay else None,
                    'runner_sp_back_available_at_scheduled_off': sum(ps['size'] for ps in runner.sp.back_stake_taken) if runner.sp.back_stake_taken else 0,
                    'runner_sp_lay_available_at_scheduled_off': sum(ps['size'] for ps in runner.sp.lay_liability_taken) if runner.sp.lay_liability_taken else 0,
                    'runner_spf_at_scheduled_off': runner.sp.far_price or None,
                    'runner_spn_at_scheduled_off': runner.sp.near_price or None
                }
                runners_at_scheduled_off.append(runner_data)
            
            runners_at_scheduled_off_df = pd.DataFrame(runners_at_scheduled_off)
            market_dataframe = pd.merge(market_dataframe,runners_at_scheduled_off_df, how="left",on=['selection_id'],suffixes=['','_x'])

            # Set dict to true and reassign dataframe
            self.scheduled_off_info_gathered[market.market_id] = True
            self.dataframe_dict[market.market_id] = market_dataframe
            print(f"Added Market Book Info at Scheduled Off for {market.venue} - {market.market_catalogue.market_name}")

        # --- BSP RECONCILIATION INFO ---
        if market.market_id not in self.bsp_info_gathered and market_book.bsp_reconciled == True:

            bsp_reconciled = []

            for runner in market_book.runners:

                runner_data = {
                    'selection_id': runner.selection_id,
                    'inplay_time_local': datetime.now(pytz.timezone(market.market_catalogue.event.time_zone)).strftime("%Y-%m-%d %H:%M:%S"),
                    'runner_bsp': round(runner.sp.actual_sp, 2) if runner.sp.actual_sp is not None else None,
                    'runner_sp_traded': runner.sp.back_stake_taken[0]['size'] if runner.sp.back_stake_taken else None
                }
                bsp_reconciled.append(runner_data)
            
            bsp_reconciled_df = pd.DataFrame(bsp_reconciled)
            market_dataframe = pd.merge(market_dataframe,bsp_reconciled_df,how="left",on=['selection_id'],suffixes=['','_x'])

            # Set dict to true and reassign dataframe
            self.bsp_info_gathered[market.market_id] = True
            self.dataframe_dict[market.market_id] = market_dataframe
            print(f"Added BSP Info for {market.venue} - {market.market_catalogue.market_name}")

        # --- MARKET_BOOK INFO AT SUSPENSION BEFORE MARKET CLOSURE
        if (market.market_id not in self.final_volume_info_gathered and 
            market_book.status == 'SUSPENDED' and 
            ((market_book.bsp_reconciled == True and market_book.inplay == True) or 
            (market_book.bsp_reconciled == True and market.market_catalogue.description.turn_in_play_enabled == False) or 
            (market_book.inplay == True and market.market_catalogue.description.bsp_market == False) or 
            (market.market_catalogue.description.turn_in_play_enabled == False and market.market_catalogue.description.bsp_market == False))):
        
        '''
        This set of conditions is rather convoluted but is designed as an exhaustive list of conditions that indicate that no further bets can be placed on a market
        For this, the market must be suspended AND:

         - Market has BSP reconciled and is inplay; OR
         - Market has BSP reconciled and does not go inplay; OR
         - Market does not offer BSP and is inplay: OR
         - Market does not offer BSP and does not go inplay
        '''
                
            final_pricing_info = []

            for runner in market_book.runners:

                runner_data = {
                    'selection_id': runner.selection_id,
                    'runner_traded_volume_total': sum(ps['size'] for ps in runner.ex.traded_volume) if runner.ex.traded_volume else None,
                    'runner_max_price_total': max(ps['price'] for ps in runner.ex.traded_volume) if runner.ex.traded_volume else None,
                    'runner_min_price_total': min(ps['price'] for ps in runner.ex.traded_volume) if runner.ex.traded_volume else None,
                    'runner_wap_traded_total': (
                        round(
                            sum(ps['price'] * ps['size'] for ps in runner.ex.traded_volume if ps['price'] is not None and ps['size'] is not None)
                            / sum(ps['size'] for ps in runner.ex.traded_volume if ps['size'] is not None), 2
                        )
                        if runner.ex.traded_volume and sum(ps['size'] for ps in runner.ex.traded_volume if ps['size'] is not None) > 0
                        else None
                    ),
                    'runner_final_traded_price': runner.last_price_traded or None
                }
                final_pricing_info.append(runner_data)
            
            final_pricing_info_df = pd.DataFrame(final_pricing_info)
            market_dataframe = pd.merge(market_dataframe,final_pricing_info_df,how="left",on=['selection_id'],suffixes=['','_x'])

            # Set dict to true and reassign dataframe
            self.final_volume_info_gathered[market.market_id] = True
            self.dataframe_dict[market.market_id] = market_dataframe

            print(f"Added Final Market Book Info for {market.venue} - {market.market_catalogue.market_name}")

    '''
    The process_closed_market function is a base method in flumine that is usually very short.
    However, we will customise it to record the market results and send our notifications to Discord

    The order of market settlement is not uniform, so there are checks in place to handle for any order of market settlement
    Not all markets are required to deduce a placing either, we will wait until the minimum number of markets have been settled
    before logging the results and sending the Discord alert
    '''

    def process_closed_market(self, market: Market, market_book: MarketBook):
        
        key = (market.event_id, market.market_start_datetime)
        self.market_groups.setdefault(key, {})

        if not market.market_catalogue:
            self.market_results[market.market_id] = True
            return super().process_closed_market(market, market_book)
        
        # Flag market type as settled
        market_type = market.market_type
        num_winners = market_book.number_of_winners

        # Check if market is voided first
        if all(r.status == "REMOVED" for r in market_book.runners):
            send_market_void_alert(market, market_book, DISCORD_ALERTS_WEBHOOK)
            print(f"Market voided for {market.event_name} - {market.market_id}. Alert sent.")
            # Be warned that if an entire meeting is abandoned, then a notification will be sent for every market for the event

            # If the market is voided, we will set this market to None in our grouping function
            # This means that we won't wait for the market to be settled before logging results
            # Usually this will occur for Exactas/Quinellas in the case of a late scratching
            if market_type == 'WIN':
                self.market_groups[key]['win_market_id'] = None
            elif market_type in ['PLACE', 'OTHER_PLACE']:
                self.market_groups[key][f'{num_winners}tbp_market_id'] = None
            elif market_type in ['FORECAST', 'EXACTA']:
                self.market_groups[key]['exacta_market_id'] = None
            elif market_type in ['REV_FORECAST', 'QUINELLA']:
                self.market_groups[key]['quinella_market_id'] = None
            return

        # Fetch market dataframe and skip if the market is empty
        market_dataframe = self.dataframe_dict.get(market.market_id)
        if market_dataframe is None or market_dataframe.empty:
            print(f"No data available for {market.event_name} - {market.market_id}. Skipping.")
            # This usually only occurs on start-up 
            return

        # Here we note which market type in the race group is settled
        if market_type == 'WIN':
            self.market_groups[key]['win_settled'] = True
        elif market_type in ['PLACE', 'OTHER_PLACE']:
            if num_winners == 2:
                self.market_groups[key]['2tbp_settled'] = True
            elif num_winners == 3:
                self.market_groups[key]['3tbp_settled'] = True
            elif num_winners == 4:
                self.market_groups[key]['4tbp_settled'] = True
        elif market_type in ['EXACTA', 'FORECAST']:
            self.market_groups[key]['exacta_settled'] = True
        elif market_type in ['QUINELLA', 'REV_FORECAST']:
            self.market_groups[key]['quinella_settled'] = True

        # Add runner status
        runner_status_map = {r.selection_id: r.status for r in market_book.runners}
        market_dataframe["runner_status"] = market_dataframe["selection_id"].map(runner_status_map)
        print(f"[{market.market_id}] Added runner status for {market.venue} - {market.market_catalogue.market_name}")

        # Remap Removal Date for Late Scratchings
        removal_date_map = {
        r.selection_id: (pytz.utc.localize(r.removal_date).astimezone(pytz.timezone(market.market_catalogue.event.time_zone)).replace(tzinfo=None).strftime("%d-%m-%y %H:%M:%S") if r.removal_date else None) for r in market_book.runners}
        market_dataframe["runner_removal_date"] = market_dataframe["selection_id"].map(removal_date_map)
        print(f"[{market.market_id}] Processed any late scratchings for {market.venue} - {market.market_catalogue.market_name}")

        # Prepare output
        country_code = market_dataframe['event_country'].iloc[0]
        market_type_code = market_dataframe['market_type'].iloc[0]
        today_str = pd.to_datetime(market_dataframe['event_date'].iloc[0]).strftime('%Y-%m-%d')
        filename = f"results-{country_code}-{market_type_code}-{today_str}.csv"

        # Ensure that all the correct columns are in the dataframe to prevent key errors
        for col in MARKET_COLUMNS:
            if col not in market_dataframe.columns:
                market_dataframe[col] = None
        
        # Reorder the dataframe (and remove any double-up columns)
        final_market_dataframe = market_dataframe[MARKET_COLUMNS]

        # This can be triggered in the case of resettlements or other issues
        time_since_start = (datetime.now(timezone.utc).replace(tzinfo=None) - market.market_start_datetime)
        if time_since_start.total_seconds() > 3000:
            save_market_csv(final_market_dataframe, filename, os.path.isfile(filename), MARKET_COLUMNS)
            print(f"[{market.market_id}] Over 50m. Saved basic info for {market.venue}")

        # Now attempt to get placings
        # This where the magic happens, the whole function will be displayed further down
        try:
            placings_df = determine_placings(
                market=market,
                market_groups=self.market_groups,
                dataframe_dict=self.dataframe_dict,
                market_types=MARKET_TYPES
            )
        except Exception as e:
            print(f"[{market.market_id}] Error determining placings: {e}")
            placings_df = None

        file_exists = os.path.isfile(filename)

        # Placings not available yet
        if placings_df is None or placings_df.empty:
            if market_type == 'WIN':
                # For WIN market with no placings, skip writing entirely
                print(f"[{market.market_id}] WIN market placings not ready. Skipping write for {market.venue}")
            else:
                # Non-WIN market with no placings: save basic market info
                save_market_csv(final_market_dataframe, filename, file_exists, MARKET_COLUMNS)
                print(f"[{market.market_id}] Placings unavailable or empty. Saved basic info for {market.venue}")

        else:
            # Placings available
            if market_type == 'WIN':
                final_market_dataframe = merge_place_into_win(self.market_groups, self.dataframe_dict, key, final_market_dataframe)
                # WIN market: save with placings, send alerts
                win_market_df = save_with_placings(final_market_dataframe, placings_df, filename, file_exists, MARKET_COLUMNS, extra_cols=['placing','places_paid','place_bsp'])
                print(f"[{market.market_id}] Saved WIN market info with placings for {market.venue}")

                run_all_discord_alerts(win_market_df, DISCORD_ALERTS_WEBHOOK)
                discord_placings_report(
                    win_market_df,
                    DISCORD_WEBHOOKS[
                        pick_webhook(
                            market.market_catalogue.event_type.name,
                            market.race_type,
                            market.market_catalogue.event.country_code
                        )
                    ]
                )
                self.win_markets_written[market.market_id] = True

            else:
                # Non-WIN market: check if WIN placings have been written
                win_market_id = self.market_groups[key].get('win_market_id')

                if (win_market_id not in self.win_markets_written
                    and win_market_id in self.market_results):
                    
                    win_filename = f"results-{country_code}-WIN-{today_str}.csv"
                    win_file_exists = os.path.isfile(win_filename)

                    win_market_df = merge_place_into_win(self.market_groups, self.dataframe_dict, key, self.dataframe_dict[win_market_id])

                    win_market_df = save_with_placings(
                        win_market_df,
                        placings_df,
                        win_filename,
                        win_file_exists,
                        MARKET_COLUMNS,
                        extra_cols=['placing','place_BSP']
                    )
                    save_market_csv(final_market_dataframe, filename, file_exists, MARKET_COLUMNS)
                    print(f"[{market.market_id}] Saved WIN market with placings and {market_type} for {market.venue}")
                    self.win_markets_written[win_market_id] = True

                    run_all_discord_alerts(win_market_df, DISCORD_ALERTS_WEBHOOK)
                    discord_placings_report(
                        win_market_df,
                        DISCORD_WEBHOOKS[
                            pick_webhook(
                                market.market_catalogue.event_type.name,
                                market.race_type,
                                market.market_catalogue.event.country_code
                            )
                        ]
                    )
                    self.win_markets_written[market.market_id] = True

                else:
                    # Either WIN market already written or win_market_id not ready
                    save_market_csv(final_market_dataframe, filename, file_exists, MARKET_COLUMNS)
                    print(f"[{market.market_id}] Saved basic non-WIN info for {market_type} at {market.venue}")

        # Mark market as processed and clean up
        self.market_results[market.market_id] = True
        # If every market for the race has been settled and written, then we erase the data from the class context
        clean_dataframe_dict_if_all_settled(self.dataframe_dict, self.market_groups, key)
        return super().process_closed_market(market, market_book)

```

Wow, that was a lot of code. Hopefully you're still with me!

As mentioned earlier, the code could be further compartmentalised but, for a tutorial, I felt it better to leave the detail here for improved reader comprehension.

So, our custom flumine class will:

 - Read and store market info and runner metadata (where applicable)
 - Read and store market_book info at the scheduled off
 - Read and store BSP info when the BSP has been reconciled
 - Read and store final market_book info upon final market suspension before closure
 - Read and store final market results
 - Combine all relevant data before writing to csv
 - Infer placings based on related market settlements
 - send an alert to our chosen Discord channels

There were a lot of functions in there which still haven't been shown. These belong to our placing_helpers.py and discord_helpers.py.
Let's outline these

## placing_helpers.py

```py title="Placing Helper Functions"

import re
import pandas as pd
from flumine.markets.market import Market

def get_market_ids(key, market_groups, market_types):
    """Safely retrieve market IDs from market_groups for the given key and market_types."""
    market_ids = {}
    market_group = market_groups.get(key, {})
    
    for mtype in market_types:
        market_ids[mtype] = market_group.get(f"{mtype}_market_id")
    
    return market_ids

def get_place_dataframe(market_groups, dataframe_dict, key):
    """
    Returns the place dataframe for a given market group key.
    Looks for 2TBP first, then 3TBP, and returns the first where market_type = 'PLACE'.
    """
    mg = market_groups.get(key, {})

    for tbp_key in ['2tbp_market_id', '3tbp_market_id']:
        market_id = mg.get(tbp_key)
        if not market_id:
            continue

        df = dataframe_dict.get(market_id)
        if df is not None and 'market_type' in df.columns:
            if (df['market_type'] == 'PLACE').any():
                return df

    return None  # No suitable dataframe found

def merge_place_into_win(market_groups, dataframe_dict, key, win_market_df):
    """
    Fetches the place dataframe (2TBP or 3TBP), keeps only selection_id and runner_bsp,
    renames runner_bsp to place_bsp, and merges into win_market_df on selection_id.
    """
    place_df = get_place_dataframe(market_groups, dataframe_dict, key)
    
    if place_df is None:
        print(f"No valid place dataframe found for market group {key}")
        return win_market_df

    # Keep only necessary columns and rename
    place_df_subset = place_df[['selection_id', 'number_of_winners', 'runner_bsp']].rename(columns={'runner_bsp': 'place_bsp','number_of_winners':'places_paid'})

    # Merge on selection_id, avoiding duplication
    merged_df = win_market_df.merge(place_df_subset, on='selection_id', how='left')

    return merged_df

def check_market_settlements(key, market_groups, market_ids):
    """
    This function returns a boolean value only
    """
    mg = market_groups.get(key, {})

    # TBP markets
    for tbp in ['4tbp', '3tbp', '2tbp']:
        if market_ids.get(tbp) and not mg.get(f"{tbp}_settled", False):
            print(f"{tbp.upper()} market not yet settled")
            return False

    # Special case: No 2TBP and exotics not settled
    if not market_ids.get('2tbp'):
        exotics_settled = True
        for exotic in ['exacta', 'quinella']:
            if market_ids.get(exotic):
                if not mg.get(f'{exotic}_settled', False):
                    exotics_settled = False
                    break
        if not exotics_settled:
            print("No 2TBP market and Exotics not yet settled")
            return False

    # WIN market
    if market_ids.get('win') and not mg.get('win_settled', False):
        print("WIN market not yet settled")
        return False

    return True  # All checks passed

def get_winners(df):
    # Function returns winners from the market
    if df is None or df.empty:
        return pd.DataFrame(columns=df.columns if df is not None else [])

    return df[df['runner_status'] == 'WINNER']

def assign_placing(placing_dict, cloth_numbers, place):

    for c in cloth_numbers:
        if placing_dict.get(c) is None:
            placing_dict[c] = place

def assign_first_place(placing_dict, dataframe_dict, market_id):
    
    df = dataframe_dict.get(market_id)
    winners = get_winners(df)
    assign_placing(placing_dict, winners['cloth_number'], '1')

def assign_second_place_tbp(placing_dict, dataframe_dict, market_id):

    df = dataframe_dict.get(market_id)
    winners = get_winners(df)

    for _, row in winners.iterrows():
        c = row['cloth_number']
        if placing_dict.get(c) != '1':
            placing_dict[c] = '2'
    return not winners.empty

def assign_second_place_exotics(placing_dict, dataframe_dict, exacta_id, quinella_id):

    # Exacta
    exacta_df = dataframe_dict.get(exacta_id)
    if exacta_df is not None:
        exf_winners = get_winners(exacta_df)
        if not exf_winners.empty:
            runner_name = exf_winners['runner_name'].iloc[0]
            if runner_name != "Any Other Result":
                try:
                    number_1, number_2 = re.search(r'(\d+)\s*-\s*(\d+)', runner_name).groups()
                    placing_dict[number_2] = '2'
                except Exception:
                    pass

    # Quinella
    quinella_df = dataframe_dict.get(quinella_id)
    if quinella_df is not None:
        quin_winners = get_winners(quinella_df)
        if not quin_winners.empty:
            runner_name = quin_winners['runner_name'].iloc[0]
            if runner_name != "Any Other Result":
                try:
                    matches = re.findall(r'(\d+)\s*-\s*(\d+)', runner_name)
                    for number_1, number_2 in matches:
                        if placing_dict.get(number_1) == '1' and placing_dict.get(number_2) != '1':
                            placing_dict[number_2] = '2'
                        elif placing_dict.get(number_2) == '1' and placing_dict.get(number_1) != '1':
                            placing_dict[number_1] = '2'
                        elif placing_dict.get(number_1) != '1' and placing_dict.get(number_2) != '1':
                            placing_dict[number_1] = '2'
                            placing_dict[number_2] = '2'
                except Exception:
                    pass

def assign_place(placing_dict, dataframe_dict, market_id, place, depend_on=None):
    """
    This function assigns places to each runner with the possible combinations being:
     - 1 / 2 (No 3TBP market)
     - 1 / 2 / 3 (3TBP market and either 2TBP market or at least one Exotics Market settled not as 'Any Other Result')
     - 1 / P / P (3TBP market and no 2TBP market and no Exotics Market settled not as 'Any Other Result')
     - 1 / 2 / 3 / 4 (4TBP/3TBP market and either 2TBP market or at least one Exotics Market settled not as 'Any Other Result')
     - 1 / P / P / 4 (4TBP/3TBP market and no 2TBP market and no Exotics Market settled not as 'Any Other Result')
    """

    df = dataframe_dict.get(market_id)
    winners = get_winners(df)
    if winners.empty:
        return

    used = set(placing_dict.keys())
    unknowns = [c for c in winners['cloth_number'] if c not in used]

    if not unknowns:
        return

    # Normal dependent logic
    if depend_on and all(p in placing_dict.values() for p in depend_on):
        placing_dict[unknowns[0]] = str(place)

    # Special case for 4th place with "P"
    elif place == 4 and depend_on:
        # Count how many Ps are already assigned
        ps_assigned = [k for k, v in placing_dict.items() if v == "P"]

        if len(ps_assigned) == 2 and "1" in placing_dict.values():
            # Only one unknown remains in 4TBP → must be 4th
            if len(unknowns) == 1:
                placing_dict[unknowns[0]] = "4"
                return

        # Fall back to generic "P" assignment if still ambiguous
        assign_placing(placing_dict, unknowns, "P")
    else:
        assign_placing(placing_dict, unknowns, "P")

def save_market_csv(df, filename, file_exists, market_columns):
    """Append market dataframe to CSV ensuring columns from market_columns exist.
    Also include 'placing' if it exists in df.
    """
    # Make a copy of market_columns to avoid modifying original list
    cols_to_write = list(market_columns)

    # If 'placing' exists in the dataframe but is not in market_columns, append it
    if 'placing' in df.columns and 'placing' not in cols_to_write:
        cols_to_write.append('placing')

    # Add missing columns with None
    for col in cols_to_write:
        if col not in df.columns:
            df[col] = None

    # Reorder columns
    df = df.reindex(columns=cols_to_write)

    # Save
    df.to_csv(filename, mode='a', index=False, header=not file_exists)

def save_with_placings(base_df, placings_df, filename, file_exists, market_columns, extra_cols=None):
    """Merge placings into base_df, add missing cols, save to CSV."""
    merged_df = base_df.merge(
        placings_df, on=['market_id', 'cloth_number'], how='left', suffixes=['', '_x']
    )
    if extra_cols:
        for col in extra_cols:
            if col not in merged_df.columns:
                merged_df[col] = None
    save_market_csv(merged_df, filename, file_exists, market_columns)

    return merged_df

def determine_placings(market: Market, market_groups, dataframe_dict, market_types):

    key = (market.event_id, market.market_start_datetime)
    print(market_groups[key])
    market_ids = get_market_ids(key, market_groups, market_types)

    if not check_market_settlements(key, market_groups, market_ids):
        return

    placing_dict = {}

    assign_first_place(placing_dict, dataframe_dict, market_ids.get('win'))

    # Assign 2nd place from 2TBP; if none, fallback to exotics
    two_tbp_assigned = assign_second_place_tbp(placing_dict, dataframe_dict, market_ids.get('2tbp'))

    if not two_tbp_assigned:
        assign_second_place_exotics(
            placing_dict,
            dataframe_dict,
            market_ids.get('exacta'),
            market_ids.get('quinella'),
        )

    # Assign 3rd place
    assign_place(placing_dict, dataframe_dict, market_ids.get('3tbp'), place=3, depend_on=['2'])

    # Assign 4th place
    assign_place(placing_dict, dataframe_dict, market_ids.get('4tbp'), place=4, depend_on=['2', '3'])

    placing_df = pd.DataFrame.from_dict(placing_dict, orient='index', columns=['placing']).reset_index()

    placing_df.rename(columns={'index': 'cloth_number'}, inplace=True)
    placing_df['market_id'] = market_ids.get('win')

    placing_df = placing_df[['market_id', 'cloth_number', 'placing']]

    return placing_df

```

## discord_helpers.py

Now if you didn't want to send messages to a Discord or other location, this next section can be disregarded (and some other function references higher up will need to be removed)

This code will send formatted text blocks to your chosen Discord channel. Other formats are possible.
The text blocks are optimised for viewing on Desktop and will overflow when viewed on the mobile app.

We've outlined the race results that we want to send but we also want some other alerts for scratchings, voided markets and other interesting things

 - **Longshot Winners** (WIN market winner has a BSP over $50)
 - **Short Priced Losers** (WIN market loser has a BSP under $1.50)
 - **Sick Beat** (WIN market loser has a min price matched less than $1.10)
 - **Victory Snatcher** (WIN market winner has a BSP under $50 and trades at over $100 inplay)
 - **Dead Heat** (More than 1 winner in WIN market)
 - **Short Price Scramble** (More than 2 runners trade under $1.50 or more than 3 trade under $2)
 - **Super Crunchy** (Runner implied win probability improved by more than 10% between scheduled off and BSP)
 - **Set Adrift** (Runner implied win probability worsened by more than 10% between scheduled off and BSP)
 - **Late Scratching** (Runner scratched in last 10 minutes before race or after race)
 - **Voided Market** (Market settled with all runners having status *REMOVED*)

!!! info "Set Adrift"
    The Set Adrift alert for a Harness race will usually indicate a runner galloping in the score-up!
    
```py title="Discord Helpers"

from betfairlightweight.resources import MarketBook
from flumine.baseflumine import Market
import pandas as pd
import requests
from datetime import datetime
import pytz

def send_discord_message(message: str, discord_webhook_url):
    payload = {"content": message}

    try:
        response = requests.post(discord_webhook_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message to Discord: {e}")

def format_row_message(row, prefix, include_bsp=True, include_ltp=False, extra_fields=None):
    """
    Format a message line for a runner.
    """
    # Market-level details
    market_details = (
        f"{row['sport_name']} - ({row['event_country']}) {row['track']} - "
        f"{row['market_name']} - {row['market_time']}"
    )

    # Runner-level details
    runner_parts = [f"{row['runner_name']}"]

    if include_bsp:
        runner_parts.append(f"BSP: {safe_round(row.get('runner_bsp'))}")
    if include_ltp:
        runner_parts.append(f"LTP: {safe_round(row.get('runner_ltp_at_scheduled_off'))}")

    if extra_fields:
        for field, label in extra_fields.items():
            runner_parts.append(f"{label}: {safe_round(row.get(field))}")

    runner_details = " ".join(runner_parts)

    return f"{prefix}\n{market_details}\n{runner_details}"

def safe_round(value, places=2):
    """Round if numeric, otherwise return as string."""
    try:
        if isinstance(value, (int, float)):
            return round(value, places)
        return value  # leave strings and others untouched
    except Exception:
        return value

def wrap_code_block(message):
    """Wrap a message in a Discord code block."""
    return f"```\n{message}\n```"

def alert_longshot(df, webhook):
    if not df.empty:
        row = df.iloc[0]
        msg = format_row_message(row,
                                "LONGSHOT WINNER ALERT",
                                extra_fields={'runner_status': 'Result'})
        send_discord_message(wrap_code_block(msg), webhook)

def alert_fave_soils_the_bed(df, webhook):
    if not df.empty:
        row = df.iloc[0]
        msg = format_row_message(row,
                                "NOT SO SURE THING ALERT",
                                extra_fields={'runner_status': 'Result'})
        send_discord_message(wrap_code_block(msg), webhook)

def alert_short_priced_losers(df, webhook):
    if not df.empty:
        messages = [
            format_row_message(
                row, "SICK BEAT ALERT", include_bsp=True, 
                extra_fields={'runner_min_price_total': 'Min Price',
                              'runner_status': 'Result'}
            )
            for _, row in df.iterrows()
        ]
        final_msg = "\n".join(messages)
        send_discord_message(wrap_code_block(final_msg), webhook)

def alert_multiple_shorties(cond_a_df, cond_b_df, webhook):
    """
    Trigger alert if more than 3 runners from cond_a_df OR more than 2 from cond_b_df.
    Merges the two sets, removes duplicates safely, and sends Discord alert.
    """
    if len(cond_a_df) > 3 or len(cond_b_df) > 2:
        # Combine the two dataframes
        combined = pd.concat([cond_a_df, cond_b_df], ignore_index=True)

        # Drop duplicates based only on key runner identifiers
        id_cols = ['sport_name', 'event_country', 'track', 'market_name', 'runner_name']
        qualifying = combined.drop_duplicates(subset=id_cols)

        if qualifying.empty:
            return

        # Use the first row for market-level details
        first_row = qualifying.iloc[0]
        header = (
            f"SHORT PRICE SCRAMBLE ALERT\n"
            f"{first_row['sport_name']} - ({first_row['event_country']}) {first_row['track']} - "
            f"{first_row['market_name']} - {first_row['market_time']}"
        )

        # Build runner lines only
        runner_lines = []
        for _, row in qualifying.iterrows():
            runner_lines.append(
                f"{row['runner_name']} "
                f"(BSP: {safe_round(row.get('runner_bsp'))}) "
                f"(Min Price: {safe_round(row.get('runner_min_price_total'))}) "
                f"Status: {row['runner_status']}"
            )

        # Combine into one message
        final_msg = header + "\n" + "\n".join(runner_lines)

        send_discord_message(wrap_code_block(final_msg), webhook)

def alert_traders_dream(df, webhook):
    if not df.empty:
        row = df.iloc[0]
        extra = {
            'runner_max_price_total': 'Max Price',
            'runner_max_price_traded_before_scheduled_off': 'Max Pre-Off',
            'runner_status': 'Result'
        }
        msg = format_row_message(row, "VICTORY SNATCHER ALERT", extra_fields=extra)
        send_discord_message(wrap_code_block(msg), webhook)

def alert_deadheat(df, webhook):
    if len(df) > 1:
        base_info = df.iloc[0]
        winners = ", ".join([
            f"{row['runner_name']} (BSP: {round(row['runner_bsp'], 2)})"
            for _, row in df.iterrows()
        ])
        message = (
            f"DEAD HEAT ALERT\n"
            f"{base_info['sport_name']} - ({base_info['event_country']}) {base_info['track']} - "
            f"{base_info['market_name']} {base_info['market_time']}\n"
            f"Winners: {winners}"
        )
        send_discord_message(wrap_code_block(message), webhook)

def alert_super_crunchy(df, webhook):
    if not df.empty:
        for _, row in df.iterrows():
            msg = format_row_message(row,
                                    "SUPER CRUNCHY ALERT",
                                    include_ltp=True,
                                    extra_fields={'runner_status': 'Result'})
            send_discord_message(wrap_code_block(msg), webhook)

def alert_set_adrift(df, webhook):
    if not df.empty:
        for _, row in df.iterrows():
            msg = format_row_message(row,
                                    "SET ADRIFT ALERT",
                                    include_ltp=True,
                                    extra_fields={'runner_status': 'Result'})
            send_discord_message(wrap_code_block(msg), webhook)

def alert_late_scratchings(df, webhook):
    """
    Send an alert for late scratchings.
    Includes removal time and whether the scratching was before or after the race.
    """
    if not df.empty:
        for _, row in df.iterrows():
            # Determine before/after relative to race start
            if pd.to_datetime(row['runner_removal_date'],format="%Y-%m-%d %H:%M:%S",errors='coerce') <= pd.to_datetime(row['inplay_time_local'],format="%Y-%m-%d %H:%M:%S",errors='coerce'):
                timing = "Before Race"
            else:
                timing = "After Race"

            msg = (
                format_row_message(
                    row,
                    "LATE SCRATCHING ALERT",
                    include_bsp=False,
                    include_ltp=False,
                    extra_fields={
                        'runner_removal_date': 'Removal Time',
                        'runner_status': 'Result'
                    }
                )
                + f" ({timing})"
            )

            send_discord_message(wrap_code_block(msg), webhook)

def run_all_discord_alerts(df, discord_webhook_url):
    try:
        longshot_df = df[(df['runner_bsp'] >= 50) & (df['runner_status'] == 'WINNER')]
        losing_fave_df = df[(df['runner_bsp'] < 1.5) & (df['runner_status'] == 'LOSER')]
        short_priced_losers_df = df[(df['runner_min_price_total'] <= 1.1) & (df['runner_status'] == 'LOSER')]
        cond_a_df = df[df['runner_min_price_total'] < 2]
        cond_b_df = df[df['runner_min_price_total'] < 1.5]
        traders_dream_df = df[
            (df['runner_max_price_total'] > 100) &
            (df['runner_max_price_total'] > df['runner_max_price_traded_before_scheduled_off']) &
            (df['runner_bsp'] < 50) &
            (df['runner_status'] == 'WINNER')
        ]
        winners_df = df[df['runner_status'] == 'WINNER']
        super_crunchy_df = df[(1 / df['runner_bsp'] - 1 / df['runner_ltp_at_scheduled_off']) > 0.1]
        set_adrift_df = df[(1 / df['runner_bsp'] - 1 / df['runner_ltp_at_scheduled_off']) < -0.1]

        # Force both columns to datetime
        df['runner_removal_date'] = pd.to_datetime(df['runner_removal_date'],format="%Y-%m-%d %H:%M:%S",errors='coerce')
        df['inplay_time_local'] = pd.to_datetime(df['inplay_time_local'],format="%Y-%m-%d %H:%M:%S",errors='coerce')

        # Filter rows where conversion succeeded and runner was removed
        late_scratchings_df = df[
            (df['runner_status'] == 'REMOVED') &
            df['runner_removal_date'].notna() &
            df['inplay_time_local'].notna()
        ]

        # Filter for removals within 10 minutes of the race
        late_scratchings_df = late_scratchings_df[
            (late_scratchings_df['inplay_time_local'] - late_scratchings_df['runner_removal_date']).abs()
            .dt.total_seconds().div(60) <= 10
        ]

        alert_longshot(longshot_df, discord_webhook_url)
        alert_fave_soils_the_bed(losing_fave_df, discord_webhook_url)
        alert_short_priced_losers(short_priced_losers_df, discord_webhook_url)
        alert_multiple_shorties(cond_a_df, cond_b_df, discord_webhook_url)
        alert_traders_dream(traders_dream_df, discord_webhook_url)
        alert_deadheat(winners_df, discord_webhook_url)
        alert_super_crunchy(super_crunchy_df, discord_webhook_url)
        alert_set_adrift(set_adrift_df, discord_webhook_url)
        alert_late_scratchings(late_scratchings_df, discord_webhook_url)

    except Exception as e:
        print(f"Error running alerts: {e}")

def discord_placings_report(df, discord_webhook_url):
    try:
        if df.empty:
            return

        placed = df.copy()

        # Define custom order for placing
        placing_order = ['1', '2', '3', 'P', '4']
        placed['placing_str'] = placed['placing'].fillna("").astype(str)

        # Sorting based on placing order
        placed['placing_sort'] = placed['placing_str'].apply(
            lambda x: placing_order.index(x) if x in placing_order else 999
        )

        # Flag SCR runners
        placed['is_scr'] = placed['runner_bsp'].isna()

        # Sort so non-SCR first, then SCR, then by placing_sort
        placed_sorted = placed.sort_values(by=['is_scr', 'placing_sort', 'runner_name'])

        # Market info
        market_info_full = format_row_message(
            placed_sorted.iloc[0],
            prefix="",
            include_bsp=False,
            include_ltp=False
        )

        runner_name_first = placed_sorted.iloc[0]['runner_name']
        if runner_name_first in market_info_full:
            market_info = market_info_full.rsplit(runner_name_first, 1)[0].strip()
        else:
            market_info = market_info_full

        # ===== Dynamic column widths =====
        place_width = max(len("Place"), max(len(str(p)) for p in placed_sorted['placing_str']))
        
        bsp_width = max(
            len("W_BSP"),
            max(
                len(f"${b:.2f}") if pd.notna(b) else len("SCR")
                for b in placed_sorted['runner_bsp']
            )
        )

        place_bsp_width = max(
            len("P_BSP"),
            max(
                len(f"${pb:.2f}") if pd.notna(pb) else len("")
                for pb in placed_sorted['place_bsp']
            )
        )

        runner_width = max(
            len("Runner"),
            max(
                len(r[:30]) + (len(f" — {rd}") if pd.isna(b) else 0)
                for r, b, pb, rd in zip(
                    placed_sorted['runner_name'],
                    placed_sorted['runner_bsp'],
                    placed_sorted['place_bsp'],
                    placed_sorted['runner_removal_date']
                )
            )
        )

        # ===== Build header & rows =====
        lines = [market_info, ""]

        # Add Actual Start Time & Places Paid line
        inplay_time_val = placed_sorted.iloc[0].get("inplay_time_local", "")
        if pd.notna(inplay_time_val):
            inplay_time = pd.to_datetime(inplay_time_val).strftime("%H:%M:%S")
        else:
            inplay_time = ""

        places_paid = str(placed_sorted.iloc[0].get("places_paid", ""))
        lines.append(f"Actual Start Time: {inplay_time} | Places Paid: {places_paid}")
        lines.append("")

        header = f"{'Place':<{place_width}} | {'W_BSP':>{bsp_width}} | {'P_BSP':>{place_bsp_width}} | {'Runner':<{runner_width}}"
        lines.append(header)

        for _, row in placed_sorted.iterrows():
            place = f"{row['placing_str']:<{place_width}}" if pd.notna(row['placing_str']) else ""

            # W_BSP
            if row['runner_status'] == 'REMOVED' or pd.isna(row['runner_bsp']):
                bsp = "SCR"
            else:
                bsp = f"${row['runner_bsp']:.2f}"

            # P_BSP
            if row['runner_status'] == 'REMOVED':
                place_bsp = "SCR"
            elif pd.notna(row['place_bsp']):
                place_bsp = f"${row['place_bsp']:.2f}"
            else:
                place_bsp = ""   # handle PLACE markets with no BSP

            bsp = f"{bsp:>{bsp_width}}"
            place_bsp = f"{place_bsp:>{place_bsp_width}}"

            runner = row['runner_name'][:30]
            if pd.isna(row['runner_bsp']) and pd.notna(row['runner_removal_date']):
                runner += f" — {row['runner_removal_date']}"
            runner = f"{runner:<{runner_width}}"

            lines.append(f"{place} | {bsp} | {place_bsp} | {runner}")

        # ===== Send to Discord in monospaced block =====
        if len(lines) > 3:
            message = "```" + "\n".join(lines) + "```"
            send_discord_message(message, discord_webhook_url)

    except Exception as e:
        print(e)
        pass

def send_market_void_alert(market: Market, market_book: MarketBook, webhook_url):
    """
    Sends a Discord alert if all runners in a market are removed (market voided).
    """
    if market.event_name is None:
        return

    msg = (
        f"⚠️ MARKET VOIDED ⚠️\n"
        f"{market.event_name} (Event ID:{market.event_id}) - {market.market_catalogue.event_type.name}\n"
        f"{market.market_catalogue.market_name} - {market.market_id}\n"
        f"Market Time: {pytz.UTC.localize(market.market_start_datetime).astimezone(pytz.timezone('Australia/Sydney')).strftime('%Y-%m-%d %H:%M:%S %Z')} | "
        f"Voided: {datetime.now(pytz.timezone("Australia/Sydney")).strftime("%Y-%m-%d %H:%M:%S %Z")}"
    )

    send_discord_message(wrap_code_block(msg), webhook_url)

```

This concludes the tutorial on logging results to csv files and using Discord to place alerts for resulted markets.
This logic and functionality could further be expanded to:

 - Alerts for Firmers and Drifters in live markets
 - Alerts for large unmatched bets being placed into live markets
 - Alerts for runners with large implied probability differences to publicly available models like the Betfair Prediction Models

If you have any questions please reach out to automation@betfair.com.au to discuss!

### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.

