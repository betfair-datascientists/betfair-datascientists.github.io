# How to Automate 5

---
!!! note "Before you start"

    This tutorial follows on from our [How to Automate series](../how_to_automate_1.ipynb) which stepped through how to create a trading bot for a few different strategies. Make sure you take a look through them first before you start here.
    

This is the final part of the How to Automate series (for a while at least). In my previous posts we have created a few different strategies, but I haven't actually backtested or simulated any of them yet. How will do we even know if they have any edge? 

Today we test those strategies by running simulations and try to optimise performance.

But how do we test strategies?

One method is to follow the steps shown in this fantastic article: [Backtesting wagering models with Betfair JSON stream data](../historicData/backtestingRatingsTutorial.ipynb). But if you already have access to Betfair historic data or you have reccorded it yourself, you are not making full use of your data. This is because the above method will take all the amazing data thats has been collected and only extract a sliver of data from a few time points.

Flumine is amazing because it can make full use of the entire dataset to simulate the market from when the market is first created to settlement. Instead of looking at the prices at 3 minutes before the race and assuming we get matched we can for example simulate placing a back bet hours before the race starts and replay exactly what happened in that market second by second to see if we would have gotten matched between the time we placed the bet and when the market settles. This is really cool because we might have a really awesome model that is close to being profitable but not quite and we want to optimise it.

This will give us the most realistic back testing available and let us test if we are getting matched for the volume and price we want and if we have any edge at all.

Something that is important to note is that although this is the most realistic backtest you can probably get, it is not 100% accurate. This is because we are simply replaying a market with our orders being added in, we cannot take into account how other market participants react. If we place a huge order e.g. $1000 or more we will likely trigger other peoples bots the market will likely move against us.

But either way, we can still try some really cool things such as testing different time points to place bets without needing to re-extract data each time, change staking methodology or placing bets a few ticks away from the best available prices and hoping it gets matched.

---

## Set up

Before we get started, although Jupyter Notebook/lab is a quants' favourite tool we need to use a different IDE such as VS Code for our simulation code (feel free to try it out, it didn't work for me and I read a note somewhere about it in the docs, but can't find it anymore). All code files are made available on [github](https://github.com/betfair-down-under/autoHubTutorials/tree/master).

I am going to use the March 2022 Greyhound Pro data and I've provided a sample of that data in the github repo which you can use to follow along, but if your an Australian and New Zealand customer make sure to shoot an email to <data@betfair.com.au>. 

Simulation mode in Flumine requires your data to be structured a certain way. So, if you have purchased data you will need it to be extracted formatted so that each market file is within a single file, instead or having files within files within files (default).

You can do it manually, which will take an unimaginable amount of time, but I've written a simple script that will do it for you. But you just need to do few things before you run the script. 

- Take your data that has the .tar extension, mine was 2022_03_MarGreyhoundsPro.tar and extract it using winrar/7zip etc this will create a file named 2022_03_MarGreyhoundsPro
- make sure 2022_03_MarGreyhoundsPro is stored in the same location as the data extractor script
- create a new empty folder that you want the extracted data to be outputted to, I created output_2022_03_MarGreyhoundsPro
- then run the script

```py title="Extracts and formats the content of .tar files" hl_lines="10 12"
# Extracts all the bzip2 files (.bz2) 
# contained within the specified output_folder and any sub-folders
# and writes them to a file with their market_id as their file name
# This will take around 10 mins to run for one month of Pro Greyhound data
import glob
import bz2
import shutil

# Folder containing bz2 files or any subfolders with bz2 files
input_folder = '2022_04_AprGreyhoundsPro'  # change to what you have named your folder e.g. 'sample_monthly_data'
# Folder to write our extracted bz2 files to, this folder needs to already be created
output_folder = 'output_2022_04_AprGreyhoundsPro'  # change to what you have named your folder e.g. 'sample_monthly_data_output'

# Returns a list of paths to bz2 files within the input folder and any sub folders
files = glob.iglob(f'{input_folder}/**/**/**/**/**/*.bz2', recursive = False)

# Extracts each bz2 file and write it to the output folder
for path in files:
    market_id = path[-15:-4]
    print(path, market_id)
    with bz2.BZ2File(path) as fr, open(f'{output_folder}/{market_id}',"wb") as fw:
        shutil.copyfileobj(fr,fw)
```

Now we are all set up lets run our sim!

---

## How the sims work

Flumine is pretty cool, by default it hooks up to the Betfair API and it will run our strategy on live markets. When we set it to simulation mode we can hook it up to the historic data instead. The historic data is basically photos of the exhange up to every 50ms, in simulation mode Flumine essentially quickly scans through each picture sequentially essentially replaying the market. Just like how you would `add_strategy()` to Flumine to add a strategy that runs live, you can do the same thing in simulation mode and it will place into the simulated markets it creates.

The coolest thing is, it is super easy to change it to simulation mode:

```py title="Setting Flumine to simulation Mode" 

# Set Flumine to simulation mode
client = clients.SimulatedClient()
framework = FlumineSimulation(client=client)

```

and instead of pointing it to markets you want to run your strategy on, you point it to your historic data files instead (as it is quite slow I would also suggest only replaying a subsection of the historic files, you can change that with the listner_kwargs), then just run it as you would any other strategy in Flumine:

```py title="Pointing the simulation to the historical files" hl_lines="12 14"

# Searches for all betfair data files within the folder sample_monthly_data_output
data_folder = 'sample_monthly_data_output'
data_files = os.listdir(data_folder,)
data_files = [f'{data_folder}/{path}' for path in data_files]

strategy = BackFavStrategy(
    # market_filter selects what portion of the historic data we simulate our strategy on
    # markets selects the list of betfair historic data files
    # market_types specifies the type of markets
    # listener_kwargs specifies the time period we simulate for each market
    market_filter={
        "markets": data_files,  
        'market_types':['WIN'],
        "listener_kwargs": {"inplay": False, "seconds_to_start": 80},  
        },
    max_order_exposure=1000,
    max_selection_exposure=1000,
    max_live_trade_count=1,
    max_trade_count=1,
)
# Run our strategy on the simulated market
framework.add_strategy(strategy)
framework.run()

```

---

## Running Sims: How to Automate II

First off the bat is simulating the strategy we created in How to Automate II. 

Its actually pretty easy to simulate using Flumine especially if your strategy doesn't require outside data. In fact almost all our code we previously made can just be copied accross. We just need to set Flumine to simulation mode and point it to our data files instead of at the Betfair API, which is only a few lines of code and once you read it, its pretty self explanatory.

One thing we must remember to do is to add the bet logging code we made in How to Automate II so we can analyse how our strategy went afterwards. I've copied both the changes you need to make and also the complete code, give that bad boy a spin, and it will create a csv file as a log of all bets placed. 

A months worth of data will take ages to run (like 8 hours on my slow laptop), but the sample data should only take around 10 mins (we will go into speeding up the sims later).

=== "Changes you need to make"

    ```py
    # Searches for all betfair data files within the folder sample_monthly_data_output
    data_folder = 'sample_monthly_data_output'
    data_files = os.listdir(data_folder,)
    data_files = [f'{data_folder}/{path}' for path in data_files]

    # Set Flumine to simulation mode
    client = clients.SimulatedClient()
    framework = FlumineSimulation(client=client)

    # Set parameters for our strategy
    strategy = BackFavStrategy(
        # market_filter selects what portion of the historic data we simulate our strategy on
        # markets selects the list of betfair historic data files
        # market_types specifies the type of markets
        # listener_kwargs specifies the time period we simulate for each market
        market_filter={
            "markets": data_files,  
            'market_types':['WIN'],
            "listener_kwargs": {"inplay": False, "seconds_to_start": 80},  
            },
        max_order_exposure=1000,
        max_selection_exposure=1000,
        max_live_trade_count=1,
        max_trade_count=1,
    )
    # Run our strategy on the simulated market
    framework.add_strategy(strategy)
    framework.add_logging_control(
        BacktestLoggingControl()
    )
    framework.run()
    ```

