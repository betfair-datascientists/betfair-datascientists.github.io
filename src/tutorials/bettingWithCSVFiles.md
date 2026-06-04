# CSV Betting Workflow Tutorial

This tutorial demonstrates a simple workflow for generating a CSV file containing today’s racing fields, entering your bets directly into the spreadsheet, and then using a separate script to place those bets programmatically through the API.

The goal is to provide a lightweight and practical example that customers can use with delayed API keys to streamline the betting process without needing to build a full automation system.

Using a CSV workflow can be useful for:

 - Reviewing all available runners and markets in one place
 - Preparing bets ahead of time in Excel or another spreadsheet tool
 - Reducing repetitive manual entry
 - Managing larger batches of bets more efficiently
 - Building simple custom workflows around API betting

The overall process is:

 1. Generate a CSV file containing today’s racing fields
 2. Open the CSV file in Excel, Google Sheets, or another spreadsheet editor
 3. Enter your desired bets and staking information
 4. Save the updated CSV file
 5. Run the placement script to submit the bets programmatically

## Requirements

To run this file, you will need:

 - Python & VSCode (or other code editor installed)
 - A funded Betfair account
 - A Betfair API key (delayed is fine)
    - To get your keys, follow these [instructions](../api/apiappkey.md)
 - A credentials.json file containing your username, password and application key

### Important Notes

This tutorial is intentionally simple and is designed as a starting point only.

It is **not**:

 - A fully automated betting bot
 - A long-running unattended service
 - A strategy engine or model-driven trading system
 - A script that reacts to market movements or live signals
 - A framework for automated execution logic

The placement script only submits the bets that already exist in the CSV file at the moment the script is run.

No betting decisions are made automatically, and no bets are placed unless the user explicitly executes the script.

## Generating the CSV File

