import logging
from typing import List, Tuple

from itertools import zip_longest
import functools

import os
import tarfile
import zipfile
import bz2
import glob
from betfair_data import PriceSize
from betfair_data import bflw

file_output = "output_py_source.csv"

market_paths = [
    "data/2021_10_OctRacingAUPro.tar",
    "data/2021_11_NovRacingAUPro.tar",
    "data/2021_12_DecRacingAUPro.tar",
]

# setup logging
logging.basicConfig(level=logging.FATAL)

# loading from tar and extracting files
def load_markets(file_paths: List[str]):
    for file_path in file_paths:
        if os.path.isdir(file_path):
            for path in glob.iglob(file_path + '**/**/*.bz2', recursive=True):
                with bz2.BZ2File(path, 'rb') as f:
                    bytes = f.read()
                    yield bflw.File(path, bytes)
        elif os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1]
            # iterate through a tar archive
            if ext == '.tar':
                with tarfile.TarFile(file_path) as archive:
                    for file in archive:
                        name = file.name
                        bytes = bz2.open(archive.extractfile(file)).read()
                        yield bflw.File(name, bytes)
            # or a zip archive
            elif ext == '.zip':
                with zipfile.ZipFile(file_path) as archive:
                    for name in archive.namelist():
                        bytes = bz2.open(archive.open(name)).read()
                        yield bflw.File(name, bytes)
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
def filter_market(market: bflw.MarketBook) -> bool: 
    d = market.market_definition
    return (d != None
        and d.country_code == 'AU' 
        and d.market_type == 'WIN' 
        and (c := split_anz_horse_market_name(d.name)[2]) != 'trot' and c != 'pace')

# record prices to a file
with open(file_output, "w") as output:
    # defining column headers
    output.write("market_id,event_date,country,track,market_name,selection_id,selection_name,result,bsp,pp_min,pp_max,pp_wap,pp_ltp,pp_volume,ip_min,ip_max,ip_wap,ip_ltp,ip_volume\n")

    for i, file in enumerate(load_markets(market_paths)):
        print("Market {}".format(i), end='\r')

        def get_pre_post_final():
            eval_market = None
            prev_market = None
            preplay_market = None
            postplay_market = None       

            for market_books in file:
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

        (preplay_market, postplay_market, final_market) = get_pre_post_final()

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