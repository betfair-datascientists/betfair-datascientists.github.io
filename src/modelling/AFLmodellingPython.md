# AFL Modelling Walkthrough 

---
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

Our data is now fully ready to be explored and for features to be created.

---
# 02. Feature Creation

These tutorials will walk you through how to construct your own basic AFL model. The output will be odds for each team to win, which will be shown on [The Hub](https://www.betfair.com.au/hub/tools/models/afl-prediction-model/).

In this notebook we will walk you through creating features from our dataset, which was cleaned in the first tutorial. Feature engineering is an integral part of the Data Science process. Creative and smart features can be the difference between an average performing model and a model profitable which beats the market odds.

---
## Grabbing Our Dataset
First, we will import our required modules, as well as the prepare_afl_data function which we created in our afl_data_cleaning script. This essentially cleans all the data for us so that we're ready to explore the data and make some features.

```python
# Import modules
from afl_data_cleaning_v2 import *
import afl_data_cleaning_v2
import pandas as pd
pd.set_option('display.max_columns', None)
import warnings
warnings.filterwarnings('ignore')
import numpy as np
```

```python
# Use the prepare_afl_data function to prepare the data for us; this function condenses what we walked through in the previous tutorial
afl_data = prepare_afl_data()
```

```python
afl_data.tail(3)
```

|  | team | f_odds | date | home_game | game | round | f_goals | f_behinds | f_points | f_margin | venue | opponent | f_opponent_goals | f_opponent_behinds | f_opponent_points | season | f_AF | f_B | f_BO | f_CCL | f_CG | f_CL | f_CM | f_CP | f_D | f_ED | f_FA | f_FF | f_G | f_GA | f_HB | f_HO | f_I50 | f_ITC | f_K | f_M | f_MG | f_MI5 | f_One.Percenters | f_R50 | f_SC | f_SCL | f_SI | f_T | f_T5 | f_TO | f_UP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3154 | Melbourne | 1.5116 | 2018-08-26 | 1 | 15397 | 23 | 15 | 12 | 102 | 45 | M.C.G. | GWS | 8 | 9 | 57 | 2018 | 1712 | 8 | 12 | 10.0 | 38 | 30 | 12 | 139 | 403 | 302 | 13 | 19 | 15 | 14 | 181 | 48 | 54 | 59.0 | 222 | 106 | 6198.0 | 16 | 34 | 39 | 1768 | 20.0 | 147.0 | 60 | 2.0 | 53.0 | 269 |
| 3155 | North Melbourne | 1.3936 | 2018-08-26 | 0 | 15398 | 23 | 17 | 15 | 117 | 23 | Docklands | St Kilda | 14 | 10 | 94 | 2018 | 1707 | 13 | 7 | 15.0 | 50 | 24 | 6 | 131 | 425 | 322 | 14 | 18 | 17 | 13 | 201 | 32 | 59 | 77.0 | 224 | 106 | 5833.0 | 23 | 33 | 29 | 1735 | 9.0 | 154.0 | 48 | 9.0 | 66.0 | 300 |
| 3156 | St Kilda | 3.5178 | 2018-08-26 | 1 | 15398 | 23 | 14 | 10 | 94 | -23 | Docklands | North Melbourne | 17 | 15 | 117 | 2018 | 1587 | 8 | 11 | 19.0 | 48 | 33 | 7 | 125 | 383 | 299 | 18 | 14 | 14 | 13 | 173 | 23 | 48 | 68.0 | 210 | 112 | 5522.0 | 14 | 46 | 35 | 1568 | 14.0 | 95.0 | 50 | 7.0 | 77.0 | 269 |

---
## Creating A Feature DataFrame
Let's create a feature DataFrame and merge all of our features into this DataFrame as we go.

```python
features = afl_data[['date', 'game', 'team', 'opponent', 'venue', 'home_game']].copy()
```

### What Each Column Refers To
Below is a DataFrame which outlines what each column refers to.

```python
column_abbreviations = pd.read_csv("data/afl_data_columns_mapping.csv")
column_abbreviations
```

|  | Feature Abbreviated | Feature |
| --- | --- | --- |
| 0 | GA | Goal Assists |
| 1 | CP | Contested Possessions |
| 2 | UP | Uncontested Possessions |
| 3 | ED | Effective Disposals |
| 4 | CM | Contested Marks |
| 5 | MI5 | Marks Inside 50 |
| 6 | One.Percenters | One Percenters |
| 7 | BO | Bounces |
| 8 | K | Kicks |
| 9 | HB | Handballs |
| 10 | D | Disposals |
| 11 | M | Marks |
| 12 | G | Goals |
| 13 | B | Behinds |
| 14 | T | Tackles |
| 15 | HO | Hitouts |
| 16 | I50 | Inside 50s |
| 17 | CL | Clearances |
| 18 | CG | Clangers |
| 19 | R50 | Rebound 50s |
| 20 | FF | Frees For |
| 21 | FA | Frees Against |
| 22 | AF | AFL Fantasy Points |
| 23 | SC | Supercoach Points |
| 24 | CCL | Centre Clearances |
| 25 | SCL | Stoppage Clearances |
| 26 | SI | Score Involvements |
| 27 | MG | Metres Gained |
| 28 | TO | Turnovers |
| 29 | ITC | Intercepts |
| 30 | T5 | Tackles Inside 50 |

---
## Feature Creation
Now let's think about what features we can create. We have a enormous amount of stats to sift through. To start, let's create some simple features based on our domain knowledge of Aussie Rules.

### Creating Expontentially Weighted Rolling Averages as Features
Next, we will create rolling averages of statistics such as Tackles, which we will use as features.

It is fair to assume that a team's performance in a certain stat may have predictive power to the overall result. And in general, if a team consistently performs well in this stat, this may have predictive power to the result of their future games. We can't simply train a model on stats from the game which we are trying to predict (i.e. data that we don't have before the game begins), as this will leak the result. We need to train our model on past data. One way of doing this is to train our model on average stats over a certain amount of games. If a team is averaging high in this stat, this may give insight into if they are a strong team. Similarly, if the team is averaging poorly in this stat (relative to the team they are playing), this may have predictive power and give rise to a predicted loss.

To do this we will create a function which calculates the rolling averages, known as create_exp_weighted_avgs, which takes our cleaned DataFrame as an input, as well as the alpha which, when higher, weights recent performances more than old performances. To read more about expontentially weighted moving averages, please read the documentation [here](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.ewm.html).

First, we will grab all the columns which we want to create EMAs for, and then use our function to create the average for that column. We will create a new DataFrame and add these columns to this new DataFrame.

```python
# Define a function which returns a DataFrame with the expontential moving average for each numeric stat
def create_exp_weighted_avgs(df, span):
    # Create a copy of the df with only the game id and the team - we will add cols to this df
    ema_features = df[['game', 'team']].copy()
    
    feature_names = [col for col in df.columns if col.startswith('f_')] # Get a list of columns we will iterate over
    
    for feature_name in feature_names:
        feature_ema = (df.groupby('team')[feature_name]
                         .transform(lambda row: (row.ewm(span=span)
                                                    .mean()
                                                    .shift(1))))
        ema_features[feature_name] = feature_ema
    
    return ema_features
```

```python
features_rolling_averages = create_exp_weighted_avgs(afl_data, span=10)
```

```python
features_rolling_averages.tail()
```

|  | game | team | f_odds | f_goals | f_behinds | f_points | f_margin | f_opponent_goals | f_opponent_behinds | f_opponent_points | f_AF | f_B | f_BO | f_CCL | f_CG | f_CL | f_CM | f_CP | f_D | f_ED | f_FA | f_FF | f_G | f_GA | f_HB | f_HO | f_I50 | f_ITC | f_K | f_M | f_MG | f_MI5 | f_One.Percenters | f_R50 | f_SC | f_SCL | f_SI | f_T | f_T5 | f_TO | f_UP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3152 | 15396 | West Coast | 2.094236 | 12.809630 | 10.047145 | 86.904928 | 8.888770 | 11.435452 | 9.403444 | 78.016158 | 3193.612782 | 16.472115 | 11.958482 | 23.379562 | 100.095244 | 68.252001 | 27.688669 | 284.463270 | 719.884644 | 525.878017 | 36.762440 | 44.867118 | 25.618202 | 17.522871 | 270.478779 | 88.139376 | 105.698031 | 148.005305 | 449.405865 | 201.198907 | 11581.929999 | 20.048124 | 95.018480 | 74.180967 | 3314.157893 | 44.872398 | 177.894442 | 126.985101 | 20.565549 | 138.876613 | 438.848376 |
| 3153 | 15397 | GWS | 1.805565 | 13.100372 | 13.179329 | 91.781563 | 18.527618 | 10.371198 | 11.026754 | 73.253945 | 3165.127358 | 19.875913 | 12.947209 | 25.114002 | 105.856671 | 80.609640 | 23.374884 | 303.160047 | 741.439198 | 534.520295 | 42.597317 | 38.160889 | 26.208715 | 18.688880 | 300.188301 | 81.540693 | 106.989070 | 143.032506 | 441.250897 | 173.050118 | 12091.630837 | 21.106142 | 103.077097 | 80.201059 | 3419.245919 | 55.495610 | 219.879895 | 138.202470 | 25.313148 | 135.966798 | 438.466439 |
| 3154 | 15397 | Melbourne | 1.706488 | 15.157271 | 13.815113 | 104.758740 | 25.170429 | 11.814319 | 8.702396 | 79.588311 | 3312.408470 | 22.077317 | 7.724955 | 28.364418 | 114.399147 | 78.406069 | 26.934677 | 324.352577 | 775.176933 | 547.385948 | 39.353251 | 36.025646 | 30.308918 | 22.461080 | 348.613592 | 99.787800 | 120.339062 | 154.417642 | 426.563341 | 178.102118 | 12395.717925 | 32.168752 | 96.390688 | 63.786515 | 3427.596843 | 50.041649 | 232.287556 | 144.875098 | 23.789233 | 149.042149 | 456.988552 |
| 3155 | 15398 | North Melbourne | 2.272313 | 12.721783 | 10.733785 | 87.064486 | -1.214246 | 12.915796 | 10.783958 | 88.278732 | 3066.272143 | 17.322710 | 9.815243 | 26.015421 | 106.465181 | 67.504286 | 26.064079 | 291.259574 | 736.279779 | 534.154748 | 34.301603 | 40.908551 | 25.386136 | 17.816570 | 341.210547 | 81.541130 | 102.589427 | 145.265493 | 395.069232 | 173.089408 | 10875.002463 | 21.802751 | 82.347511 | 70.416194 | 3171.120023 | 41.488865 | 197.620152 | 122.547684 | 22.286256 | 142.780474 | 450.374058 |
| 3156 | 15398 | St Kilda | 5.516150 | 10.464266 | 11.957047 | 74.742643 | -21.138101 | 14.105551 | 11.247440 | 95.880745 | 3094.163405 | 20.523847 | 14.569589 | 24.134276 | 102.540441 | 66.976211 | 18.018350 | 270.674857 | 773.086015 | 573.769838 | 41.319843 | 36.198820 | 20.850476 | 14.443658 | 364.405251 | 63.498760 | 103.803779 | 130.494307 | 408.680763 | 184.780054 | 10765.717942 | 21.572806 | 94.731555 | 65.790561 | 3228.278599 | 42.841935 | 196.086493 | 115.901425 | 18.796764 | 127.364334 | 508.844514 |

As you can see our function worked perfectly! Now we have a full DataFrame of exponentially weighted moving averages. Note that as these rolling averages have been shifted by 1 to ensure no data leakage, the first round of the data will have all NA values. We can drop these later.

Let's add these averages to our features DataFrame

```python
features = pd.merge(features, features_rolling_averages, on=['game', 'team'])
```

### Creating a 'Form Between the Teams' Feature
It is well known in Aussie Rules that often some teams perform better against certain teams than others. If we isolate our features to pure stats based on previous games not between the teams playing, or elo ratings, we won't account for any relationships between certain teams. An example is the [Kennett Curse](https://en.wikipedia.org/wiki/Kennett_curse), where Geelong won 11 consecutive games against Hawthorn, despite being similarly matched teams. Let's create a feature which calculates how many games a team has won against their opposition over a given window of games.

To do this, we will need to use historical data that dates back well before our current DataFrame starts at. Otherwise we will be using a lot of our games to calculate form, meaning we will have to drop these rows before feeding it into an algorithm. So let's use our prepare_match_results function which we defined in the afl_data_cleaning tutorial to grab a clean DataFrame of all match results since 1897. We can then calculate the form and join this to our current DataFrame.

```python
match_results = afl_data_cleaning_v2.get_cleaned_match_results()
```

```python
match_results.head(3)
```

|  | game | date | round | team | goals | behinds | points | margin | venue | opponent | opponent_goals | opponent_behinds | opponent_points | home_game |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1897-05-08 | 1 | Fitzroy | 6 | 13 | 49 | 33 | Brunswick St | Carlton | 2 | 4 | 16 | 1 |
| 1 | 1 | 1897-05-08 | 1 | Carlton | 2 | 4 | 16 | -33 | Brunswick St | Fitzroy | 6 | 13 | 49 | 0 |
| 2 | 2 | 1897-05-08 | 1 | Collingwood | 5 | 11 | 41 | 25 | Victoria Park | St Kilda | 2 | 4 | 16 | 1 |

```python
form_btwn_teams = match_results[['game', 'team', 'opponent', 'margin']].copy()

form_btwn_teams['f_form_margin_btwn_teams'] = (match_results.groupby(['team', 'opponent'])['margin']
                                                          .transform(lambda row: row.rolling(5).mean().shift())
                                                          .fillna(0))

form_btwn_teams['f_form_past_5_btwn_teams'] = \
(match_results.assign(win=lambda df: df.apply(lambda row: 1 if row.margin > 0 else 0, axis='columns'))
              .groupby(['team', 'opponent'])['win']
              .transform(lambda row: row.rolling(5).mean().shift() * 5)
              .fillna(0))
```

```python
form_btwn_teams.tail(3)
```

|  | game | team | opponent | margin | f_form_margin_btwn_teams | f_form_past_5_btwn_teams |
| --- | --- | --- | --- | --- | --- | --- |
| 30793 | 15397 | Melbourne | GWS | 45 | -23.2 | 2.0 |
| 30794 | 15398 | St Kilda | North Melbourne | -23 | -3.2 | 2.0 |
| 30795 | 15398 | North Melbourne | St Kilda | 23 | 3.2 | 3.0 |

```python
# Merge to our features df
features = pd.merge(features, form_btwn_teams.drop(columns=['margin']), on=['game', 'team', 'opponent'])
```

### Creating Efficiency Features
#### Disposal Efficiency
Disposal efficiency is pivotal in Aussie Rules football. If you are dispose of the ball effectively you are much more likely to score and much less likely to concede goals than if you dispose of it ineffectively.

Let's create a disposal efficiency feature by dividing Effective Disposals by Disposals.

#### Inside 50/Rebound 50 Efficiency
Similarly, one could hypothesise that teams who keep the footy in their Inside 50 regularly will be more likely to score, whilst teams who are effective at getting the ball out of their Defensive 50 will be less likely to concede. Let's use this logic to create Inside 50 Efficiency and Rebound 50 Efficiency features.

The formula used will be:
```
Inside 50 Efficiency = R50_Opponents / I50 (lower is better).
Rebound 50 Efficiency = R50 / I50_Opponents (higher is better).
```

Using these formulas, I50 Efficiency = R50 Efficiency_Opponent. So we will just need to create the formulas for I50 efficiency.
To create these features we will need the opposition's Inside 50s/Rebound 50s. So we will split out data into two DataFrames, create a new DataFrame by joining these two DataFrames on the Game, calculate our efficiency features, then join our features with our main features DataFrame.

```python
# Get each match on single rows
single_row_df = (afl_data[['game', 'team', 'f_I50', 'f_R50', 'f_D', 'f_ED', 'home_game', ]]
                    .query('home_game == 1')
                    .rename(columns={'team': 'home_team', 'f_I50': 'f_I50_home', 'f_R50': 'f_R50_home', 'f_D': 'f_D_home', 'f_ED': 'f_ED_home'})
                    .drop(columns='home_game')
                    .pipe(pd.merge, afl_data[['game', 'team', 'f_I50', 'f_R50', 'f_D', 'f_ED', 'home_game']]
                                    .query('home_game == 0')
                                    .rename(columns={'team': 'away_team', 'f_I50': 'f_I50_away', 'f_R50': 'f_R50_away', 'f_D': 'f_D_away', 'f_ED': 'f_ED_away'})
                                    .drop(columns='home_game'), on='game'))
```

```python
single_row_df.head()
```

|  | game | home_team | f_I50_home | f_R50_home | f_D_home | f_ED_home | away_team | f_I50_away | f_R50_away | f_D_away | f_ED_away |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 13764 | Carlton | 69 | 21 | 373 | 268 | Richmond | 37 | 50 | 316 | 226 |
| 1 | 13765 | Geelong | 54 | 40 | 428 | 310 | St Kilda | 52 | 45 | 334 | 246 |
| 2 | 13766 | Collingwood | 70 | 38 | 398 | 289 | Port Adelaide | 50 | 44 | 331 | 232 |
| 3 | 13767 | Adelaide | 59 | 38 | 366 | 264 | Hawthorn | 54 | 38 | 372 | 264 |
| 4 | 13768 | Brisbane | 50 | 39 | 343 | 227 | Fremantle | 57 | 30 | 351 | 250 |

```python
single_row_df = single_row_df.assign(f_I50_efficiency_home=lambda df: df.f_R50_away / df.f_I50_home,
                                    f_I50_efficiency_away=lambda df: df.f_R50_home / df.f_I50_away)

feature_efficiency_cols = ['f_I50_efficiency_home', 'f_I50_efficiency_away']

# Now let's create an Expontentially Weighted Moving Average for these features - we will need to reshape our DataFrame to do this
efficiency_features_multi_row = (single_row_df[['game', 'home_team'] + feature_efficiency_cols]
                                    .rename(columns={
                                        'home_team': 'team',
                                        'f_I50_efficiency_home': 'f_I50_efficiency',
                                        'f_I50_efficiency_away': 'f_I50_efficiency_opponent',
                                    })
                                    .append((single_row_df[['game', 'away_team'] + feature_efficiency_cols]
                                                 .rename(columns={
                                                     'away_team': 'team',
                                                     'f_I50_efficiency_home': 'f_I50_efficiency_opponent',
                                                     'f_I50_efficiency_away': 'f_I50_efficiency',
                                                 })), sort=True)
                                    .sort_values(by='game')
                                    .reset_index(drop=True))

efficiency_features = efficiency_features_multi_row[['game', 'team']].copy()
feature_efficiency_cols = ['f_I50_efficiency', 'f_I50_efficiency_opponent']

for feature in feature_efficiency_cols:
    efficiency_features[feature] = (efficiency_features_multi_row.groupby('team')[feature]
                                        .transform(lambda row: row.ewm(span=10).mean().shift(1)))
    
# Get feature efficiency df back onto single rows
efficiency_features = pd.merge(efficiency_features, afl_data[['game', 'team', 'home_game']], on=['game', 'team'])
efficiency_features_single_row = (efficiency_features.query('home_game == 1')
                                    .rename(columns={
                                        'team': 'home_team', 
                                        'f_I50_efficiency': 'f_I50_efficiency_home',
                                        'f_I50_efficiency_opponent': 'f_R50_efficiency_home'})
                                    .drop(columns='home_game')
                                    .pipe(pd.merge, (efficiency_features.query('home_game == 0')
                                                        .rename(columns={
                                                            'team': 'away_team',
                                                            'f_I50_efficiency': 'f_I50_efficiency_away',
                                                            'f_I50_efficiency_opponent': 'f_R50_efficiency_away'})
                                                        .drop(columns='home_game')), on='game'))
```

```python
efficiency_features_single_row.tail(5)
```

|  | game | home_team | f_I50_efficiency_home | f_R50_efficiency_home | away_team | f_I50_efficiency_away | f_R50_efficiency_away |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1580 | 15394 | Carlton | 0.730668 | 0.675002 | Adelaide | 0.691614 | 0.677128 |
| 1581 | 15395 | Sydney | 0.699994 | 0.778280 | Hawthorn | 0.699158 | 0.673409 |
| 1582 | 15396 | Brisbane | 0.683604 | 0.691730 | West Coast | 0.696822 | 0.709605 |
| 1583 | 15397 | Melbourne | 0.667240 | 0.692632 | GWS | 0.684525 | 0.753783 |
| 1584 | 15398 | St Kilda | 0.730843 | 0.635819 | North Melbourne | 0.697018 | 0.654991 |

We will merge these features back to our features df later, when the features data frame is on a single row as well.

### Creating an Elo Feature
Another feature which we could create is an Elo feature. If you don't know what Elo is, go ahead and read our article on it [here](https://www.betfair.com.au/hub/better-betting/betting-strategies/tennis/tennis-elo-modelling/). We have also written a guide on using elo to model the 2018 FIFA World Cup [here](https://www.betfair.com.au/hub/how-to-use-elo-to-model-the-world-cup/).

Essentially, Elo ratings increase if you win. The amount the rating increases is based on how strong the opponent is relative to the team who won. Weak teams get more points for beating stronger teams than they do for beating weaker teams, and vice versa for losses (teams lose points for losses).

Mathematically, Elo ratings can also assign a probability for winning or losing based on the two Elo Ratings of the teams playing.

So let's get into it. We will first define a function which calculates the elo for each team and applies these elos to our DataFrame.

```python
# Define a function which finds the elo for each team in each game and returns a dictionary with the game ID as a key and the
# elos as the key's value, in a list. It also outputs the probabilities and a dictionary of the final elos for each team
def elo_applier(df, k_factor):
    # Initialise a dictionary with default elos for each team
    elo_dict = {team: 1500 for team in df['team'].unique()}
    elos, elo_probs = {}, {}
    
    # Get a home and away dataframe so that we can get the teams on the same row
    home_df = df.loc[df.home_game == 1, ['team', 'game', 'f_margin', 'home_game']].rename(columns={'team': 'home_team'})
    away_df = df.loc[df.home_game == 0, ['team', 'game']].rename(columns={'team': 'away_team'})
    
    df = (pd.merge(home_df, away_df, on='game')
            .sort_values(by='game')
            .drop_duplicates(subset='game', keep='first')
            .reset_index(drop=True))

    # Loop over the rows in the DataFrame
    for index, row in df.iterrows():
        # Get the Game ID
        game_id = row['game']
        
        # Get the margin
        margin = row['f_margin']
        
        # If the game already has the elos for the home and away team in the elos dictionary, go to the next game
        if game_id in elos.keys():
            continue
        
        # Get the team and opposition
        home_team = row['home_team']
        away_team = row['away_team']
        
        # Get the team and opposition elo score
        home_team_elo = elo_dict[home_team]
        away_team_elo = elo_dict[away_team]
        
        # Calculated the probability of winning for the team and opposition
        prob_win_home = 1 / (1 + 10**((away_team_elo - home_team_elo) / 400))
        prob_win_away = 1 - prob_win_home
        
        # Add the elos and probabilities our elos dictionary and elo_probs dictionary based on the Game ID
        elos[game_id] = [home_team_elo, away_team_elo]
        elo_probs[game_id] = [prob_win_home, prob_win_away]
        
        # Calculate the new elos of each team
        if margin > 0: # Home team wins; update both teams' elo
            new_home_team_elo = home_team_elo + k_factor*(1 - prob_win_home)
            new_away_team_elo = away_team_elo + k_factor*(0 - prob_win_away)
        elif margin < 0: # Away team wins; update both teams' elo
            new_home_team_elo = home_team_elo + k_factor*(0 - prob_win_home)
            new_away_team_elo = away_team_elo + k_factor*(1 - prob_win_away)
        elif margin == 0: # Drawn game' update both teams' elo
            new_home_team_elo = home_team_elo + k_factor*(0.5 - prob_win_home)
            new_away_team_elo = away_team_elo + k_factor*(0.5 - prob_win_away)
        
        # Update elos in elo dictionary
        elo_dict[home_team] = new_home_team_elo
        elo_dict[away_team] = new_away_team_elo
    
    return elos, elo_probs, elo_dict
```

```python
# Use the elo applier function to get the elos and elo probabilities for each game - we will map these later
elos, probs, elo_dict = elo_applier(afl_data, 30)
```

Great! now we have both rolling averages for stats as a feature, and the elo of the teams! Let's have a quick look at the current elo standings with a k-factor of 30, out of curiosity.

```python
for team in sorted(elo_dict, key=elo_dict.get)[::-1]:
    print(team, elo_dict[team])

    Richmond 1695.2241513840117
    Sydney 1645.548990879842
    Hawthorn 1632.5266709780622
    West Coast 1625.871701773721
    Geelong 1625.423154644809
    GWS 1597.4158602131877
    Adelaide 1591.1704934545442
    Collingwood 1560.370309216614
    Melbourne 1558.5666572771509
    Essendon 1529.0198398117086
    Port Adelaide 1524.8882517820093
    North Melbourne 1465.5637511922569
    Western Bulldogs 1452.2110697845148
    Fremantle 1393.142087030804
    St Kilda 1360.9120149937303
    Brisbane 1276.2923772139352
    Gold Coast 1239.174528704772
    Carlton 1226.6780896643265
```

This looks extremely similar to the currently AFL ladder, so this is a good sign for elo being an effective predictor of winning.

### Merging Our Features Into One Features DataFrame
Now we need to reshape our features df so that we have all of the statistics for both teams in a game on a single row. We can then merge our elo and efficiency features to this df.

```python
# Look at our current features df
features.tail(3)
```

|  | date | game | team | opponent | venue | home_game | f_odds | f_goals | f_behinds | f_points | f_margin | f_opponent_goals | f_opponent_behinds | f_opponent_points | f_AF | f_B | f_BO | f_CCL | f_CG | f_CL | f_CM | f_CP | f_D | f_ED | f_FA | f_FF | f_G | f_GA | f_HB | f_HO | f_I50 | f_ITC | f_K | f_M | f_MG | f_MI5 | f_One.Percenters | f_R50 | f_SC | f_SCL | f_SI | f_T | f_T5 | f_TO | f_UP | f_form_margin_btwn_teams | f_form_past_5_btwn_teams |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3156 | 2018-08-26 | 15397 | Melbourne | GWS | M.C.G. | 1 | 1.706488 | 15.157271 | 13.815113 | 104.758740 | 25.170429 | 11.814319 | 8.702396 | 79.588311 | 3312.408470 | 22.077317 | 7.724955 | 28.364418 | 114.399147 | 78.406069 | 26.934677 | 324.352577 | 775.176933 | 547.385948 | 39.353251 | 36.025646 | 30.308918 | 22.461080 | 348.613592 | 99.78780 | 120.339062 | 154.417642 | 426.563341 | 178.102118 | 12395.717925 | 32.168752 | 96.390688 | 63.786515 | 3427.596843 | 50.041649 | 232.287556 | 144.875098 | 23.789233 | 149.042149 | 456.988552 | -23.2 | 2.0 |
| 3157 | 2018-08-26 | 15398 | North Melbourne | St Kilda | Docklands | 0 | 2.272313 | 12.721783 | 10.733785 | 87.064486 | -1.214246 | 12.915796 | 10.783958 | 88.278732 | 3066.272143 | 17.322710 | 9.815243 | 26.015421 | 106.465181 | 67.504286 | 26.064079 | 291.259574 | 736.279779 | 534.154748 | 34.301603 | 40.908551 | 25.386136 | 17.816570 | 341.210547 | 81.54113 | 102.589427 | 145.265493 | 395.069232 | 173.089408 | 10875.002463 | 21.802751 | 82.347511 | 70.416194 | 3171.120023 | 41.488865 | 197.620152 | 122.547684 | 22.286256 | 142.780474 | 450.374058 | 3.2 | 3.0 |
| 3158 | 2018-08-26 | 15398 | St Kilda | North Melbourne | Docklands | 1 | 5.516150 | 10.464266 | 11.957047 | 74.742643 | -21.138101 | 14.105551 | 11.247440 | 95.880745 | 3094.163405 | 20.523847 | 14.569589 | 24.134276 | 102.540441 | 66.976211 | 18.018350 | 270.674857 | 773.086015 | 573.769838 | 41.319843 | 36.198820 | 20.850476 | 14.443658 | 364.405251 | 63.49876 | 103.803779 | 130.494307 | 408.680763 | 184.780054 | 10765.717942 | 21.572806 | 94.731555 | 65.790561 | 3228.278599 | 42.841935 | 196.086493 | 115.901425 | 18.796764 | 127.364334 | 508.844514 | -3.2 | 2.0 |

```python
one_line_cols = ['game', 'team', 'home_game'] + [col for col in features if col.startswith('f_')]

# Get all features onto individual rows for each match
features_one_line = (features.loc[features.home_game == 1, one_line_cols]
                     .rename(columns={'team': 'home_team'})
                     .drop(columns='home_game')
                     .pipe(pd.merge, (features.loc[features.home_game == 0, one_line_cols]
                                              .drop(columns='home_game')
                                              .rename(columns={'team': 'away_team'})
                                              .rename(columns={col: col+'_away' for col in features.columns if col.startswith('f_')})), on='game')
                    .drop(columns=['f_form_margin_btwn_teams_away', 'f_form_past_5_btwn_teams_away']))

# Add our created features - elo, efficiency etc.
features_one_line = (features_one_line.assign(f_elo_home=lambda df: df.game.map(elos).apply(lambda x: x[0]),
                                            f_elo_away=lambda df: df.game.map(elos).apply(lambda x: x[1]))
                                      .pipe(pd.merge, efficiency_features_single_row, on=['game', 'home_team', 'away_team'])
                                      .pipe(pd.merge, afl_data.loc[afl_data.home_game == 1, ['game', 'date', 'round', 'venue']], on=['game'])
                                      .dropna()
                                      .reset_index(drop=True)
                                      .assign(season=lambda df: df.date.apply(lambda row: row.year)))

ordered_cols = [col for col in features_one_line if col[:2] != 'f_'] + [col for col in features_one_line if col.startswith('f_')]

feature_df = features_one_line[ordered_cols]
```

Finally, let's reduce the dimensionality of the features df by subtracting the home features from the away features. This will reduce the huge amount of columns we have and make our data more manageable. To do this, we will need a list of columns which we are subtracting from each other. We will then loop over each of these columns to create our new differential columns. 

We will then add in the implied probability from the odds of the home and away team, as our current odds feature is simply an exponential moving average over the past n games.

```python
# Create differential df - this df is the home features - the away features
diff_cols = [col for col in feature_df.columns if col + '_away' in feature_df.columns and col != 'f_odds' and col.startswith('f_')]
non_diff_cols = [col for col in feature_df.columns if col not in diff_cols and col[:-5] not in diff_cols]

diff_df = feature_df[non_diff_cols].copy()

for col in diff_cols:
    diff_df[col+'_diff'] = feature_df[col] - feature_df[col+'_away']

# Add current odds in to diff_df
odds = get_cleaned_odds()
home_odds = (odds[odds.home_game == 1]
             .assign(f_current_odds_prob=lambda df: 1 / df.odds)
             .rename(columns={'team': 'home_team'})
             .drop(columns=['home_game', 'odds']))

away_odds = (odds[odds.home_game == 0]
             .assign(f_current_odds_prob_away=lambda df: 1 / df.odds)
             .rename(columns={'team': 'away_team'})
             .drop(columns=['home_game', 'odds']))

diff_df = (diff_df.pipe(pd.merge, home_odds, on=['date', 'home_team'])
              .pipe(pd.merge, away_odds, on=['date', 'away_team']))
```

```python
diff_df.tail()
```

|  | game | home_team | away_team | date | round | venue | season | f_odds | f_form_margin_btwn_teams | f_form_past_5_btwn_teams | f_odds_away | f_elo_home | f_elo_away | f_I50_efficiency_home | f_R50_efficiency_home | f_I50_efficiency_away | f_R50_efficiency_away | f_goals_diff | f_behinds_diff | f_points_diff | f_margin_diff | f_opponent_goals_diff | f_opponent_behinds_diff | f_opponent_points_diff | f_AF_diff | f_B_diff | f_BO_diff | f_CCL_diff | f_CG_diff | f_CL_diff | f_CM_diff | f_CP_diff | f_D_diff | f_ED_diff | f_FA_diff | f_FF_diff | f_G_diff | f_GA_diff | f_HB_diff | f_HO_diff | f_I50_diff | f_ITC_diff | f_K_diff | f_M_diff | f_MG_diff | f_MI5_diff | f_One.Percenters_diff | f_R50_diff | f_SC_diff | f_SCL_diff | f_SI_diff | f_T_diff | f_T5_diff | f_TO_diff | f_UP_diff | f_current_odds_prob | f_current_odds_prob_away |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1626 | 15394 | Carlton | Adelaide | 2018-08-25 | 23 | Docklands | 2018 | 6.467328 | -26.2 | 1.0 | 2.066016 | 1230.072138 | 1587.776445 | 0.730668 | 0.675002 | 0.691614 | 0.677128 | -3.498547 | -5.527193 | -26.518474 | -34.473769 | 1.289715 | 0.217006 | 7.955295 | -341.342677 | -9.317269 | 3.088569 | -2.600593 | 15.192839 | -12.518345 | -4.136673 | -41.855717 | -72.258378 | -51.998775 | 9.499447 | 8.670917 | -6.973088 | -4.740623 | -26.964945 | -13.147675 | -23.928700 | -28.940883 | -45.293433 | -15.183406 | -1900.784014 | -0.362402 | -1.314627 | 4.116133 | -294.813511 | -9.917793 | -34.724925 | -5.462844 | -9.367141 | -19.623785 | -38.188082 | 0.187709 | 0.816860 |
| 1627 | 15395 | Sydney | Hawthorn | 2018-08-25 | 23 | S.C.G. | 2018 | 2.128611 | 1.0 | 2.0 | 1.777290 | 1662.568452 | 1615.507209 | 0.699994 | 0.778280 | 0.699158 | 0.673409 | -1.756730 | -0.874690 | -11.415069 | -15.575319 | 0.014390 | 4.073909 | 4.160250 | -174.005092 | -0.942357 | -4.078635 | -4.192916 | 7.814496 | -2.225780 | 6.215760 | 15.042979 | -34.894261 | -50.615255 | 4.214158 | 0.683548 | -3.535594 | -3.168608 | -12.068691 | -30.493980 | -9.867332 | 2.588103 | -22.825570 | -5.604199 | 253.086090 | -2.697132 | -22.612327 | 25.340623 | -90.812188 | 1.967104 | -31.047879 | 0.007606 | -6.880120 | 11.415593 | -49.957313 | 0.440180 | 0.561924 |
| 1628 | 15396 | Brisbane | West Coast | 2018-08-26 | 23 | Gabba | 2018 | 3.442757 | -49.2 | 0.0 | 2.094236 | 1279.963814 | 1622.200265 | 0.683604 | 0.691730 | 0.696822 | 0.709605 | -0.190413 | 1.182699 | 0.040221 | -13.621456 | 1.772577 | 3.026217 | 13.661677 | -22.709485 | 2.424261 | -4.848054 | 1.800473 | 5.051157 | 6.440524 | -5.549630 | -17.041838 | 27.543023 | 33.983159 | 4.459181 | -3.213885 | -0.428455 | 1.514474 | 42.646138 | -7.141638 | 1.457375 | -17.472537 | -15.103115 | 8.001966 | -383.083539 | 6.458915 | 7.275716 | 0.942863 | 44.461590 | 4.640136 | 13.180967 | -15.704694 | 2.366444 | -5.985843 | 38.195255 | 0.433501 | 0.569866 |
| 1629 | 15397 | Melbourne | GWS | 2018-08-26 | 23 | M.C.G. | 2018 | 1.706488 | -23.2 | 2.0 | 1.805565 | 1540.367850 | 1615.614668 | 0.667240 | 0.692632 | 0.684525 | 0.753783 | 2.056899 | 0.635785 | 12.977177 | 6.642811 | 1.443121 | -2.324358 | 6.334366 | 147.281112 | 2.201404 | -5.222254 | 3.250416 | 8.542475 | -2.203571 | 3.559792 | 21.192530 | 33.737734 | 12.865653 | -3.244066 | -2.135243 | 4.100203 | 3.772200 | 48.425291 | 18.247107 | 13.349992 | 11.385136 | -14.687556 | 5.052000 | 304.087088 | 11.062610 | -6.686409 | -16.414544 | 8.350924 | -5.453961 | 12.407662 | 6.672628 | -1.523915 | 13.075351 | 18.522113 | 0.661551 | 0.340379 |
| 1630 | 15398 | St Kilda | North Melbourne | 2018-08-26 | 23 | Docklands | 2018 | 5.516150 | -3.2 | 2.0 | 2.272313 | 1372.453734 | 1454.022032 | 0.730843 | 0.635819 | 0.697018 | 0.654991 | -2.257517 | 1.223261 | -12.321842 | -19.923855 | 1.189755 | 0.463481 | 7.602012 | 27.891262 | 3.201137 | 4.754346 | -1.881145 | -3.924740 | -0.528075 | -8.045729 | -20.584717 | 36.806235 | 39.615090 | 7.018240 | -4.709732 | -4.535660 | -3.372912 | 23.194704 | -18.042370 | 1.214353 | -14.771187 | 13.611531 | 11.690647 | -109.284521 | -0.229945 | 12.384044 | -4.625633 | 57.158576 | 1.353070 | -1.533659 | -6.646259 | -3.489492 | -15.416140 | 58.470456 | 0.284269 | 0.717566 |

---
## Wrapping it Up
We now have a fairly decent amount of features. Some other features which could be added include whether the game is in a major Capital city outisde of Mebourne (i.e. Sydney, Adelaide or Peth), how many 'Elite' players are playing (which could be judged by average SuperCoach scores over 110, for example), as well as your own metrics for attacking and defending.

Note that all of our features have columns starting with 'f_' so in the section, we will grab this feature dataframe and use these features to sport predicting the matches.

---
# 03. Modelling

These tutorials will walk you through how to construct your own basic AFL model, using publically available data. The output will be odds for each team to win, which will be shown on [The Hub](https://www.betfair.com.au/hub/tools/models/afl-prediction-model/).

In this notebook we will walk you through modelling our AFL data to create predictions. We will train a variety of quick and easy models to get a feel of what works and what doesn't. We will then tune our hyperparameters so that we are ready to make week by week predictions.

---
## Grabbing Our Dataset
First, we will import our required modules, as well as the prepare_afl_features function which we created in our afl_feature_creation script. This essentially creates some basic features for us so that we can get started on the modelling component.

```python
# Import libraries
from afl_data_cleaning_v2 import *
import datetime
import pandas as pd
import numpy as np
from sklearn import svm, tree, linear_model, neighbors, naive_bayes, ensemble, discriminant_analysis, gaussian_process
# from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score, GridSearchCV, train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.feature_selection import RFECV
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn import feature_selection
from sklearn import metrics
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
import warnings
warnings.filterwarnings('ignore')
import afl_feature_creation_v2
import afl_data_cleaning_v2
```

```python
# Grab our feature DataFrame which we created in the previous tutorial
feature_df = afl_feature_creation_v2.prepare_afl_features()
afl_data = afl_data_cleaning_v2.prepare_afl_data()
```

```python
feature_df.tail(3)
```

|  | game | home_team | away_team | date | round | venue | season | f_odds | f_form_margin_btwn_teams | f_form_past_5_btwn_teams | f_odds_away | f_elo_home | f_elo_away | f_I50_efficiency_home | f_R50_efficiency_home | f_I50_efficiency_away | f_R50_efficiency_away | f_goals_diff | f_behinds_diff | f_points_diff | f_margin_diff | f_opponent_goals_diff | f_opponent_behinds_diff | f_opponent_points_diff | f_AF_diff | f_B_diff | f_BO_diff | f_CCL_diff | f_CG_diff | f_CL_diff | f_CM_diff | f_CP_diff | f_D_diff | f_ED_diff | f_FA_diff | f_FF_diff | f_G_diff | f_GA_diff | f_HB_diff | f_HO_diff | f_I50_diff | f_ITC_diff | f_K_diff | f_M_diff | f_MG_diff | f_MI5_diff | f_One.Percenters_diff | f_R50_diff | f_SC_diff | f_SCL_diff | f_SI_diff | f_T_diff | f_T5_diff | f_TO_diff | f_UP_diff | f_current_odds_prob | f_current_odds_prob_away |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1628 | 15396 | Brisbane | West Coast | 2018-08-26 | 23 | Gabba | 2018 | 3.442757 | -49.2 | 0.0 | 2.094236 | 1279.963814 | 1622.200265 | 0.683604 | 0.691730 | 0.696822 | 0.709605 | -0.190413 | 1.182699 | 0.040221 | -13.621456 | 1.772577 | 3.026217 | 13.661677 | -22.709485 | 2.424261 | -4.848054 | 1.800473 | 5.051157 | 6.440524 | -5.549630 | -17.041838 | 27.543023 | 33.983159 | 4.459181 | -3.213885 | -0.428455 | 1.514474 | 42.646138 | -7.141638 | 1.457375 | -17.472537 | -15.103115 | 8.001966 | -383.083539 | 6.458915 | 7.275716 | 0.942863 | 44.461590 | 4.640136 | 13.180967 | -15.704694 | 2.366444 | -5.985843 | 38.195255 | 0.433501 | 0.569866 |
| 1629 | 15397 | Melbourne | GWS | 2018-08-26 | 23 | M.C.G. | 2018 | 1.706488 | -23.2 | 2.0 | 1.805565 | 1540.367850 | 1615.614668 | 0.667240 | 0.692632 | 0.684525 | 0.753783 | 2.056899 | 0.635785 | 12.977177 | 6.642811 | 1.443121 | -2.324358 | 6.334366 | 147.281112 | 2.201404 | -5.222254 | 3.250416 | 8.542475 | -2.203571 | 3.559792 | 21.192530 | 33.737734 | 12.865653 | -3.244066 | -2.135243 | 4.100203 | 3.772200 | 48.425291 | 18.247107 | 13.349992 | 11.385136 | -14.687556 | 5.052000 | 304.087088 | 11.062610 | -6.686409 | -16.414544 | 8.350924 | -5.453961 | 12.407662 | 6.672628 | -1.523915 | 13.075351 | 18.522113 | 0.661551 | 0.340379 |
| 1630 | 15398 | St Kilda | North Melbourne | 2018-08-26 | 23 | Docklands | 2018 | 5.516150 | -3.2 | 2.0 | 2.272313 | 1372.453734 | 1454.022032 | 0.730843 | 0.635819 | 0.697018 | 0.654991 | -2.257517 | 1.223261 | -12.321842 | -19.923855 | 1.189755 | 0.463481 | 7.602012 | 27.891262 | 3.201137 | 4.754346 | -1.881145 | -3.924740 | -0.528075 | -8.045729 | -20.584717 | 36.806235 | 39.615090 | 7.018240 | -4.709732 | -4.535660 | -3.372912 | 23.194704 | -18.042370 | 1.214353 | -14.771187 | 13.611531 | 11.690647 | -109.284521 | -0.229945 | 12.384044 | -4.625633 | 57.158576 | 1.353070 | -1.533659 | -6.646259 | -3.489492 | -15.416140 | 58.470456 | 0.284269 | 0.717566 |

```python
# Get the result and merge to the feature_df

match_results = (pd.read_csv("data/afl_match_results.csv")
                    .rename(columns={'Game': 'game'})
                    .assign(result=lambda df: df.apply(lambda row: 1 if row['Home.Points'] > row['Away.Points'] else 0, axis=1)))

# Merge result column to feature_df
feature_df = pd.merge(feature_df, match_results[['game', 'result']], on='game')
```

---
## Creating a Training and Testing Set
So that we don't train our data on the data that we will later test our model on, we will create separate train and test sets. For this exercise we will use the 2018 season to test how our model performs, whilst the rest of the data can be used to train the model.

```python
# Create our test and train sets from our afl DataFrame; drop the columns which leak the result, duplicates, and the advanced
# stats which don't have data until 2015

feature_columns = [col for col in feature_df if col.startswith('f_')]

# Create our test set
test_x = feature_df.loc[feature_df.season == 2018, ['game'] + feature_columns]
test_y = feature_df.loc[feature_df.season == 2018, 'result']

# Create our train set
X = feature_df.loc[feature_df.season != 2018, ['game'] + feature_columns]
y = feature_df.loc[feature_df.season != 2018, 'result']

# Scale features
scaler = StandardScaler()
X[feature_columns] = scaler.fit_transform(X[feature_columns])
test_x[feature_columns] = scaler.transform(test_x[feature_columns])
```

---
## Using Cross Validation to Find The Best Algorithms
Now that we have our training set, we can run through a list of popular classifiers to determine which classifier is best for modelling our data. To do this we will create a function which uses Kfold cross-validation to find the 'best' algorithms, based on how accurate the algorithms' predictions are.

This function will take in a list of classifiers, which we will define below, as well as the training set and it's outcome, and output a DataFrame with the mean and std of the accuracy of each algorithm. Let's jump into it!

```python
# Create a list of standard classifiers
classifiers = [
    #Ensemble Methods
    ensemble.AdaBoostClassifier(),
    ensemble.BaggingClassifier(),
    ensemble.ExtraTreesClassifier(),
    ensemble.GradientBoostingClassifier(),
    ensemble.RandomForestClassifier(),

    #Gaussian Processes
    gaussian_process.GaussianProcessClassifier(),
    
    #GLM
    linear_model.LogisticRegressionCV(),
    
    #Navies Bayes
    naive_bayes.BernoulliNB(),
    naive_bayes.GaussianNB(),
    
    #SVM
    svm.SVC(probability=True),
    svm.NuSVC(probability=True),
    
    #Discriminant Analysis
    discriminant_analysis.LinearDiscriminantAnalysis(),
    discriminant_analysis.QuadraticDiscriminantAnalysis(),
    
    #xgboost: http://xgboost.readthedocs.io/en/latest/model.html
#     XGBClassifier()    
]

# Define a functiom which finds the best algorithms for our modelling task
def find_best_algorithms(classifier_list, X, y):
    # This function is adapted from https://www.kaggle.com/yassineghouzam/titanic-top-4-with-ensemble-modeling
    # Cross validate model with Kfold stratified cross validation
    kfold = StratifiedKFold(n_splits=5)
    
    # Grab the cross validation scores for each algorithm
    cv_results = [cross_val_score(classifier, X, y, scoring = "neg_log_loss", cv = kfold) for classifier in classifier_list]
    cv_means = [cv_result.mean() * -1 for cv_result in cv_results]
    cv_std = [cv_result.std() for cv_result in cv_results]
    algorithm_names = [alg.__class__.__name__ for alg in classifiers]
    
    # Create a DataFrame of all the CV results
    cv_results = pd.DataFrame({
        "Mean Log Loss": cv_means,
        "Log Loss Std": cv_std,
        "Algorithm": algorithm_names
    })
    
    return cv_results.sort_values(by='Mean Log Loss').reset_index(drop=True)
```

```python
best_algos = find_best_algorithms(classifiers, X, y)
best_algos
```

|  | Mean Log Loss | Log Loss Std | Algorithm |
| --- | --- | --- | --- |
| 0 | 0.539131 | 3.640578e-02 | LogisticRegressionCV |
| 1 | 0.551241 | 5.775685e-02 | LinearDiscriminantAnalysis |
| 2 | 0.630994 | 8.257481e-02 | GradientBoostingClassifier |
| 3 | 0.670041 | 9.205780e-03 | AdaBoostClassifier |
| 4 | 0.693147 | 2.360121e-08 | GaussianProcessClassifier |
| 5 | 0.712537 | 2.770864e-02 | SVC |
| 6 | 0.712896 | 2.440755e-02 | NuSVC |
| 7 | 0.836191 | 2.094224e-01 | ExtraTreesClassifier |
| 8 | 0.874307 | 1.558144e-01 | RandomForestClassifier |
| 9 | 1.288174 | 3.953037e-01 | BaggingClassifier |
| 10 | 1.884019 | 4.769589e-01 | QuadraticDiscriminantAnalysis |
| 11 | 2.652161 | 6.886897e-01 | BernoulliNB |
| 12 | 3.299651 | 6.427551e-01 | GaussianNB |

```python
# Try a logistic regression model and see how it performs in terms of accuracy
kfold = StratifiedKFold(n_splits=5)
cv_scores = cross_val_score(linear_model.LogisticRegressionCV(), X, y, scoring='accuracy', cv=kfold)
cv_scores.mean()
    0.7452268937025035
```

### Choosing Our Algorithms
As we can see from above, there are some pretty poor algorithms for predicting the winner. On the other hand, whilst attaining an accuracy of 74.5% (at the time of writing) may seem like a decent result; we must first establish a baseline to judge our performance on. In this case, we will have two baselines; the proportion of games won by the home team and what the odds predict. If we can beat the odds we have created a very powerful model.

Note that a baseline for the log loss can also be both the odds log loss and randomly guessing. Randomly guessing between two teams attains a log loss of log(2) = 0.69, so we have beaten this result.

Once we establish our baseline, we will choose the top algorithms from above and tune their hyperparameters, as well as automatically selecting the best features to be used in our model.

---
## Defining Our Baseline
As stated above, we must define our baseline so that we have a measure to beat. We will use the proportion of games won by the home team, as well as the proportion of favourites who won, based off the odds. To establish this baseline we will use our feature_df, as this has no dropped rows.

```python
# Find the percentage chance of winning at home in each season.
afl_data = afl_data_cleaning_v2.prepare_afl_data()
afl_data['home_win'] = afl_data.apply(lambda x: 1 if x['f_margin'] > 0 else 0, axis=1)
home_games = afl_data[afl_data['home_game'] == 1]
home_games[["home_win", 'season']].groupby(['season']).mean()
```

| season | home_win |
| --- | --- |
| 2011 | 0.561856 |
| 2012 | 0.563725 |
| 2013 | 0.561576 |
| 2014 | 0.574257 |
| 2015 | 0.539604 |
| 2016 | 0.606742 |
| 2017 | 0.604061 |
| 2018 | 0.540404 |

```python
# Find the proportion of favourites who have won

# Define a function which finds if the odds correctly guessed the response
def find_odds_prediction(a_row):
    if a_row['f_odds'] <= a_row['f_odds_away'] and a_row['home_win'] == 1:
        return 1
    elif a_row['f_odds_away'] < a_row['f_odds'] and a_row['home_win'] == 0:
        return 1
    else:
        return 0

# Define a function which splits our DataFrame so each game is on one row instead of two
def get_df_on_one_line(df):
    cols_to_drop = ['date', 'home_game', 'opponent', 
       'f_opponent_behinds', 'f_opponent_goals', 'f_opponent_points', 'f_points',
       'round', 'venue', 'season']
    
    home_df = df[df['home_game'] == 1].rename(columns={'team': 'home_team'})
    away_df = df[df['home_game'] == 0].rename(columns={'team': 'away_team'})
    away_df = away_df.drop(columns=cols_to_drop)

    # Rename away_df columns
    away_df_renamed = away_df.rename(columns={col: col + '_away' for col in away_df.columns if col != 'game'})
    merged_df = pd.merge(home_df, away_df_renamed, on='game')
    
    merged_df['home_win'] = merged_df.f_margin.apply(lambda x: 1 if x > 0 else 0)
    return merged_df
    
afl_data_one_line = get_df_on_one_line(afl_data)
afl_data_one_line['odds_prediction'] = afl_data_one_line.apply(find_odds_prediction, axis=1)
print('The overall mean accuracy of choosing the favourite based on the odds is {}%'.format(
    round(afl_data_one_line['odds_prediction'].mean() * 100, 2)))
afl_data_one_line[["odds_prediction", 'season']].groupby(['season']).mean()
```

    The overall mean accuracy of choosing the favourite based on the odds is 73.15%
    
| season | odds_prediction |
| --- | --- |
| 2011 | 0.784615 |
| 2012 | 0.774510 |
| 2013 | 0.748768 |
| 2014 | 0.727723 |
| 2015 | 0.727723 |
| 2016 | 0.713483 |
| 2017 | 0.659898 |
| 2018 | 0.712121 |

```python
## Get a baseline log loss score from the odds
afl_data_one_line['odds_home_prob'] = 1 / afl_data_one_line.f_odds
afl_data_one_line['odds_away_prob'] = 1 / afl_data_one_line.f_odds_away
```

```python
metrics.log_loss(afl_data_one_line.home_win, afl_data_one_line[['odds_away_prob', 'odds_home_prob']])
    0.5375306549682837
```

We can see that the odds are MUCH more accurate than just choosing the home team to win. We can also see that the mean accuracy of choosing the favourite is around 73%. That means that this is the score we need to beat. Similarly, the log loss of the odds is around 0.5385, whilst our model scores around 0.539 (at the time of writing), without hyperparamter optimisation. Let's choose only the algorithms with log losses below 0.67

```python
chosen_algorithms = best_algos.loc[best_algos['Mean Log Loss'] < 0.67, 'Algorithm'].tolist()
chosen_algorithms
    ['LogisticRegressionCV',
     'LinearDiscriminantAnalysis',
     'GradientBoostingClassifier']
```

---
## Using Grid Search To Tune Hyperparameters
Now that we have our best models, we can use [Grid Search](https://en.wikipedia.org/wiki/Hyperparameter_optimization#Grid_search) to optimise our hyperparameters. Grid search basically involves searching through a range of different algorithm hyperparameters, and choosing those which result in the best score from some metrics, which in our case is accuracy. Let's do this for the algorithms which have hyperparameters which can be tuned. Note that if you are running this on your own computer it may take up to 10 minutes.

```python
# Define a function which optimises the hyperparameters of our chosen algorithms
def optimise_hyperparameters(train_x, train_y, algorithms, parameters):
    kfold = StratifiedKFold(n_splits=5)
    best_estimators = []
    
    for alg, params in zip(algorithms, parameters):
        gs = GridSearchCV(alg, param_grid=params, cv=kfold, scoring='neg_log_loss', verbose=1)
        gs.fit(train_x, train_y)
        best_estimators.append(gs.best_estimator_)
    return best_estimators

# Define our parameters to run a grid search over
lr_grid = {
    "C": [0.0001, 0.001, 0.01, 0.05, 0.2, 0.5],
    "solver": ["newton-cg", "lbfgs", "liblinear"]
}

# Add our algorithms and parameters to lists to be used in our function
alg_list = [LogisticRegression()]
param_list = [lr_grid]
```

```python
# Find the best estimators, then add our other estimators which don't need optimisation
best_estimators = optimise_hyperparameters(X, y, alg_list, param_list)
```
    Fitting 5 folds for each of 18 candidates, totalling 90 fits
    
    [Parallel(n_jobs=1)]: Done  90 out of  90 | elapsed:    5.2s finished

```python
lr_best_params = best_estimators[0].get_params()
lr_best_params
    {'C': 0.01,
     'class_weight': None,
     'dual': False,
     'fit_intercept': True,
     'intercept_scaling': 1,
     'max_iter': 100,
     'multi_class': 'ovr',
     'n_jobs': 1,
     'penalty': 'l2',
     'random_state': None,
     'solver': 'newton-cg',
     'tol': 0.0001,
     'verbose': 0,
     'warm_start': False}
```

```python
kfold = StratifiedKFold(n_splits=10)
cv_scores = cross_val_score(linear_model.LogisticRegression(**lr_best_params), X, y, scoring='neg_log_loss', cv=kfold)
cv_scores.mean()
    -0.528741673153639
```

In the next iteration of this tutorial we will also optimise an XGB model and hopefully outperform our logistic regression model.

---
## Creating Predictions for the 2018 Season
Now that we have an optimised logistic regression model, let's see how it performs on predicting the 2018 season.

```python
lr = LogisticRegression(**lr_best_params)
lr.fit(X, y)
final_predictions = lr.predict(test_x)

accuracy = (final_predictions == test_y).mean() * 100

print("Our accuracy in predicting the 2018 season is: {:.2f}%".format(accuracy))
```

    Our accuracy in predicting the 2018 season is: 67.68%
    
Now let's have a look at all the games which we incorrectly predicted.

```python
game_ids = test_x[(final_predictions != test_y)].game
afl_data_one_line.loc[afl_data_one_line.game.isin(game_ids), ['date', 'home_team', 'opponent', 'f_odds', 'f_odds_away', 'f_margin']]
```

|  | date | home_team | opponent | f_odds | f_odds_away | f_margin |
| --- | --- | --- | --- | --- | --- | --- |
| 1386 | 2018-03-24 | Gold Coast | North Melbourne | 2.0161 | 1.9784 | 16 |
| 1388 | 2018-03-25 | Melbourne | Geelong | 1.7737 | 2.2755 | -3 |
| 1391 | 2018-03-30 | North Melbourne | St Kilda | 3.5769 | 1.3867 | 52 |
| 1392 | 2018-03-31 | Carlton | Gold Coast | 1.5992 | 2.6620 | -34 |
| 1396 | 2018-04-01 | Western Bulldogs | West Coast | 1.8044 | 2.2445 | -51 |
| 1397 | 2018-04-01 | Sydney | Port Adelaide | 1.4949 | 3.0060 | -23 |
| 1398 | 2018-04-02 | Geelong | Hawthorn | 1.7597 | 2.3024 | -1 |
| 1406 | 2018-04-08 | Western Bulldogs | Essendon | 3.8560 | 1.3538 | 21 |
| 1408 | 2018-04-13 | Adelaide | Collingwood | 1.2048 | 5.9197 | -48 |
| 1412 | 2018-04-14 | North Melbourne | Carlton | 1.5799 | 2.7228 | 86 |
| 1415 | 2018-04-15 | Hawthorn | Melbourne | 2.2855 | 1.7772 | 67 |
| 1417 | 2018-04-20 | Sydney | Adelaide | 1.2640 | 4.6929 | -10 |
| 1420 | 2018-04-21 | Port Adelaide | Geelong | 1.5053 | 2.9515 | -34 |
| 1422 | 2018-04-22 | North Melbourne | Hawthorn | 2.6170 | 1.6132 | 28 |
| 1423 | 2018-04-22 | Brisbane | Gold Coast | 1.7464 | 2.3277 | -5 |
| 1425 | 2018-04-25 | Collingwood | Essendon | 1.8372 | 2.1754 | 49 |
| 1427 | 2018-04-28 | Geelong | Sydney | 1.5019 | 2.9833 | -17 |
| 1434 | 2018-04-29 | Fremantle | West Coast | 2.4926 | 1.6531 | -8 |
| 1437 | 2018-05-05 | Essendon | Hawthorn | 2.8430 | 1.5393 | -23 |
| 1439 | 2018-05-05 | Sydney | North Melbourne | 1.2777 | 4.5690 | -2 |
| 1444 | 2018-05-11 | Hawthorn | Sydney | 1.6283 | 2.5818 | -8 |
| 1445 | 2018-05-12 | GWS | West Coast | 1.5425 | 2.8292 | -25 |
| 1446 | 2018-05-12 | Carlton | Essendon | 3.1742 | 1.4570 | 13 |
| 1452 | 2018-05-13 | Collingwood | Geelong | 2.4127 | 1.7040 | -21 |
| 1455 | 2018-05-19 | North Melbourne | GWS | 1.5049 | 2.9752 | 43 |
| 1456 | 2018-05-19 | Essendon | Geelong | 5.6530 | 1.2104 | 34 |
| 1460 | 2018-05-20 | Brisbane | Hawthorn | 3.2891 | 1.4318 | 56 |
| 1461 | 2018-05-20 | West Coast | Richmond | 1.9755 | 2.0154 | 47 |
| 1466 | 2018-05-26 | GWS | Essendon | 1.4364 | 3.2652 | -35 |
| 1467 | 2018-05-27 | Hawthorn | West Coast | 2.2123 | 1.8133 | -15 |
| ... | ... | ... | ... | ... | ... | ... |
| 1483 | 2018-06-10 | Brisbane | Essendon | 2.3018 | 1.7543 | -22 |
| 1485 | 2018-06-11 | Melbourne | Collingwood | 1.6034 | 2.6450 | -42 |
| 1492 | 2018-06-21 | West Coast | Essendon | 1.3694 | 3.6843 | -28 |
| 1493 | 2018-06-22 | Port Adelaide | Melbourne | 1.7391 | 2.3426 | 10 |
| 1499 | 2018-06-29 | Western Bulldogs | Geelong | 6.2067 | 1.1889 | 2 |
| 1501 | 2018-06-30 | Adelaide | West Coast | 1.4989 | 2.9756 | 10 |
| 1504 | 2018-07-01 | Melbourne | St Kilda | 1.1405 | 7.7934 | -2 |
| 1505 | 2018-07-01 | Essendon | North Melbourne | 2.0993 | 1.9022 | 17 |
| 1506 | 2018-07-01 | Fremantle | Brisbane | 1.2914 | 4.3743 | -55 |
| 1507 | 2018-07-05 | Sydney | Geelong | 1.7807 | 2.2675 | -12 |
| 1514 | 2018-07-08 | Essendon | Collingwood | 2.5442 | 1.6473 | -16 |
| 1515 | 2018-07-08 | West Coast | GWS | 1.6790 | 2.4754 | 11 |
| 1516 | 2018-07-12 | Adelaide | Geelong | 2.0517 | 1.9444 | 15 |
| 1518 | 2018-07-14 | Hawthorn | Brisbane | 1.2281 | 5.4105 | -33 |
| 1521 | 2018-07-14 | GWS | Richmond | 2.7257 | 1.5765 | 2 |
| 1522 | 2018-07-15 | Collingwood | West Coast | 1.5600 | 2.7815 | -35 |
| 1523 | 2018-07-15 | North Melbourne | Sydney | 1.9263 | 2.0647 | -6 |
| 1524 | 2018-07-15 | Fremantle | Port Adelaide | 5.9110 | 1.2047 | 9 |
| 1527 | 2018-07-21 | Sydney | Gold Coast | 1.0342 | 27.8520 | -24 |
| 1529 | 2018-07-21 | Brisbane | Adelaide | 2.4614 | 1.6730 | -5 |
| 1533 | 2018-07-22 | Port Adelaide | GWS | 1.6480 | 2.5452 | -22 |
| 1538 | 2018-07-28 | Gold Coast | Carlton | 1.3933 | 3.5296 | -35 |
| 1546 | 2018-08-04 | Adelaide | Port Adelaide | 2.0950 | 1.9135 | 3 |
| 1548 | 2018-08-04 | St Kilda | Western Bulldogs | 1.6120 | 2.6368 | -35 |
| 1555 | 2018-08-11 | Port Adelaide | West Coast | 1.4187 | 3.3505 | -4 |
| 1558 | 2018-08-12 | North Melbourne | Western Bulldogs | 1.3175 | 4.1239 | -7 |
| 1559 | 2018-08-12 | Melbourne | Sydney | 1.3627 | 3.7445 | -9 |
| 1564 | 2018-08-18 | GWS | Sydney | 1.8478 | 2.1672 | -20 |
| 1576 | 2018-08-26 | Brisbane | West Coast | 2.3068 | 1.7548 | -26 |
| 1578 | 2018-08-26 | St Kilda | North Melbourne | 3.5178 | 1.3936 | -23 |

Very interesting! Most of the games we got wrong were upsets. Let's have a look at the games we incorrectly predicted that weren't upsets.

```python
(afl_data_one_line.loc[afl_data_one_line.game.isin(game_ids), ['date', 'home_team', 'opponent', 'f_odds', 'f_odds_away', 'f_margin']]
    .assign(home_favourite=lambda df: df.apply(lambda row: 1 if row.f_odds < row.f_odds_away else 0, axis=1))
    .assign(upset=lambda df: df.apply(lambda row: 1 if row.home_favourite == 1 and row.f_margin < 0 else 
                                      (1 if row.home_favourite == 0 and row.f_margin > 0 else 0), axis=1))
    .query('upset == 0'))
```

|  | date | home_team | opponent | f_odds | f_odds_away | f_margin | home_favourite | upset |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1412 | 2018-04-14 | North Melbourne | Carlton | 1.5799 | 2.7228 | 86 | 1 | 0 |
| 1425 | 2018-04-25 | Collingwood | Essendon | 1.8372 | 2.1754 | 49 | 1 | 0 |
| 1434 | 2018-04-29 | Fremantle | West Coast | 2.4926 | 1.6531 | -8 | 0 | 0 |
| 1437 | 2018-05-05 | Essendon | Hawthorn | 2.8430 | 1.5393 | -23 | 0 | 0 |
| 1452 | 2018-05-13 | Collingwood | Geelong | 2.4127 | 1.7040 | -21 | 0 | 0 |
| 1455 | 2018-05-19 | North Melbourne | GWS | 1.5049 | 2.9752 | 43 | 1 | 0 |
| 1461 | 2018-05-20 | West Coast | Richmond | 1.9755 | 2.0154 | 47 | 1 | 0 |
| 1467 | 2018-05-27 | Hawthorn | West Coast | 2.2123 | 1.8133 | -15 | 0 | 0 |
| 1479 | 2018-06-08 | Port Adelaide | Richmond | 1.7422 | 2.3420 | 14 | 1 | 0 |
| 1483 | 2018-06-10 | Brisbane | Essendon | 2.3018 | 1.7543 | -22 | 0 | 0 |
| 1493 | 2018-06-22 | Port Adelaide | Melbourne | 1.7391 | 2.3426 | 10 | 1 | 0 |
| 1501 | 2018-06-30 | Adelaide | West Coast | 1.4989 | 2.9756 | 10 | 1 | 0 |
| 1514 | 2018-07-08 | Essendon | Collingwood | 2.5442 | 1.6473 | -16 | 0 | 0 |
| 1515 | 2018-07-08 | West Coast | GWS | 1.6790 | 2.4754 | 11 | 1 | 0 |
| 1529 | 2018-07-21 | Brisbane | Adelaide | 2.4614 | 1.6730 | -5 | 0 | 0 |
| 1576 | 2018-08-26 | Brisbane | West Coast | 2.3068 | 1.7548 | -26 | 0 | 0 |
| 1578 | 2018-08-26 | St Kilda | North Melbourne | 3.5178 | 1.3936 | -23 | 0 | 0 |

Let's now look at our model's log loss for the 2018 season compared to the odds.

```python
predictions_probs = lr.predict_proba(test_x)
```

```python
metrics.log_loss(test_y, predictions_probs)
    0.584824211055384
```

```python
test_x_unscaled = feature_df.loc[feature_df.season == 2018, ['game'] + feature_columns]

metrics.log_loss(test_y, test_x_unscaled[['f_current_odds_prob_away', 'f_current_odds_prob']])
    0.5545776633924343
```

So whilst our model performs decently, it doesn't beat the odds in terms of log loss. That's okay, it's still a decent start. In future iterations we can implement other algorithms and create new features which may improve performance.

---
## Next Steps
Now that we have a model up and running, the next steps are to implement the model on a week to week basis.

---
# 04. Weekly Predictions

Now that we have explored different algorithms for modelling, we can implement our chosen model and predict this week's AFL games! All you need to do is run the afl_modelling script each Thursday or Friday to predict the following week's games.

```python
# Import Modules
from afl_feature_creation_v2 import prepare_afl_features
import afl_data_cleaning_v2
import afl_feature_creation_v2
import afl_modelling_v2
import datetime
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')
```

---
## Creating The Features For This Weekend's Games
To actually predict this weekend's games, we need to create the same features that we have created in the previous tutorials for the games that will be played this weekend. This includes all the rolling averages, efficiency features, elo features etc. So the majority of this tutorial will be using previously defined functions to create features for the following weekend's games.

### Create Next Week's DataFrame
Let's first get our cleaned afl_data dataset, as well as the odds for next weekend and the 2018 fixture.

```python
# Grab the cleaned AFL dataset and the column order
afl_data = afl_data_cleaning_v2.prepare_afl_data()
ordered_cols = afl_data.columns

# Define a function which grabs the odds for each game for the following weekend
def get_next_week_odds(path):
    # Get next week's odds
    next_week_odds = pd.read_csv(path)
    next_week_odds = next_week_odds.rename(columns={"team_1": "home_team", 
                                                "team_2": "away_team", 
                                                "team_1_odds": "odds", 
                                                "team_2_odds": "odds_away"
                                               })
    return next_week_odds

# Import the fixture
# Define a function which gets the fixture and cleans it up
def get_fixture(path):
    # Get the afl fixture
    fixture = pd.read_csv(path)

    # Replace team names and reformat
    fixture = fixture.replace({'Brisbane Lions': 'Brisbane', 'Footscray': 'Western Bulldogs'})
    fixture['Date'] = pd.to_datetime(fixture['Date']).dt.date.astype(str)
    fixture = fixture.rename(columns={"Home.Team": "home_team", "Away.Team": "away_team"})
    return fixture

next_week_odds = get_next_week_odds("data/weekly_odds.csv")
fixture = get_fixture("data/afl_fixture_2018.csv")
```

```python
fixture.tail()
```

|  | Date | Season | Season.Game | Round | home_team | away_team | Venue |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 202 | 2018-09-14 | 2018 | 1 | 26 | Hawthorn | Melbourne | MCG |
| 203 | 2018-09-15 | 2018 | 1 | 26 | Collingwood | GWS | MCG |
| 204 | 2018-09-21 | 2018 | 1 | 27 | Richmond | Collingwood | MCG |
| 205 | 2018-09-22 | 2018 | 1 | 27 | West Coast | Melbourne | Optus Stadium |
| 206 | 2018-09-29 | 2018 | 1 | 28 | West Coast | Collingwood | MCG |


```python
next_week_odds
```

|  | home_team | away_team | odds | odds_away |
| --- | --- | --- | --- | --- |
| 0 | West Coast | Collingwood | 2.34 | 1.75 |

Now that we have these DataFrames, we will define a function which combines the fixture and next week's odds to create a single DataFrame for the games over the next 7 days. To use this function we will need Game IDs for next week. So we will create another function which creates Game IDs by using the Game ID from the last game played and adding 1 to it.

```python
# Define a function which creates game IDs for this week's footy games
def create_next_weeks_game_ids(afl_data):
    odds = get_next_week_odds("data/weekly_odds.csv")

    # Get last week's Game ID
    last_afl_data_game = afl_data['game'].iloc[-1]

    # Create Game IDs for next week
    game_ids = [(i+1) + last_afl_data_game for i in range(odds.shape[0])]
    return game_ids

# Define a function which creates this week's footy game DataFrame
def get_next_week_df(afl_data):
    # Get the fixture and the odds for next week's footy games
    fixture = get_fixture("data/afl_fixture_2018.csv")
    next_week_odds = get_next_week_odds("data/weekly_odds.csv")
    next_week_odds['game'] = create_next_weeks_game_ids(afl_data)

    # Get today's date and next week's date and create a DataFrame for next week's games
#     todays_date = datetime.datetime.today().strftime('%Y-%m-%d')

#     date_in_7_days = (datetime.datetime.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    todays_date = '2018-09-27'
    date_in_7_days = '2018-10-04'
    fixture = fixture[(fixture['Date'] >= todays_date) & (fixture['Date'] < date_in_7_days)].drop(columns=['Season.Game'])
    next_week_df = pd.merge(fixture, next_week_odds, on=['home_team', 'away_team'])

    # Split the DataFrame onto two rows for each game
    h_df = (next_week_df[['Date', 'game', 'home_team', 'away_team', 'odds', 'Season', 'Round', 'Venue']]
               .rename(columns={'home_team': 'team', 'away_team': 'opponent'})
               .assign(home_game=1))

    a_df = (next_week_df[['Date', 'game', 'home_team', 'away_team', 'odds_away', 'Season', 'Round', 'Venue']]
                .rename(columns={'odds_away': 'odds', 'home_team': 'opponent', 'away_team': 'team'})
                .assign(home_game=0))

    next_week = a_df.append(h_df).sort_values(by='game').rename(columns={
        'Date': 'date',
        'Season': 'season',
        'Round': 'round',
        'Venue': 'venue'
    })
    next_week['date'] = pd.to_datetime(next_week.date)
    next_week['round'] = afl_data['round'].iloc[-1] + 1
    return next_week
```

```python
next_week_df = get_next_week_df(afl_data)
game_ids_next_round = create_next_weeks_game_ids(afl_data)
next_week_df
```

|  | date | round | season | venue | game | home_game | odds | opponent | team |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 2018-09-29 | 27 | 2018 | MCG | 15407 | 0 | 1.75 | West Coast | Collingwood |
| 0 | 2018-09-29 | 27 | 2018 | MCG | 15407 | 1 | 2.34 | Collingwood | West Coast |


```python
fixture.tail()
```

|  | Date | Season | Season.Game | Round | home_team | away_team | Venue |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 202 | 2018-09-14 | 2018 | 1 | 26 | Hawthorn | Melbourne | MCG |
| 203 | 2018-09-15 | 2018 | 1 | 26 | Collingwood | GWS | MCG |
| 204 | 2018-09-21 | 2018 | 1 | 27 | Richmond | Collingwood | MCG |
| 205 | 2018-09-22 | 2018 | 1 | 27 | West Coast | Melbourne | Optus Stadium |
| 206 | 2018-09-29 | 2018 | 1 | 28 | West Coast | Collingwood | MCG |

### Create Each Feature
Now let's append next week's DataFrame to our afl_data, match_results and odds DataFrames and then create all the features we used in the [AFL Feature Creation Tutorial](/modelling/AFLmodelPart2). We need to append the games and then feed them into our function so that we can create features for upcoming games.

```python
# Append next week's games to our afl_data DataFrame
afl_data = afl_data.append(next_week_df).reset_index(drop=True)

# Append next week's games to match results (we need to do this for our feature creation to run)
match_results = afl_data_cleaning_v2.get_cleaned_match_results().append(next_week_df)

# Append next week's games to odds
odds = (afl_data_cleaning_v2.get_cleaned_odds().pipe(lambda df: df.append(next_week_df[df.columns]))
       .reset_index(drop=True))
```

```python
features_df = afl_feature_creation_v2.prepare_afl_features(afl_data=afl_data, match_results=match_results, odds=odds)
```

```python
features_df.tail()
```

|  | game | home_team | away_team | date | round | venue | season | f_odds | f_form_margin_btwn_teams | f_form_past_5_btwn_teams | f_odds_away | f_elo_home | f_elo_away | f_I50_efficiency_home | f_R50_efficiency_home | f_I50_efficiency_away | f_R50_efficiency_away | f_AF_diff | f_B_diff | f_BO_diff | f_CCL_diff | f_CG_diff | f_CL_diff | f_CM_diff | f_CP_diff | f_D_diff | f_ED_diff | f_FA_diff | f_FF_diff | f_G_diff | f_GA_diff | f_GA1_diff | f_HB_diff | f_HO_diff | f_I50_diff | f_ITC_diff | f_K_diff | f_M_diff | f_MG_diff | f_MI5_diff | f_One.Percenters_diff | f_R50_diff | f_SC_diff | f_SCL_diff | f_SI_diff | f_T_diff | f_T5_diff | f_TO_diff | f_UP_diff | f_Unnamed: 0_diff | f_behinds_diff | f_goals_diff | f_margin_diff | f_opponent_behinds_diff | f_opponent_goals_diff | f_opponent_points_diff | f_points_diff | f_current_odds_prob | f_current_odds_prob_away |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1065 | 15397 | Melbourne | GWS | 2018-08-26 | 23 | M.C.G. | 2018 | 1.966936 | -23.2 | 2.0 | 1.813998 | 1523.456734 | 1609.444874 | 0.653525 | 0.680168 | 0.704767 | 0.749812 | 140.535514 | 0.605144 | -9.771981 | 5.892176 | 7.172376 | 6.614609 | -1.365211 | 30.766262 | 21.998618 | 0.067228 | -1.404730 | -3.166732 | 6.933998 | 6.675576 | 0.000000 | 38.708158 | 24.587333 | 12.008987 | 10.482382 | -16.709540 | -15.415060 | 289.188486 | 6.350287 | -2.263536 | -20.966818 | 50.388632 | 0.723637 | 15.537783 | 22.912269 | 2.065039 | 10.215523 | -6.689429 | 3259.163465 | -0.136383 | 3.553795 | 16.563721 | -2.353514 | 1.162696 | 4.622664 | 21.186385 | 0.661551 | 0.340379 |
| 1066 | 15398 | St Kilda | North Melbourne | 2018-08-26 | 23 | Docklands | 2018 | 5.089084 | -3.2 | 2.0 | 2.577161 | 1397.237139 | 1499.366007 | 0.725980 | 0.655749 | 0.723949 | 0.677174 | 51.799992 | 3.399035 | 6.067393 | -2.189489 | -10.475859 | 1.154766 | -8.883840 | -21.810962 | 33.058382 | 40.618410 | 2.286314 | -0.345734 | -3.778445 | -2.182673 | 0.000000 | 19.816372 | -21.562916 | 2.678384 | -14.777698 | 13.242010 | 12.065594 | -82.381996 | -2.176564 | 2.335825 | -4.952336 | 45.719406 | 3.344217 | -2.095613 | -3.929084 | -3.182381 | -12.832197 | 57.226776 | -20221.371526 | 1.968709 | -1.897958 | -15.177001 | 1.067099 | 0.781811 | 5.757963 | -9.419038 | 0.284269 | 0.717566 |
| 1067 | 15404 | Collingwood | GWS | 2018-09-15 | 25 | M.C.G. | 2018 | 1.882301 | 12.6 | 3.0 | 2.018344 | 1546.000498 | 1590.806454 | 0.693185 | 0.706222 | 0.718446 | 0.727961 | 205.916671 | -1.642954 | -2.980828 | -0.266023 | 8.547225 | -3.751909 | -0.664977 | 10.563513 | 48.175985 | 43.531908 | -5.836979 | 5.388668 | 4.395675 | 2.555152 | 0.000000 | 51.588962 | 11.558254 | 4.276481 | 11.284445 | -3.412977 | -2.206815 | -234.577304 | 2.637758 | -10.537765 | -11.127876 | 125.607377 | -3.485896 | 3.532031 | 15.102292 | -2.500685 | 8.187543 | 38.053445 | 12500.525732 | -1.006173 | 2.520135 | 18.634835 | -2.159882 | -0.393386 | -4.520198 | 14.114637 | 0.608495 | 0.393856 |
| 1068 | 15406 | West Coast | Melbourne | 2018-09-22 | 26 | Perth Stadium | 2018 | 2.013572 | 21.2 | 3.0 | 1.884148 | 1577.888606 | 1542.095154 | 0.688877 | 0.708941 | 0.649180 | 0.698319 | -118.135184 | -3.005709 | 2.453190 | -5.103869 | -14.368949 | -12.245458 | 2.771411 | -45.364271 | -60.210182 | -24.049523 | -2.791277 | 6.115918 | -5.041030 | -5.335746 | 0.000000 | -78.816902 | -18.784547 | -13.957754 | -5.527613 | 18.606721 | 25.366778 | -910.988860 | -5.515812 | -9.483590 | 8.914093 | -131.380758 | -7.142529 | -49.484957 | -13.718798 | -4.862994 | -9.834616 | -23.673638 | -3178.282073 | -1.785349 | -2.569957 | -20.008787 | 0.476202 | 0.387915 | 2.803694 | -17.205093 | 0.543774 | 0.457875 |
| 1069 | 15407 | West Coast | Collingwood | 2018-09-29 | 27 | MCG | 2018 | 1.981832 | 17.2 | 3.0 | 1.838864 | 1591.348723 | 1562.924273 | 0.679011 | 0.724125 | 0.711352 | 0.709346 | 159.522670 | 0.893421 | -0.475725 | 3.391070 | -5.088751 | 5.875388 | 5.352234 | 7.729063 | -7.358202 | -4.719968 | 6.113565 | 4.822252 | 2.871241 | 2.690270 | 3.636364 | -64.238180 | -0.631102 | 2.078832 | 6.005613 | 56.879978 | 34.373271 | 1016.491933 | 1.199751 | 2.454685 | 12.197047 | 219.666562 | 2.484363 | 0.379162 | 2.566991 | 0.639666 | 2.258377 | -23.841529 | -368920.360240 | -0.646160 | 0.892051 | 3.040850 | 1.589568 | 0.012622 | 1.665299 | 4.706148 | 0.427350 | 0.571429 |

---
## Create Predictions For the Upcoming Round
Now that we have our features, we can use our model that we created in [part 3](/modelling/AFLmodelPart3) to predict the next round. First we need to filter our features_df into a training df and a df with next round's features/matches. Then we can use the model created in the last tutorial to create predictions. For simplicity, I have hardcoded the parameters we used in the last tutorial.

```python
# Get the train df by only taking the games IDs which aren't in the next week df
train_df = features_df[~features_df.game.isin(next_week_df.game)]

# Get the result and merge to the feature_df
match_results = (pd.read_csv("data/afl_match_results.csv")
                    .rename(columns={'Game': 'game'})
                    .assign(result=lambda df: df.apply(lambda row: 1 if row['Home.Points'] > row['Away.Points'] else 0, axis=1)))

train_df = pd.merge(train_df,  match_results[['game', 'result']], on='game')

train_x = train_df.drop(columns=['result'])
train_y = train_df.result

next_round_x = features_df[features_df.game.isin(next_week_df.game)]
```

```python
# Fit out logistic regression model - note that our predictions come out in the order of [away_team_prob, home_team_prob]

lr_best_params = {'C': 0.01,
 'class_weight': None,
 'dual': False,
 'fit_intercept': True,
 'intercept_scaling': 1,
 'max_iter': 100,
 'multi_class': 'ovr',
 'n_jobs': 1,
 'penalty': 'l2',
 'random_state': None,
 'solver': 'newton-cg',
 'tol': 0.0001,
 'verbose': 0,
 'warm_start': False}

feature_cols = [col for col in train_df if col.startswith('f_')]

# Scale features
scaler = StandardScaler()
train_x[feature_cols] = scaler.fit_transform(train_x[feature_cols])
next_round_x[feature_cols] = scaler.transform(next_round_x[feature_cols])

lr = LogisticRegression(**lr_best_params)
lr.fit(train_x[feature_cols], train_y)
prediction_probs = lr.predict_proba(next_round_x[feature_cols])

modelled_home_odds = [1/i[1] for i in prediction_probs]
modelled_away_odds = [1/i[0] for i in prediction_probs]
```

```python
# Create a predictions df
preds_df = (next_round_x[['date', 'home_team', 'away_team', 'venue', 'game']].copy()
               .assign(modelled_home_odds=modelled_home_odds,
                      modelled_away_odds=modelled_away_odds)
               .pipe(pd.merge, next_week_odds, on=['home_team', 'away_team'])
               .pipe(pd.merge, features_df[['game', 'f_elo_home', 'f_elo_away']], on='game')
               .drop(columns='game')
           )
```

```python
preds_df
```

|  | date | home_team | away_team | venue | modelled_home_odds | modelled_away_odds | odds | odds_away | f_elo_home | f_elo_away |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 2018-09-29 | West Coast | Collingwood | MCG | 2.326826 | 1.753679 | 2.34 | 1.75 | 1591.348723 | 1562.924273 |

Alternatively, if you want to generate predictions using a script which uses all the above code, just run the following:

```python
print(afl_modelling_v2.create_predictions())
```

            date   home_team    away_team venue  modelled_home_odds  \
    0 2018-09-29  West Coast  Collingwood   MCG            2.326826   
    
       modelled_away_odds  odds  odds_away   f_elo_home   f_elo_away  
    0            1.753679  2.34       1.75  1591.348723  1562.924273  
   
---
## Conclusion
Congratulations! You have created AFL predictions for this week. If you are beginner to this, don't be overwhelmed. The process gets easier each time you do it. And it is super rewarding. In future iterations we will update this tutorial to predict actual odds, and then integrate this with [Betfair's API](../../api/apiappkey) so that you can create an automated betting strategy using Machine Learning to create your predictions!

--- 
### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.