```python

# Import libraries
import betfairlightweight
import pandas as pd
import json
import tzlocal
import re

def bflw_trading():

    with open('credentials.json') as f:
        cred = json.load(f)
        username = cred['username']
        password = cred['password']
        app_key = cred['app_key']

    trading = betfairlightweight.APIClient(username, password, app_key=app_key)

    return trading

def process_runner_catalogue(runner_catalogue):

    rows = []

    for r in runner_catalogue:

        m = r.metadata
        runner_name = getattr(r, 'runner_name', None)

        form = m.get('FORM', None)

        last_start_result = None

        try:
            if isinstance(form, str):
                digits = re.findall(r"\d", form)  # single digits only
                if digits:
                    last_start_result = int(digits[-1])
        except Exception:
            last_start_result = None

        row = {
            'selection_id': r.selection_id,
            'runner_name': runner_name,
            'stall_draw': m.get('STALL_DRAW', None),
            'jockey_name': m.get('JOCKEY_NAME', None),
            'trainer_name': m.get('TRAINER_NAME', None),
            'form': m.get('FORM', None),
            'weight_carried': m.get('WEIGHT_VALUE', None),
            'days_since_last_run': m.get('DAYS_SINCE_LAST_RUN', None),
            'last_start_result': last_start_result,
        }

        rows.append(row)

    return pd.DataFrame(rows)

def process_runner_books(runner_books):
    '''
    This function processes the runner books and returns a DataFrame with the best back/lay prices + vol for each runner
    :param runner_books:
    :return:
    '''
    best_back_prices = [runner_book.ex.available_to_back[0]['price']
        if runner_book.ex.available_to_back
        else 1.01
        for runner_book
        in runner_books]
    best_lay_prices = [runner_book.ex.available_to_lay[0]['price']
        if runner_book.ex.available_to_lay
        else 1000.0
        for runner_book
        in runner_books]

    selection_ids = [runner_book.selection_id for runner_book in runner_books]
    last_prices_traded = [runner_book.last_price_traded for runner_book in runner_books]
    statuses = [runner_book.status for runner_book in runner_books]
    adjustment_factors = [runner_book.adjustment_factor for runner_book in runner_books]

    df = pd.DataFrame({
        'selection_id': selection_ids,
        'best_back_price': best_back_prices,
        'best_lay_price': best_lay_prices,
        'last_traded_price': last_prices_traded,
        'runner_status': statuses,
        'adjustment_factor': adjustment_factors
    })

    return df

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


local_tz = tzlocal.get_localzone()

trading = bflw_trading()
trading.login_interactive()

# -----------------------------
# Filters
# -----------------------------
event_filter = betfairlightweight.filters.market_filter(
    market_countries=['AU'],
    event_type_ids=['7'],
    market_type_codes=['WIN'],
    race_types=['Flat', 'Jumps', 'Hurdle']
)

price_filter = betfairlightweight.filters.price_projection(
    price_data=['EX_BEST_OFFERS'],
    virtualise=True
)

# -----------------------------
# MARKET CATALOGUE (RUNNERS META)
# -----------------------------
market_catalogues = trading.betting.list_market_catalogue(
    filter=event_filter,
    market_projection=[
        "MARKET_START_TIME",
        "MARKET_DESCRIPTION",
        "RUNNER_DESCRIPTION",
        "RUNNER_METADATA",
        "EVENT"
    ],
    max_results=100,
    sort='FIRST_TO_START'
)

catalogue_rows = []

for m in market_catalogues:

    runner_df = process_runner_catalogue(m.runners)

    race_time_local = (
        pd.to_datetime(m.market_start_time)
        .tz_localize("UTC") # Remove this line for betfairlightweight versions 2.23 and above
        .tz_convert(local_tz)
    )

    runner_df.insert(0, 'venue', m.event.venue)
    runner_df.insert(1, 'market_name', m.market_name)
    runner_df.insert(2, 'market_id', m.market_id)
    runner_df.insert(3, 'race_time', race_time_local)
    runner_df.insert(4, 'turn_in_play', m.description.turn_in_play_enabled)
    runner_df.insert(5, 'bsp_enabled', m.description.bsp_market)

    catalogue_rows.append(runner_df)

all_catalogues_df = pd.concat(catalogue_rows, ignore_index=True)

# -----------------------------
# MARKET BOOKS (LIVE PRICES)
# -----------------------------
market_ids = [m.market_id for m in market_catalogues]

book_rows = []

for chunk in chunk_list(market_ids, 10):

    market_books = trading.betting.list_market_book(
        market_ids=chunk,
        price_projection=price_filter,
    )

    for book in market_books:
        df = process_runner_books(book.runners)
        df['market_id'] = book.market_id
        book_rows.append(df)

all_runner_books_df = pd.concat(book_rows, ignore_index=True)

# -----------------------------
# MERGE + CLEAN
# -----------------------------
final_df = all_catalogues_df.merge(
    all_runner_books_df,
    how='left',
    on=['market_id', 'selection_id']
)

final_df = final_df.loc[final_df['runner_status'] == 'ACTIVE'].copy()

final_df.sort_values(
    by=['venue', 'race_time'],
    inplace=True
)

# -----------------------------
# MODEL INPUT COLUMNS
# -----------------------------
final_df[['backers_stake', 'lay_liability', 'price', 'bet_type', 'side', 'persistence_type']] = None
print(final_df.head())

# -----------------------------
# EXPORT
# -----------------------------
final_df.to_csv(
    'todays_fields.csv',
    index=False
)

```

### Adjusting the filter

```text title='Aus Thoroughbred Racing'

event_filter = betfairlightweight.filters.market_filter(
    market_countries=['AU'],
    event_type_ids=['7'],
    market_type_codes=['WIN'],
    race_types=['Flat', 'Jumps', 'Hurdle']
)

```

```text title='Aus Harness Racing'

event_filter = betfairlightweight.filters.market_filter(
    market_countries=['AU'],
    event_type_ids=['7'],
    market_type_codes=['WIN'],
    race_types=['Harness']
)

```

```text title='Aus Greyhound Racing'

event_filter = betfairlightweight.filters.market_filter(
    market_countries=['AU'],
    event_type_ids=['4339'],
    market_type_codes=['WIN']
)

```

## Next Steps

What we've done in the previous step is to download information about upcoming Australian Thoroughbred Races taking place. This information is available in a CSV file where it is possible to manually input your bets to place. This is done by filling in the various columns depending on your strategy.

