# JSON to CSV tutorial: making a market summary
---

!!! note "Before you start"

    This tutorial was original shared in 2021. Since then a new library has been created that allows you to run the same logic included here with about a 97% reduction in run time, which makes a significant difference in usability. To learn about these changes and how to implement them to speed up your code take a look at our [JSON to CSV revisited article](../jsonToCsvRevisited).

The historic pricing data available on the [Betfair Historic Data site](https://historicdata.betfair.com/#/home) is an excellent resource, including almost every market offered on the Exchange back to 2016. We do appreciate though that the JSON format of the data sets can make it challenging to find value in the data, especially if you're not confident in working with large data sets. 

In this tutorial we're going to step through the process of using the Python `betfairlightweight` library to take in a compressed tar folder, process the historic JSON files, and convert the data into a simple csv output, including basic market summary data for each runner split into pre play and in play values. We're also going to include a filter function, to allow us to filter out markets we're not interested in. 

The idea of this tutorial is to share a way of using existing libraries to make working with the JSON data sets easier, and hopefully the provide a foundation that you can build your own code base and data sets from. We'll be focusing on horse racing data; what we want to produce is a csv output that includes one row per runner for each market we're interested in, along with summary pre-play and in-play data for the runner. We'll step through the issues we encountered and how we went about solving the various challenges, including sharing relevant code snips along the way. 

We're not Python natives and acknowledge that there are probably more efficient and neater ways of achieving the same end goal! As always please [reach out](mailto:automation@betfair.com.au) with feedback, suggestions or queries, or feel free to submit a [pull request](https://github.com/betfair-down-under/autoHubTutorials/blob/master/jsonToCsv/main.py) if you catch some bugs or have other improvements! 

!!! note "Cheat sheet"
    - If you're looking for the complete code [head to the bottom of the page](https://betfair-datascientists.github.io/tutorials/jsonToCsvTutorial/#sample-code) or [download the script from Github](https://github.com/betfair-down-under/autoHubTutorials/blob/master/jsonToCsv/main.py).

    - To run the code, save it to your machine, open a command prompt, or a terminal in your text editor of choice (we're using [VS code](https://code.visualstudio.com/download)), make sure you've navigated in the terminal to the folder you've saved the script in and then type `py main.py` (or whatever you've called your script file if not main) then hit enter. To stop the code running use Ctrl C. 

    - The script will take some time before it starts outputting to the output.csv file, so let it run for a few minutes before getting worried that it's not working!

    - Make sure you amend your data path to point to your data file (instructions below). We'll be taking in an input of a historical tar file downloaded from the [Betfair historic data site](https://historicdata.betfair.com/#/help). We're using a PRO version, though the code should work on ADVANCED too. This approach won't work with the BASIC data tier. 

    - We're using the [`betfairlightweight`](https://github.com/liampauling/betfair/tree/master/betfairlightweight) package to do the heavy lifting

    - We've also posted the completed code logic on the [`betfair-downunder` Github repo](https://github.com/betfair-down-under/autoHubTutorials/blob/master/jsonToCsv/main.py).

---
### Setting up your environment

You're going to need to make sure you have [Python](https://www.python.org/downloads/) and [pip](https://pypi.org/project/pip/) installed to get this code to run. If you're just starting out with Python, you may have to add Python to [your environment variables](https://www.educative.io/edpresso/how-to-add-python-to-path-variable-in-windows). The is generally easiest to do by checking the box when you're installing Python choosing to 'add to PATH'. 

The alternative approach to the above is to use a [Jupyter notebook](https://jupyter.org/) which has the environment already set up - this might be the easier option for people new to programming. 

We're using some pretty new Python features, so it might be worth [checking your version](https://phoenixnap.com/kb/check-python-version) and updating if you're keen to follow along. 

To install `betfairlightweight` open a command prompt, or a terminal in your text editor of choice and input `pip install betfairlightweight` then return. 

---
### Data input

We started with the [historic data parsing example](https://github.com/liampauling/betfair/blob/master/examples/examplestreaminghistorical.py) from [liampauling](https://github.com/liampauling)'s Github repo. 

Our first issue was that the example provided was expecting to take in an individual market file. We wanted to be able to accept data in a tar archive, a zipped folder, or a directory of individual bz2 files.

Here's the code we used for handling the different file formats. 

``` Python
# loading from tar and extracting files
def load_markets(file_paths: List[str]):
    for file_path in file_paths:
        if os.path.isdir(file_path):
            for path in glob.iglob(file_path + '**/**/*.bz2', recursive=True):
                f = bz2.BZ2File(path, 'rb')
                yield f
                f.close()
        elif os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1]
            # iterate through a tar archive
            if ext == '.tar':
                with tarfile.TarFile(file_path) as archive:
                    for file in archive:
                        yield bz2.open(archive.extractfile(file))
            # or a zip archive
            elif ext == '.zip':
                with zipfile.ZipFile(file_path) as archive:
                    for file in archive.namelist():
                        yield bz2.open(archive.open(file))
        
    return None
```

and then used it like this:

``` Python
# the path directories to the data sets
# accepts tar files, zipped files or 
# directory with bz2 file(s)
market_paths = [
    './2020_12_DecRacingPro.zip',
    './PRO',
    './2021_01_JanRacingPro.tar'
]

... 

for file_obj in load_markets(market_paths):
    stream = trading.streaming.create_historical_generator_stream(
        file_path=file_obj,
        listener=listener,
    )

    def get_pre_post_final(s):
        with patch("builtins.open", lambda f, _: f):  
```

This means we can pass in the tar and/or zipped file in its compressed form and/or directory with individual bz2 files in it and not worry about extracting the file contents, or having to handle the logic of iterating over the inner nested file structure. 

!!! note "File paths"
    The program will look at the file path you pass in relative to the location of the script you're running. So it will start by looking in the same folder it's saved in and then follow your navigation instructions from there, using `/` to indicate a folder and `../` to navigate up a level in the folder structure. 

    If our example the data files sit in the same folder as the script (`./PRO`).

    If it were in a folder at the same level as the folder that our script is in then we'd need to navigate 'up' a level (using `../`) and then into the folder housing the data, i.e. `'../dataFolder/PRO'` and if the data were in a different folder within the same folder as our script file we'd use `'./dataFolder/PRO'` etc.

---
### Type definitions 

If you're used to working in strongly typed languages, especially those with type definitions, you might find it a bit frustrating to try and figure out where you can access the different data types, for example market name or runner BSP. There are some things you can do to make this a bit easier, other than digging into the `betfairlightweight` source code, which was where we started. 

If you want to look at the definitions from the source code:

- [`MarketBook, RunnerBook`](https://github.com/liampauling/betfair/blob/f370d111d2e7adf1ca4221fc8cc4b028e4b2b2f8/betfairlightweight/resources/bettingresources.py#L466)
- [`MarketDefinitionRunner, MarketDefinition`](https://github.com/liampauling/betfair/blob/f370d111d2e7adf1ca4221fc8cc4b028e4b2b2f8/betfairlightweight/resources/streamingresources.py#L32)

There are some Python extensions you can use in your ide that go some way to helping here. 

``` Python
# importing data types
import betfairlightweight
from betfairlightweight.resources.bettingresources import (
    PriceSize,
    MarketBook
)
```

---
### Market summary data 

The raw files show the data at 50ms (PRO) or 1 second (ADVANCED) intervals. Too produce our csv we will need to look at the state of the market before the market goes in play, and then the state at the end of the market, and calculate from that what the pre play and in play figures are. 

This is the data we're going to include in our output csv.

|**Column**     |**Definition**    
|:------------  |:---------------       
|market_id      |unique market identifier   
|event_date     |scheduled start date/time (UTC)
|country        |event country code
|track          |track name
|market_name    |market name
|selection_id   |unique runner identifier
|selection_name |runner name
|result         |win/loss/removed
|bsp            |Betfair starting price
|pp_min         |pre play min price traded
|pp_max         |pre play max price traded
|pp_wap         |pre play weighted average price
|pp_ltp         |pre play last traded price
|pp_volume      |pre play matched volume
|ip_min         |in play min price traded
|ip_max         |in play max price traded
|ip_wap         |in play weighted average price
|ip_ltp         |in play last traded price
|ip_volume      |in play matched volume

`betfairlightweight` exposes snapshots of the market that include all the price data we need. To allow us to compute pre play and in play figures there are three market snapshots we need to find. These are the final view before the market turns in play, the market at the end of the race once it's no longer open but the price ladder hasn't yet been cleared, and the final closed snapshot that shows winner/loser status etc. We can then use the deltas between these market views to calculate the pre play and in play summary statistics. 

We iterate over these market snapshots and when we find the first market showing as in play we go back to the previous update, and use this as our pre play view. After this we keep iterating until we find the last time that the market status shows as 'open' and then use the data from the following update for the final pricing data (i.e. the first market view once the market was suspended at the end of the race). The winner/loser statuses come from the final market view. 

``` Python
def get_pre_post_final(s):
    with patch("builtins.open", lambda f, _: f):   
        eval_market = None
        prev_market = None
        preplay_market = None
        postplay_market = None       

        gen = stream.get_generator()
        
        for market_books in gen():
            for market_book in market_books:

                # if market doesn't meet filter return out
                if eval_market is None and ((eval_market := filter_market(market_book)) == False):
                    return (None, None, None)
                
                # final market view before market goes in play
                if prev_market is not None and prev_market.inplay != market_book.inplay:
                    preplay_market = prev_market
                
                # final market view at the conclusion of the market
                if prev_market is not None and prev_market.status == "OPEN" and market_book.status != prev_market.status:
                    postplay_market = market_book
                
                # update reference to previous market
                prev_market = market_book
        
        return (preplay_market, postplay_market, prev_market) # prev is now final
    
(preplay_market, postplay_market, final_market) = get_pre_post_final(stream)
```

We needed to write a function to parse the price data (pre play and in play) and pull out the values we're interested in. We used a reduce function to go over each matched price point, and calculate the four necessary values. 

To calculate weighted average price we multiplied price by size for each price point, and added them together. Once they're summed, we divided that figure by the total matched value. 

The matched volume is simply the sum of all matched stakes. 

The min price and max price are the lowest and highest values where money has matched on the runner.

!!! note "Reduce functions"
    I gather from some actual Python gurus in our community that while reduce functions are very common in other languages (i.e. the ones I normally work in!), apparently they're not very Pythonic... if you're super keen, feel free to rewrite this section into a list/dict comprehension or another more Pythonic solution!

``` Python
# parsing price data and pulling out weighted avg price, matched, min price and max price
def parse_traded(traded: List[PriceSize]) -> (float, float, float, float):
    if len(traded) == 0: 
        return (None, None, None, None)
     
    (wavg_sum, matched, min_price, max_price) = functools.reduce(
        lambda total, ps: (
            total[0] + (ps.price * ps.size), # wavg_sum before we divide by total matched
            total[1] + ps.size, # total matched
            min(total[2], ps.price), # min price matched
            max(total[3], ps.price), # max price matched
        ),
        traded,
        (0, 0, 1001, 0) # starting default values
    )

    wavg_sum = (wavg_sum / matched) if matched > 0 else None # dividing sum of wavg by total matched
    matched = matched if matched > 0 else None 
    min_price = min_price if min_price != 1001 else None
    max_price = max_price if max_price != 0 else None

    return (wavg_sum, matched, min_price, max_price)
```

Our volume figures don't include BSP bets yet, so to account for that we're looking at the `back_stake_taken` and `lay_liability_taken` values on the SP object from the post play market snapshot, then finding whichever the smaller of those two values is and saving it that so we can add it to the `traded_volume` field in a later step. We use the smaller value of `back_stake_taken` or (`lay_liability_taken`/(BSP - 1)) (i.e. backer's stake for SP lay bets) as any difference between the two values will have matched against non-BSP money and therefore is already accounted for in our matched volume. 

``` Python
preplay_traded = [ (r.last_price_traded, r.ex.traded_volume) for r in preplay_market.runners ] if preplay_market is not None else None
postplay_traded = [ (
    r.last_price_traded,
    r.ex.traded_volume,
    # calculating SP traded vol as smaller of back_stake_taken or (lay_liability_taken / (BSP - 1))        
    min_gr0(
        next((pv.size for pv in r.sp.back_stake_taken if pv.size > 0), 0),
        next((pv.size for pv in r.sp.lay_liability_taken if pv.size > 0), 0)  / ((r.sp.actual_sp if (type(r.sp.actual_sp) is float) or (type(r.sp.actual_sp) is int) else 0) - 1)
    )
) for r in postplay_market.runners ]
```

For our csv, we have columns for runner id, runner name, winning status and BSP, so we'll store these values too. The runner name is a bit harder to get, as we need to match up the runner definition with the same `selection_id` as the `market_book` object we're currently looking at.

``` Python
# generic runner data
    runner_data = [
        {
            'selection_id': r.selection_id,
            'selection_name': next((rd.name for rd in final_market.market_definition.runners if rd.selection_id == r.selection_id), None),
            'selection_status': r.status,
            'sp': as_str(r.sp.actual_sp),
        }
        for r in final_market.runners 
    ]
```

Not all markets go in play, and therefore won't have any values for the in play portion of the csv, so we need to make sure we can handle this case.

We don't have in play figures separate to pre play; we have a snapshot before the market went in play, and then the view at the end of the market, so we need to use the difference between these two sets of figures to figure out what happened in play.

We have two ladders, one post play and one pre play. We go through every price point in the post play ladder, and remove any volume that's showing in the pre play ladder at the corresponding price point. This leaves us with the volumes matched while the market was in play. 

One corner case we had to catch is that our resulting list might have prices with 0 volume, which trip up our min and max values, which doesn't use volume in its calculations. To catch this we filter out any items from the ladder with a volume of 0.

Note: there are some markets included in the data files that are effective empty and don't contain any price data. We're disregarding these markets and printing out an error message to the log (`market has no price data`).

``` Python
# runner price data for markets that go in play
if preplay_traded is not None:
    def runner_vals(r):
        (pre_ltp, pre_traded), (post_ltp, post_traded, sp_traded) = r

        inplay_only = list(filter(lambda ps: ps.size > 0, [
            PriceSize(
                price=post_ps.price, 
                size=post_ps.size - next((pre_ps.size for pre_ps in pre_traded if pre_ps.price == post_ps.price), 0)
            )
            for post_ps in post_traded 
        ]))

        (ip_wavg, ip_matched, ip_min, ip_max) = parse_traded(inplay_only)
        (pre_wavg, pre_matched, pre_min, pre_max) = parse_traded(pre_traded)

        return {
            'preplay_ltp': as_str(pre_ltp),
            'preplay_min': as_str(pre_min),
            'preplay_max': as_str(pre_max),
            'preplay_wavg': as_str(pre_wavg),
            'preplay_matched': as_str((pre_matched or 0) + (sp_traded or 0)),
            'inplay_ltp': as_str(post_ltp),
            'inplay_min': as_str(ip_min),
            'inplay_max': as_str(ip_max),
            'inplay_wavg': as_str(ip_wavg),
            'inplay_matched': as_str(ip_matched),
        }

    runner_traded = [ runner_vals(r) for r in zip_longest(preplay_traded, postplay_traded, fillvalue=PriceSize(0, 0)) ]

# runner price data for markets that don't go in play
else:
    def runner_vals(r):
        (ltp, traded, sp_traded) = r
        (wavg, matched, min_price, max_price) = parse_traded(traded)

        return {
            'preplay_ltp': as_str(ltp),
            'preplay_min': as_str(min_price),
            'preplay_max': as_str(max_price),
            'preplay_wavg': as_str(wavg),
            'preplay_matched': as_str((matched or 0) + (sp_traded or 0)),
            'inplay_ltp': '',
            'inplay_min': '',
            'inplay_max': '',
            'inplay_wavg': '',
            'inplay_matched': '',
        }
    
    runner_traded = [ runner_vals(r) for r in postplay_traded ]
```

---
### Writing to CSV

We defined the columns we want for our csv pretty early in the code. 

``` Python
# record prices to a file
with open("output.csv", "w") as output:
    # defining column headers
    output.write("market_id,event_date,country,track,market_name,selection_id,selection_name,result,bsp,pp_min,pp_max,pp_wap,pp_ltp,pp_volume,ip_min,ip_max,ip_wap,ip_ltp,ip_volume\n")
```

We then assign the values for each column.

``` Python
# printing to csv for each runner
for (rdata, rprices) in zip(runner_data, runner_traded):
    # defining data to go in each column
    output.write(
        "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
            postplay_market.market_id,
            postplay_market.market_definition.market_time,
            postplay_market.market_definition.country_code,
            postplay_market.market_definition.venue,
            postplay_market.market_definition.name,
            rdata['selection_id'],
            rdata['selection_name'],
            rdata['selection_status'],
            rdata['sp'],
            rprices['preplay_min'],
            rprices['preplay_max'],
            rprices['preplay_wavg'],
            rprices['preplay_ltp'],
            rprices['preplay_matched'],
            rprices['inplay_min'],
            rprices['inplay_max'],
            rprices['inplay_wavg'],
            rprices['inplay_ltp'],
            rprices['inplay_matched'],
        )
    )
```

---
### Filtering markets

Currently we're going through every file provided in the raw data folders, which in our case included markets from different countries, all different market types and both gallops and harness races. To save filtering these markets manually later in Excel, and also to avoid processing additional data we don't need and slowing the process down further, we decided to add a market filter so we only kept the markets we were interested in.

We filtered on three things:

- event country code (i.e. AU, NZ, GB etc)
- market type (i.e. win, place etc)
- race type (i.e. gallops or harness)

Using this logic, we are only keeping Australian win markets for gallops races.

``` Python
# filtering markets to those that fit the following criteria
def filter_market(market: MarketBook) -> bool: 
    d = market.market_definition
    return (d.country_code == 'AU' 
        and d.market_type == 'WIN' 
        and (c := split_anz_horse_market_name(d.name)[2]) != 'trot' and c != 'pace')
```

Filtering out harness markets was the trickiest part of the process, as there's no neat way of separating harness meetings from gallops. To do this we had to parse the market name and look for the words 'trot' and 'pace', and treat the market as harness if we found either. To make it a little tidier we wrote a function to split the market name into its component parts. 

``` Python
# splitting race name and returning the parts 
def split_anz_horse_market_name(market_name: str) -> (str, str, str):
    # return race no, length, race type
    # input samples: 
    # 'R6 1400m Grp1' -> ('R6','1400m','grp1')
    # 'R1 1609m Trot M' -> ('R1', '1609m', 'trot')
    # 'R4 1660m Pace M' -> ('R4', '1660m', 'pace')
    parts = market_name.split(' ')
    race_no = parts[0] 
    race_len = parts[1] 
    race_type = parts[2].lower()

    return (race_no, race_len, race_type)
```

We declare an `evaluate_market` flag and set it to none, and then in our loop the first time we evaluate the market we run the filter and skip any markets that don't meet our criteria.

``` Python
eval_market = None

gen = stream.get_generator()

for market_books in gen():
    for market_book in market_books:

        # if market doesn't meet filter return out
        if eval_market is None and ((eval_market := filter_market(market_book)) == False):
            return (None, None, None)
```

---
### Helper functions

There are a couple of helper functions we wrote along the way to make the rest of the code easier to handle. 

**As string**

Takes in a number and returns a text representation of it, rounding to two decimal places. 

``` Python
# rounding to 2 decimal places or returning '' if blank
def as_str(v) -> str:
    return '%.2f' % v if (type(v) is float) or (type(v) is int) else v if type(v) is str else ''
```

**Min value greater than 0**

Returns the smaller of two numbers, where the smaller isn't 0. 

``` Python
# returning smaller of two numbers where min not 0
def min_gr0(a: float, b: float) -> float:
    if a <= 0:
        return b
    if b <= 0:
        return a
    
    return min(a, b)
```

---
### Final thoughts

`betfairlightweight` provides a ready made package that makes it easier to work with the JSON data and a pretty easy way to convert the data into a csv format, allowing you to then do your data wrangling in Excel if that's where you're more comfortable. 

Our intention is that you don't need a heap of Python experience to be able to work through this tutorial; as long as you're prepared to get the Python environment set up and learn some basic programming skills, the hope is that you'll be able to customise your own csv file and maybe even extend on what we've covered and produced here.

We're planning on writing some more tutorials to help make it easier to work with the JSON data sets. If there are particular examples or data sets you'd like to see us walk through [please reach out](mailto:automation@betfair.com.au).

!!! note "Community support"
    - There's a really active [Betcode (formerly Betfairlightweight) slack group](https://betcode-org.slack.com/ssb/redirect) that's a great place to go to ask questions about the library and get support from other people who are also working in the space

--- 
### Complete code

Run the code from your ide by using `py <filename>.py`, making sure you amend the path to point to your input data. Please note: the script will take some time before it starts outputting to the output.csv file, so let it run for a few minutes before getting worried that it's not working! You'll also see errors logged to the out file or terminal screen depending on your set up. 

[Download from Github](https://github.com/betfair-down-under/autoHubTutorials/blob/master/jsonToCsv/main.py)

``` Python
import logging
from typing import List, Tuple

from unittest.mock import patch
from itertools import zip_longest
import functools

import os
import tarfile
import zipfile
import bz2
import glob

# importing data types
import betfairlightweight
from betfairlightweight.resources.bettingresources import (
    PriceSize,
    MarketBook 
)

file_output = "output_bflw.csv"

market_paths = [
    "data/2021_10_OctRacingAUPro.tar",
    "data/2021_11_NovRacingAUPro.tar",
    "data/2021_12_DecRacingAUPro.tar",
]

# setup logging
logging.basicConfig(level=logging.FATAL)

# create trading instance (don't need username/password)
trading = betfairlightweight.APIClient("username", "password", "appkey")

# create listener
listener = betfairlightweight.StreamListener(
    max_latency=None,   # ignore latency errors
    output_queue=None,  # use generator rather than a queue (faster)
    lightweight=False,  # lightweight mode is faster
    update_clk=False,   # do not update clk on updates (not required when backtesting)

    cumulative_runner_tv=True, 
    calculate_market_tv=True
)

# loading from tar and extracting files
def load_markets(file_paths: List[str]):
    for file_path in file_paths:
        if os.path.isdir(file_path):
            for path in glob.iglob(file_path + '**/**/*.bz2', recursive=True):
                f = bz2.BZ2File(path, 'rb')
                yield f
                f.close()
        elif os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1]
            # iterate through a tar archive
            if ext == '.tar':
                with tarfile.TarFile(file_path) as archive:
                    for file in archive:
                        yield bz2.open(archive.extractfile(file))
            # or a zip archive
            elif ext == '.zip':
                with zipfile.ZipFile(file_path) as archive:
                    for file in archive.namelist():
                        yield bz2.open(archive.open(file))
    return None

# rounding to 2 decimal places or returning '' if blank
def as_str(v) -> str:
    return '%.2f' % v if (type(v) is float) or (type(v) is int) else v if type(v) is str else ''

# returning smaller of two numbers where min not 0
def min_gr0(a: float, b: float) -> float:
    if a <= 0:
        return b
    if b <= 0:
        return a

    return min(a, b)

# parsing price data and pulling out weighted avg price, matched, min price and max price
def parse_traded(traded: List[PriceSize]) -> Tuple[float, float, float, float]:
    if len(traded) == 0: 
        return (None, None, None, None)

    (wavg_sum, matched, min_price, max_price) = functools.reduce(
        lambda total, ps: (
            total[0] + (ps.price * ps.size), # wavg_sum before we divide by total matched
            total[1] + ps.size, # total matched
            min(total[2], ps.price), # min price matched
            max(total[3], ps.price), # max price matched
        ),
        traded,
        (0, 0, 1001, 0) # starting default values
    )

    wavg_sum = (wavg_sum / matched) if matched > 0 else None # dividing sum of wavg by total matched
    matched = matched if matched > 0 else None 
    min_price = min_price if min_price != 1001 else None
    max_price = max_price if max_price != 0 else None

    return (wavg_sum, matched, min_price, max_price)

# splitting race name and returning the parts 
def split_anz_horse_market_name(market_name: str) -> Tuple[str, str, str]:
    # return race no, length, race type
    # input samples: 
    # 'R6 1400m Grp1' -> ('R6','1400m','grp1')
    # 'R1 1609m Trot M' -> ('R1', '1609m', 'trot')
    # 'R4 1660m Pace M' -> ('R4', '1660m', 'pace')
    parts = market_name.split(' ')
    race_no = parts[0] 
    race_len = parts[1] 
    race_type = parts[2].lower() 

    return (race_no, race_len, race_type)

# filtering markets to those that fit the following criteria
def filter_market(market: MarketBook) -> bool: 
    d = market.market_definition
    return (d != None
        and d.country_code == 'AU' 
        and d.market_type == 'WIN' 
        and (c := split_anz_horse_market_name(d.name)[2]) != 'trot' and c != 'pace')

# record prices to a file
with open(file_output, "w") as output:
    # defining column headers
    output.write("market_id,event_date,country,track,market_name,selection_id,selection_name,result,bsp,pp_min,pp_max,pp_wap,pp_ltp,pp_volume,ip_min,ip_max,ip_wap,ip_ltp,ip_volume\n")

    for i, file_obj in enumerate(load_markets(market_paths)):
        print("Market {}".format(i), end='\r')

        stream = trading.streaming.create_historical_generator_stream(
            file_path=file_obj,
            listener=listener,
        )

        def get_pre_post_final(s):
            with patch("builtins.open", lambda f, _: f):   
                eval_market = None
                prev_market = None
                preplay_market = None
                postplay_market = None       

                gen = stream.get_generator()

                for market_books in gen():
                    for market_book in market_books:
                        # if market doesn't meet filter return out
                        if eval_market is None and ((eval_market := filter_market(market_book)) == False):
                            return (None, None, None)

                        # final market view before market goes in play
                        if prev_market is not None and prev_market.inplay != market_book.inplay:
                            preplay_market = prev_market

                        # final market view at the conclusion of the market
                        if prev_market is not None and prev_market.status == "OPEN" and market_book.status != prev_market.status:
                            postplay_market = market_book

                        # update reference to previous market
                        prev_market = market_book

                return (preplay_market, postplay_market, prev_market) # prev is now final

        (preplay_market, postplay_market, final_market) = get_pre_post_final(stream)

        # no price data for market
        if postplay_market is None:
            continue; 

        preplay_traded = [ (r.last_price_traded, r.ex.traded_volume) for r in preplay_market.runners ] if preplay_market is not None else None
        postplay_traded = [ (
            r.last_price_traded,
            r.ex.traded_volume,
            # calculating SP traded vol as smaller of back_stake_taken or (lay_liability_taken / (BSP - 1))        
            min_gr0(
                next((pv.size for pv in r.sp.back_stake_taken if pv.size > 0), 0),
                next((pv.size for pv in r.sp.lay_liability_taken if pv.size > 0), 0)  / ((r.sp.actual_sp if (type(r.sp.actual_sp) is float) or (type(r.sp.actual_sp) is int) else 0) - 1)
            ) if r.sp.actual_sp is not None else 0,
        ) for r in postplay_market.runners ]

        # generic runner data
        runner_data = [
            {
                'selection_id': r.selection_id,
                'selection_name': next((rd.name for rd in final_market.market_definition.runners if rd.selection_id == r.selection_id), None),
                'selection_status': r.status,
                'sp': as_str(r.sp.actual_sp),
            }
            for r in final_market.runners 
        ]

        # runner price data for markets that go in play
        if preplay_traded is not None:
            def runner_vals(r):
                (pre_ltp, pre_traded), (post_ltp, post_traded, sp_traded) = r

                inplay_only = list(filter(lambda ps: ps.size > 0, [
                    PriceSize(
                        price=post_ps.price, 
                        size=post_ps.size - next((pre_ps.size for pre_ps in pre_traded if pre_ps.price == post_ps.price), 0)
                    )
                    for post_ps in post_traded 
                ]))

                (ip_wavg, ip_matched, ip_min, ip_max) = parse_traded(inplay_only)
                (pre_wavg, pre_matched, pre_min, pre_max) = parse_traded(pre_traded)

                return {
                    'preplay_ltp': as_str(pre_ltp),
                    'preplay_min': as_str(pre_min),
                    'preplay_max': as_str(pre_max),
                    'preplay_wavg': as_str(pre_wavg),
                    'preplay_matched': as_str((pre_matched or 0) + (sp_traded or 0)),
                    'inplay_ltp': as_str(post_ltp),
                    'inplay_min': as_str(ip_min),
                    'inplay_max': as_str(ip_max),
                    'inplay_wavg': as_str(ip_wavg),
                    'inplay_matched': as_str(ip_matched),
                }

            runner_traded = [ runner_vals(r) for r in zip_longest(preplay_traded, postplay_traded, fillvalue=PriceSize(0, 0)) ]

        # runner price data for markets that don't go in play
        else:
            def runner_vals(r):
                (ltp, traded, sp_traded) = r
                (wavg, matched, min_price, max_price) = parse_traded(traded)

                return {
                    'preplay_ltp': as_str(ltp),
                    'preplay_min': as_str(min_price),
                    'preplay_max': as_str(max_price),
                    'preplay_wavg': as_str(wavg),
                    'preplay_matched': as_str((matched or 0) + (sp_traded or 0)),
                    'inplay_ltp': '',
                    'inplay_min': '',
                    'inplay_max': '',
                    'inplay_wavg': '',
                    'inplay_matched': '',
                }

            runner_traded = [ runner_vals(r) for r in postplay_traded ]

        # printing to csv for each runner
        for (rdata, rprices) in zip(runner_data, runner_traded):
            # defining data to go in each column
            output.write(
                "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                    postplay_market.market_id,
                    postplay_market.market_definition.market_time,
                    postplay_market.market_definition.country_code,
                    postplay_market.market_definition.venue,
                    postplay_market.market_definition.name,
                    rdata['selection_id'],
                    rdata['selection_name'],
                    rdata['selection_status'],
                    rdata['sp'],
                    rprices['preplay_min'],
                    rprices['preplay_max'],
                    rprices['preplay_wavg'],
                    rprices['preplay_ltp'],
                    rprices['preplay_matched'],
                    rprices['inplay_min'],
                    rprices['inplay_max'],
                    rprices['inplay_wavg'],
                    rprices['inplay_ltp'],
                    rprices['inplay_matched'],
                )
            )
```

---
### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.