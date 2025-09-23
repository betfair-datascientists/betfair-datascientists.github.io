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
|CORRECT_SCORE        |0 - 0                 |BACK  |$1.11   |$454.54|
|OVER_UNDER_05        |Under 0.5 Goals        |BACK  |$1.11   |$454.54|
|MATCH_ODDS_AND_BTTS  |Draw/No               |BACK  |$1.11   |$454.54|

These prices and stakes are calculated as **1 / (1 - 1 / (Price))** with the price then rounded down to the nearest tick 