There are various error-handling steps included in the bet placement code below, however, the general guide on how to enter your bets is as follows:

 - **BSP Bets (No Price Limit)**
    - **Lay**
        - bet_type = 'SP'
        - side = 'LAY'
        - liability = '30' (amount to lose)
    - **Back Bets**
        - bet_type = 'SP'
        - side = 'BACK'
        - stake = '5.00' (amount to lose)
 - **BSP Bets (Price Limit)**
     - **Lay Bets**
        - bet_type = 'SP'
        - side = 'LAY'
        - price = '10' (maximum lay price)
        - liability = '30' (amount to lose)
    - **Back Bets**
        - bet_type = 'SP'
        - side = 'BACK'
        - price = '3.20' (minimum back price)
        - stake = '5.00' (amount to lose)
 - **Exchange Bets**
    - **Lapse Bets**
        - **Lay Bets**
            - bet_type = 'EX'
            - side = 'LAY'
            - price = '10'
            - persistence_type = 'LAPSE'
            - liability = '30' OR stake = '5.00'
        - **Back Bets**
            - bet_type = 'EX'
            - side = 'BACK'
            - price = '3.20'
            - persistence_type = 'LAPSE'
            - liability = '30' OR stake = '5.00'
    - **Keep Bets**
        - **Lay Bets**
            - bet_type = 'EX'
            - side = 'LAY'
            - price = '10'
            - persistence_type = 'PERSIST'
            - liability = '30' OR stake = '5.00'
        - **Back Bets**
            - bet_type = 'EX'
            - side = 'BACK'
            - price = '3.20'
            - persistence_type = 'PERSIST'
            - liability = '30' OR stake = '5.00'
    - **Take BSP Bets**
        - **Lay Bets**
            - bet_type = 'EX'
            - side = 'LAY'
            - price = '10'
            - persistence_type = 'MARKET_ON_CLOSE'
            - liability = '30' OR stake = '5.00'
        - **Back Bets**
            - bet_type = 'EX'
            - side = 'BACK'
            - price = '3.20'
            - persistence_type = 'MARKET_ON_CLOSE'
            - liability = '30' OR stake = '5.00'

You will need to ensure that the values inserted in the cells match the acceptable values as outlined here:

 - bet_type: **EX** & **SP**
 - side: **BACK** & **LAY**
 - price: number between 1 & 1000
 - liability/stake: positive number
 - persistence_type: **LAPSE**, **PERSIST**, **MARKET_ON_CLOSE** (defaults to LAPSE if missing)

## Bet Placement

Here follows the bet placement code. If, for any reason, the entered parameters fail the checks, these bets will be output to a separate 'failed_bets.csv' file where you can make any requisite changes (e.g. missing price, missing stake) and then re-run the script, placing ONLY those bets. 

Successful bets will be output to their own csv file.