=== "Complete Code, changes are at the bottom"

    ```py 
    # Import libraries
    import glob
    import os
    import time
    import logging
    import csv
    import pandas as pd
    import json
    import math
    from pythonjsonlogger import jsonlogger
    from flumine import FlumineSimulation, BaseStrategy, utils, clients
    from flumine.order.trade import Trade
    from flumine.order.order import LimitOrder, OrderStatus
    from flumine.order.ordertype import OrderTypes
    from flumine.markets.market import Market
    from flumine.controls.loggingcontrols import LoggingControl
    from betfairlightweight.filters import streaming_market_filter
    from betfairlightweight.resources import MarketBook
    from pythonjsonlogger import jsonlogger
    from concurrent import futuresimport glob

    # Logging
    logger = logging.getLogger()
    custom_format = "%(asctime) %(levelname) %(message)"
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(custom_format)
    formatter.converter = time.gmtime
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)  # Set to logging.CRITICAL to speed up simulation

    class BackFavStrategy(BaseStrategy):

        # Defines what happens when we start our strategy i.e. this method will run once when we first start running our strategy
        def start(self) -> None:
            print("starting strategy 'BackFavStrategy'")

        def check_market_book(self, market: Market, market_book: MarketBook) -> bool:
            # process_market_book only executed if this returns True
            if market_book.status != "CLOSED":
                return True

        def process_market_book(self, market: Market, market_book: MarketBook) -> None:
            
            # Collect data on last price traded and the number of bets we have placed
            snapshot_last_price_traded = []
            snapshot_runner_context = []
            for runner in market_book.runners:
                    snapshot_last_price_traded.append([runner.selection_id,runner.last_price_traded])
                    # Get runner context for each runner
                    runner_context = self.get_runner_context(
                        market.market_id, runner.selection_id, runner.handicap
                    )
                    snapshot_runner_context.append([runner_context.selection_id, runner_context.executable_orders, runner_context.live_trade_count, runner_context.trade_count])

            # Convert last price traded data to dataframe
            snapshot_last_price_traded = pd.DataFrame(snapshot_last_price_traded, columns=['selection_id','last_traded_price'])
            # Find the selection_id of the favourite
            snapshot_last_price_traded = snapshot_last_price_traded.sort_values(by = ['last_traded_price'])
            fav_selection_id = snapshot_last_price_traded['selection_id'].iloc[0]
            logging.info(snapshot_last_price_traded) # logging

            # Convert data on number of bets we have placed to a dataframe
            snapshot_runner_context = pd.DataFrame(snapshot_runner_context, columns=['selection_id','executable_orders','live_trade_count','trade_count'])
            logging.info(snapshot_runner_context) # logging

            for runner in market_book.runners:
                if runner.status == "ACTIVE" and market.seconds_to_start < 60 and market_book.inplay == False and runner.selection_id == fav_selection_id and snapshot_runner_context.iloc[:,1:].sum().sum() == 0:
                    trade = Trade(
                        market_id=market_book.market_id,
                        selection_id=runner.selection_id,
                        handicap=runner.handicap,
                        strategy=self,
                    )
                    order = trade.create_order(
                        side="BACK", order_type=LimitOrder(price=runner.last_price_traded, size=5)
                    )
                    market.place_order(order)

    # Fields we want to log in our simulations
    FIELDNAMES = [
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

    # Log results from simulation into csv file named sim_hta_2.csv
    # If the csv file doesn't exist then it is created, otherwise we append results to the csv file
    class BacktestLoggingControl(LoggingControl):
        NAME = "BACKTEST_LOGGING_CONTROL"

        def __init__(self, *args, **kwargs):
            super(BacktestLoggingControl, self).__init__(*args, **kwargs)
            self._setup()

        def _setup(self):
            if os.path.exists("sim_hta_2.csv"):
                logging.info("Results file exists")
            else:
                with open("sim_hta_2.csv", "w") as m:
                    csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                    csv_writer.writeheader()

        def _process_cleared_orders_meta(self, event):
            orders = event.event
            with open("sim_hta_2.csv", "a") as m:
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
                            "profit": order.simulated.profit,
                            "side": order.side,
                            "elapsed_seconds_executable": order.elapsed_seconds_executable,
                            "order_status": order.status.value,
                            "market_note": order.trade.market_notes,
                            "trade_notes": order.trade.notes_str,
                            "order_notes": order.notes_str,
                        }
                        csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                        csv_writer.writerow(order_data)
                    except Exception as e:
                        logger.error(
                            "_process_cleared_orders_meta: %s" % e,
                            extra={"order": order, "error": e},
                        )

            logger.info("Orders updated", extra={"order_count": len(orders)})

        def _process_cleared_markets(self, event):
            cleared_markets = event.event
            for cleared_market in cleared_markets.orders:
                logger.info(
                    "Cleared market",
                    extra={
                        "market_id": cleared_market.market_id,
                        "bet_count": cleared_market.bet_count,
                        "profit": cleared_market.profit,
                        "commission": cleared_market.commission,
                    },
                )

    # Searches for all betfair data files within the folder sample_monthly_data_output
    data_folder = 'sample_monthly_data_output'
    data_files = os.listdir(data_folder,)
    data_files = [f'{data_folder}/{path}' for path in data_files]

    # Set Flumine to simulation mode
    client = clients.SimulatedClient()
    framework = FlumineSimulation(client=client)

    # Set parameters for our strategy
    strategy = BackFavStrategy(
        # market_filter selects what portion of the historic data we simulate our strategy on
        # markets selects the list of betfair historic data files
        # market_types specifies the type of markets
        # listener_kwargs specifies the time period we simulate for each market
        market_filter={
            "markets": data_files,  
            'market_types':['WIN'],
            "listener_kwargs": {"inplay": False, "seconds_to_start": 80},  
            },
        max_order_exposure=1000,
        max_selection_exposure=1000,
        max_live_trade_count=1,
        max_trade_count=1,
    )
    # Run our strategy on the simulated market
    framework.add_strategy(strategy)
    framework.add_logging_control(
        BacktestLoggingControl()
    )
    framework.run()
    ```

---

## Running Sims: How to Automate III

Okay, so we got the first one running pretty easily, a little too easily (a few lines of code and no major issues or hacky work arounds), lets test out a strategy that requires external data. In [How to Automate III](../How_to_Automate_3) we automated the betfair data scientists model, lets now simulate performance. I'm going to do just the greyhound model, 'Iggy', at the moment, but the code is basically the same for the thoroughbred model, 'Kash'.

Because we didn't save any of our ratings in How to Automate III we will need to redownload it now. And instead or redownloading just one days worth of data lets test out a whole month at a time. Lets reuse the function we created in How to Automate IV that we used a hacky work around that downloads the ratings for a range of dates:

```py title="Download a whole month of Iggy ratings and convert it to a DataFrame"
def download_iggy_ratings(date):
    """Downloads the Betfair Iggy model ratings for a given date and formats it into a nice DataFrame.

    Args:
        date (datetime): the date we want to download the ratings for
    """
    iggy_url_1 = 'https://betfair-data-supplier-prod.herokuapp.com/api/widgets/iggy-joey/datasets?date='
    iggy_url_2 = date.strftime("%Y-%m-%d")
    iggy_url_3 = '&presenter=RatingsPresenter&csv=true'
    iggy_url = iggy_url_1 + iggy_url_2 + iggy_url_3

    # Download todays greyhounds ratings
    iggy_df = pd.read_csv(iggy_url)

    # Data clearning
    iggy_df = iggy_df.rename(columns={"meetings.races.bfExchangeMarketId":"market_id","meetings.races.runners.bfExchangeSelectionId":"selection_id","meetings.races.runners.ratedPrice":"rating"})
    iggy_df = iggy_df[['market_id','selection_id','rating']]
    iggy_df['market_id'] = iggy_df['market_id'].astype(str)

    # Set market_id and selection_id as index for easy referencing
    iggy_df = iggy_df.set_index(['market_id','selection_id'])
    return(iggy_df)

# Download historical ratings over a time period and convert into a big DataFrame.
back_test_period = pd.date_range(start='2022/02/27', end='2022/03/05')
frames = [download_iggy_ratings(day) for day in back_test_period]
iggy_df = pd.concat(frames)
print(iggy_df)
```

