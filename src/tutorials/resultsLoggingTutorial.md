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

**Note:** Read-only access to the live Betfair API is not allowed, so any results recording bot should be supplemented with betting activity to maintain live access

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
The opposing customer would then see a back bet available to take of $50 at a price of $10
The cross-matching engine could, in theory, offer this bet on the following equivalent selections within the same event:

| Market Type         | Selection            | Side | Price | Size  |
|---------------------|----------------------|------|-------|-------|
|CORRECT_SCORE        |0 - 0                 |BACK  |$10.00 |$50.00 |
|OVER_UNDER_05        |Over 0.5 Goals        |LAY   |$1.11  |$454.54|
|MATCH_ODDS_AND_BTTS  |Draw/No               |BACK  |$10.00 |$50.00 |

These prices and stakes are calculated as **1 / (1 - 1 / (Price))** with the price then rounded down to the nearest tick for back and up for lay

This logic covers all 2 selection markets like Over/Under markets, but **how is it calculated for markets of 3 or more selections?**
As the number of runners increase in a market, the calculations become more complex but the cross-matching does help in closing the gap between back and lay prices

Let's consider a racing win market with 5 runners

| Runner | BATB | Prob  |100%-SUM_OTHER_RUNNERS|XM Unrounded|XM Rounded|
|--------|------|-------|----------------------|------------|----------|
|1       |$7.00 |14.28% |13.49%                |$7.41       |$7.50     |
|2       |$9.20 |10.87% |10.08%                |$9.92       |$10.00    |
|3       |$2.50 |40.00% |39.21%                |$2.55       |$2.56     |
|2       |$3.90 |25.64% |24.85%                |$4.02       |$4.10     |
|3       |$10.00|10.00% |9.21%                 |$10.86      |$11.00    |

The column indicates how much market percentage is remaining if you took the current best available back prices for each runner excluding the current runner.
Using the fact that backing all other runners is the same as laying just one, the cross-matcher is able to calculate the price to offer on that one runner.

In the event that someone takes the cross-matcher price, then the cross-matcher would take all other back bets to ensure an even position. Obviously it can only offer
valid Betfair ticks, so it will round up the prices where it is backing (a lay bet for someone else to take) and round down lay bets. If someone were to take one of the back
bets available, then the cross matcher price would be invalid and then recalculated.

By default, Flumine does not return the cross-matching bets (also called virtual bets) so we must explicitly call it. These bets are available to take, so it makes sense to call them.
To do this we call **"EX_BEST_OFFERS_DISP"** in the streaming_market_data_filter

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

Placing information is not something that can be easily inferred from the Betfair API as the runner status only returns whether a runner (or runner/handicap combination) is a winner in a specific market
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

 - 'OTHER_PLACE' refers to alternate place markets with a differing number of winners from the main place market. (BSP may not be offered on these markets)
 - Both Exacta and Quinella markets are used as redundancies in case one is present and not the other, or 'Any Other Result' is the result of one of them

The logic used to infer placings is as follows (assuming all markets are present and settled):

 - 4th Place = 'WINNER' in 4TBP market and 'LOSER' in 3TBP market
 - 3rd Place = 'WINNER' in 3TBP market and 'LOSER' in 2TBP market OR cloth number not part of winning selection in Quinella/Exacta market
 - 2nd Place = ('WINNER' in 2TBP market or cloth number part of winning selection in Quinella/Exacta market) and 'LOSER' in WIN market
 - 1st Place = 'WINNER' in Win Market

It can occur that the 2nd and 3rd place runners' order cannot be determined due to the 2TBP not being offered or the Quinella/Exacta markets being voided/not offered or 'Any Other Result' being the winning selection in those markets.
In these instances we will define the result as 'P' instead of the numerical value. This is common for Harness markets and 'OTHER_PLACE' is not commonly offered and no exotics are normally offered.

## racing_logger.py

Now let's outline our custom flumine class. While this code could be refactored further, keeping the process_market_book function as flat as possible enables better readability.