```python

# Import libraries
import betfairlightweight
import pandas as pd
import json
import math
import bisect
from datetime import datetime
import os

def bet_checker(
    stake,
    liability,
    price,
    bet_type,
    side,
    turn_in_play,
    bsp_enabled,
    persistence_type,
    max_liability
):

    BACK_SIDES = ['B', 'BACK', 'Back']
    LAY_SIDES = ['L', 'LAY', 'Lay']

    # -------------------------
    # Helpers
    # -------------------------
    def is_missing(x):
        return pd.isna(x) or str(x).strip().lower() == 'nan'

    # -------------------------
    # Persistence validation
    # -------------------------
    if not bsp_enabled and persistence_type == 'MARKET_ON_CLOSE':
        return False, 'Invalid Persistence Type - BSP not enabled'

    if not bsp_enabled and bet_type == 'SP':
        return False, 'Invalid Bet Type - BSP not enabled - EX bets only'

    if not turn_in_play and persistence_type == 'PERSIST':
        return False, 'Invalid Persistence Type - Market does not go in play'

    # -------------------------
    # Side validation
    # -------------------------
    if side not in BACK_SIDES + LAY_SIDES:
        return False, 'Invalid or Missing Bet Side - use BACK or LAY'

    # -------------------------
    # Bet type validation
    # -------------------------
    if bet_type not in ['EX', 'SP']:
        return False, 'Invalid or Missing Bet Type - use EX or SP'

    # -------------------------
    # Stake / Liability presence
    # -------------------------
    stake_missing = is_missing(stake)
    liability_missing = is_missing(liability)

    if stake_missing and liability_missing:
        return False, 'Missing Bet Size'

    if not stake_missing and not liability_missing:
        return False, 'Duplicate Bet Size'

    # -------------------------
    # Stake validation
    # -------------------------
    if not stake_missing:

        try:
            stake = float(stake)

            if stake <= 0:
                return False, 'Negative Bet Size'

            if side in BACK_SIDES and stake > max_liability:
                return False, 'Max Back Exposure Exceeded'

        except (TypeError, ValueError):
            return False, 'Invalid Bet Size'

    # -------------------------
    # Liability validation
    # -------------------------
    if not liability_missing:

        try:
            liability = float(liability)

            if liability <= 0:
                return False, 'Negative Lay Liability or Target Winnings'

            if side in LAY_SIDES and liability > max_liability:
                return False, 'Max Lay Exposure Exceeded'

        except (TypeError, ValueError):
            return False, 'Invalid Lay Liability or Target Winnings'

    # -------------------------
    # Price validation
    # -------------------------
    if is_missing(price):

        if bet_type == 'EX':
            return False, 'Missing Price for Non-SP Bet'

    else:

        try:
            price = float(price)

            if price < 1.01:
                return False, 'Price Too Low'

            if price > 1000:
                return False, 'Price Too High'

        except (TypeError, ValueError):
            return False, 'Invalid Price'

    # -------------------------
    # SP logic
    # -------------------------
    if (
        bet_type == 'SP'
        and side in LAY_SIDES
        and not stake_missing
    ):
        return False, 'Cannot specify Backers Stake for Lay SP Bets'

    if (
        bet_type == 'SP'
        and side in BACK_SIDES
        and not liability_missing
    ):
        return False, 'Cannot specify Target Winnings for Back SP Bets'
    
    if (
        bet_type == 'SP'
        and not is_missing(persistence_type)
    ):
        return False, 'Cannot specify persistence for SP Bets'

    return True, 'Check Passed'

def round_to_tick(price, side):

    TICK_SIZES = {
        1.0: 0.01,
        2.0: 0.02,
        3.0: 0.05,
        4.0: 0.1,
        6.0: 0.2,
        10.0: 0.5,
        20.0: 1.0,
        30.0: 2.0,
        50.0: 5.0,
        100.0: 10.0,
        1000.0: 1000,
    }

    BANDS = sorted(TICK_SIZES.keys())

    if price is None:
        return None

    idx = bisect.bisect_right(BANDS, price) - 1
    base = BANDS[max(idx, 0)]
    tick = TICK_SIZES[base]

    steps = price / tick

    if side in ['B', 'BACK', 'Back']:
        # always round DOWN for BACK
        return round(math.floor(steps) * tick, 8)

    if side in ['L', 'LAY', 'Lay']:
        # always round UP for LAY
        return round(math.ceil(steps) * tick, 8)

    raise ValueError(f"Unknown side: {side}")

def place_bet(trading,market_id,selection_id,stake,liability,price,bet_type,side,persistence_type):

    def is_missing(x):
        return pd.isna(x) or str(x).strip().lower() == 'nan'

    if not is_missing(price):
        price = round_to_tick(price, side)

    if not is_missing(stake):
        size = stake
            
    if not is_missing(liability):
        size = liability/(price-1)

    if bet_type == 'EX':

        if side in ['B','Back','BACK']:

            instruction = betfairlightweight.filters.place_instruction(
                order_type="LIMIT",
                selection_id=selection_id,
                side='BACK',
                limit_order=betfairlightweight.filters.limit_order(
                size=round(size,2),
                price=price,
                persistence_type=persistence_type
                )
            )
            response = trading.betting.place_orders(
                market_id=market_id,
                instructions=[instruction]
            )

            return response.status

        if side in ['L','Lay','LAY']:

            instruction = betfairlightweight.filters.place_instruction(
                order_type="LIMIT",
                selection_id=selection_id,
                side='LAY',
                limit_order=betfairlightweight.filters.limit_order(
                size=round(size,2),
                price=price,
                persistence_type=persistence_type
                )
            )
            response = trading.betting.place_orders(
                market_id=market_id,
                instructions=[instruction]
            )

            return response.status
    
    if bet_type == 'SP':

        if side in ['B','Back','BACK']:

            if is_missing(price):
                instruction = betfairlightweight.filters.place_instruction(
                    order_type="MARKET_ON_CLOSE",
                    selection_id=selection_id,
                    side='BACK',
                    market_on_close_order=betfairlightweight.filters.market_on_close_order(
                    liability=round(stake,2)
                    )
                )
                response = trading.betting.place_orders(
                    market_id=market_id,
                    instructions=[instruction]
                )

                return response.status

            if not is_missing(price):

                instruction = betfairlightweight.filters.place_instruction(
                    order_type="LIMIT_ON_CLOSE",
                    selection_id=selection_id,
                    side='BACK',
                    limit_on_close_order=betfairlightweight.filters.limit_on_close_order(
                    liability=round(stake,2),
                    price=price
                    )
                )
                response = trading.betting.place_orders(
                    market_id=market_id,
                    instructions=[instruction]
                )

                return response.status

        if side in ['L','Lay','LAY']:

            if is_missing(price):
                instruction = betfairlightweight.filters.place_instruction(
                    order_type="MARKET_ON_CLOSE",
                    selection_id=selection_id,
                    side='LAY',
                    market_on_close_order=betfairlightweight.filters.market_on_close_order(
                    liability=round(stake,2)
                    )
                )
                response = trading.betting.place_orders(
                    market_id=market_id,
                    instructions=[instruction]
                )

                return response.status

            if not is_missing(price):

                instruction = betfairlightweight.filters.place_instruction(
                    order_type="LIMIT_ON_CLOSE",
                    selection_id=selection_id,
                    side='LAY',
                    limit_on_close_order=betfairlightweight.filters.limit_on_close_order(
                    liability=round(stake,2),
                    price=price
                    )
                )
                response = trading.betting.place_orders(
                    market_id=market_id,
                    instructions=[instruction]
                )

                return response.status

def bflw_trading():

    with open('credentials.json') as f:
        cred = json.load(f)
        username = cred['username']
        password = cred['password']
        app_key = cred['app_key']

    trading = betfairlightweight.APIClient(username, password, app_key=app_key)

    return trading

def main(filename, max_liability):

    trading = bflw_trading()
    trading.login_interactive()

    failed_bets = []
    successful_bets = []

    try:
        betting_df = pd.read_csv(filename).dropna(
            subset=['bet_type', 'side'],
            how='all'
        )
    except Exception as e:
        print(f"Failed reading {filename}: {e}")
        return False

    if betting_df.empty:
        print(f"{filename} is empty")
        return False

    betting_df = betting_df[
        [
            'venue',
            'market_name',
            'turn_in_play',
            'bsp_enabled',
            'market_id',
            'selection_id',
            'runner_name',
            'backers_stake',
            'lay_liability',
            'price',
            'bet_type',
            'side',
            'persistence_type'
        ]
    ]

    print(betting_df)

    for idx, row in betting_df.iterrows():

        row_dict = row.to_dict()

        check_passed, reason = bet_checker(
            row_dict.get("backers_stake"),
            row_dict.get("lay_liability"),
            row_dict.get("price"),
            row_dict.get("bet_type"),
            row_dict.get("side"),
            row_dict.get("turn_in_play"),
            row_dict.get("bsp_enabled"),
            row_dict.get("persistence_type", "LAPSE"),
            max_liability,
        )

        if not check_passed:
            row_dict["failure_reason"] = reason
            failed_bets.append(row_dict)
            continue

        # -------------------------
        # Market ID validation
        # -------------------------
        market_id = str(row_dict.get("market_id", ""))

        if "." not in market_id or len(market_id) > 11:
            row_dict["failure_reason"] = "invalid_market_id"
            failed_bets.append(row_dict)
            continue

        market_id = market_id.ljust(11, "0")

        # -------------------------
        # Selection ID validation
        # -------------------------
        try:
            selection_id = int(row_dict.get("selection_id"))
        except (TypeError, ValueError):
            row_dict["failure_reason"] = "invalid_selection_id"
            failed_bets.append(row_dict)
            continue

        # -------------------------
        # Place bet
        # -------------------------
        response = place_bet(
            trading,
            market_id,
            selection_id,
            row_dict.get("backers_stake"),
            row_dict.get("lay_liability"),
            row_dict.get("price"),
            row_dict.get("bet_type"),
            row_dict.get("side"),
            row_dict.get("persistence_type"),
        )

        row_dict["status"] = response
        print(response)

        if response == 'SUCCESS':
            successful_bets.append(row_dict)
        else:
            row_dict["failure_reason"] = response
            failed_bets.append(row_dict)

    # Save outputs
    if successful_bets:
        pd.DataFrame(successful_bets).to_csv(
            "successful_bets.csv",
            index=False,
            mode='a',
            header=not os.path.exists("successful_bets.csv")
        )

    if failed_bets:
        pd.DataFrame(failed_bets).to_csv(
            "failed_bets.csv",
            index=False,
            mode='w'
        )
    else:
        # remove old failed file if everything succeeded
        if os.path.exists("failed_bets.csv"):
            os.remove("failed_bets.csv")

    return True


if __name__ == '__main__':

    MAX_LIABILITY = 100

    failed_exists = (
        os.path.exists("failed_bets.csv")
        and os.path.getsize("failed_bets.csv") > 0
    )

    if failed_exists:
        print("Retrying failed bets...")
        main("failed_bets.csv", MAX_LIABILITY)

    else:
        print("Processing today's bets...")
        source_file = "todays_fields.csv"

        processed = main(source_file, MAX_LIABILITY)

        if processed:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            os.rename(
                source_file,
                f"todays_fields_processed_{timestamp}.csv"
            )

```

---
### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.