Now that we have downloaded a whole month of Iggy ratings to simulate it is crazy easy to simulate. We do the same thing we did when simulating How to Automate II: copy and paste the original code, and set Flumine into simulation mode pointing it to the historic data instead of the Betfair API.

=== "Changes made to the original How to Automate III code"

    ```py
    def download_iggy_ratings(date):
        """Downloads the Betfair Iggy model ratings for a given date and formats it into a nice DataFrame.

        Args:
            date (datetime): the date we want to download the ratings for
        """
        iggy_url_1 = 'https://betfair-data-supplier-prod.herokuapp.com/api/widgets/iggy-joey/datasets?date='
        iggy_url_2 = date.strftime("%Y-%m-%d")
        iggy_url_3 = '&presenter=RatingsPresenter&csv=true'
        iggy_url = iggy_url_1 + iggy_url_2 + iggy_url_3

        # Download todays greyhounds ratings
        iggy_df = pd.read_csv(iggy_url)

        # Data clearning
        iggy_df = iggy_df.rename(columns={"meetings.races.bfExchangeMarketId":"market_id","meetings.races.runners.bfExchangeSelectionId":"selection_id","meetings.races.runners.ratedPrice":"rating"})
        iggy_df = iggy_df[['market_id','selection_id','rating']]
        iggy_df['market_id'] = iggy_df['market_id'].astype(str)

        # Set market_id and selection_id as index for easy referencing
        iggy_df = iggy_df.set_index(['market_id','selection_id'])
        return(iggy_df)

    # Download historical ratings over a time period and convert into a big DataFrame.
    back_test_period = pd.date_range(start='2022/02/27', end='2022/03/05')
    frames = [download_iggy_ratings(day) for day in back_test_period]
    iggy_df = pd.concat(frames)
    print(iggy_df)

    # Searches for all betfair data files within the folder sample_monthly_data_output
    data_folder = 'sample_monthly_data_output'
    data_files = os.listdir(data_folder,)
    data_files = [f'{data_folder}/{path}' for path in data_files]

    # Set Flumine to simulation mode
    client = clients.SimulatedClient()
    framework = FlumineSimulation(client=client)

    # Set parameters for our strategy
    strategy = FlatIggyModel(
        market_filter={
            "markets": data_files,  
            'market_types':['WIN'],
            "listener_kwargs": {"inplay": False, "seconds_to_start": 80},  
            },
        max_order_exposure=1000,
        max_selection_exposure=1000,
        max_live_trade_count=1,
        max_trade_count=1,
    )
    # Run our strategy on the simulated market
    framework.add_strategy(strategy)
    framework.add_logging_control(
        BacktestLoggingControl()
    )
    framework.run()
    ```

=== "Complete Code"

    ```py 
    # Import libraries
    import glob
    import os
    import time
    import logging
    import csv
    import pandas as pd
    from pythonjsonlogger import jsonlogger
    from flumine import FlumineSimulation, BaseStrategy, utils, clients
    from flumine.order.trade import Trade
    from flumine.order.order import LimitOrder, OrderStatus
    from flumine.order.ordertype import OrderTypes
    from flumine.markets.market import Market
    from flumine.controls.loggingcontrols import LoggingControl
    from betfairlightweight.filters import streaming_market_filter
    from betfairlightweight.resources import MarketBook

    # Logging
    logger = logging.getLogger()
    custom_format = "%(asctime) %(levelname) %(message)"
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(custom_format)
    formatter.converter = time.gmtime
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)  # Set to logging.CRITICAL to speed up simulation

    def download_iggy_ratings(date):
        """Downloads the Betfair Iggy model ratings for a given date and formats it into a nice DataFrame.

        Args:
            date (datetime): the date we want to download the ratings for
        """
        iggy_url_1 = 'https://betfair-data-supplier-prod.herokuapp.com/api/widgets/iggy-joey/datasets?date='
        iggy_url_2 = date.strftime("%Y-%m-%d")
        iggy_url_3 = '&presenter=RatingsPresenter&csv=true'
        iggy_url = iggy_url_1 + iggy_url_2 + iggy_url_3

        # Download todays greyhounds ratings
        iggy_df = pd.read_csv(iggy_url)

        # Data clearning
        iggy_df = iggy_df.rename(columns={"meetings.races.bfExchangeMarketId":"market_id","meetings.races.runners.bfExchangeSelectionId":"selection_id","meetings.races.runners.ratedPrice":"rating"})
        iggy_df = iggy_df[['market_id','selection_id','rating']]
        iggy_df['market_id'] = iggy_df['market_id'].astype(str)

        # Set market_id and selection_id as index for easy referencing
        iggy_df = iggy_df.set_index(['market_id','selection_id'])
        return(iggy_df)

    # Download historical ratings over a time period and convert into a big DataFrame.
    back_test_period = pd.date_range(start='2022/02/27', end='2022/03/05')
    frames = [download_iggy_ratings(day) for day in back_test_period]
    iggy_df = pd.concat(frames)
    print(iggy_df)

    # Create strategy, this is the exact same strategy shown in How to Automate III
    class FlatIggyModel(BaseStrategy):
        def start(self) -> None:
            print("starting strategy 'FlatIggyModel'")

        def check_market_book(self, market: Market, market_book: MarketBook) -> bool:
            if market_book.status != "CLOSED":
                return True

        def process_market_book(self, market: Market, market_book: MarketBook) -> None:
            if market.seconds_to_start < 60 and market_book.inplay == False:
                for runner in market_book.runners:
                    if runner.status == "ACTIVE" and runner.ex.available_to_back[0]['price'] > iggy_df.loc[market_book.market_id].loc[runner.selection_id].item():
                        trade = Trade(
                        market_id=market_book.market_id,
                        selection_id=runner.selection_id,
                        handicap=runner.handicap,
                        strategy=self,
                        )
                        order = trade.create_order(
                            side="BACK", order_type=LimitOrder(price=runner.ex.available_to_back[0]['price'], size=5.00)
                        )
                        market.place_order(order)
                    if runner.status == "ACTIVE" and runner.ex.available_to_lay[0]['price'] < iggy_df.loc[market_book.market_id].loc[runner.selection_id].item():
                        trade = Trade(
                        market_id=market_book.market_id,
                        selection_id=runner.selection_id,
                        handicap=runner.handicap,
                        strategy=self,
                        )
                        order = trade.create_order(
                            side="LAY", order_type=LimitOrder(price=runner.ex.available_to_lay[0]['price'], size=5.00)
                        )
                        market.place_order(order)

    # Fields we want to log in our simulations
    FIELDNAMES = [
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

    # Log results from simulation into csv file named sim_hta_3.csv
    # If the csv file doesn't exist then it is created, otherwise we append results to the csv file
    class BacktestLoggingControl(LoggingControl):
        NAME = "BACKTEST_LOGGING_CONTROL"

        def __init__(self, *args, **kwargs):
            super(BacktestLoggingControl, self).__init__(*args, **kwargs)
            self._setup()

        def _setup(self):
            if os.path.exists("sim_hta_3.csv"):
                logging.info("Results file exists")
            else:
                with open("sim_hta_3.csv", "w") as m:
                    csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                    csv_writer.writeheader()

        def _process_cleared_orders_meta(self, event):
            orders = event.event
            with open("sim_hta_3.csv", "a") as m:
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
                            "profit": order.simulated.profit,
                            "side": order.side,
                            "elapsed_seconds_executable": order.elapsed_seconds_executable,
                            "order_status": order.status.value,
                            "market_note": order.trade.market_notes,
                            "trade_notes": order.trade.notes_str,
                            "order_notes": order.notes_str,
                        }
                        csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                        csv_writer.writerow(order_data)
                    except Exception as e:
                        logger.error(
                            "_process_cleared_orders_meta: %s" % e,
                            extra={"order": order, "error": e},
                        )

            logger.info("Orders updated", extra={"order_count": len(orders)})

        def _process_cleared_markets(self, event):
            cleared_markets = event.event
            for cleared_market in cleared_markets.orders:
                logger.info(
                    "Cleared market",
                    extra={
                        "market_id": cleared_market.market_id,
                        "bet_count": cleared_market.bet_count,
                        "profit": cleared_market.profit,
                        "commission": cleared_market.commission,
                    },
                )

    # Searches for all betfair data files within the folder sample_monthly_data_output
    data_folder = 'sample_monthly_data_output'
    data_files = os.listdir(data_folder,)
    data_files = [f'{data_folder}/{path}' for path in data_files]

    # Set Flumine to simulation mode
    client = clients.SimulatedClient()
    framework = FlumineSimulation(client=client)

    # Set parameters for our strategy
    strategy = FlatIggyModel(
        market_filter={
            "markets": data_files,  
            'market_types':['WIN'],
            "listener_kwargs": {"inplay": False, "seconds_to_start": 80},  
            },
        max_order_exposure=1000,
        max_selection_exposure=1000,
        max_live_trade_count=1,
        max_trade_count=1,
    )
    # Run our strategy on the simulated market
    framework.add_strategy(strategy)
    framework.add_logging_control(
        BacktestLoggingControl()
    )
    framework.run()
    ```

