# Betfair API tutorial in Python

This tutorial will walk you through the process of connecting to Betfair's API, grabbing data and placing a bet in Python. It will utilise the `betfairlightweight` Python library.

---
## Requirements

This tutorial will assume that you have an API app key. If you don't, please follow [the steps outlined here](../../api/apiappkey).

This tutorial will also assume that you have a basic understanding of what an API is. For a summary in layman's terms, [read this article](https://medium.freecodecamp.org/what-is-an-api-in-english-please-b880a3214a82).

---
## Quick Links

Here are some other useful links for accessing our API:

- [How to create an API app key](../../api/apiappkey)
- [Developer Docs](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni) - the official dev docs for Betfair's API
- [Sports API Visualiser](https://docs.developer.betfair.com/visualisers/api-ng-sports-operations/) - Useful for exploring what the API has to offer
- [Account API Visualiser](https://docs.developer.betfair.com/visualisers/api-ng-account-operations/)
- [Examples using `betfairlightweight`](https://github.com/liampauling/betfair/tree/master/examples)
- There's a more [complete list of resources here](../../index)

---
##Getting Started

### Setting Up Your Certificates

To use the API securely, Betfair recommends generating certificates. The `betfairlightweight` package requires this to login non-interactively. For detailed instructions on how to generate certificates on a windows machine, follow the [instructions outlined here](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Certificate+Generation+With+XCA). For alternate instructions for Windows, or for Mac/Linux machines, follow the [instructions outlined here](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Non-Interactive+%28bot%29+login). You should then create a folder for your certs, perhaps named 'certs' and grab the path location.

### Installing `betfairlightweight`

We also need to install `betfairlightweight`. To do this, simply use pip install `betfairlightweight` in the cmd prompt/terminal. If this doesn't work, you will have to Google your error. If you're just starting out with Python, you may have to add Python to your environment variables.

---
## Sending Requests to the API

### Log into the API Client

Now we're finally ready to log in and use the API. First, we create an APIClient object and then log in. To log in, we'll need to specify where we put our certs. In this example, I'll put them in a folder named 'certs', on my desktop.

You'll also need to change the `username`, `password` and `app_key` variables to your own.

**`In [206]:`**

``` py
# Import libraries
import betfairlightweight
from betfairlightweight import filters
import pandas as pd
import numpy as np
import os
import datetime
import json

# Change this certs path to wherever you're storing your certificates

# Your credentials.json file should look like this:

# {
#     "username" : "johnsmith123",
#     "password" : "guest",
#     "app_key" : "****************"
# }

with open('credentials.json') as f:
    cred = json.load(f)
    my_username = cred['username']
    my_password = cred['password']
    my_app_key = cred['app_key']

trading = betfairlightweight.APIClient(username=my_username,
                                       password=my_password,
                                       app_key=my_app_key,
                                       certs=certs_path)

trading.login()

# if you're having issues with certs, you can login this way without using certificates (at your own risk)

# with open('credentials.json') as f:
#     cred = json.load(f)
#     my_username = cred['username']
#     my_password = cred['password']
#     my_app_key = cred['app_key']

# trading = betfairlightweight.APIClient(username=my_username,
#                                        password=my_password,
#                                        app_key=my_app_key
#                                        )

# trading.login_interactive()

```

**`Out[206]:`**

``` python
<LoginResource>
```

### Get Event IDs
Betfair's API has a number of operations. For example, if you want to list the market book for a market, you would use the listMarketBook operation. These endpoints are shown in the [Sports API Visualiser](https://docs.developer.betfair.com/visualisers/api-ng-sports-operations/) and in the docs. They are also listed below:

#### Sports API

- listEventTypes
- listCompetitions
- listTimeRanges
- listEvents
- listMarketTypes
- listCountries
- listVenues
- listMarketCatalogue
- listMarketBook
- listRunnerBook
- placeOrders
- cancelOrders
- updateOrders
- replaceOrders
- listCurrentOrders
- listClearedOrders
- listMarketProfitAndLoss

The Account Operations API operations/endpoints [can be found here](https://docs.developer.betfair.com/visualisers/api-ng-account-operations/).

First we need to grab the 'Event Type Id'. Each sport has a different ID. Below we will find the ids for all sports by requesting the event_type_ids without a filter.

**`In [43]:`**

``` python
# Grab all event type ids. This will return a list which we will iterate over to print out the id and the name of the sport
event_types = trading.betting.list_event_types()

sport_ids = pd.DataFrame({
    'Sport': [event_type_object.event_type.name for event_type_object in event_types],
    'ID': [event_type_object.event_type.id for event_type_object in event_types]
}).set_index('Sport').sort_index()

sport_ids
```

**`Out[43]:`**

Sport | ID	
--------|--------
American Football	| 6423
Athletics	| 3988
Australian Rules	| 61420
Baseball	| 7511
Basketball	| 7522
Boxing	| 6
Chess	| 136332
Cricket	| 4
Cycling	| 11
Darts	| 3503
Esports	| 27454571
Financial Bets	| 6231
Gaelic Games	| 2152880
Golf	| 3
Greyhound Racing	| 4339
Handball	| 468328
Horse Racing	| 7
Ice Hockey	| 7524
Mixed Martial Arts	| 26420387
Motor Sport	| 8
Netball	| 606611
Politics	| 2378961
Rugby League	| 1477
Rugby Union	| 5
Snooker	| 6422
Soccer	| 1
Special Bets	| 10
Tennis	| 2
Volleyball	| 998917

If we just wanted to get the event id for horse racing, we could use the filter function from `betfairlightweight` as shown in the examples and below.

**`In [50]:`**

``` python
# Filter for just horse racing
horse_racing_filter = betfairlightweight.filters.market_filter(text_query='Horse Racing')

# This returns a list
horse_racing_event_type = trading.betting.list_event_types(
    filter=horse_racing_filter)

# Get the first element of the list
horse_racing_event_type = horse_racing_event_type[0]

horse_racing_event_type_id = horse_racing_event_type.event_type.id
print(f"The event type id for horse racing is {horse_racing_event_type_id}")

# The event type id for horse racing is 7
```

### Get Competition IDs

Sometimes you may want to get markets based on the competition. An example may be the Brownlow medal, or the EPL. Let's have a look at all the soccer competitions over the next week and filter to only get the EPL Competition ID.

**`In [90]:`**

``` python
# Get a datetime object in a week and convert to string
datetime_in_a_week = (datetime.datetime.utcnow() + datetime.timedelta(weeks=1)).strftime("%Y-%m-%dT%TZ")

# Create a competition filter
competition_filter = betfairlightweight.filters.market_filter(
    event_type_ids=[1], # Soccer's event type id is 1
    market_start_time={
        'to': datetime_in_a_week
    })

# Get a list of competitions for soccer
competitions = trading.betting.list_competitions(
    filter=competition_filter
)

# Iterate over the competitions and create a dataframe of competitions and competition ids
soccer_competitions = pd.DataFrame({
    'Competition': [competition_object.competition.name for competition_object in competitions],
    'ID': [competition_object.competition.id for competition_object in competitions]
})
```

**`In [94]:`**

``` python
# Get the English Premier League Competition ID
soccer_competitions[soccer_competitions.Competition.str.contains('English Premier')]
```

**`Out[94]:`**

| | Competition	| ID
---|-----------|-------
116	| English Premier League	| 10932509

### Get Upcoming Events

Say you want to get all the upcoming events for Thoroughbreads for the next 24 hours. We will use the `listEvents` operation for this. First, as before, we define a market filter, and then using the betting method from our trading object which we defined earlier.

**`In [207]:`**

``` python
# Define a market filter
thoroughbreds_event_filter = betfairlightweight.filters.market_filter(
    event_type_ids=[horse_racing_event_type_id],
    market_countries=['AU'],
    market_start_time={
        'to': (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%TZ")
    }
)

# Print the filter
thoroughbreds_event_filter
```

**`Out[207]:`**

``` python
{'eventTypeIds': ['7'],
 'marketCountries': ['AU'],
 'marketStartTime': {'to': '2018-10-26T22:25:00Z'}}
```

**`In [208]:`**

``` python
# Get a list of all thoroughbred events as objects
aus_thoroughbred_events = trading.betting.list_events(
    filter=thoroughbreds_event_filter
)

# Create a DataFrame with all the events by iterating over each event object
aus_thoroughbred_events_today = pd.DataFrame({
    'Event Name': [event_object.event.name for event_object in aus_thoroughbred_events],
    'Event ID': [event_object.event.id for event_object in aus_thoroughbred_events],
    'Event Venue': [event_object.event.venue for event_object in aus_thoroughbred_events],
    'Country Code': [event_object.event.country_code for event_object in aus_thoroughbred_events],
    'Time Zone': [event_object.event.time_zone for event_object in aus_thoroughbred_events],
    'Open Date': [event_object.event.open_date for event_object in aus_thoroughbred_events],
    'Market Count': [event_object.market_count for event_object in aus_thoroughbred_events]
})

aus_thoroughbred_events_today
```

**`Out[208]:`**

| | Event Name	| Event ID	| Event Venue	| Country Code	| Time Zone	| Open Date	| Market Count
---|---|---|---|---|---|---|---
0	| MVal (AUS) 26th Oct	| 28971066	| Moonee Valley	| AU	| Australia/Sydney	| 2018-10-26 07:30:00	| 24
1	| Newc (AUS) 26th Oct	| 28974559	| Newcastle	| AU	| Australia/Sydney	| 2018-10-26 07:07:00	| 20
2	| Bath (AUS) 26th Oct	| 28974547	| Bathurst	| AU	| Australia/Sydney	| 2018-10-26 02:43:00	| 16
3	| Cant (AUS) 26th Oct	| 28974545	| Canterbury	| AU	| Australia/Sydney	| 2018-10-26 07:15:00	| 16
4	| Scne (AUS) 26th Oct	| 28973942	| Scone	| AU	| Australia/Sydney	| 2018-10-26 02:25:00	| 16
5	| Gawl (AUS) 26th Oct	| 28974550	| Gawler	| AU	| Australia/Adelaide	| 2018-10-26 04:00:00	| 16
6	| Gatt (AUS) 26th Oct	| 28974549	| Gatton	| AU	| Australia/Queensland	| 2018-10-26 01:55:00	| 16
7	| GlPk (AUS) 26th Oct	| 28974562	| Gloucester Park	| AU	| Australia/Perth	| 2018-10-26 09:10:00	| 20
8	| Hoba (AUS) 26th Oct	| 28974563	| Hobart	| AU	| Australia/Sydney	| 2018-10-26 05:23:00	| 18
9	| Echu (AUS) 26th Oct	| 28974016	| Echuca	| AU	| Australia/Sydney	| 2018-10-26 01:30:00	| 18
10	| Melt (AUS) 26th Oct	| 28974560	| Melton	| AU	| Australia/Sydney	| 2018-10-26 07:18:00	| 18
11	| MVal (AUS) 26th Oct	| 28921730	| None	| AU	| Australia/Sydney	| 2018-10-26 11:00:00	| 1
12	| Redc (AUS) 26th Oct	| 28974561	| Redcliffe	| AU	| Australia/Queensland	| 2018-10-26 02:17:00	| 16
13	| SCst (AUS) 26th Oct	| 28974149	| Sunshine Coast	| AU	| Australia/Queensland	| 2018-10-26 06:42:00	| 20

### Get Market Types

Say we want to know what market types a certain event is offering. To do this, we use the `listMarketTypes` operation. Let's take the Moonee Valley event from above (ID: 28971066). As this is a horse race we would expect that it would have Win and Place markets.

**`In [209]:`**

``` python
# Define a market filter
market_types_filter = betfairlightweight.filters.market_filter(event_ids=['28971066'])

# Request market types
market_types = trading.betting.list_market_types(
        filter=market_types_filter
)

# Create a DataFrame of market types
market_types_mooney_valley = pd.DataFrame({
    'Market Type': [market_type_object.market_type for market_type_object in market_types],
})

market_types_mooney_valley
```

**`Out[209]:`**

Market | Type
-------|-------
0	| OTHER_PLACE
1	| PLACE
2	| WIN

### Get Market Catalogues

If we want to know the various market names that there are for a particular event, as well as how much has been matched on each market, we want to request data from the `listMarketCatalogue` operation. We can provide a number of filters, including the Competition ID, the Event ID, the Venue etc. to the filter.

We must also specify the maximum number of results, and if we want additional data like the event data or runner data, we can also request that.

For a more comprehensive understanding of the options for filters and what we can request, please have a look at the [Sports API Visualiser](https://docs.developer.betfair.com/visualisers/api-ng-sports-operations/). The options listed under market filter should be put into a filter, whilst the others should be arguments to the relevant operation function in `betfairlightweight`.

For example, if we want all the markets for Moonee Valley, we should use the following filters and arguments.

**`In [210]:`**

``` python
market_catalogue_filter = betfairlightweight.filters.market_filter(event_ids=['28971066'])

market_catalogues = trading.betting.list_market_catalogue(
    filter=market_catalogue_filter,
    max_results='100',
    sort='FIRST_TO_START'
)

# Create a DataFrame for each market catalogue
market_types_mooney_valley = pd.DataFrame({
    'Market Name': [market_cat_object.market_name for market_cat_object in market_catalogues],
    'Market ID': [market_cat_object.market_id for market_cat_object in market_catalogues],
    'Total Matched': [market_cat_object.total_matched for market_cat_object in market_catalogues],
})

market_types_mooney_valley
```

**`Out[210]:`**

| | Market Name	| Market ID	| Total Matched
---|---|---|---
0	| 4 TBP	| 1.150090094	| 0.000000
1	| To Be Placed	| 1.150090092	| 0.000000
2	| R1 1000m 3yo	| 1.150090091	| 2250.188360
3	| 4 TBP	| 1.150090101	| 0.000000
4	| To Be Placed	| 1.150090099	| 141.775816
5	| R2 2040m Hcap	| 1.150090098	| 1093.481760
6	| To Be Placed	| 1.150090106	| 0.000000
7	| R3 1500m Hcap	| 1.150090105	| 1499.642480
8	| 4 TBP	| 1.150090108	| 0.000000
9	| To Be Placed	| 1.150090113	| 19.855136
10	| R4 2040m Hcap	| 1.150090112	| 588.190288
11	| 4 TBP	| 1.150090115	| 0.000000
12	| 4 TBP	| 1.150090122	| 0.000000
13	| R5 955m Hcap	| 1.150090119	| 545.762616
14	| To Be Placed	| 1.150090120	| 91.920584
15	| 4 TBP	| 1.150090129	| 48.623344
16	| To Be Placed	| 1.150090127	| 65.616152
17	| R6 1200m Hcap	| 1.150090126	| 506.342200
18	| R7 1200m Grp1	| 1.150038686	| 34480.834976
19	| 4 TBP	| 1.150038689	| 701.052968
20	| To Be Placed	| 1.150038687	| 1504.823656
21	| R8 1500m Hcap	| 1.150090140	| 232.971760
22	| 4 TBP	| 1.150090143	| 0.000000
23	| To Be Placed	| 1.150090141	| 73.768352

### Get Market Books

If we then want to get the prices available/last traded for a market, we should use the `listMarketBook` operation. Let's Look at the market book for Moonee Valley R7. We will need to define a function which processes the runner books and collates the data into a DataFrame.

**`In [212]:`**

``` python
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
    best_back_sizes = [runner_book.ex.available_to_back[0]['size']
        if runner_book.ex.available_to_back
        else 1.01
        for runner_book
        in runner_books]

    best_lay_prices = [runner_book.ex.available_to_lay[0]['price']
        if runner_book.ex.available_to_lay
        else 1000.0
        for runner_book
        in runner_books]
    best_lay_sizes = [runner_book.ex.available_to_lay[0]['size']
        if runner_book.ex.available_to_lay
        else 1.01
        for runner_book
        in runner_books]
    
    selection_ids = [runner_book.selection_id for runner_book in runner_books]
    last_prices_traded = [runner_book.last_price_traded for runner_book in runner_books]
    total_matched = [runner_book.total_matched for runner_book in runner_books]
    statuses = [runner_book.status for runner_book in runner_books]
    scratching_datetimes = [runner_book.removal_date for runner_book in runner_books]
    adjustment_factors = [runner_book.adjustment_factor for runner_book in runner_books]

    df = pd.DataFrame({
        'Selection ID': selection_ids,
        'Best Back Price': best_back_prices,
        'Best Back Size': best_back_sizes,
        'Best Lay Price': best_lay_prices,
        'Best Lay Size': best_lay_sizes,
        'Last Price Traded': last_prices_traded,
        'Total Matched': total_matched,
        'Status': statuses,
        'Removal Date': scratching_datetimes,
        'Adjustment Factor': adjustment_factors
    })
    return df
```

**`In [213]:`**

``` python
# Create a price filter. Get all traded and offer data
price_filter = betfairlightweight.filters.price_projection(
    price_data=['EX_BEST_OFFERS']
)

# Request market books
market_books = trading.betting.list_market_book(
    market_ids=['1.150038686'],
    price_projection=price_filter
)

# Grab the first market book from the returned list as we only requested one market 
market_book = market_books[0]

runners_df = process_runner_books(market_book.runners)

runners_df
```

**`Out[213]:`**

| | Selection ID	| Best Back Price	| Best Back Size	| Best Lay Price	| Best Lay Size	| Last Price Traded	| Total Matched	| Status	| Removal | Date	| Adjustment Factor
---|---|---|---|---|---|---|---|---|---|---|---
0	| 16905731	| 12.0	| 65.54	| 13.0	| 33.09	| 12.0	| 1226.67	| ACTIVE	| None	| 8.333
1	| 15815968	| 6.6	| 96.64	| 7.0	| 9.00	| 6.6	| 5858.61	| ACTIVE	| None	| 14.286
2	| 9384677	| 14.0	| 114.71	| 15.0	| 76.71	| 14.0	| 964.80	| ACTIVE	| None	| 6.667
3	| 8198751	| 17.5	| 14.67	| 19.0	| 33.02	| 17.5	| 940.56	| ACTIVE	| None	| 5.556
4	| 9507057	| 38.0	| 53.13	| 100.0	| 40.22	| 46.0	| 224.72	| ACTIVE	| None	| 3.125
5	| 21283266	| 15.0	| 121.46	| 19.5	| 5.56	| 19.5	| 1102.37	| ACTIVE	| None	| 7.692
6	| 21283267	| 80.0	| 37.58	| 760.0	| 9.70	| 760.0	| 125.30	| ACTIVE	| None	| 1.087
7	| 21063807	| 6.4	| 1503.62	| 7.2	| 50.00	| 6.6	| 8011.44	| ACTIVE	| None	| 13.333
8	| 21283268	| 48.0	| 54.57	| 60.0	| 51.93	| 50.0	| 150.22	| ACTIVE	| None	| 2.381
9	| 21283269	| 8.8	| 235.77	| 9.4	| 30.40	| 8.8	| 1729.96	| ACTIVE	| None	| 11.111
10	| 4883975	| 46.0	| 33.42	| 55.0	| 5.00	| 46.0	| 208.45	| ACTIVE	| None	| 2.381
11	| 202351	| 25.0	| 20.00	| 30.0	| 6.00	| 24.0	| 658.09	| ACTIVE	| None	| 2.632
12	| 21283270	| 19.5	| 69.33	| 22.0	| 20.00	| 19.5	| 825.59	| ACTIVE	| None	| 4.545
13	| 21283271	| 5.3	| 96.14	| 5.7	| 5.03	| 5.3	| 12654.32	| ACTIVE	| None	| 16.871

---
## Orderbook Workflow

Now that we have the market book in an easy to read DataFrame, we can go ahead and start placing orders based on the market book. Although it is a simple (and probably not profitable) strategy, in the next few sections we will be backing the favourite and adjusting our orders.

### Placing Orders

To place an order we use the `placeOrders` operation. A handy component of `placeOrders` is that you can send your strategy along with the runner that you want to back, so it is extremely easy to analyse how your strategy performed later. Let's place a 5 dollar back bet on the favourite at $7 call this strategy `'back_the_fav'`.

Note that if you are placing a limit order you must specify a price which is allowed by Betfair. For example, the price 6.3 isn't allowed, whereas 6.4 is, as prices go up by 20c increments at that price range. You can read about [tick points here](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/placeOrders#placeOrders-BetfairPriceIncrements).

**`In [232]:`**

``` python
# Get the favourite's price and selection id
fav_selection_id = runners_df.loc[runners_df['Best Back Price'].idxmin(), 'Selection ID']
fav_price = runners_df.loc[runners_df['Best Back Price'].idxmin(), 'Best Back Price']
```

**`In [276]:`**

``` python
# Define a limit order filter
limit_order_filter = betfairlightweight.filters.limit_order(
    size=5, 
    price=7,
    persistence_type='LAPSE'
)

# Define an instructions filter
instructions_filter = betfairlightweight.filters.place_instruction(
    selection_id=str(fav_selection_id),
    order_type="LIMIT",
    side="BACK",
    limit_order=limit_order_filter
)

instructions_filter
```

**`Out[276]:`**

``` python
{'limitOrder': {'persistenceType': 'LAPSE', 'price': 7, 'size': 5},
 'orderType': 'LIMIT',
 'selectionId': '21283271',
 'side': 'BACK'}
```

**`In [277]:`**

``` python
# Place the order
order = trading.betting.place_orders(
    market_id='1.150038686', # The market id we obtained from before
    customer_strategy_ref='back_the_fav',
    instructions=[instructions_filter] # This must be a list
)
```

Now that we've placed the other, we can check if the order placing was a success and if any has been matched.

**`In [306]:`**

``` python
order.__dict__
```

**`Out[306]:`**

``` python
{'_data': {'instructionReports': [{'averagePriceMatched': 0.0,
    'betId': '142384852665',
    'instruction': {'limitOrder': {'persistenceType': 'LAPSE',
      'price': 7.0,
      'size': 5.0},
     'orderType': 'LIMIT',
     'selectionId': 21283271,
     'side': 'BACK'},
    'orderStatus': 'EXECUTABLE',
    'placedDate': '2018-10-26T00:46:46.000Z',
    'sizeMatched': 0.0,
    'status': 'SUCCESS'}],
  'marketId': '1.150038686',
  'status': 'SUCCESS'},
 '_datetime_created': datetime.datetime(2018, 10, 26, 0, 46, 46, 455349),
 '_datetime_updated': datetime.datetime(2018, 10, 26, 0, 46, 46, 455349),
 'customer_ref': None,
 'elapsed_time': 1.484069,
 'error_code': None,
 'market_id': '1.150038686',
 'place_instruction_reports': [<betfairlightweight.resources.bettingresources.PlaceOrderInstructionReports at 0x23e0f7952e8>],
 'status': 'SUCCESS'}
```

As we can see, the status is `'SUCCESS'`, whilst the `sizeMatched` is 0. Let's now look at our current orders.

### Get Current Orders

To get our current orders, we need to use the `listCurrentOrders` operation. We can then use either the bet id, the market id, or the bet strategy to filter our orders.

**`In [311]:`**

``` python
trading.betting.list_current_orders(customer_strategy_refs=['back_the_fav']).__dict__
Out[311]:
{'_data': {'currentOrders': [{'averagePriceMatched': 0.0,
    'betId': '142384852665',
    'bspLiability': 0.0,
    'customerStrategyRef': 'back_the_fav',
    'handicap': 0.0,
    'marketId': '1.150038686',
    'orderType': 'LIMIT',
    'persistenceType': 'LAPSE',
    'placedDate': '2018-10-26T00:46:46.000Z',
    'priceSize': {'price': 7.0, 'size': 5.0},
    'regulatorCode': 'MALTA LOTTERIES AND GAMBLING AUTHORITY',
    'selectionId': 21283271,
    'side': 'BACK',
    'sizeCancelled': 0.0,
    'sizeLapsed': 0.0,
    'sizeMatched': 0.0,
    'sizeRemaining': 5.0,
    'sizeVoided': 0.0,
    'status': 'EXECUTABLE'}],
  'moreAvailable': False},
 '_datetime_created': datetime.datetime(2018, 10, 26, 2, 14, 56, 84036),
 '_datetime_updated': datetime.datetime(2018, 10, 26, 2, 14, 56, 84036),
 'elapsed_time': 1.327456,
 'more_available': False,
 'orders': [<betfairlightweight.resources.bettingresources.CurrentOrder at 0x23e0e7acd30>],
 'publish_time': None,
 'streaming_unique_id': None,
 'streaming_update': None}
```

As we can see, we have one order which is unmatched for our strategy `'back_the_fav'`

### Cancelling Orders

Let's now cancel this bet. To do this, we will use the `cancelOrders` operation. If you pass in a market ID it will cancel all orders for that specific market ID, like you can do on the website.

**`In [312]:`**

``` python
cancelled_order = trading.betting.cancel_orders(market_id='1.150038686')
```

**`In [328]:`**

``` python
# Create a DataFrame to view the instruction report
pd.Series(cancelled_order.cancel_instruction_reports[0].__dict__).to_frame().T
```

**`Out[328]:`**

| | status	| size_cancelled	| cancelled_date	| instruction	| error_code
---|---|---|---|---|---
0	| SUCCESS	| 5	| 2018-10-26 06:01:26	| betfairlightweight.resources.bettingresources...	| None

---
## Get Past Orders and Results
If we want to go back and look at past orders we have made, there are two main operations for this:

- `listClearedOrders` - this operation takes a range of data down to the individual selection ID level, and returns a summary of those specific orders
- `listMarketProfitAndLoss` - this operation is more specific, and only takes Market IDs to return the Profit/Loss for that market
Alternatively, we can use the `getAccountStatement` operation from the Account Operations API.

Let's now use both Sports API operations based on our previous orders and then compare it to the `getAccountStatement` operation.

### Get Cleared Orders

**`In [346]:`**

``` python
# listClearedOrders
cleared_orders = trading.betting.list_cleared_orders(bet_status="SETTLED",
                                                    market_ids=["1.150038686"])
```

**`In [371]:`**

``` python
# Create a DataFrame from the orders
pd.DataFrame(cleared_orders._data['clearedOrders'])
```

**`Out[371]:`**

| | betCount	| betId	| betOutcome	| eventId	| eventTypeId	| handicap	| lastMatchedDate	| marketId	| orderType	| persistenceType	| placedDate	| priceMatched	| priceReduced	| priceRequested	| profit	| selectionId	| settledDate	| side	| sizeSettled
---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---
0	| 1	| 142383373022	| LOST	| 28971066	| 7	| 0.0	| 2018-10-26T10:31:53.000Z	| 1.150038686	| MARKET_ON_CLOSE	| LAPSE	| 2018-10-26T00:12:03.000Z	| 5.74	| False	| 5.74	| -5.0	| 21283271	| 2018-10-26T10:34:39.000Z	| BACK	| 5.0
1	| 1	| 142383570640	| WON	| 28971066	| 7	| 0.0	| 2018-10-26T00:16:32.000Z	| 1.150038686	| LIMIT	| LAPSE	| 2018-10-26T00:16:31.000Z	| 5.40	| False	| 5.50	| 5.0	| 21283271	| 2018-10-26T10:34:39.000Z	| LAY	| 5.0

Note that we can also filter for certain dates, bet ids, event ids, selection ids etc. We can also group by the event type, the event, the market, the runner, the side, the bet and the strategy, which is extremely useful if you're looking for a quick summary of how your strategy is performing.

### Get Market Profit and Loss

Now let's find the Profit and Loss for the market. To do this we will use the `listMarketProfitAndLoss` operation. Note that this function only works with market IDs, and once the website clears the market, the operation will no longer work. However the market is generally up for about a minute after the race, so if your strategy is automated, you can check once if your bet is settled and if it is, hit the `getMarketProfitAndLoss` endpoint.

Because of this, we will check a different market ID to the example above.

**`In [406]:`**

``` python
# Get the profit/loss - this returns a list
pl = trading.betting.list_market_profit_and_loss(market_ids=["1.150318913"], 
                                                 include_bsp_bets='true', 
                                                 include_settled_bets='true')
```

**`In [410]:`**

``` python
# Create a profit/loss DataFrame
pl_df = pd.DataFrame(pl[0]._data['profitAndLosses']).assign(marketId=pl[0].market_id)
pl_df
```

**`Out[410]:`**

| | ifWin	| selectionId	| marketId
---|---|---|---
0	| -5.0	| 10065177	| 1.150318913
1	| 14.0	| 17029506	| 1.150318913
2	| -5.0	| 5390339	| 1.150318913
3	| -5.0	| 13771011	| 1.150318913
4	| -5.0	| 138209	| 1.150318913
5	| -5.0	| 10503541	| 1.150318913
6	| -5.0	| 12165809	| 1.150318913

### Get Account Statement

Another method is to use the `getAccountStatement`, which provides an overview of all your bets over a certain time period. You can then filter this for specific dates if you wish.

**`In [428]:`**

``` python
# Define a date filter - get all bets for the past 4 days
four_days_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=4)).strftime("%Y-%m-%dT%TZ")
acct_statement_date_filter = betfairlightweight.filters.time_range(from_=four_days_ago)

# Request account statement
account_statement = trading.account.get_account_statement(item_date_range=acct_statement_date_filter)
```

**`In [450]:`**

``` python
# Create df of recent transactions
recent_transactions = pd.DataFrame(account_statement._data['accountStatement'])
recent_transactions
```

**`Out[450]:`**

| | amount	| balance	| itemClass	| itemClassData	| itemDate	| legacyData	| refId
---|---|---|---|---|---|---|---
0	| -5.0	| 256.74	| UNKNOWN	{'unknownStatementItem': '{"avgPrice":3.8,"bet...	| 2018-10-28T23:14:28.000Z	| {'avgPrice': 3.8, 'betSize': 5.0, 'betType': '...	| 142845441633
1	| 5.0	| 261.74	| UNKNOWN	| {'unknownStatementItem': '{"avgPrice":5.4,"bet...	| 2018-10-26T10:34:39.000Z	| {'avgPrice': 5.4, 'betSize': 5.0, 'betType': '...	| 142383570640
2	| -5.0	| 256.74	| UNKNOWN	| {'unknownStatementItem': '{"avgPrice":5.74,"be...	| 2018-10-26T10:34:39.000Z	| {'avgPrice': 5.74, 'betSize': 5.0, 'betType': ...	| 142383373022

**`In [468]:`**

``` python
# Create df of itemClassData - iterate over the account statement list and convert to json so that the DataFrame function
# can read it correctly
class_data = [json.loads(account_statement.account_statement[i].item_class_data['unknownStatementItem']) 
              for i in range(len(account_statement.account_statement))]
```

**`In [471]:`**

``` python
class_df = pd.DataFrame(class_data)
class_df
```

**`Out [471]:`**

| | avgPrice	| betCategoryType	| betSize	| betType	| commissionRate	| eventId	| eventTypeId	| fullMarketName	| grossBetAmount	| marketName	| marketType	| placedDate	| selectionId	| selectionName	| startDate	| transactionId	| transactionType	| winLose
---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---
0	| 3.80	| M	| 5.0	B	| None	| 150318913	| 7	| USA / TPara (US) 28th Oct/ 16:06 R8 1m Allw Claim	| 0.0	| R8 1m Allw Claim	| O	| 2018-10-28T23:02:28.000Z	| 17029506	| Gato Guapo	| 2018-10-28T23:06:00.000Z	| 0	| ACCOUNT_DEBIT	| RESULT_LOST
1	| 5.40	| E	| 5.0	| L	| None	| 150038686	| 7	| AUS / MVal (AUS) 26th Oct/ 21:30 R7 1200m Grp1	| 0.0	| R7 1200m Grp1	| O	| 2018-10-26T00:16:31.000Z	| 21283271	| 14. Sunlight	| 2018-10-26T10:30:00.000Z	| 0	| | ACCOUNT_CREDIT	| RESULT_WON
2	| 5.74	| M	| 5.0	| B	| None	| 150038686	| 7	| AUS / MVal (AUS) 26th Oct/ 21:30 R7 1200m Grp1	| 0.0	| R7 1200m Grp1	| O	| 2018-10-26T00:12:03.000Z	| 21283271	| 14. Sunlight	| 2018-10-26T10:30:00.000Z	| 0	| ACCOUNT_DEBIT	| RESULT_LOST

As we can see, this DataFrame provides a much more comprehensive view of each of our bets. However, it lacks the ability to filter by strategy like the `listClearedOrders` operation in the Sports API.