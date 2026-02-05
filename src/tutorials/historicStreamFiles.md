# How To Read and Utilise The Betfair Stream Files

The Betfair Historic Stream Files are made available for purchase on the [Betfair Historic Data Site](https://historicdata.betfair.com/#/mydata).
These files are recordings of the Stream API and come in three levels of granularity:

 - BASIC (Free)
 - ADVANCED (Paid)
 - PRO (Paid)

Whilst the BASIC files have their uses, we believe the PRO level files are required for any robust simulations or backtesting on a series of markets. Australian customers should contact automation@betfair.com.au regarding accessing the PRO level files.

The specifications for the files can be found [here](https://historicdata.betfair.com/Betfair-Historical-Data-Feed-Specification.pdf)

Now whilst it's all well and good to have the specifications to hand, how is it possible to actually interpret the data from inspecting the files? The data is in JSON format, and whilst machines can read it quite easily, it's not overly suited to being interpreted by humans. So let's do a walkthrough of the data contained within a single stream file, and we'll even output a video file at the end so you can watch the market back.

## The Data

So first let's walk through exactly what is and what is not contained in the stream files.

What it contains:

 - Every bet that was placed, matched, or cancelled on every runner in the market in GBP (British Pounds)
 - Information about the market and status of every runner at every point in time

What it does not contain:

 - Cross Matching / Virtual Bets
 - Persistence Types
 - Information about the Race Status or the Match Score
 - Race Type
 - Competition Id

These last two items (race type and competition id) pose quite a challenge when processing a large number of stream files, especially if you're only targeting a certain section (e.g. Harness races or English Premier League). For this we recommend sourcing a csv file that you can use as a key to determine if any given stream file fits your use case (with event id or market id values).

## Market Definition

The first message contained within any stream file will be the **marketDefinition**. This is a dictionary that is sent **in full** every time there is a change to the definition of the market (e.g. scratching, adjustment factor updates, market suspension, bsp reconciliation etc.)

```py title="Market Definition"

{
    "op":"mcm", # Market Change Message - included in every update
    "clk":"15290288555", # A token used to load a complete market image when connecting to the stream - ignore in historical files
    "pt":1766988791945, # Timestamp in Epoch Time
    "mc":[
        {
            "id":"1.252161052", # Market Id
            "marketDefinition":{
                "bspMarket":true, # Is BSP Offered?
                "turnInPlayEnabled":true, # Does the market go inplay?
                "persistenceEnabled":true, # Are TAKE_SP or KEEP bets enabled? 
                "marketBaseRate":8.0, # Base Commission Rate
                "eventId":"35097807", 
                "eventTypeId":"7", # Sport Id
                "numberOfWinners":1, # Important for Place Markets
                "bettingType":"ODDS",
                "marketType":"WIN",
                "marketTime":"2025-12-31T08:00:00.000Z",
                "suspendTime":"2025-12-31T08:00:00.000Z",
                "bspReconciled":false, # Is the BSP finalised?
                "complete":true, # No more runners can be added
                "inPlay":false, 
                "crossMatching":false, # This will be false for the first message and may change later
                "runnersVoidable":false,
                "numberOfActiveRunners":19, # Non-removed runners
                "betDelay":0,
                "status":"OPEN",
                "runners":[
                    {
                    "adjustmentFactor":10.82, # Only for Horse Racing
                    "status":"ACTIVE",  # REMOVED means "SCRATCHED"
                    "sortPriority":1, # Order displayed on website and app
                    "id":93168069, # Selection Id
                    "name":"1. Sea Poem" # Runner Name
                    },
                    {
                    "adjustmentFactor":5.96,
                    "status":"ACTIVE",
                    "sortPriority":2,
                    "id":93168070,
                    "name":"2. Ballynacally"
                    },
                # -----
                # ALL OTHER RUNNERS
                # ----
                    ],
                "regulators":[
                    "MR_INT" # MR_INT means Betfair Global
                    ],
                "venue":"Flemington", # Track
                "countryCode":"AU",
                "discountAllowed":true, # Are discounts on commission allowed?
                "timezone":"Australia/Sydney",
                "openDate":"2025-12-31T04:40:00.000Z", # Market Time for earliest market for the event (i.e. Race 1 for racing)
                "version":7065986324, # This counts up every time the market status changes
                "name":"R7 1100m Hcap", # Market Name
                "eventName":"Flemington (AUS) 31st Dec"
                },
                "rc":[ #rc means Runner Change - the first one of these will be empty
                ],
                "con":true, # Ignore for Historical Files
                "img":false  # Ignore for Historical Files
                }
    ]
}

```

It's important that any bot listens to the market definition for any updates as this may affect your betting strategy.
For example, if your strategy places BSP bets, then implementing a check for "bspReconciled":true can stop large numbers of failed transactions that may cause Transaction Charges.

## Runner Changes

The other, much more numerous, type of message in the stream is **Runner Change** denoted by the field 'rc'.
These updates contain information about the available to back and available to lay volumes at each price point, as well as traded volumes and volumes available at the BSP.

Importantly, these messages only contain **changes** and do not contain the full ladder, so to understand the full ladder at any single point in time, you'll need to build the orderbook from these messages. This would not be a trivial process to do by hand, but as the API is designed for computers rather than humans, luckily you don't have to.

First, lets walk through each type of runner change message

### Exchange Bets / Limit Bets

These messages contain the price point and available size at a specific price point denoted by a tuple in the form **[[price,size]]**
This is the **full** currently available volume at that price point and should override any previous volume value rather than add to it, as the volume value is a float that is zero or positive (i.e. there is no message than indicates a reduction in volume other than 0)

A volume value of 0 means that there was volume available at that price that is no longer available because the volume has been matched or cancelled.

A runner change message may only have one runner with an update at one price point or, in the case of an application of a reduction factor due to a scratching, all levels of every runner may be contained, leading to truly enormous (relatively speaking) runner change messages.

```py title="Exchange Bet Ladder"

"rc":[
        {
            "atb":[[34,0.14]],
            "id":93168076}],
            "con":true,
            "img":false
        }
    ]

# This means this runner has 0.14GBP available to back at a price of $34

"rc":[
        {
            "atl":[[13,44.66]],
            "id":93168069}],
            "con":true,
            "img":false
        }
    ]

# This means this runner has 44.66GBP available to lay at a price of $13
```

### Traded Volume

These messages contain the price point and volume of bets that have been traded at a particular price point denoted by a tuple in the form **[[price,size]]** as well as the last traded price and full traded volume for that runner in that update. If only one price has been traded in an update, then 'ltp' will be identical to the price in the tuple but if more than one price has been traded then it will include the bet fragment with the highest bet id value for last traded price. As with atb/atl changes, the size associated with each price is the **total** volume traded at that price and not the volume in that update.

If the volume value is 0 then this means that either the runner has been scratched, bets have been voided for some reason or the runner has been settled - losers may be settled before the end of the market, but winners will all be settled at the conclusion of the market. In fact the penultimate message in every market is to set every level of traded volume of every runner to 0.

Traded volume may also fluctuate slightly with changes to FX rates (i.e. currency conversion) as, while the stream files are in GBP, customers may bet in other currencies, and any markets managed in Australia operate in Australian dollars.

Additionally, it is possible to see an addition of volume traded at a price without a message for that price appearing as "atl" or "atl" messages. This is due to the absence of the cross-matching bets.

```py title="Traded Volume"

"rc":[
        {
            "trd":[[17,2.97],[17.5,0.82]],
            "ltp":17.0,
            "tv":2.79,
            "id":93168070}],
            "con":true,
            "img":false
        }
    ]

# This means that 2.97GBP was traded at $17 and 0.82GBP was traded at $17.50
# $17 was the most recently traded price and 2.79GBP has been traded on this runner in this update
```

### Betfair Starting Price

The final type of message that may appear in the stream files, where bspMarket = True in the marketDefinition, is messages relating to the Betfair Starting Price. There are two main types of message here:

 - Volume Available to Back / Lay At BSP
 - Projected BSP Prices

The volume messages contain tuples **[[price,size]]** relating to volume available to match against in the BSP Reconciliation with the following characteristics:

 - MARKET_ON_CLOSE Back bets appear as "spl":[[1.01,volume]]
 - MARKET_ON_CLOSE Lay bets appear as "spb":[[1000,volume]]
 - LIMIT_ON_CLOSE Back bets with a lower limit of X will appear as "spl":[[X,volume]]
 - LIMIT_ON_CLOSE Lay bets with an upper limit of X will appear as "spb":[[X,volume]]

Note that each message contains the FULL volume available at the price point

The projected BSP messages contain float or string ('inf') values and take into account volumes available to calculate the Betfair Starting Price at the race start. These values update every 60 seconds or so in real time:

 - **spn** means Starting Price Near and includes volume in the SP ladder only
 - **spf** means Starting Price Far and includes volume in the exchange ladder with MARKET_ON_CLOSE/TAKE_SP persistence

```py title="BSP Messages"

"rc":[
        {
            "spb":[[1000,13004.99]],
            "spl":[[1.01,19452.99]],
            "id":93168070}],
            "con":true,
            "img":false
        }
    ]

# This means there is 13,004.99GBP available to back at BSP and 19452.99GBP available to lay at BSP for this runner

"rc":[
        {
            "spn":7.4,
            "spf":7.45,
            "id":93168070}],
            "con":true,
            "img":false
        }
    ]

# This means that the projected BSP based on BSP bets only is $7.40 and $7.45 based on unmatched limit bets
# These values tend to converge as the market becomes more liquid
```

### BSP Reconciliation

When the BSP is reconciled, a lot of things happen in a short period of time:

 - First the status of the market goes to SUSPENDED
 - Using available volume the BSP will be calculated and added to each runner dictionary in the marketDefinition object.
 - Then any unmatched limit bets which, according to the principles of best price execution, would be matched at the BSP will be "transformed" and moved from the atl/atb ladders to spl/spb ladders.
 - Any other unmatched limits set to lapse will be automatically cancelled
 - Then the marketDefinition will be resent with bspReconciled set to "true"
 - Then for the spb ladder, any bets at prices BELOW the BSP will lapse and any bets at price AT/ABOVE BSP will have their price changed to the BSP, and for the spl ladder, any bets at prices ABOVE the BSP will lapse and any bets at price AT/BELOW BSP will have their price changed to the BSP. All other levels of spl/spb will be set to 0 volume.
 - Finally, if the market is set to go in-play, the market definition will be resent with "inplay":true, "status":"OPEN" and "betDelay":1 (may be greater than 1 for sport markets)

All this happens in the space of 7-8 lines within the file with 4 marketDefinition updates

## Replaying a market

Ok, now that we've stepped through exactly what detail can be found in a stream file, let's step through how we can replay a market and make a video of it. Note that this process does not use Rust, only Python, and so to process large numbers of markets would be tediously slow and as such, is intended only as an example.

Here's the actual file I've used: [Flemington R7 31/12/25](../resources/252161052.json)

```py title="Import Packages"

import json
import numpy as np
import matplotlib.pyplot as plt
import cv2 # pip install opencv-python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import math

```

```py title="config"

INPUT_FILE = "252161052.json"   # your stream file
OUTPUT_VIDEO = "market.mp4"

MAX_LINES = 25_000 # Can set this to a lower value to check a small section of the file
FPS = 10 # Default Frames Per Second value

WIDTH, HEIGHT = 1600, 900 # Output Dimensions

BACK_COLOR = "#a6d8ff" # Default Betfair Back Colour
LAY_COLOR  = "#fac9d1" # Default Betfair Lay Colour

```

Now let's create our Runner Class. This will help us to keep track of every runner as we move through the file. Now, it's possible to use a dictionary instead of a class, but a class will provide a bit more order to the chaos. 

```py title="Runner Class"

# =====================================================
# Runner state
# =====================================================

class RunnerState:
    def __init__(self, name, sort_priority):
        self.name = name
        self.sort_priority = sort_priority
        self.status = "ACTIVE"
        self.bsp = None
        self.atb = {}  # back ladder as dict
        self.atl = {} # lay ladder as dict
        self.trd_ladder = {} # trade ladder as dict
        self.spn = None
        self.ltp = None
        self.tv = 0.0
        

```

Now some helper functions to build the ladders

```py title="Ladder Functions"

# =====================================================
# Ladder updates
# =====================================================

def apply_ladder_update(ladder, updates):

    for price, vol in updates:
        price = float(price)
        vol = float(vol)

        if vol == 0:
            ladder.pop(price, None)
        else:
            ladder[price] = vol

def apply_rc_list(runners, rc_list):

    """
    runners: list of runners
    rc_list: list of runner changes in mc["rc"]
    """

    updates_per_runner = {}

    # merge multiple updates per runner in the same message
    for rc in rc_list:
        rid = rc["id"]
        if rid not in updates_per_runner:
            updates_per_runner[rid] = {}
        updates_per_runner[rid].update(rc)

    # apply per runner
    for rid, rc in updates_per_runner.items():
        if rid not in runners:
            continue
        r = runners[rid]

        # ladders
        if "atb" in rc:
            apply_ladder_update(r.atb, rc["atb"])
        if "atl" in rc:
            apply_ladder_update(r.atl, rc["atl"])

        # spn
        if "spn" in rc:
            try:
                val = float(rc["spn"])
                if math.isfinite(val):
                    r.spn = val
            except:
                pass

        # inside apply_rc_list, per runner:
        if "trd" in rc:
            apply_ladder_update(r.trd_ladder, rc["trd"])

            # recompute total volume

            if "tv" in rc:
                try:
                    val = float(rc["tv"])
                    if math.isfinite(val):
                        r.tv = r.tv + val

        # lt
        if "ltp" in rc:
            try:
                val = float(rc["ltp"])
                if math.isfinite(val):
                    r.ltp = val
            except:
                pass

        # status
        if "status" in rc:
            r.status = rc["status"]
```

Now some other helper functions

```py title="utils"

# =====================================================
# Helpers
# =====================================================

def fmt_price(x):
    if x is None:
        return ""
    try:
        v = float(x)
    except:
        return ""

    if not math.isfinite(v):
        return ""

    return f"{v:g}"   # magic: trims trailing zeros

def epoch_to_tz_str(pt, tz_name):
    dt = datetime.fromtimestamp(pt/1000, tz=ZoneInfo("UTC"))
    dt = dt.astimezone(ZoneInfo(tz_name))
    return dt.strftime("%H:%M:%S %d-%m-%Y")

def iso_to_tz_str(iso, tz_name):
    dt = datetime.fromisoformat(iso.replace("Z","+00:00"))
    dt = dt.astimezone(ZoneInfo(tz_name))
    return dt.strftime("%H:%M %d-%m-%Y")

def best_levels(ladder, n, reverse=False):
    return sorted(ladder.items(), reverse=reverse)[:n]

def cell_text(price, vol):
    if price is None:
        return ""
    return f"$\\bf{{{fmt_price(price)}}}$\n{fmt_price(vol)}"

def epoch_to_str(pt):
    dt = datetime.fromtimestamp(pt / 1000, tz=timezone.utc)
    return dt.strftime("%H:%M:%S %d-%m-%Y UTC")

def iso_to_epoch_ms(iso_str):
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1000)

def get_frame_interval(pt_ms, market_start_ms):
    """
    pt_ms: current stream timestamp in ms
    market_start_ms: market start timestamp in ms
    Returns interval in ms to wait before rendering next frame.
    This means the video moves quickly through the early less-liquid life of the market,
    then speeds up as the market start approaches
    """

    time_to_start = market_start_ms - pt_ms  # in ms

    if time_to_start > 2 * 3600 * 1000:  # more than 2 hours
        return 600_000  # 600,000 ms = 10 min = 1 frame per 10 min? adjust units as needed
    elif time_to_start > 5 * 60 * 1000:  # more than 5 minutes
        return 60_000   # 1 frame per minute
    else:
        return 100      # final 5 minutes: 10 fps → 1 frame per 100 ms

def safe_price(x):
    if x is None:
        return ""

    try:
        v = float(x)
    except (TypeError, ValueError):
        return ""

    if not math.isfinite(v):
        return ""

    return f"{v:.2f}"

```

Now we're going to display this market in a table view, like viewing the exchange website, so we'll need a function to build each row of the table

```py title="Build Rows"

# =====================================================
# Build rows
# =====================================================

def build_rows():

    rows = []

    ordered = sorted(runners.values(), key=lambda r: r.sort_priority)

    for r in ordered:

        backs = best_levels(r.atb, 3, reverse=True)
        lays  = best_levels(r.atl, 3, reverse=False)

        backs += [(None,None)]*(3-len(backs))
        lays  += [(None,None)]*(3-len(lays))

        row = [
            r.name,

            fmt_price(r.ltp),
            fmt_price(r.tv),

            cell_text(*backs[2]),
            cell_text(*backs[1]),
            cell_text(*backs[0]),

            fmt_price(r.bsp if r.bsp is not None else r.spn),

            cell_text(*lays[0]),
            cell_text(*lays[1]),
            cell_text(*lays[2]),
        ]

        rows.append((row, r.status))

    return rows

```

Now let's render the image of our table

```py title="Renderer"

# =====================================================
# Renderer
# =====================================================

def draw_table(ax, row_data, timestamp, market_volume):

    ax.clear()

    sp_label = "BSP" if market_info.get("inPlay") else "Proj_SP"
    cols = ["Runner","LTP","TV","B3","B2","B1", sp_label, "L1","L2","L3"]

    rows = [r for r,_ in row_data]

    table = ax.table(
        cellText=rows,
        colLabels=cols,
        loc="center",
        cellLoc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(8)

    n_rows = len(rows)
    n_cols = len(cols)

    ROW_HEIGHT = 0.05

    for r in range(n_rows + 1):
        for c in range(n_cols):
            table[(r,c)].set_height(ROW_HEIGHT)

    for r in range(n_rows + 1):

        table[(r,0)].set_width(0.18)  # runner smaller
        table[(r,1)].set_width(0.06)
        table[(r,2)].set_width(0.06)

        for c in [3,4,5,7,8,9]:
            table[(r,c)].set_width(0.085)

        table[(r,6)].set_width(0.07)


    # runner font smaller
    for r in range(1, n_rows+1):
        table[(r,0)].get_text().set_fontsize(7)
        table[(r,0)].get_text().set_ha("left")

    # colors
    for r,(row,status) in enumerate(row_data, start=1):

        if status == "REMOVED":
            for c in range(1,n_cols):
                table[(r,c)].set_facecolor("black")
                table[(r,c)].get_text().set_color("black")
            continue

        for c in [3,4,5]:
            table[(r,c)].set_facecolor(BACK_COLOR)

        for c in [7,8,9]:
            table[(r,c)].set_facecolor(LAY_COLOR)
        
        # SPN turns green once in-play
        if market_info.get("inPlay"):
            table[(r,6)].set_facecolor("#b6f2c2")  # soft green

    # header bold
    for c in range(n_cols):
        table[(0,c)].get_text().set_fontweight("bold")

    # -------- left info panel --------
    info = market_info

    left_text = (
        f"{info.get('venue','')}\n"
        f"{info.get('name','')}\n"
        f"Event: {info.get('eventId','')}\n"
        f"Start: {iso_to_tz_str(info.get('marketTime',''), info.get('timezone','UTC'))}\n"
        f"Inplay: {info.get('inPlay','')}\n"
        f"Matched: {market_volume:,.0f}"
    )

    ax.text(
        0.02, 0.5,
        left_text,
        va="center",
        ha="right",
        fontsize=11,
        transform=ax.transAxes
    )

    # time title
    ax.set_title(
        epoch_to_tz_str(timestamp, info.get("timezone","UTC")),
        fontsize=16
    )

    ax.axis("off")

    fig.canvas.draw()

    img = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (4,))

    return cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

```

We'll display information about each runner including their available volumes, last traded price, traded volume and projected starting price, turned the runner's volume info black if the runner is scratched and even added code to turn the SP column green once the market goes in play.

**Time to build the video!!**

```py title="Generate the movie file"

# =====================================================
# Video writer
# =====================================================

video = cv2.VideoWriter(
    OUTPUT_VIDEO,
    cv2.VideoWriter_fourcc(*"mp4v"),
    FPS,
    (WIDTH, HEIGHT)
)

# =====================================================
# Main loop
# =====================================================

last_frame_time = None
fig, ax = plt.subplots(figsize=(WIDTH/100, HEIGHT/100), dpi=100)
runners = {}

with open(INPUT_FILE, "r", encoding="utf-8") as stream_lines:

    for line_number, line in enumerate(stream_lines, start=1):

        if line_number >= MAX_LINES:
            break

        # parse the JSON line
        msg = json.loads(line)
        pt = msg["pt"]

        for mc in msg["mc"]:

            # ------------------------------
            # MARKET DEFINITION
            # ------------------------------
            if "marketDefinition" in mc:
                md = mc["marketDefinition"]

                market_info = {
                    "venue": md.get("venue"),
                    "name": md.get("name"),
                    "eventId": md.get("eventId"),
                    "marketTime": md.get("marketTime"),
                    "timezone": md.get("timezone", "UTC"),
                    "inPlay": md.get("inPlay")
                }
                # We'll display all this info in a block next to our table

                market_start_ms = iso_to_epoch_ms(market_info["marketTime"])

                # preserve existing RunnerState
                existing_ids = set(runners.keys())

                for rdef in md["runners"]:
                    rid = rdef["id"]

                    if rid in runners:
                        r = runners[rid]
                        r.name = rdef["name"]
                        r.sort_priority = rdef["sortPriority"]
                        r.status = rdef.get("status", r.status)
                        r.bsp = rdef.get("bsp", r.bsp)
                    else:
                        runners[rid] = RunnerState(
                            rdef["name"],
                            rdef["sortPriority"]
                        )

            # ------------------------------
            # RUNNER CHANGES (rc)
            # ------------------------------
            if "rc" in mc:
                apply_rc_list(runners, mc["rc"])

        # ------------------------------
        # RENDER VIDEO FRAME
        # ------------------------------
        if last_frame_time is None:
            last_frame_time = pt

        frame_interval = get_frame_interval(pt, market_start_ms)

        if pt - last_frame_time >= frame_interval:
            rows, market_volume = build_rows()
            frame = draw_table(ax, rows, pt, market_volume)
            video.write(frame)
            last_frame_time = pt

        # progress logging
        if line_number % 100 == 0:
            print(f"Processed {line_number} lines")

video.release()
plt.close()

print("Done → market.mp4")

```

---

As mentioned, this takes a while. For this one market, the video took about 15 minutes to process and render, so isn't suitable to processing large volumes of markets. However, it's a useful tool to be able to use to replay markets of interest or just as a little project to work on and improve to be more visually "cool". Who said you need a camera to create a video file?

Any Australian customers interested in accessing the PRO files can contact automation@betfair.com.au.

---

## Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.