---

## Simulating How to Automate IV

Because we coded How to Automate IV with simulating in mind (I didn't originally and had to recode it a few times), its easy for us to simulate the performance of our model. As we saved our model ratings to a csv, reading it in now actually makes the code simpler then what we created for placing live bets. This is because the issues we had working around reserve dogs and matching with the Betfair API has been taken care of (there are no reserve dogs to work around in the historic data). In fact thanks to my hacky work around in How to Automate IV the data is also in the same format as How to Automate III so we can basically use almost the exact same code we used to simulate How to Automate III. 

The only real differences from simulating How to Automate III and How to Automate IV is that we need to have the csv file of predictions already, read that in, and change any naming conventions that might be different.

=== "Read in model predictions and format dataframe for easy reference"

    ```py
    # Read in predictions from hta_4
    todays_data = pd.read_csv('backtest.csv', dtype = ({"market_id":str}))
    todays_data = todays_data.set_index(['market_id','selection_id'])
    ```

=== "Complete code, almost the same as simulating How to Automate III"

    ```py
    # Import libraries
    import glob
    import os
    import time
    import logging
    import csv
    import pandas as pd
    import json
    from pythonjsonlogger import jsonlogger
    from flumine import FlumineSimulation, BaseStrategy, utils, clients
    from flumine.order.trade import Trade
    from flumine.order.order import LimitOrder, OrderStatus
    from flumine.order.ordertype import OrderTypes
    from flumine.markets.market import Market
    from flumine.controls.loggingcontrols import LoggingControl
    from betfairlightweight.filters import streaming_market_filter
    from betfairlightweight.resources import MarketBook
    from dateutil import tz
    from datetime import datetime, timedelta
    from dateutil.relativedelta import relativedelta
    from betfairlightweight.resources import MarketCatalogue
    from flumine.markets.middleware import Middleware

    # Logging
    logger = logging.getLogger()
    custom_format = "%(asctime) %(levelname) %(message)"
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(custom_format)
    formatter.converter = time.gmtime
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)  # Set to logging.CRITICAL to speed up simulation

    # Read in predictions from hta_4
    todays_data = pd.read_csv('backtest.csv', dtype = ({"market_id":str}))
    todays_data = todays_data.set_index(['market_id','selection_id'])

    ### New implementation
    class FlatBetting(BaseStrategy):
        def start(self) -> None:
            print("starting strategy 'FlatBetting' using the model we created the Greyhound modelling in Python Tutorial")

        def check_market_book(self, market: Market, market_book: MarketBook) -> bool:
            if market_book.status != "CLOSED":
                return True

        def process_market_book(self, market: Market, market_book: MarketBook) -> None:

            # At the 60 second mark:
            if market.seconds_to_start < 60 and market_book.inplay == False:

                # Can't simulate polling API
                # Only use streaming API:
                for runner in market_book.runners:
                    model_price = todays_data.loc[market.market_id].loc[runner.selection_id]['rating']
                    # If best available to back price is > rated price then flat $5 back
                    if runner.status == "ACTIVE" and runner.ex.available_to_back[0]['price'] > model_price:
                        trade = Trade(
                        market_id=market_book.market_id,
                        selection_id=runner.selection_id,
                        handicap=runner.handicap,
                        strategy=self,
                        )
                        order = trade.create_order(
                            side="BACK", order_type=LimitOrder(price=runner.ex.available_to_back[0]['price'], size=5.00)
                        )
                        market.place_order(order)
                    # If best available to lay price is < rated price then flat $5 lay
                    if runner.status == "ACTIVE" and runner.ex.available_to_lay[0]['price'] < model_price:
                        trade = Trade(
                        market_id=market_book.market_id,
                        selection_id=runner.selection_id,
                        handicap=runner.handicap,
                        strategy=self,
                        )
                        order = trade.create_order(
                            side="LAY", order_type=LimitOrder(price=runner.ex.available_to_lay[0]['price'], size=5.00)
                        )
                        market.place_order(order)

    # Fields we want to log in our simulations
    FIELDNAMES = [
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

    # Log results from simulation into csv file named sim_hta_4.csv
    # If the csv file doesn't exist then it is created, otherwise we append results to the csv file
    class BacktestLoggingControl(LoggingControl):
        NAME = "BACKTEST_LOGGING_CONTROL"

        def __init__(self, *args, **kwargs):
            super(BacktestLoggingControl, self).__init__(*args, **kwargs)
            self._setup()

        def _setup(self):
            if os.path.exists("sim_hta_4.csv"):
                logging.info("Results file exists")
            else:
                with open("sim_hta_4.csv", "w") as m:
                    csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                    csv_writer.writeheader()

        def _process_cleared_orders_meta(self, event):
            orders = event.event
            with open("sim_hta_4.csv", "a") as m:
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
                            "profit": order.simulated.profit,
                            "side": order.side,
                            "elapsed_seconds_executable": order.elapsed_seconds_executable,
                            "order_status": order.status.value,
                            "market_note": order.trade.market_notes,
                            "trade_notes": order.trade.notes_str,
                            "order_notes": order.notes_str,
                        }
                        csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                        csv_writer.writerow(order_data)
                    except Exception as e:
                        logger.error(
                            "_process_cleared_orders_meta: %s" % e,
                            extra={"order": order, "error": e},
                        )

            logger.info("Orders updated", extra={"order_count": len(orders)})

        def _process_cleared_markets(self, event):
            cleared_markets = event.event
            for cleared_market in cleared_markets.orders:
                logger.info(
                    "Cleared market",
                    extra={
                        "market_id": cleared_market.market_id,
                        "bet_count": cleared_market.bet_count,
                        "profit": cleared_market.profit,
                        "commission": cleared_market.commission,
                    },
                )

    # Searches for all betfair data files within the folder sample_monthly_data_output
    data_folder = 'sample_monthly_data_output'
    data_files = os.listdir(data_folder,)
    data_files = [f'{data_folder}/{path}' for path in data_files]

    # Set Flumine to simulation mode
    client = clients.SimulatedClient()
    framework = FlumineSimulation(client=client)

    # Set parameters for our strategy
    strategy = FlatBetting(
        market_filter={
            "markets": data_files,  
            'market_types':['WIN'],
            "listener_kwargs": {"inplay": False, "seconds_to_start": 80},  
            },
        max_order_exposure=1000,
        max_selection_exposure=1000,
        max_live_trade_count=1,
        max_trade_count=1,
    )
    # Run our strategy on the simulated market
    framework.add_strategy(strategy)
    framework.add_logging_control(
        BacktestLoggingControl()
    )
    framework.run()
    ```

---

## Gotta go fast
Now that we have everything working, if you have tried any of the simulations you may notice its pretty slow. I definitely have, especially for larger files such as on 1 months worth of data (probably took me around 8 hours of just running the code in the background). The good thing is we can speed it up, the bad thing is, its via multiprocessing which I have never touched before. But turns out its not too bad. 

You really only need to wrap your Flumine client into a function:

``` py

def run_process(markets):
    """Replays a Betfair historic data. Places bets according to the user defined strategy and tries to accurately simulate matching by replaying the historic data.

    Args:
        markets (list: [file paths]): a list of file paths to where the historic data is stored locally. e.g. user/zhoui/downloads/test.csv
    """    
    # Set Flumine to simulation mode
    client = clients.SimulatedClient()
    framework = FlumineSimulation(client=client)

    # Set parameters for our strategy
    strategy = FlatBetting(
        market_filter={
            "markets": markets,  
            'market_types':['WIN'],
            "listener_kwargs": {"inplay": False, "seconds_to_start": 80},  
            },
        max_order_exposure=1000,
        max_selection_exposure=1000,
        max_live_trade_count=1,
        max_trade_count=1,
    )
    # Run our strategy on the simulated market
    framework.add_strategy(strategy)
    framework.add_logging_control(
        BacktestLoggingControl()
    )
    framework.run()

# Searches for all betfair data files within the folder sample_monthly_data_output
data_folder = 'sample_monthly_data_output'
data_files = os.listdir(data_folder,)
data_files = [f'{data_folder}/{path}' for path in data_files]
```

and then split the files to run on muliple processors. You can copy the code, which is what I did, and it works without a hitch. 

```py
# Multi processing
if __name__ == "__main__":
    all_markets = data_files  # All the markets we want to simulate
    processes = os.cpu_count()  # Returns the number of CPUs in the system.
    markets_per_process = 8   # 8 is optimal as it prevents data leakage.

    _process_jobs = []
    with futures.ProcessPoolExecutor(max_workers=processes) as p:
        # Number of chunks to split the process into depends on the number of markets we want to process and number of CPUs we have.
        chunk = min(
            markets_per_process, math.ceil(len(all_markets) / processes)
        )
        # Split all the markets we want to process into chunks to run on separate CPUs and then run them on the separate CPUs
        for m in (utils.chunks(all_markets, chunk)):
            _process_jobs.append(
                p.submit(
                    run_process,
                    markets=m,
                )
            )
        for job in futures.as_completed(_process_jobs):
            job.result()  # wait for result

```

Essentially it takes all the historical markets you have e.g. 1000, and splits it into 8 chunks. Then we run our strategy on all 8 chunks simultaniously. And this gives serious speed improvements. The complete code for all three simulations using multi processing are available at the end of this post. 

Future versions of Flumine are using the new BetfairData library to speed up simulations which once fully implemented should also give some serious speed benefits. 

---

## Analysing and optimising our results

Now that we have all our speedy simulation code lets look at our results and see if we found anything good.

```py
import numpy as np
import pandas as pd
import plotly.express as px

# Read data
results = pd.read_csv('sim_hta_4.csv', parse_dates = ['date_time_placed'], dtype = {'market_id':str})
# calculate and display cumulative pnl
results = results.sort_values(by = ['date_time_placed'])
results['cum_profit'] = results['profit'].cumsum()
px.line(results, 'date_time_placed', 'cum_profit').show()
```

![post_sim_analysis_v1](hta_img/post_sim_analysis_v1.png)

Before commissions the model is profitable, which is awesome as I didn't think that would be the case. Bruno has mentioned to me that the model in the tutorial was quite "basic" and not profitable, but it seems we got super lucky with a few long shots getting up in March. Lets incorporate commissions into our results and see if it remains profitable:

```py
gross_profit = pd.DataFrame(results.groupby(['market_id'])['profit'].sum())
# 7% commission rate on greyhounds, commissions calculated on profit at a market level
calc_comms = lambda gross_profit: np.where(gross_profit>0, gross_profit*(1-0.07), gross_profit)
gross_profit['net_pnl'] = calc_comms(gross_profit['profit'])
gross_profit['cum_npl'] = gross_profit['net_pnl'].cumsum()
px.line(gross_profit, gross_profit.index, 'cum_npl').show()
```

![post_sim_analysis_v2](hta_img/post_sim_analysis_v2.png)

We are close, infact we were up a bit at the start but it seems after taking into account commissions we are no longer profitable and end the month down around $800. Lets try two different things to see if we can optimse our strategy: a different staking methodology and also a different time we start placing our bets.

My theory is that because we are crossing the spread and taking whatever prices are available we are probably losing a bit of our edge there. If we bet when markets are more liquid then we will may lose less. But as markets become more liquid they also tend to become more efficient so lets it could work against us. Nonetheless lets test it out:

=== "Placing bets at 30 seconds instead of 60 seconds"
    
    ``` py
    def process_market_book(self, market: Market, market_book: MarketBook) -> None:
        # At the 60 second mark:
        if market.seconds_to_start < 30 and market_book.inplay == False:
            # Can't simulate polling API
            # Only use streaming API:
            for runner in market_book.runners:
    ```
=== "Results Before Commissions"

    ![post_sim_analysis_30secs](hta_img/post_sim_analysis_30secs.png)

=== "Results After Commissions"

    ![post_sim_analysis_30secs_v2](hta_img/post_sim_analysis_30secs_v2.png)

So the results seem pretty similar to before. After commisions we are down around $700 so we seem to be doing slighlty better.

Lets try a different staking method instead, this time I have opted for a proportional staking strategy going for a fixed $10 profit on back bets and a fixed $10 liability on lay bets. There is an excellent post [analysing different staking methods](https://betfair-datascientists.github.io/modelling/stakingMethods/) and I would encourage everyone to take a look at it. Lets see how our simulation went:

=== "Proportional Staking instead of Flat Staking"
    
    ``` py
    if market.seconds_to_start < 60 and market_book.inplay == False:
        # Can't simulate polling API
        # Only use streaming API:
        for runner in market_book.runners:
            model_price = todays_data.loc[market.market_id].loc[runner.selection_id]['rating']
            # If best available to back price is > rated price then proportional back stake
            if runner.status == "ACTIVE" and runner.ex.available_to_back[0]['price'] > model_price:
                trade = Trade(
                market_id=market_book.market_id,
                selection_id=runner.selection_id,
                handicap=runner.handicap,
                strategy=self,
                )
                order = trade.create_order(
                    side="BACK", order_type=LimitOrder(price=runner.ex.available_to_back[0]['price'], size=round(10/(runner.ex.available_to_back[0]['price']-1),2))
                )
                market.place_order(order)
            # If best available to lay price is < rated price then proportional lay stake
            if runner.status == "ACTIVE" and runner.ex.available_to_lay[0]['price'] < model_price:
                trade = Trade(
                market_id=market_book.market_id,
                selection_id=runner.selection_id,
                handicap=runner.handicap,
                strategy=self,
                )
                order = trade.create_order(
                    side="LAY", order_type=LimitOrder(price=runner.ex.available_to_lay[0]['price'], size=round(10/(runner.ex.available_to_lay[0]['price']-1),2))
                )
                market.place_order(order)
    ```
=== "Results Before Commissions"

    ![post_sim_analysis_ps](hta_img/post_sim_analysis_ps.png)

=== "Results After Commissions"

    ![post_sim_analysis_ps_v2](hta_img/post_sim_analysis_ps_v2.png)

I'm pretty surprised, I really did not expect to be profitable after commissions. We are slightly profitable at the end but we spent a significant amount of time in the negatives during the month. Without testing it out further with more historic data I going to put this down as variance for now. And I'll hand it over to you.

---

## Conclusion and next steps

While we have tested our strategy and optimised it so far, I mearly tried one month of data and only three different variations of our strategy (most of which are unprofitable). Hopefully these posts help you think about what is possible when automating your strategy and how to optimise your strategy. 

There are plenty of other things to look at when optimising your strategy such as different staking methodologies or being more selective with your bets based on the track or state. The natural next step based on my above results would be to test out proportional staking at 30 seconds and to use a longer backtesting period.

We need more data to draw a good conclusion about long term results, I have definitely found some strategies that fluke one month, but are long term losers using this method.

### Complete Code

=== "Multiprocess How to Automate II"
    [Download from Github](https://github.com/betfair-down-under/autoHubTutorials/tree/master)

    ```py
    # Import libraries
    import glob
    import os
    import time
    import logging
    import csv
    import math
    from pythonjsonlogger import jsonlogger
    from concurrent import futures
    from flumine import FlumineSimulation, clients, utils
    from flumine.controls.loggingcontrols import LoggingControl
    from flumine.order.ordertype import OrderTypes

    from flumine import BaseStrategy 
    from flumine.order.trade import Trade
    from flumine.order.order import LimitOrder, OrderStatus
    from flumine.markets.market import Market
    from betfairlightweight.filters import streaming_market_filter
    from betfairlightweight.resources import MarketBook

    import pandas as pd
    import numpy as np
    import logging

    # Logging
    logger = logging.getLogger()
    custom_format = "%(asctime) %(levelname) %(message)"
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(custom_format)
    formatter.converter = time.gmtime
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)  # Set to logging.CRITICAL to speed up simulation

    # Create a new strategy as a new class called BackFavStrategy, this in turn will allow us to create a new Python object later
        # BackFavStrategy is a child class inhereting from a predefined class in Flumine we imported above called BaseStrategy
    class BackFavStrategy(BaseStrategy):
        # Defines what happens when we start our strategy i.e. this method will run once when we first start running our strategy
        def start(self) -> None:
            # We will want to change what is printed with we have multiple strategies
            print("starting strategy 'BackFavStrategy'")

        # Defines what happens when we first look at a market
        # This method will prevent looking at markets that are closed
        def check_market_book(self, market: Market, market_book: MarketBook) -> bool:
            # process_market_book only executed if this returns True
            if market_book.status != "CLOSED":
                return True

        # If check_market_book returns true i.e. the market is open and not closed then we will run process_market_book once initially
        # After the first inital time process_market_book has been run, every single time the market ticks, process_market_book will run again
        def process_market_book(self, market: Market, market_book: MarketBook) -> None:
            
            # Find last traded price as a dataframe
            snapshot_last_price_traded = []
            snapshot_runner_context = []
            for runner in market_book.runners:
                    snapshot_last_price_traded.append([runner.selection_id,runner.last_price_traded])
                    # Get runner context for each runner
                    runner_context = self.get_runner_context(
                        market.market_id, runner.selection_id, runner.handicap
                    )
                    snapshot_runner_context.append([runner_context.selection_id, runner_context.executable_orders, runner_context.live_trade_count, runner_context.trade_count])

            snapshot_last_price_traded = pd.DataFrame(snapshot_last_price_traded, columns=['selection_id','last_traded_price'])
            snapshot_last_price_traded = snapshot_last_price_traded.sort_values(by = ['last_traded_price'])
            fav_selection_id = snapshot_last_price_traded['selection_id'].iloc[0]

            snapshot_runner_context = pd.DataFrame(snapshot_runner_context, columns=['selection_id','executable_orders','live_trade_count','trade_count'])

            for runner in market_book.runners:
                if runner.status == "ACTIVE" and market.seconds_to_start < 60 and market_book.inplay == False and runner.selection_id == fav_selection_id and snapshot_runner_context.iloc[:,1:].sum().sum() == 0:
                    trade = Trade(
                        market_id=market_book.market_id,
                        selection_id=runner.selection_id,
                        handicap=runner.handicap,
                        strategy=self,
                    )
                    order = trade.create_order(
                        side="BACK", order_type=LimitOrder(price=runner.last_price_traded, size=5)
                    )
                    market.place_order(order)


    # Fields we want to log in our simulations
    FIELDNAMES = [
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

    # Log results from simulation into csv file named sim_hta_2.csv
    # If the csv file doesn't exist then it is created, otherwise we append results to the csv file
    class BacktestLoggingControl(LoggingControl):
        NAME = "BACKTEST_LOGGING_CONTROL"

        def __init__(self, *args, **kwargs):
            super(BacktestLoggingControl, self).__init__(*args, **kwargs)
            self._setup()

        def _setup(self):
            if os.path.exists("sim_hta_2.csv"):
                logging.info("Results file exists")
            else:
                with open("sim_hta_2.csv", "w") as m:
                    csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                    csv_writer.writeheader()

        def _process_cleared_orders_meta(self, event):
            orders = event.event
            with open("sim_hta_2.csv", "a") as m:
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
                            "profit": order.simulated.profit,
                            "side": order.side,
                            "elapsed_seconds_executable": order.elapsed_seconds_executable,
                            "order_status": order.status.value,
                            "market_note": order.trade.market_notes,
                            "trade_notes": order.trade.notes_str,
                            "order_notes": order.notes_str,
                        }
                        csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                        csv_writer.writerow(order_data)
                    except Exception as e:
                        logger.error(
                            "_process_cleared_orders_meta: %s" % e,
                            extra={"order": order, "error": e},
                        )

            logger.info("Orders updated", extra={"order_count": len(orders)})

        def _process_cleared_markets(self, event):
            cleared_markets = event.event
            for cleared_market in cleared_markets.orders:
                logger.info(
                    "Cleared market",
                    extra={
                        "market_id": cleared_market.market_id,
                        "bet_count": cleared_market.bet_count,
                        "profit": cleared_market.profit,
                        "commission": cleared_market.commission,
                    },
                )

    # Searches for all betfair data files within the folder sample_monthly_data_output
    data_folder = 'sample_monthly_data_output'
    data_files = os.listdir(data_folder,)
    data_files = [f'{data_folder}/{path}' for path in data_files]

    def run_process(markets):
        """Replays a Betfair historic data. Places bets according to the user defined strategy and tries to accurately simulate matching by replaying the historic data.

        Args:
            markets (list: [file paths]): a list of file paths to where the historic data is stored locally. e.g. user/zhoui/downloads/test.csv
        """    
        # Set Flumine to simulation mode
        client = clients.SimulatedClient()
        framework = FlumineSimulation(client=client)    

        # Set parameters for our strategy
        strategy = BackFavStrategy(
            # market_filter selects what portion of the historic data we simulate our strategy on
            # markets selects the list of betfair historic data files
            # market_types specifies the type of markets
            # listener_kwargs specifies the time period we simulate for each market
            market_filter={
                "markets": markets,  
                'market_types':['WIN'],
                "listener_kwargs": {"inplay": False, "seconds_to_start": 80},  
                },
            max_order_exposure=1000,
            max_selection_exposure=1000,
            max_live_trade_count=1,
            max_trade_count=1,
        )
        # Run our strategy on the simulated market
        framework.add_strategy(strategy)
        framework.add_logging_control(
            BacktestLoggingControl()
        )
        framework.run()

    # Multi processing
    if __name__ == "__main__":
        all_markets = data_files  # All the markets we want to simulate
        processes = os.cpu_count()  # Returns the number of CPUs in the system.
        markets_per_process = 8   # 8 is optimal as it prevents data leakage.

        _process_jobs = []
        with futures.ProcessPoolExecutor(max_workers=processes) as p:
            # Number of chunks to split the process into depends on the number of markets we want to process and number of CPUs we have.
            chunk = min(
                markets_per_process, math.ceil(len(all_markets) / processes)
            )
            # Split all the markets we want to process into chunks to run on separate CPUs and then run them on the separate CPUs
            for m in (utils.chunks(all_markets, chunk)):
                _process_jobs.append(
                    p.submit(
                        run_process,
                        markets=m,
                    )
                )
            for job in futures.as_completed(_process_jobs):
                job.result()  # wait for result

    ```

=== "Multiprocess How to Automate III"
    [Download from Github](https://github.com/betfair-down-under/autoHubTutorials/tree/master)

    ```py
    # Import libraries
    import glob
    import os
    import time
    import logging
    import csv
    import math
    import pandas as pd
    from pythonjsonlogger import jsonlogger
    from concurrent import futures
    from flumine import FlumineSimulation, BaseStrategy, utils, clients
    from flumine.order.trade import Trade
    from flumine.order.order import LimitOrder, OrderStatus
    from flumine.order.ordertype import OrderTypes
    from flumine.markets.market import Market
    from flumine.controls.loggingcontrols import LoggingControl
    from betfairlightweight.filters import streaming_market_filter
    from betfairlightweight.resources import MarketBook

    # Logging
    logger = logging.getLogger()
    custom_format = "%(asctime) %(levelname) %(message)"
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(custom_format)
    formatter.converter = time.gmtime
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)  # Set to logging.CRITICAL to speed up simulation

    def download_iggy_ratings(date):
        """Downloads the Betfair Iggy model ratings for a given date and formats it into a nice DataFrame.

        Args:
            date (datetime): the date we want to download the ratings for
        """
        iggy_url_1 = 'https://betfair-data-supplier-prod.herokuapp.com/api/widgets/iggy-joey/datasets?date='
        iggy_url_2 = date.strftime("%Y-%m-%d")
        iggy_url_3 = '&presenter=RatingsPresenter&csv=true'
        iggy_url = iggy_url_1 + iggy_url_2 + iggy_url_3

        # Download todays greyhounds ratings
        iggy_df = pd.read_csv(iggy_url)

        # Data clearning
        iggy_df = iggy_df.rename(columns={"meetings.races.bfExchangeMarketId":"market_id","meetings.races.runners.bfExchangeSelectionId":"selection_id","meetings.races.runners.ratedPrice":"rating"})
        iggy_df = iggy_df[['market_id','selection_id','rating']]
        iggy_df['market_id'] = iggy_df['market_id'].astype(str)

        # Set market_id and selection_id as index for easy referencing
        iggy_df = iggy_df.set_index(['market_id','selection_id'])
        return(iggy_df)

    back_test_period = pd.date_range(start='2022/02/27', end='2022/03/05')
    frames = [download_iggy_ratings(day) for day in back_test_period]
    iggy_df = pd.concat(frames)
    print(iggy_df)

    # Create strategy, this is the exact same strategy shown in How to Automate III
    class FlatIggyModel(BaseStrategy):
        def start(self) -> None:
            print("starting strategy 'FlatIggyModel'")

        def check_market_book(self, market: Market, market_book: MarketBook) -> bool:
            if market_book.status != "CLOSED":
                return True

        def process_market_book(self, market: Market, market_book: MarketBook) -> None:
            if market.seconds_to_start < 60 and market_book.inplay == False:
                for runner in market_book.runners:
                    if runner.status == "ACTIVE" and runner.ex.available_to_back[0]['price'] > iggy_df.loc[market_book.market_id].loc[runner.selection_id].item():
                        trade = Trade(
                        market_id=market_book.market_id,
                        selection_id=runner.selection_id,
                        handicap=runner.handicap,
                        strategy=self,
                        )
                        order = trade.create_order(
                            side="BACK", order_type=LimitOrder(price=runner.ex.available_to_back[0]['price'], size=5.00)
                        )
                        market.place_order(order)
                    if runner.status == "ACTIVE" and runner.ex.available_to_lay[0]['price'] < iggy_df.loc[market_book.market_id].loc[runner.selection_id].item():
                        trade = Trade(
                        market_id=market_book.market_id,
                        selection_id=runner.selection_id,
                        handicap=runner.handicap,
                        strategy=self,
                        )
                        order = trade.create_order(
                            side="LAY", order_type=LimitOrder(price=runner.ex.available_to_lay[0]['price'], size=5.00)
                        )
                        market.place_order(order)

    # Fields we want to log in our simulations
    FIELDNAMES = [
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

    # Log results from simulation into csv file named sim_hta_3.csv
    # If the csv file doesn't exist then it is created, otherwise we append results to the csv file
    class BacktestLoggingControl(LoggingControl):
        NAME = "BACKTEST_LOGGING_CONTROL"

        def __init__(self, *args, **kwargs):
            super(BacktestLoggingControl, self).__init__(*args, **kwargs)
            self._setup()

        def _setup(self):
            if os.path.exists("sim_hta_3.csv"):
                logging.info("Results file exists")
            else:
                with open("sim_hta_3.csv", "w") as m:
                    csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                    csv_writer.writeheader()

        def _process_cleared_orders_meta(self, event):
            orders = event.event
            with open("sim_hta_3.csv", "a") as m:
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
                            "profit": order.simulated.profit,
                            "side": order.side,
                            "elapsed_seconds_executable": order.elapsed_seconds_executable,
                            "order_status": order.status.value,
                            "market_note": order.trade.market_notes,
                            "trade_notes": order.trade.notes_str,
                            "order_notes": order.notes_str,
                        }
                        csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                        csv_writer.writerow(order_data)
                    except Exception as e:
                        logger.error(
                            "_process_cleared_orders_meta: %s" % e,
                            extra={"order": order, "error": e},
                        )

            logger.info("Orders updated", extra={"order_count": len(orders)})

        def _process_cleared_markets(self, event):
            cleared_markets = event.event
            for cleared_market in cleared_markets.orders:
                logger.info(
                    "Cleared market",
                    extra={
                        "market_id": cleared_market.market_id,
                        "bet_count": cleared_market.bet_count,
                        "profit": cleared_market.profit,
                        "commission": cleared_market.commission,
                    },
                )

    # Searches for all betfair data files within the folder sample_monthly_data_output
    data_folder = 'sample_monthly_data_output'
    data_files = os.listdir(data_folder,)
    data_files = [f'{data_folder}/{path}' for path in data_files]

    def run_process(markets):
        """Replays a Betfair historic data. Places bets according to the user defined strategy and tries to accurately simulate matching by replaying the historic data.

        Args:
            markets (list: [file paths]): a list of file paths to where the historic data is stored locally. e.g. user/zhoui/downloads/test.csv
        """    
        # Set Flumine to simulation mode
        client = clients.SimulatedClient()
        framework = FlumineSimulation(client=client)

        # Set parameters for our strategy
        strategy = FlatIggyModel(
            market_filter={
                "markets": markets,  
                'market_types':['WIN'],
                "listener_kwargs": {"inplay": False, "seconds_to_start": 80},  
                },
            max_order_exposure=1000,
            max_selection_exposure=1000,
            max_live_trade_count=1,
            max_trade_count=1,
        )
        # Run our strategy on the simulated market
        framework.add_strategy(strategy)
        framework.add_logging_control(
            BacktestLoggingControl()
        )
        framework.run()

    # Multi processing
    if __name__ == "__main__":
        all_markets = data_files  # All the markets we want to simulate
        processes = os.cpu_count()  # Returns the number of CPUs in the system.
        markets_per_process = 8   # 8 is optimal as it prevents data leakage.

        _process_jobs = []
        with futures.ProcessPoolExecutor(max_workers=processes) as p:
            # Number of chunks to split the process into depends on the number of markets we want to process and number of CPUs we have.
            chunk = min(
                markets_per_process, math.ceil(len(all_markets) / processes)
            )
            # Split all the markets we want to process into chunks to run on separate CPUs and then run them on the separate CPUs
            for m in (utils.chunks(all_markets, chunk)):
                _process_jobs.append(
                    p.submit(
                        run_process,
                        markets=m,
                    )
                )
            for job in futures.as_completed(_process_jobs):
                job.result()  # wait for result

    ```

=== "Multiprocess How to Automate IV"
    [Download from Github](https://github.com/betfair-down-under/autoHubTutorials/tree/master)

    ```py
    # Import libraries
    import glob
    import os
    import time
    import logging
    import csv
    import pandas as pd
    import json
    import math
    from pythonjsonlogger import jsonlogger
    from flumine import FlumineSimulation, BaseStrategy, utils, clients
    from flumine.order.trade import Trade
    from flumine.order.order import LimitOrder, OrderStatus
    from flumine.order.ordertype import OrderTypes
    from flumine.markets.market import Market
    from flumine.controls.loggingcontrols import LoggingControl
    from betfairlightweight.filters import streaming_market_filter
    from betfairlightweight.resources import MarketBook
    from pythonjsonlogger import jsonlogger
    from concurrent import futures

    # Logging
    logger = logging.getLogger()
    custom_format = "%(asctime) %(levelname) %(message)"
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(custom_format)
    formatter.converter = time.gmtime
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)  # Set to logging.CRITICAL to speed up simulation

    # Read in predictions from hta_4
    todays_data = pd.read_csv('backtest.csv', dtype = ({"market_id":str}))
    todays_data = todays_data.set_index(['market_id','selection_id'])

    ### New implementation
    class FlatBetting(BaseStrategy):
        def start(self) -> None:
            print("starting strategy 'FlatBetting' using the model we created the Greyhound modelling in Python Tutorial")

        def check_market_book(self, market: Market, market_book: MarketBook) -> bool:
            if market_book.status != "CLOSED":
                return True

        def process_market_book(self, market: Market, market_book: MarketBook) -> None:

            # At the 60 second mark:
            if market.seconds_to_start < 60 and market_book.inplay == False:

                # Can't simulate polling API
                # Only use streaming API:
                for runner in market_book.runners:
                    model_price = todays_data.loc[market.market_id].loc[runner.selection_id]['rating']
                    # If best available to back price is > rated price then flat $5 back
                    if runner.status == "ACTIVE" and runner.ex.available_to_back[0]['price'] > model_price:
                        trade = Trade(
                        market_id=market_book.market_id,
                        selection_id=runner.selection_id,
                        handicap=runner.handicap,
                        strategy=self,
                        )
                        order = trade.create_order(
                            side="BACK", order_type=LimitOrder(price=runner.ex.available_to_back[0]['price'], size=5.00)
                        )
                        market.place_order(order)
                    # If best available to lay price is < rated price then flat $5 lay
                    if runner.status == "ACTIVE" and runner.ex.available_to_lay[0]['price'] < model_price:
                        trade = Trade(
                        market_id=market_book.market_id,
                        selection_id=runner.selection_id,
                        handicap=runner.handicap,
                        strategy=self,
                        )
                        order = trade.create_order(
                            side="LAY", order_type=LimitOrder(price=runner.ex.available_to_lay[0]['price'], size=5.00)
                        )
                        market.place_order(order)

    # Fields we want to log in our simulations
    FIELDNAMES = [
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

    # Log results from simulation into csv file named sim_hta_4.csv
    # If the csv file doesn't exist then it is created, otherwise we append results to the csv file
    class BacktestLoggingControl(LoggingControl):
        NAME = "BACKTEST_LOGGING_CONTROL"

        def __init__(self, *args, **kwargs):
            super(BacktestLoggingControl, self).__init__(*args, **kwargs)
            self._setup()

        def _setup(self):
            if os.path.exists("sim_hta_4.csv"):
                logging.info("Results file exists")
            else:
                with open("sim_hta_4.csv", "w") as m:
                    csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                    csv_writer.writeheader()

        def _process_cleared_orders_meta(self, event):
            orders = event.event
            with open("sim_hta_4.csv", "a") as m:
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
                            "profit": order.simulated.profit,
                            "side": order.side,
                            "elapsed_seconds_executable": order.elapsed_seconds_executable,
                            "order_status": order.status.value,
                            "market_note": order.trade.market_notes,
                            "trade_notes": order.trade.notes_str,
                            "order_notes": order.notes_str,
                        }
                        csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                        csv_writer.writerow(order_data)
                    except Exception as e:
                        logger.error(
                            "_process_cleared_orders_meta: %s" % e,
                            extra={"order": order, "error": e},
                        )

            logger.info("Orders updated", extra={"order_count": len(orders)})

        def _process_cleared_markets(self, event):
            cleared_markets = event.event
            for cleared_market in cleared_markets.orders:
                logger.info(
                    "Cleared market",
                    extra={
                        "market_id": cleared_market.market_id,
                        "bet_count": cleared_market.bet_count,
                        "profit": cleared_market.profit,
                        "commission": cleared_market.commission,
                    },
                )

    # Searches for all betfair data files within the folder sample_monthly_data_output
    data_folder = 'sample_monthly_data_output'
    data_files = os.listdir(data_folder,)
    data_files = [f'{data_folder}/{path}' for path in data_files]

    def run_process(markets):
        """Replays a Betfair historic data. Places bets according to the user defined strategy and tries to accurately simulate matching by replaying the historic data.

        Args:
            markets (list: [file paths]): a list of file paths to where the historic data is stored locally. e.g. user/zhoui/downloads/test.csv
        """    
        # Set Flumine to simulation mode
        client = clients.SimulatedClient()
        framework = FlumineSimulation(client=client)

        # Set parameters for our strategy
        strategy = FlatBetting(
            market_filter={
                "markets": markets,  
                'market_types':['WIN'],
                "listener_kwargs": {"inplay": False, "seconds_to_start": 80},  
                },
            max_order_exposure=1000,
            max_selection_exposure=1000,
            max_live_trade_count=1,
            max_trade_count=1,
        )
        # Run our strategy on the simulated market
        framework.add_strategy(strategy)
        framework.add_logging_control(
            BacktestLoggingControl()
        )
        framework.run()

    # Multi processing
    if __name__ == "__main__":
        all_markets = data_files  # All the markets we want to simulate
        processes = os.cpu_count()  # Returns the number of CPUs in the system.
        markets_per_process = 8   # 8 is optimal as it prevents data leakage.

        _process_jobs = []
        with futures.ProcessPoolExecutor(max_workers=processes) as p:
            # Number of chunks to split the process into depends on the number of markets we want to process and number of CPUs we have.
            chunk = min(
                markets_per_process, math.ceil(len(all_markets) / processes)
            )
            # Split all the markets we want to process into chunks to run on separate CPUs and then run them on the separate CPUs
            for m in (utils.chunks(all_markets, chunk)):
                _process_jobs.append(
                    p.submit(
                        run_process,
                        markets=m,
                    )
                )
            for job in futures.as_completed(_process_jobs):
                job.result()  # wait for result
    
    ```

---

## Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.