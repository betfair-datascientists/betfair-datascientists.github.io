# JSON to CSV tutorial: producing a market summary

---
The historic pricing data available on the [Betfair Historic Data site](https://historicdata.betfair.com/#/home) is an excellent resource, including almost every market offered on the Exchange back to 2016. We do appreciate though that the JSON format of the data sets can make it challenging to find value in the data, especially if you're not confident in working with large data sets. 

In this tutorial we're going to step through the process of using `betfairlightweight` to take in a compressed tar folder, process the historic JSON files, and convert the data into a simple csv output, including basic market summary data for each runner split into pre play and in play values. We're also going to include a filter function, to allow us to filter out markets we're not interested in. 

The idea of this tutorial is to share a way of using existing libraries to make working with the JSON data sets easier, and hopefully the provide a foundation that you can build your own code base and data sets from. We'll be focusing on horse racing data; what we want to produce is a csv output that includes one row per runner for each market we're interested in, along with summary pre-play and in-play data for the runner. We'll step through the issues we encountered and how we went about solving the various challenges, including sharing relevant code snips along the way. 

<!-- We've also posted the completed code logic on the [`betfair-downunder`]() Github repo.

TODO -->

We're not Python natives and acknowledge that there are probably more efficient and neater ways of achieving the same end goal! As always please [reach out](mailto:data@betfair.com.au) with feedback, suggestions or queries. 

!!! note "Resources"
    - We'll be taking in an input of a historical tar file downloaded from the [Betfair historic data site](https://historicdata.betfair.com/#/help). We're using a PRO version, though the code should work on ADVANCED too.

    - We're using the [`betfairlightweight`](https://github.com/liampauling/betfair/tree/master/betfairlightweight) package to do the heavy lifting

---
### Setting up your environment

You're going to need to make sure you have [Python](https://www.python.org/downloads/) and [pip](https://pypi.org/project/pip/) installed to get this code to run. If you're just starting out with Python, you may have to add Python to your environment variables. We're using some pretty new Python features, so it might be worth [checking your version](https://phoenixnap.com/kb/check-python-version) and updating if you're keen to follow along. 

Open a command prompt, or a terminal in your text editor of choice (we're using [VS code](https://code.visualstudio.com/download)) and input `pip install betfairlightweight`

---
### Data input

We started with the [historic data parsing example](https://github.com/liampauling/betfair/blob/master/examples/examplestreaminghistorical.py) from [liampauling](https://github.com/liampauling)'s Github repo. 

Our first issue was that the example provided was expecting to take in an individual market file. We wanted to be able to accept data in a tar or zipped folder, or a set of individual bz2 files.

``` Python
# the path directories to the data sets
# accepts tar files, zipped files or 
# directory with bz2 file(s)
market_paths = [
    '../_data/2020_12_DecRacingPro.zip',
    '../_data/PRO',
    '../_data/2021_01_JanRacingPro.tar'
]

# loading from tar and extracting files
def load_markets(file_paths: List[str]):
    for file_path in file_paths:
        print(file_path)
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
for file_obj in load_markets(market_paths):
    stream = trading.streaming.create_historical_generator_stream(
        file_path=file_obj,
        listener=listener,
    )

    with patch("builtins.open", lambda f, _: f):  
```

This means we can pass in the tar and/or zipped file in its compressed form and/or directory with individual bz2 files in it and not worry about extracting the file contents, or having to handle the logic of iterating over the inner nested file structure. 

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

This is the logic we used to identify the last market view before the market went in play, and the final market view. We determined the last market pre play by comparing the in play status, and when we found a market that was in play we took our pre play data from the previous market version. Similarly, we took the final in play data from the last market view where the market status showed as 'open'.

``` Python
# final market view before market goes in play
if preplay_market is not None and preplay_market.inplay != market_book.inplay:
    preplay_traded = [ (r.last_price_traded, r.ex.traded_volume.copy()) for r in preplay_market.runners ]
preplay_market = market_book

# final market view at the conclusion of the market
if postplay_market is not None and postplay_market.status == "OPEN" and market_book.status != postplay_market.status:
    postplay_traded = [ (r.last_price_traded, r.ex.traded_volume.copy()) for r in market_book.runners ]
postplay_market = market_book   
```

We needed to write a function to parse the price data (pre play and in play) and pull out the values we're interested in. We used a reduce function to go over each matched price point, and calculate the four necessary values.

To calculate weighted average price we multiplied price by size for each price point, and added them together. Once they're summed, we divided that figure by the total matched value. 

The matched volume is simply the sum of all matched stakes. 

The min price and max price are the lowest and highest values where money has matched on the runner.

``` Python
# parsing price data and pulling out weighted avg price, 
# matched volume, min matched price and max matched price
def parse_traded(traded: List[PriceSize]) -> (float, float, float, float):
    if len(traded) == 0: 
        return (None, None, None, None)
     
    (wavg_sum, matched, min_price, max_price) = functools.reduce(
        lambda total, ps: (
            total[0] + (ps.price * ps.size), # wavg_sum
            total[1] + ps.size, # matched
            min(total[2], ps.price), # min_price
            max(total[3], ps.price), # max_price
        ),
        traded,
        (0, 0, 1001, 0)
    )

    wavg_sum = (wavg_sum / matched) if matched > 0 else None
    matched = matched if matched > 0 else None
    min_price = min_price if min_price != 1001 else None
    max_price = max_price if max_price != 0 else None

    return (wavg_sum, matched, min_price, max_price)
```

For our csv, we have columns for runner id, runner name, winning status and BSP, so we'll store these values too. The runner name is a bit harder to get, as we need to match up the runner definition with the same `selection_id` as the `market_book` object we're currently looking at.

``` Python
# runner data
runner_data = [
    {
        'selection_id': r.selection_id,
        'selection_name': next((rd.name for rd in postplay_market.market_definition.runners if rd.selection_id == r.selection_id), None),
        'selection_status': r.status,
        'sp': as_str(r.sp.actual_sp),
    }
    for r in postplay_market.runners 
]
```

Not all markets go in play, and therefore won't have any values for the in play portion of the csv, so we need to make sure we can handle this case.

We don't have in play figures separate to pre play; we have a snapshot before the market went in play, and then the view at the end of the market, so we need to use the difference between these two sets of figures to figure out what happened in play.

We have two ladders, one post play and one pre play. We go through every price point in the post play ladder, and remove any volume that's showing in the pre play ladder at the corresponding price point. This leaves us with the volumes matched while the market was in play. 

One corner case we had to catch is that our resulting list might have prices with 0 volume, which trip up our min and max values, which doesn't use volume in its calculations. To catch this we filter out any items from the ladder with a volume of 0.

``` Python
# runner price data for markets that go in play
if preplay_traded is not None:
    def runner_vals(r):
        (pre_ltp, pre_traded), (post_ltp, post_traded) = r

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
            'preplay_matched': as_str(pre_matched),
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
        (ltp, traded) = r
        (wavg, matched, min_price, max_price) = parse_traded(traded)

        return {
            'preplay_ltp': as_str(ltp),
            'preplay_min': as_str(min_price),
            'preplay_max': as_str(max_price),
            'preplay_wavg': as_str(wavg),
            'preplay_matched': as_str(matched),
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

Currently we're going through every file provided in the raw data folders, which in our case included markets from different countries, all different market types and both gallops and harness races. To save filtering these markets manually later in Excel, and also to avoid processing additional data we don't need and slowing the process down, we decided to add a market filter so we only kept the markets we were interested in.

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
    # input sample: R6 1400m Grp1
    parts = market_name.split(' ')
    race_no = parts[0] # return example R6
    race_len = parts[1] # return example 1400m
    race_type = parts[2].lower() # return example grp1, trot, pace

    return (race_no, race_len, race_type)
```

We set an `evaluate_market` flag to `false`, ran the filter and skipped any markets that didn't meet our criteria, and set the flag to `true` for any that did.

``` Python
evaluate_market = False         

for market_books in gen():
    for market_book in market_books:
        
        # skipping markets that don't meet the filter
        if evaluate_market == False and filter_market(market_book) == False:
            continue
        else:
            evaluate_market = True
```

<!-- ---
### Comparing the results

We ran our code over the January 2021 JSON data and compared our output with the equivalent data set produced monthly by our in house reporting team from our database. Here's a sample of the two outputs to see how similar they are.  -->

---
### Final thoughts

`betfairlightweight` provides a ready made package that makes it easier to work with the JSON data and a pretty easy way to convert the data into a csv format, allowing you to then do your data wrangling in Excel if that's where you're more comfortable. 

Our intention is that you don't need a heap of Python experience to be able to work through this tutorial; as long as you're prepared to get the Python environment set up and learn some basic programming skills the hope is that you'll be able to customise your own csv file and maybe even extend on what we've covered and produced here.

We're planning on writing some more tutorials to help make it easier to work with the JSON data sets. If there are particular examples or data sets you'd like to see us walk through [please reach out](mailto:data@betfair.com.au).

!!! note "Community help"
    - There's a really active [`betfairlightweight` Slack community](https://betfairlightweight.herokuapp.com/) that's a great place to go to ask questions about the library 

--- 
### Sample code

Run the code from your ide by using `py <filename>.py`, making sure you amend the path to point to your input data.

``` Python
import logging
from typing import List, Set, Dict, Tuple, Optional

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

# the path directories to the data sets
# accepts tar files, zipped files or 
# directory with bz2 file(s)
market_paths = [
    '../_data/2020_12_DecRacingPro.zip',
    '../_data/PRO',
    '../_data/2021_01_JanRacingPro.tar'
]

# loading from tar and extracting files
def load_markets(file_paths: List[str]):
    for file_path in file_paths:
        print(file_path)
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
def as_str(v: float) -> str:
    return '%.2f' % v if v is not None else ''

# parsing price data and pulling out weighted avg price, matched, min price and max price
def parse_traded(traded: List[PriceSize]) -> (float, float, float, float):
    if len(traded) == 0: 
        return (None, None, None, None)
     
    (wavg_sum, matched, min_price, max_price) = functools.reduce(
        lambda total, ps: (
            total[0] + (ps.price * ps.size),
            total[1] + ps.size,
            min(total[2], ps.price),
            max(total[3], ps.price),
        ),
        traded,
        (0, 0, 1001, 0)
    )

    wavg_sum = (wavg_sum / matched) if matched > 0 else None
    matched = matched if matched > 0 else None
    min_price = min_price if min_price != 1001 else None
    max_price = max_price if max_price != 0 else None

    return (wavg_sum, matched, min_price, max_price)

# splitting race name and returning the parts 
def split_anz_horse_market_name(market_name: str) -> (str, str, str):
    # return race no, length, race type
    # input sample: R6 1400m Grp1
    parts = market_name.split(' ')
    race_no = parts[0] # return example R6
    race_len = parts[1] # return example 1400m
    race_type = parts[2].lower() # return example grp1, trot, pace

    return (race_no, race_len, race_type)

# filtering markets to those that fit the following criteria
def filter_market(market: MarketBook) -> bool: 
    d = market.market_definition
    return (d.country_code == 'AU' 
        and d.market_type == 'WIN' 
        and (c := split_anz_horse_market_name(d.name)[2]) != 'trot' and c != 'pace')

# setup logging
# logging.basicConfig(level=logging.WARN)

# create trading instance (don't need username/password)
trading = betfairlightweight.APIClient("username", "password")

# create listener
listener = betfairlightweight.StreamListener(max_latency=None)

# record prices to a file
with open("output.csv", "w") as output:
    # defining column headers
    output.write("market_id,event_date,country,track,market_name,selection_id,selection_name,result,bsp,pp_min,pp_max,pp_wap,pp_ltp,pp_volume,ip_min,ip_max,ip_wap,ip_ltp,ip_volume\n")

    for file_obj in load_markets(market_paths):
        stream = trading.streaming.create_historical_generator_stream(
            file_path=file_obj,
            listener=listener,
        )

        with patch("builtins.open", lambda f, _: f):   
            evaluate_market = False
            preplay_market = None
            postplay_market = None
            preplay_traded = None
            postplay_traded = None            

            gen = stream.get_generator()
            for market_books in gen():
                for market_book in market_books:
                    
                    # skipping markets that don't meet the filter
                    if evaluate_market == False and filter_market(market_book) == False:
                        continue
                    else:
                        evaluate_market = True

                    # final market view before market goes in play
                    if preplay_market is not None and preplay_market.inplay != market_book.inplay:
                        preplay_traded = [ (r.last_price_traded, r.ex.traded_volume.copy()) for r in preplay_market.runners ]
                    preplay_market = market_book
                    
                    # final market view at the conclusion of the market
                    if postplay_market is not None and postplay_market.status == "OPEN" and market_book.status != postplay_market.status:
                        postplay_traded = [ (r.last_price_traded, r.ex.traded_volume.copy()) for r in market_book.runners ]
                    postplay_market = market_book   

            # no price data for market
            if postplay_traded is None:
                print('didnt find postplay results?')
                continue; 

            # generic runner data
            runner_data = [
                {
                    'selection_id': r.selection_id,
                    'selection_name': next((rd.name for rd in postplay_market.market_definition.runners if rd.selection_id == r.selection_id), None),
                    'selection_status': r.status,
                    'sp': as_str(r.sp.actual_sp),
                }
                for r in postplay_market.runners 
            ]

            # runner price data for markets that go in play
            if preplay_traded is not None:
                def runner_vals(r):
                    (pre_ltp, pre_traded), (post_ltp, post_traded) = r

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
                        'preplay_matched': as_str(pre_matched),
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
                    (ltp, traded) = r
                    (wavg, matched, min_price, max_price) = parse_traded(traded)

                    return {
                        'preplay_ltp': as_str(ltp),
                        'preplay_min': as_str(min_price),
                        'preplay_max': as_str(max_price),
                        'preplay_wavg': as_str(wavg),
                        'preplay_matched': as_str(matched),
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