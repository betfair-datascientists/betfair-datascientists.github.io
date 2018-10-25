# AFL Modelling Walkthrough 

# 01. Data Cleaning

These tutorials will walk you through how to construct your own basic AFL model, using publicly available data. The output will be odds for each team to win, which will be shown on [The Hub](https://www.betfair.com.au/hub/tools/models/afl-prediction-model/).

In this notebook we will walk you through the basics of cleaning this dataset and how we have done it. If you want to get straight to feature creation or modelling, feel free to jump ahead!

```python
# Import libraries
import pandas as pd
import numpy as np
import re
pd.set_option('display.max_columns', None)
```

We will first explore the DataFrames, and then create functions to wrangle them and clean them into more consistent sets of data.

```python
# Read/clean each DataFrame
match_results = pd.read_csv("data/afl_match_results.csv")
odds = pd.read_csv("data/afl_odds.csv")
player_stats = pd.read_csv("data/afl_player_stats.csv")
```

```python
odds.tail(3)
```

|  |trunc     |event_name|path                                 |selection_name |odds
|----|----------|----------|-------------------------------------|---------------|------
|4179|2018-09-01|Match Odds|VFL/Richmond Reserves v Williamstown |Williamstown   |2.3878
|4180|2018-09-01|Match Odds|WAFL/South Fremantle v West Perth    |South Fremantle|1.5024
|4181|2018-09-01|Match Odds|WAFL/South Fremantle v West Perth    |West Perth     |2.7382

```python
match_results.tail(3)
```

| |Game|Date|Round|Home.Team|Home.Goals|Home.Behinds|Home.Points|Away.Team|Away.Goals|Away.Behinds|Away.Points|Venue|Margin|Season|Round.Type|Round.Number
|-----|-----|----------|---|---|---|---|---|---|---|---|---|---|---|---|---|---
|15395|15396|2018-08-26|R23|Brisbane Lions|11|6|72|West Coast|14|14|98|Gabba|-26|2018|Regular|23
|15396|15397|2018-08-26|R23|Melbourne|15|12|102|GWS|8|9|57|M.C.G.|45|2018|Regular|23
|15397|15398|2018-08-26|R23|St Kilda|14|10|94|North Melbourne|17|15|117|Docklands|-23|2018|Regular|23

```python
player_stats.tail(3)
```

| |AF|B|BO|CCL|CG|CL|CM|CP|D|DE|Date|ED|FA|FF|G|GA|HB|HO|I50|ITC|K|M|MG|MI5|Match\_id|One.Percenters|Opposition|Player|R50|Round|SC|SCL|SI|Season|Status|T|T5|TO|TOG|Team|UP|Venue
|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:
|89317|38|1|0|0.0|0|0|1|2|9|55.6|25/08/2018|5|0|0|0|0|3|0|0|2.0|6|3|132.0|2|9711|0|Fremantle|Christopher Mayne|1|Round 23|35|0.0|2.0|2018|Away|1|0.0|1.0|57|Collingwood|7|Optus Stadium
|89318|38|0|0|0.0|3|0|0|3|9|55.6|25/08/2018|5|0|1|0|0|3|0|0|4.0|6|3|172.0|0|9711|2|Fremantle|Nathan Murphy|5|Round 23|29|0.0|0.0|2018|Away|1|0.0|3.0|70|Collingwood|6|Optus Stadium
|89319|56|1|0|0.0|1|0|0|3|8|62.5|25/08/2018|5|0|0|2|0|2|0|0|2.0|6|3|180.0|3|9711|2|Fremantle|Jaidyn Stephenson|0|Round 23|56|0.0|4.0|2018|Away|3|1.0|2.0|87|Collingwood|5|Optus Stadium

Have a look at the structure of the DataFrames. Notice that for the odds DataFrame, each game is split between two rows, whilst for the match_results each game is on one row. We will have to get around this by splitting the games up onto two rows, as this will allow our feature transformation functions to be applied more easily later on. For the player_stats DataFrame we will aggregate these stats into each game on separate rows.

First, we will write functions to make the odds data look a bit nicer, with only a team column, a date column and a 'home_game' column which takes the values 0 or 1 depending on if it was a home game for that team. To do this we will use the [regex](https://docs.python.org/3/howto/regex.html) module to extract the team names from the path column, as well as the to_datetime function from pandas. We will also replace all the inconsistent team names with consistent team names.

```python
def get_cleaned_odds(df=None):
    # If a df hasn't been specified as a parameter, read the odds df
    if df is None:
        df = pd.read_csv("data/afl_odds.csv")

    # Get a dictionary of team names we want to change and their new values
    team_name_mapping = {
    'Adelaide Crows': 'Adelaide',
    'Brisbane Lions': 'Brisbane',
    'Carlton Blues': 'Carlton',
    'Collingwood Magpies': 'Collingwood',
    'Essendon Bombers': 'Essendon',
    'Fremantle Dockers': 'Fremantle',
    'GWS Giants': 'GWS',
    'Geelong Cats': 'Geelong',
    'Gold Coast Suns': 'Gold Coast',
    'Greater Western Sydney': 'GWS',
    'Greater Western Sydney Giants': 'GWS',
    'Hawthorn Hawks': 'Hawthorn',
    'Melbourne Demons': 'Melbourne', 
    'North Melbourne Kangaroos': 'North Melbourne',
    'Port Adelaide Magpies': 'Port Adelaide',
    'Port Adelaide Power': 'Port Adelaide', 
    'P Adelaide': 'Port Adelaide',
    'Richmond Tigers': 'Richmond',
    'St Kilda Saints': 'St Kilda', 
    'Sydney Swans': 'Sydney',
    'West Coast Eagles': 'West Coast',
    'Wetsern Bulldogs': 'Western Bulldogs',
    'Western Bullbogs': 'Western Bulldogs'
    }

    # Add columns
    df = (df.assign(date=lambda df: pd.to_datetime(df.trunc), # Create a datetime column
                    home_team=lambda df: df.path.str.extract('(([\w\s]+) v ([\w\s]+))', expand=True)[1].str.strip(),
                    away_team=lambda df: df.path.str.extract('(([\w\s]+) v ([\w\s]+))', expand=True)[2].str.strip())
            .drop(columns=['path', 'trunc', 'event_name']) # Drop irrelevant columns
            .rename(columns={'selection_name': 'team'}) # Rename columns
            .replace(team_name_mapping)
            .sort_values(by='date')
            .reset_index(drop=True)
            .assign(home_game=lambda df: df.apply(lambda row: 1 if row.home_team == row.team else 0, axis='columns'))
            .drop(columns=['home_team', 'away_team']))
    return df
```

```python
# Apply the wrangling and cleaning function
odds = get_cleaned_odds(odds)
odds.tail()
```

|  | team | odds | date | home_game |
| --- | --- | --- | --- | --- |
| 4177 | South Fremantle | 1.5024 | 2018-09-01 | 1 |
| 4178 | Port Melbourne | 2.8000 | 2018-09-01 | 0 |
| 4179 | Box Hill Hawks | 1.4300 | 2018-09-01 | 1 |
| 4180 | Casey Demons | 1.9000 | 2018-09-01 | 1 |
| 4181 | West Perth | 2.7382 | 2018-09-01 | 0 |

We now have a DataFrame that looks nice and easy to join with our other DataFrames. Now let's lean up the match_details DataFrame.

```python
# Define a function which cleans the match results df, and separates each teams' stats onto individual rows
def get_cleaned_match_results(df=None):
    # If a df hasn't been specified as a parameter, read the match_results df
    if df is None:
        df = pd.read_csv("data/afl_match_results.csv")

    # Create column lists to loop through - these are the columns we want in home and away dfs
    home_columns = ['Game', 'Date', 'Round.Number', 'Home.Team', 'Home.Goals', 'Home.Behinds', 'Home.Points', 'Margin', 'Venue', 'Away.Team', 'Away.Goals', 'Away.Behinds', 'Away.Points']
    away_columns = ['Game', 'Date', 'Round.Number', 'Away.Team', 'Away.Goals', 'Away.Behinds', 'Away.Points', 'Margin', 'Venue', 'Home.Team', 'Home.Goals', 'Home.Behinds', 'Home.Points']
    
    mapping = ['game', 'date', 'round', 'team', 'goals', 'behinds', 'points', 'margin', 'venue', 'opponent', 'opponent_goals', 'opponent_behinds', 'opponent_points']
    
    team_name_mapping = {
    'Brisbane Lions': 'Brisbane',
    'Footscray': 'Western Bulldogs'
    }

    # Create a df with only home games
    df_home = (df[home_columns]
                .rename(columns={old_col: new_col for old_col, new_col in zip(home_columns, mapping)})
                .assign(home_game=1))

    # Create a df with only away games
    df_away = (df[away_columns]
                .rename(columns={old_col: new_col for old_col, new_col in zip(away_columns, mapping)})
                .assign(home_game=0,
                        margin=lambda df: df.margin * -1))

    # Append these dfs together
    new_df = (df_home.append(df_away)
                     .sort_values(by='game') # Sort by game ID
                     .reset_index(drop=True) # Reset index
                     .assign(date=lambda df: pd.to_datetime(df.date)) # Create a datetime column
                     .replace(team_name_mapping)) # Rename team names to be consistent with other dfs
    return new_df
```

```python
match_results = get_cleaned_match_results(match_results)
match_results.head()
```

|  | game | date | round | team | goals | behinds | points | margin | venue | opponent | opponent_goals | opponent_behinds | opponent_points | home_game |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1897-05-08 | 1 | Fitzroy | 6 | 13 | 49 | 33 | Brunswick St | Carlton | 2 | 4 | 16 | 1 |
| 1 | 1 | 1897-05-08 | 1 | Carlton | 2 | 4 | 16 | -33 | Brunswick St | Fitzroy | 6 | 13 | 49 | 0 |
| 2 | 2 | 1897-05-08 | 1 | Collingwood | 5 | 11 | 41 | 25 | Victoria Park | St Kilda | 2 | 4 | 16 | 1 |
| 3 | 2 | 1897-05-08 | 1 | St Kilda | 2 | 4 | 16 | -25 | Victoria Park | Collingwood | 5 | 11 | 41 | 0 |
| 4 | 3 | 1897-05-08 | 1 | Geelong | 3 | 6 | 24 | -23 | Corio Oval | Essendon | 7 | 5 | 47 | 1 |

Now we have both the odds DataFrame and match_results DataFrame ready for feature creation! Finally, we will aggregate the player_stats DataFrame stats for each game rather than individual player stats. For this DataFrame we have regular stats, such as disposals, marks etc. and Advanced Stats, such as Tackles Inside 50 and Metres Gained. However these advanced stats are only available from 2015, so we will not be using them in this tutorial - as there isn't enough data from 2015 to train our models.

Let's now aggregate the player_stats DataFrame.

```python
def get_cleaned_aggregate_player_stats(df=None):
    # If a df hasn't been specified as a parameter, read the player_stats df
    if df is None:
        df = pd.read_csv("data/afl_player_stats.csv")

    agg_stats = (df.rename(columns={ # Rename columns to lowercase
                    'Season': 'season',
                    'Round': 'round',
                    'Team': 'team',
                    'Opposition': 'opponent',
                    'Date': 'date'
                    })
                   .groupby(by=['date', 'season', 'team', 'opponent'], as_index=False) # Groupby to aggregate the stats for each game
                   .sum()
                   .drop(columns=['DE', 'TOG', 'Match_id']) # Drop columns
                   .assign(date=lambda df: pd.to_datetime(df.date, format="%d/%m/%Y")) # Create a datetime object
                   .sort_values(by='date')
                   .reset_index(drop=True))
    return agg_stats
```

```python
agg_stats = get_cleaned_aggregate_player_stats(player_stats)
```

```python
agg_stats.tail()
```

|  | date | season | team | opponent | AF | B | BO | CCL | CG | CL | CM | CP | D | ED | FA | FF | G | GA | HB | HO | I50 | ITC | K | M | MG | MI5 | One.Percenters | R50 | SC | SCL | SI | T | T5 | TO | UP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3621 | 2018-08-26 | 2018 | Brisbane | West Coast | 1652 | 5 | 0 | 14.0 | 49 | 37 | 8 | 132 | 394 | 302 | 20 | 18 | 11 | 9 | 167 | 48 | 49 | 59.0 | 227 | 104 | 5571.0 | 6 | 48 | 39 | 1645 | 23.0 | 86.0 | 62 | 13.0 | 69.0 | 256 |
| 3622 | 2018-08-26 | 2018 | West Coast | Brisbane | 1548 | 11 | 5 | 13.0 | 49 | 42 | 9 | 141 | 360 | 262 | 18 | 20 | 14 | 8 | 137 | 39 | 56 | 70.0 | 223 | 95 | 5809.0 | 12 | 39 | 34 | 1655 | 29.0 | 94.0 | 55 | 6.0 | 59.0 | 217 |
| 3623 | 2018-08-26 | 2018 | St Kilda | North Melbourne | 1587 | 8 | 11 | 19.0 | 48 | 33 | 7 | 125 | 383 | 299 | 18 | 14 | 14 | 13 | 173 | 23 | 48 | 68.0 | 210 | 112 | 5522.0 | 14 | 46 | 35 | 1568 | 14.0 | 95.0 | 50 | 7.0 | 77.0 | 269 |
| 3624 | 2018-08-26 | 2018 | GWS | Melbourne | 1449 | 7 | 17 | 14.0 | 42 | 31 | 12 | 111 | 355 | 274 | 19 | 13 | 8 | 7 | 159 | 18 | 50 | 54.0 | 196 | 110 | 5416.0 | 10 | 62 | 34 | 1532 | 17.0 | 78.0 | 46 | 5.0 | 58.0 | 254 |
| 3625 | 2018-08-26 | 2018 | Melbourne | GWS | 1712 | 8 | 12 | 10.0 | 38 | 30 | 12 | 139 | 403 | 302 | 13 | 19 | 15 | 14 | 181 | 48 | 54 | 59.0 | 222 | 106 | 6198.0 | 16 | 34 | 39 | 1768 | 20.0 | 147.0 | 60 | 2.0 | 53.0 | 269 |

We now have a three fully prepared DataFrames which are almost ready to be analysed and for a model to be built on! Let's have a look at how they look and then merge them together into our final DataFrame.

```python
odds.tail(3)
```

|  | team | odds | date | home_game |
| --- | --- | --- | --- | --- |
| 4179 | Box Hill Hawks | 1.4300 | 2018-09-01 | 1 |
| 4180 | Casey Demons | 1.9000 | 2018-09-01 | 1 |
| 4181 | West Perth | 2.7382 | 2018-09-01 | 0 |

```python
match_results.tail(3)
```

|  | game | date | round | team | goals | behinds | points | margin | venue | opponent | opponent_goals | opponent_behinds | opponent_points | home_game |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 30793 | 15397 | 2018-08-26 | 23 | Melbourne | 15 | 12 | 102 | 45 | M.C.G. | GWS | 8 | 9 | 57 | 1 |
| 30794 | 15398 | 2018-08-26 | 23 | St Kilda | 14 | 10 | 94 | -23 | Docklands | North Melbourne | 17 | 15 | 117 | 1 |
| 30795 | 15398 | 2018-08-26 | 23 | North Melbourne | 17 | 15 | 117 | 23 | Docklands | St Kilda | 14 | 10 | 94 | 0 |

```python
agg_stats.tail(3)
```

|  | date | season | team | opponent | AF | B | BO | CCL | CG | CL | CM | CP | D | ED | FA | FF | G | GA | HB | HO | I50 | ITC | K | M | MG | MI5 | One.Percenters | R50 | SC | SCL | SI | T | T5 | TO | UP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3623 | 2018-08-26 | 2018 | St Kilda | North Melbourne | 1587 | 8 | 11 | 19.0 | 48 | 33 | 7 | 125 | 383 | 299 | 18 | 14 | 14 | 13 | 173 | 23 | 48 | 68.0 | 210 | 112 | 5522.0 | 14 | 46 | 35 | 1568 | 14.0 | 95.0 | 50 | 7.0 | 77.0 | 269 |
| 3624 | 2018-08-26 | 2018 | GWS | Melbourne | 1449 | 7 | 17 | 14.0 | 42 | 31 | 12 | 111 | 355 | 274 | 19 | 13 | 8 | 7 | 159 | 18 | 50 | 54.0 | 196 | 110 | 5416.0 | 10 | 62 | 34 | 1532 | 17.0 | 78.0 | 46 | 5.0 | 58.0 | 254 |
| 3625 | 2018-08-26 | 2018 | Melbourne | GWS | 1712 | 8 | 12 | 10.0 | 38 | 30 | 12 | 139 | 403 | 302 | 13 | 19 | 15 | 14 | 181 | 48 | 54 | 59.0 | 222 | 106 | 6198.0 | 16 | 34 | 39 | 1768 | 20.0 | 147.0 | 60 | 2.0 | 53.0 | 269 |

```python
merged_df = (odds[odds.team.isin(agg_stats.team.unique())]
                .pipe(pd.merge, match_results, on=['date', 'team', 'home_game'])
                .pipe(pd.merge, agg_stats, on=['date', 'team', 'opponent'])
                .sort_values(by=['game']))
```

```python
merged_df.tail(3)
```

|  | team | odds | date | home_game | game | round | goals | behinds | points | margin | venue | opponent | opponent_goals | opponent_behinds | opponent_points | season | AF | B | BO | CCL | CG | CL | CM | CP | D | ED | FA | FF | G | GA | HB | HO | I50 | ITC | K | M | MG | MI5 | One.Percenters | R50 | SC | SCL | SI | T | T5 | TO | UP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3199 | Melbourne | 1.5116 | 2018-08-26 | 1 | 15397 | 23 | 15 | 12 | 102 | 45 | M.C.G. | GWS | 8 | 9 | 57 | 2018 | 1712 | 8 | 12 | 10.0 | 38 | 30 | 12 | 139 | 403 | 302 | 13 | 19 | 15 | 14 | 181 | 48 | 54 | 59.0 | 222 | 106 | 6198.0 | 16 | 34 | 39 | 1768 | 20.0 | 147.0 | 60 | 2.0 | 53.0 | 269 |
| 3195 | North Melbourne | 1.3936 | 2018-08-26 | 0 | 15398 | 23 | 17 | 15 | 117 | 23 | Docklands | St Kilda | 14 | 10 | 94 | 2018 | 1707 | 13 | 7 | 15.0 | 50 | 24 | 6 | 131 | 425 | 322 | 14 | 18 | 17 | 13 | 201 | 32 | 59 | 77.0 | 224 | 106 | 5833.0 | 23 | 33 | 29 | 1735 | 9.0 | 154.0 | 48 | 9.0 | 66.0 | 300 |
| 3200 | St Kilda | 3.5178 | 2018-08-26 | 1 | 15398 | 23 | 14 | 10 | 94 | -23 | Docklands | North Melbourne | 17 | 15 | 117 | 2018 | 1587 | 8 | 11 | 19.0 | 48 | 33 | 7 | 125 | 383 | 299 | 18 | 14 | 14 | 13 | 173 | 23 | 48 | 68.0 | 210 | 112 | 5522.0 | 14 | 46 | 35 | 1568 | 14.0 | 95.0 | 50 | 7.0 | 77.0 | 269 |

Great! We now have a clean looking datset with each row representing one team in a game. Let's now eliminate the outliers from a dataset. We know that Essendon had a doping scandal which resulted in their entire team being banned for a year in 2016, so let's remove all of their 2016 games. To do this we will filter based on the team and season, and then invert this with ~.

```python
# Define a function which eliminates outliers
def outlier_eliminator(df):
    # Eliminate Essendon 2016 games
    essendon_filter_criteria = ~(((df['team'] == 'Essendon') & (df['season'] == 2016)) | ((df['opponent'] == 'Essendon') & (df['season'] == 2016)))
    df = df[essendon_filter_criteria].reset_index(drop=True)
    
    return df
```

```python
afl_data = outlier_eliminator(merged_df)
```

```python
afl_data.tail(3)
```

|  | team | odds | date | home_game | game | round | goals | behinds | points | margin | venue | opponent | opponent_goals | opponent_behinds | opponent_points | season | AF | B | BO | CCL | CG | CL | CM | CP | D | ED | FA | FF | G | GA | HB | HO | I50 | ITC | K | M | MG | MI5 | One.Percenters | R50 | SC | SCL | SI | T | T5 | TO | UP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3154 | Melbourne | 1.5116 | 2018-08-26 | 1 | 15397 | 23 | 15 | 12 | 102 | 45 | M.C.G. | GWS | 8 | 9 | 57 | 2018 | 1712 | 8 | 12 | 10.0 | 38 | 30 | 12 | 139 | 403 | 302 | 13 | 19 | 15 | 14 | 181 | 48 | 54 | 59.0 | 222 | 106 | 6198.0 | 16 | 34 | 39 | 1768 | 20.0 | 147.0 | 60 | 2.0 | 53.0 | 269 |
| 3155 | North Melbourne | 1.3936 | 2018-08-26 | 0 | 15398 | 23 | 17 | 15 | 117 | 23 | Docklands | St Kilda | 14 | 10 | 94 | 2018 | 1707 | 13 | 7 | 15.0 | 50 | 24 | 6 | 131 | 425 | 322 | 14 | 18 | 17 | 13 | 201 | 32 | 59 | 77.0 | 224 | 106 | 5833.0 | 23 | 33 | 29 | 1735 | 9.0 | 154.0 | 48 | 9.0 | 66.0 | 300 |
| 3156 | St Kilda | 3.5178 | 2018-08-26 | 1 | 15398 | 23 | 14 | 10 | 94 | -23 | Docklands | North Melbourne | 17 | 15 | 117 | 2018 | 1587 | 8 | 11 | 19.0 | 48 | 33 | 7 | 125 | 383 | 299 | 18 | 14 | 14 | 13 | 173 | 23 | 48 | 68.0 | 210 | 112 | 5522.0 | 14 | 46 | 35 | 1568 | 14.0 | 95.0 | 50 | 7.0 | 77.0 | 269 |

Finally, let's mark all of the columns that we are going to use in feature creation with the string 'f_' at the start of their column name so that we can easily filter for these columns.

```python
non_feature_cols = ['team', 'date', 'home_game', 'game', 'round', 'venue', 'opponent', 'season']
afl_data = afl_data.rename(columns={col: 'f_' + col for col in afl_data if col not in non_feature_cols})
```

```python
afl_data.tail(3)
```

|  | team | f_odds | date | home_game | game | round | f_goals | f_behinds | f_points | f_margin | venue | opponent | f_opponent_goals | f_opponent_behinds | f_opponent_points | season | f_AF | f_B | f_BO | f_CCL | f_CG | f_CL | f_CM | f_CP | f_D | f_ED | f_FA | f_FF | f_G | f_GA | f_HB | f_HO | f_I50 | f_ITC | f_K | f_M | f_MG | f_MI5 | f_One.Percenters | f_R50 | f_SC | f_SCL | f_SI | f_T | f_T5 | f_TO | f_UP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3154 | Melbourne | 1.5116 | 2018-08-26 | 1 | 15397 | 23 | 15 | 12 | 102 | 45 | M.C.G. | GWS | 8 | 9 | 57 | 2018 | 1712 | 8 | 12 | 10.0 | 38 | 30 | 12 | 139 | 403 | 302 | 13 | 19 | 15 | 14 | 181 | 48 | 54 | 59.0 | 222 | 106 | 6198.0 | 16 | 34 | 39 | 1768 | 20.0 | 147.0 | 60 | 2.0 | 53.0 | 269 |
| 3155 | North Melbourne | 1.3936 | 2018-08-26 | 0 | 15398 | 23 | 17 | 15 | 117 | 23 | Docklands | St Kilda | 14 | 10 | 94 | 2018 | 1707 | 13 | 7 | 15.0 | 50 | 24 | 6 | 131 | 425 | 322 | 14 | 18 | 17 | 13 | 201 | 32 | 59 | 77.0 | 224 | 106 | 5833.0 | 23 | 33 | 29 | 1735 | 9.0 | 154.0 | 48 | 9.0 | 66.0 | 300 |
| 3156 | St Kilda | 3.5178 | 2018-08-26 | 1 | 15398 | 23 | 14 | 10 | 94 | -23 | Docklands | North Melbourne | 17 | 15 | 117 | 2018 | 1587 | 8 | 11 | 19.0 | 48 | 33 | 7 | 125 | 383 | 299 | 18 | 14 | 14 | 13 | 173 | 23 | 48 | 68.0 | 210 | 112 | 5522.0 | 14 | 46 | 35 | 1568 | 14.0 | 95.0 | 50 | 7.0 | 77.0 | 269 |

Our data is now fully ready to be explored and for features to be created, which we will walk you through in our next tutorial, [AFL Feature Creation Tutorial](/modelling/AFLmodelPart2).