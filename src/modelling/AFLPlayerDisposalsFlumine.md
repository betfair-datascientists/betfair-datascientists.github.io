# AFL Player Disposals Tutorial - Part 2

This article draws on the content from the [AFL Player Disposals Tutorial](https://betfair-datascientists.github.io/modelling/AFLPlayerDisposalsTutorial/). 
You will need a predictions file from that model to follow along with this betting tutorial.

Here we will take our predictions and then bet into the AFL Player Disposal Markets. 
These markets are loaded on the day of the match, and so if there is no AFL match starting today then there will likely be no markets up.

## Requirements

- A code editor with Python functionality (e.g. VS Code)
- Latest Python Version
- [Betfair API key](https://betfair-datascientists.github.io/api/apiappkey/) 

## The Code

```py title="Import Libraries and Load Predictions"

# Import basic libraries
import os
import csv
import sys
import logging
import json
import pandas as pd
from collections import OrderedDict
from datetime import datetime, timedelta

# Import Betfair-specific libraries
from flumine import Flumine, clients
from flumine import BaseStrategy 
from flumine.order.trade import Trade
from flumine.order.order import LimitOrder
from flumine.markets.market import Market
from flumine.controls.loggingcontrols import LoggingControl
from flumine.order.ordertype import OrderTypes
from flumine.utils import price_ticks_away
from flumine.worker import BackgroundWorker
from flumine.events.events import TerminationEvent
import betfairlightweight
from betfairlightweight.filters import streaming_market_filter
from betfairlightweight.resources import MarketBook

'''
First we need to import our predictions file that we previously generated and create a friendly data format for our strategy.
The key things required are:

    - Match date (this is only a check to ensure that the match date is today or in the future to avoid using old predictions)
    - Player Name as one string (this may require concatenation with a space in the middle) with any hyphens and apostrophes removed
    - Disposal Prediction

The file used for this will have the following columns:
    - match_date
    - player_first_name
    - player_last_name
    - disposals_prediction
'''

def load_predictions():
    # Load the csv file, ensuring we load the match_date in datetime format
    disposals_df = pd.read_csv('this_round_disposal_predictions.csv', parse_dates=['match_date'],dayfirst=True)
    # Create the full player name
    disposals_df['player_name'] = disposals_df['player_first_name'] + ' ' + disposals_df['player_last_name']
    # Remove hyphens and apostrophes
    disposals_df['player_name'] = disposals_df['player_name'].str.replace("-|'","")
    # Define a dictionary to fix known player name mapping issues
    names_fixes = {
        'Mitch Hinge':'Mitchell Hinge',
        'Harry Himmelberg':'Harrison Himmelberg'
    }
    disposals_df.replace(names_fixes,inplace=True)
    # Define today's date and keep only the rows for today's or future matches
    today = pd.Timestamp(datetime.now().date())
    disposals_df=disposals_df[disposals_df['match_date'] >= today]
    # Check if the dataframe is empty and exit the script if it is, else return the processed dataframe
    if disposals_df.empty:
        print('No future predictions available - Please check your data')
        sys.exit(1)
    else:
        disposals_df = disposals_df[['player_name','disposals_prediction']]
        return disposals_df

```

Now lets define our Flumine class

```py title="Load Flumine and define the class"

'''
This code block defines the API Client and accesses our credentials json file.
It is advisable to keep credentials seperate to any script to reduce the chances of old passwords locking your account
or having account credentials leaked if sharing this file.
'''
def bflw_trading():

    with open('credentials.json') as f:
        cred = json.load(f)
        username = cred['username']
        password = cred['password']
        app_key = cred['app_key']

    trading = betfairlightweight.APIClient(username, password, app_key=app_key)

    return trading

# This logs in to the API and allows us to read the markets
trading = bflw_trading()
client = clients.BetfairClient(trading, interactive_login=True, min_bet_validation = False)
framework = Flumine(client=client)

'''
This is where we set the logging level. If you are new to this or encountering issues with the program,
then set the level to INFO, otherwise this can be set to CRITICAL or FATAL
'''
logging.basicConfig(filename = 'player_disposals_bets.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


# Function to process the runner_books and generate our selection ids
def process_runner_books(runner_books):
    selection_ids = [runner_book.selection_id for runner_book in runner_books]

    df = pd.DataFrame({
        'selection_id': selection_ids,
    })
    return df.set_index('selection_id')

# Function to process the runner_catalogue to gather our selection names
def process_runner_catalogue(market: Market):

    runners_df = process_runner_books(market.market_catalogue.runners)

    for runner in market.market_catalogue.runners:
        runner_name = next((rd.runner_name for rd in market.market_catalogue.runners if rd.selection_id == runner.selection_id), None)
        runners_df.loc[runner.selection_id, 'runner_name'] = runner_name

    return runners_df

# Our Flumine class where we define our rules
class PlayerDisposalsBets(BaseStrategy):

    '''
    The __init__ function defines what the strategy should do when it first fires
    We define our external dataframe where we have loaded our player disposal predictions
    It is essential that we tie the dataframe to the class using a "self." definition
    We also define two empty lists here to use later
    '''
    def __init__(self, *args, disposals_df, **kwargs):
        super().__init__(*args, **kwargs)
        self.processed_selection_ids = []
        self.disposals_df = disposals_df
        self.markets_bet_into = {}

    def check_market_book(self, market: Market, market_book: MarketBook) -> bool:
        ''' 
        process_market_book only executed if this returns True.
        if True is not returned then the framework will skip to the next market
        '''
        if market.market_id in self.markets_bet_into:
            return False
        if market_book.status != "CLOSED" and market_book.inplay == False:
            return True

    def process_market_book(self, market: Market, market_book: MarketBook) -> None:

        # If there is less than 30 minutes before the match start and the market is a Most Disposals - Group market or a Most Disposals - H2H market
        if round(market.seconds_to_start, 0) < 3600 and 'Most Disposals' in market.market_catalogue.market_name:

            # Create a dataframe with all the selection_ids and runner_names from the market
            runners_df = process_runner_catalogue(market)

            '''
            For these markets the player names are the runner_names so we can easily join our predictions file
            We'll only join the selections contained in the current market, then we'll find which player we have predicted
            to have the highest disposals in the group/match-up using the rank function and back that selection
            '''
            afl_players_df = pd.merge(runners_df,self.disposals_df,how="left",left_on=['runner_name'],right_on=['player_name'])
            afl_players_df.index = runners_df.index
            # These parameters rank on disposals_predictions from highest to lowest, with equal predictions having the same rank
            afl_players_df['rank'] = afl_players_df['disposals_prediction'].rank(ascending=False,method='min')
            # Loop over each runner in the market
            for runner in market_book.runners:
                # Check runner isn't scratched and that first layer of back price exists
                if runner.status == "ACTIVE" and len(runner.ex.available_to_back) > 0:
                    # Set the rank and runner_name for each selection_id
                    rank = afl_players_df.loc[runner.selection_id, 'rank']
                    runner_name = runners_df.loc[runner.selection_id, 'runner_name']
                    # If the player is ranked first for the disposal prediction and we haven't yet placed a bet
                    if rank == 1:
                        # Create our ordered dictionary to store our order notes
                        notes = OrderedDict()
                        # Write our order notes
                        notes["selection"] = "Highest Disposals Prediction: " + str(runner_name)
                        trade = Trade(
                            market_id=market_book.market_id,
                            selection_id=runner.selection_id,
                            handicap=runner.handicap,
                            notes=notes,
                            strategy=self,
                        )
                        # Place a back bet at one tick below the best available back price with a size of 50/price rounded to .2dp
                        # This market is not BSP so "MARKET_ON_CLOSE" is not valid, and we don't want to keep inplay, so set to "LAPSE"
                        order = trade.create_order(
                            side="BACK",
                            order_type=LimitOrder(
                                price=runner.ex.available_to_back[0]['price'],
                                size=round(20 / runner.ex.available_to_back[0]['price'], 2),
                                persistence_type="LAPSE"
                            )
                        )
                        market.place_order(order)

            # Add the market to the list so we don't process it again
            self.markets_bet_into[market.market_id] = True

        # If there is less than 30 minutes before the match start and the market is a Player Disposals Line market
        elif round(market.seconds_to_start, 0) < 3600 and 'Player Disposals' in market.market_catalogue.market_name:

            # Create a dataframe with all the selection_ids and runner_names from the market
            runners_df = process_runner_catalogue(market)

            '''
            These markets have the player_name in the market_name rather than the runner_name so we'll need to split this up,
            and remove any hyphens or apostrophes to match our player names.
            We'll also need to parse the selection names, which are in the format 'Under 18.5 Disposals',
            to define which selection is over and which is under and exactly what the disposal line is. 
            '''
            # Split the market_name on ' - ' and keep the value to the right
            runners_df['player_name'] = market.market_catalogue.market_name.split(' - ', 1)[1]
            # Remove any - or ' in the player name
            runners_df['player_name'] = runners_df['player_name'].str.replace("-|'","")
            # Extract the string 'Over' or 'Under' from the runner_name
            runners_df['overUnder'] = runners_df['runner_name'].str.split(' ').str[0]
            # Extract 'XX.5 Disposals' from the runner_name by keeping the value to the right of the first space
            runners_df['disposals_market_line'] = runners_df['runner_name'].str.split(' ').str[1]
            # Extract the disposals_market_line by splitting on the space and keeping the left value, then transform to a float
            runners_df['disposals_market_line'] = runners_df['disposals_market_line'].str.split(' ').str[0].astype('float')
            # Merge the dataframes together on the player name
            afl_players_df = pd.merge(runners_df,self.disposals_df,how="left",on=['player_name'])
            afl_players_df.index = runners_df.index
            print(afl_players_df)
            # Calculate the difference between our line and the market line
            afl_players_df['prediction_differential'] = afl_players_df['disposals_prediction'] - afl_players_df['disposals_market_line']
            # Loop over each runner in the market ['Over XX.5 Disposals','Under XX.5 Disposals']
            for runner in market_book.runners:
                # Check runner isn't scratched and that first layer of back price exists
                if runner.status == "ACTIVE" and len(runner.ex.available_to_back) > 0:

                    # Set relevant variables according to our dataframe
                    disposal_prediction = afl_players_df.loc[runner.selection_id, 'disposals_prediction']
                    disposal_difference = afl_players_df.loc[runner.selection_id, 'prediction_differential']
                    over_under = afl_players_df.loc[runner.selection_id, 'overUnder']
                    player_name = afl_players_df.loc[runner.selection_id,'player_name']
                    market_line = afl_players_df.loc[runner.selection_id,'disposals_market_line']

                    if disposal_prediction > 12 and disposal_difference > 0 and over_under == 'Over':
                        # Place a back set if the selection is the Overs and our model has predicted higher than the line and we haven't bet previously
                        '''
                        If we decide to bet only on overs where we've predicted over the line by a minimum amount or offset,
                        then we would use:
                            disposal_difference > offset
                        rather than:
                            disposal_difference > 0
                        '''
                        # Create our ordered dictionary to store our order notes
                        notes = OrderedDict()
                        # Write our order notes
                        notes["selection"] = player_name + " Over " + str(market_line) + " Disposals"
                        trade = Trade(
                            market_id=market_book.market_id,
                            selection_id=runner.selection_id,
                            handicap=runner.handicap,
                            notes=notes,
                            strategy=self,
                        )
                        # Place a back bet at one tick below the best available back price with a size of 50/price rounded to .2dp
                        # This market is not BSP so "MARKET_ON_CLOSE" is not valid, and we don't want to keep inplay, so set to "LAPSE"
                        order = trade.create_order(
                            side="BACK",
                            order_type=LimitOrder(
                                price=1.01,
                                size=10,
                                persistence_type="LAPSE"
                            )
                        )
                        market.place_order(order)
                    
                    elif disposal_prediction > 12 and disposal_difference < 0 and over_under == 'Under':
                        # Place a back set if the selection is the Overs and our model has predicted higher than the line and we haven't bet previously
                        '''
                        If we decide to bet only on unders where we've predicted under the line by a minimum amount or offset,
                        then we would use:
                            disposal_difference < offset * -1
                        rather than:
                            disposal_difference < 0
                        '''
                        # Create our ordered dictionary to store our order notes
                        notes = OrderedDict()
                        # Write our order notes
                        notes["selection"] = player_name + " Under " + str(market_line) + " Disposals"
                        trade = Trade(
                            market_id=market_book.market_id,
                            selection_id=runner.selection_id,
                            handicap=runner.handicap,
                            notes=notes,
                            strategy=self,
                        )
                        # Place a back bet at one tick below the best available back price with a size of 50/price rounded to .2dp
                        # This market is not BSP so "MARKET_ON_CLOSE" is not valid, and we don't want to keep inplay, so set to "LAPSE"
                        order = trade.create_order(
                            side="BACK",
                            order_type=LimitOrder(
                                price=1.01,
                                size=10,
                                persistence_type="LAPSE"
                            )
                        )
                        market.place_order(order)

            # Add the market to the list so we don't process it again
            self.markets_bet_into[market.market_id] = True

```

Before we run our strategy we'll need to define how we handle our betting output, and inout a terminate function to stop betting once the round is over

```py title="Define the class and logging bets"

# Here we load our strategy including our disposal predictions from our model
'''
The parameters here where we set our maximum number of orders per selection and maximum exposure are in addition to
the checks input into the class using the markets_bet_into and processed_selection_ids lists. 
These redundancies are part of the swiss cheese model of safety put in place to protect our account balance
from being drained in the event of something odd happening.
'''
# Load and parse our predictions file
disposals_df = load_predictions()

# Define our class
disposals_strategy = PlayerDisposalsBets(
    market_filter=streaming_market_filter(event_type_ids=["61420"]), # Australian Rules,
    disposals_df=disposals_df,
    max_order_exposure= 100,
    max_trade_count=1,
    max_live_trade_count=1,
    max_selection_exposure=100)

# Add the strategy to our framework
framework.add_strategy(disposals_strategy)

'''
The lines below are where we define the logging for these markets.
We want to ensure that all our orders are written to a csv file using listClearedOrders
and our markets, inclusive of commission, are written to a csv file using listClearedMarkets
'''
logger = logging.getLogger(__name__)

# Define columns for cleared orders
CLEARED_ORDERS_FIELDNAMES = [
    "bet_id",
    "strategy_name",
    "market_id",
    "selection_id",
    "trade_id",
    "date_time_placed",
    "price",
    "price_matched",
    "size",
    "size_matched",
    "profit",
    "side",
    "elapsed_seconds_executable",
    "order_status",
    "market_note",
    "trade_notes",
    "order_notes",
]
# Define columns for cleared markets
CLEARED_MARKETS_FIELDNAMES = [
    "market_id",
    "bet_count",
    "profit",
    "commission"
]
# Define our logging class to add to our Flumine framework
class LiveLoggingControl(LoggingControl):
    NAME = "BACKTEST_LOGGING_CONTROL"

    def __init__(self, *args, **kwargs):
        super(LiveLoggingControl, self).__init__(*args, **kwargs)
        self._setup()

    def _setup(self):
        # Check to see if our logging files exist, if not then create them with headers
        if os.path.exists("player_disposals_cleared_orders.csv"):
            logging.info("Cleared Orders file exists")
        else:
            with open("player_disposals_cleared_orders.csv", "w") as m:
                csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=CLEARED_ORDERS_FIELDNAMES)
                csv_writer.writeheader()
        if os.path.exists("player_disposals_cleared_markets.csv"):
            logging.info("Cleared Markets file exists")
        else:
            with open("player_disposals_cleared_markets.csv", "w") as m:
                csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=CLEARED_MARKETS_FIELDNAMES)
                csv_writer.writeheader()

    def _process_cleared_orders_meta(self, event):
        # Write completed trades to the files once they are settled
        orders = event.event
        with open("player_disposals_cleared_orders.csv", "a") as m:
            for order in orders:
                if order.order_type.ORDER_TYPE == OrderTypes.LIMIT:
                    size = order.order_type.size
                else:
                    size = order.order_type.liability
                if order.order_type.ORDER_TYPE == OrderTypes.MARKET_ON_CLOSE:
                    price = None
                else:
                    price = order.order_type.price
                try:
                    order_data = {
                        "bet_id": order.bet_id,
                        "strategy_name": order.trade.strategy,
                        "market_id": order.market_id,
                        "selection_id": order.selection_id,
                        "trade_id": order.trade.id,
                        "date_time_placed": order.responses.date_time_placed,
                        "price": price,
                        "price_matched": order.average_price_matched,
                        "size": size,
                        "size_matched": order.size_matched,
                        "profit": 0 if not order.cleared_order else order.cleared_order.profit,
                        "side": order.side,
                        "elapsed_seconds_executable": order.elapsed_seconds_executable,
                        "order_status": order.status.value,
                        "market_note": order.trade.market_notes,
                        "trade_notes": order.trade.notes_str,
                        "order_notes": order.notes_str,
                    }
                    csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=CLEARED_ORDERS_FIELDNAMES)
                    csv_writer.writerow(order_data)
                except Exception as e:
                    logger.error(
                        "_process_cleared_orders_meta: %s" % e,
                        extra={"order": order, "error": e},
                    )

        logger.info("Orders updated", extra={"order_count": len(orders)})

    def _process_cleared_markets(self, event):
        # Write cleared markets to the files once they are settled
        cleared_markets = event.event
        with open("player_disposals_cleared_markets.csv","a") as m:
            for cleared_market in cleared_markets.orders:
                extra={
                    "market_id": cleared_market.market_id,
                    "bet_count": cleared_market.bet_count,
                    "profit": cleared_market.profit,
                    "commission": cleared_market.commission,
                }
                csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=CLEARED_MARKETS_FIELDNAMES)
                csv_writer.writerow(extra)

# Add the logging control to our framework
framework.add_logging_control(
    LiveLoggingControl()
)

'''
The below lines add a termination worker into our Flumine framework to check if there are available markets commencing in the next 4 days.
The worker will commence checking the markets one hour after the start and then every 30 minutes afterwards
'''
def terminate(
    # terminate the framework if all matches for the round are resulted
    context: dict, flumine, seconds_closed: int = 600) -> None:
    # create a list of markets from our framework
    markets = list(flumine.markets.markets.values())
    # add the market to a list if the market is starting in less than 4 days
    '''
    This method works for a standard Thursday-Sunday round, however other rounds may not.
    '''
    this_round_markets = [m for m in markets 
                          if m.market_start_datetime.date() <= datetime.datetime.now().date() + timedelta(days=4)
                          and (m.elapsed_seconds_closed is None or (m.elapsed_seconds_closed and m.elapsed_seconds_closed < seconds_closed))
    ]
    # check the length of this round's markets
    market_count = len(this_round_markets)
    # if there are no more markets beginning then terminate the strategy. 
    if market_count == 0:
        logger.info("No more markets available, terminating framework")
        flumine.handler_queue.put(TerminationEvent(flumine))

# add the worker to our framework.
framework.add_worker(
    BackgroundWorker(
        framework,
        terminate,
        func_kwargs={"seconds_closed" : 3600},
        interval = 1800,
        start_delay = 3600
    )
)


```

## Final Step

Running the below line of code will start the flumine instance and place real bets, so run this at your own risk

```py title="GO FLUMINE BOT"

framework.run()

```

### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.