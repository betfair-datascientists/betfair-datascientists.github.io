# EPL Machine Learning Walkthrough

# 04. Weekly Predictions

Welcome to the third part of this Machine Learning Walkthrough. This tutorial will be a walk through of creating weekly EPL predictions from the basic logistic regression model we built in the previous tutorial. We will then analyse our predictions and create staking strategies in the next tutorial.

Specifically, this tutorial will cover a few things:

1. Obtaining Weekly Odds / Game Info Using Betfair's API
2. Data Wrangling This Week's Game Info Into Our Feature Set

---
## Obtaining Weekly Odds / Game Info Using Betfair's API
The first thing we need to do to create weekly predictions is get both the games being played this week, as well as match odds from Betfair to be used as features.

To make this process easier, I have created a csv file with the fixture for the 2018/19 season. Let's load that now.

```python
## Import libraries
import pandas as pd
from weekly_prediction_functions import *
from data_preparation_functions import *
from sklearn.metrics import log_loss, confusion_matrix
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 100)
```

```python
fixture = (pd.read_csv('data/fixture.csv')
              .assign(Date=lambda df: pd.to_datetime(df.Date)))
```

```python
fixture.head()
```

|  | Date | Time (AEST) | HomeTeam | AwayTeam | Venue | TV | Year | round | season |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 2018-08-11 | 5:00 AM | Man United | Leicester | Old Trafford, Manchester | Optus, Fox Sports (delay) | 2018 | 1 | 1819 |
| 1 | 2018-08-11 | 9:30 PM | Newcastle | Tottenham | St.James’ Park, Newcastle | Optus, SBS | 2018 | 1 | 1819 |
| 2 | 2018-08-12 | 12:00 AM | Bournemouth | Cardiff | Vitality Stadium, Bournemouth | Optus | 2018 | 1 | 1819 |
| 3 | 2018-08-12 | 12:00 AM | Fulham | Crystal Palace | Craven Cottage, London | Optus | 2018 | 1 | 1819 |
| 4 | 2018-08-12 | 12:00 AM | Huddersfield | Chelsea | John Smith’s Stadium, Huddersfield | Optus, Fox Sports (delay) | 2018 | 1 | 1819 |

Now we are going to connect to the API and retrieve game level information for the next week. To do this, we will use an R script. If you are not familiar with R, don't worry, it is relatively simple to read through. For this, we will run the script weekly_game_info_puller.R. Go ahead and run that script now.

Note that for this step, you will require a Betfair API App Key. If you don't have one, visit [this page and follow the instructions](../../api/apiappkey).

I will upload an updated weekly file, so you can follow along regardless of if you have an App Key or not. Let's load that file in now.

```python
game_info = create_game_info_df("data/weekly_game_info.csv")
```

```python
game_info.head(3)
```

|  | AwayTeam | HomeTeam | awaySelectionId | drawSelectionId | homeSelectionId | draw | marketId | marketStartTime | totalMatched | eventId | eventName | homeOdds | drawOdds | awayOdds | competitionId | Date | localMarketStartTime |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Arsenal | Cardiff | 1096 | 58805 | 79343 | The Draw | 1.146897152 | 2018-09-02 12:30:00 | 30123.595116 | 28852020 | Cardiff v Arsenal | 7.00 | 4.3 | 1.62 | 10932509 | 2018-09-02 | Sun September  2, 10:30PM |
| 1 | Bournemouth | Chelsea | 1141 | 58805 | 55190 | The Draw | 1.146875421 | 2018-09-01 14:00:00 | 30821.329656 | 28851426 | Chelsea v Bournemouth | 1.32 | 6.8 | 12.00 | 10932509 | 2018-09-01 | Sun September  2, 12:00AM |
| 2 | Fulham | Brighton | 56764 | 58805 | 18567 | The Draw | 1.146875746 | 2018-09-01 14:00:00 | 16594.833096 | 28851429 | Brighton v Fulham | 2.36 | 3.5 | 3.50 | 10932509 | 2018-09-01 | Sun September  2, 12:00AM |

Finally, we will use the API to grab the weekly odds. This R script is also provided, but I have also included the weekly odds csv for convenience.

```python
odds = (pd.read_csv('data/weekly_epl_odds.csv')
           .replace({
                'Man Utd': 'Man United',
                'C Palace': 'Crystal Palace'}))
```

```python
odds.head(3)
```

|  | HomeTeam | AwayTeam | f_homeOdds | f_drawOdds | f_awayOdds |
| --- | --- | --- | --- | --- | --- |
| 0 | Leicester | Liverpool | 7.80 | 5.1 | 1.48 |
| 1 | Brighton | Fulham | 2.36 | 3.5 | 3.50 |
| 2 | Everton | Huddersfield | 1.54 | 4.4 | 8.20 |

---
## Data Wrangling This Week's Game Info Into Our Feature Set
Now we have the arduous task of wrangling all of this info into a feature set that we can use to predict this week's games. Luckily our functions we created earlier should work if we just append the non-features to our main dataframe.

```python
df = create_df('data/epl_data.csv')
```

```python
df.head()
```

|  | AC | AF | AR | AS | AST | AY | AwayTeam | B365A | B365D | B365H | BWA | BWD | BWH | Bb1X2 | BbAH | BbAHh | BbAv<2.5 | BbAv>2.5 | BbAvA | BbAvAHA | BbAvAHH | BbAvD | BbAvH | BbMx<2.5 | BbMx>2.5 | BbMxA | BbMxAHA | BbMxAHH | BbMxD | BbMxH | BbOU | Date | Day | Div | FTAG | FTHG | FTR | HC | HF | HR | HS | HST | HTAG | HTHG | HTR | HY | HomeTeam | IWA | IWD | IWH | LBA | LBD | LBH | Month | Referee | VCA | VCD | VCH | Year | season | gameId | homeWin | awayWin | result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6.0 | 14.0 | 1.0 | 11.0 | 5.0 | 1.0 | Blackburn | 2.75 | 3.20 | 2.50 | 2.90 | 3.30 | 2.20 | 55.0 | 20.0 | 0.00 | 1.71 | 2.02 | 2.74 | 2.04 | 1.82 | 3.16 | 2.40 | 1.80 | 2.25 | 2.90 | 2.08 | 1.86 | 3.35 | 2.60 | 35.0 | 2005-08-13 | 13 | E0 | 1.0 | 3.0 | H | 2.0 | 11.0 | 0.0 | 13.0 | 5.0 | 1.0 | 0.0 | A | 0.0 | West Ham | 2.7 | 3.0 | 2.3 | 2.75 | 3.00 | 2.38 | 8 | A Wiley | 2.75 | 3.25 | 2.40 | 2005 | 0506 | 1 | 1 | 0 | home |
| 1 | 8.0 | 16.0 | 0.0 | 13.0 | 6.0 | 2.0 | Bolton | 3.00 | 3.25 | 2.30 | 3.15 | 3.25 | 2.10 | 56.0 | 22.0 | -0.25 | 1.70 | 2.01 | 3.05 | 1.84 | 2.01 | 3.16 | 2.20 | 1.87 | 2.20 | 3.40 | 1.92 | 2.10 | 3.30 | 2.40 | 36.0 | 2005-08-13 | 13 | E0 | 2.0 | 2.0 | D | 7.0 | 14.0 | 0.0 | 3.0 | 2.0 | 2.0 | 2.0 | D | 0.0 | Aston Villa | 3.1 | 3.0 | 2.1 | 3.20 | 3.00 | 2.10 | 8 | M Riley | 3.10 | 3.25 | 2.20 | 2005 | 0506 | 2 | 0 | 0 | draw |
| 2 | 6.0 | 14.0 | 0.0 | 12.0 | 5.0 | 1.0 | Man United | 1.72 | 3.40 | 5.00 | 1.75 | 3.35 | 4.35 | 56.0 | 23.0 | 0.75 | 1.79 | 1.93 | 1.69 | 1.86 | 2.00 | 3.36 | 4.69 | 1.87 | 2.10 | 1.80 | 1.93 | 2.05 | 3.70 | 5.65 | 36.0 | 2005-08-13 | 13 | E0 | 2.0 | 0.0 | A | 8.0 | 15.0 | 0.0 | 10.0 | 5.0 | 1.0 | 0.0 | A | 3.0 | Everton | 1.8 | 3.1 | 3.8 | 1.83 | 3.20 | 3.75 | 8 | G Poll | 1.80 | 3.30 | 4.50 | 2005 | 0506 | 3 | 0 | 1 | away |
| 3 | 6.0 | 13.0 | 0.0 | 7.0 | 4.0 | 2.0 | Birmingham | 2.87 | 3.25 | 2.37 | 2.80 | 3.20 | 2.30 | 56.0 | 21.0 | 0.00 | 1.69 | 2.04 | 2.87 | 2.05 | 1.81 | 3.16 | 2.31 | 1.77 | 2.24 | 3.05 | 2.11 | 1.85 | 3.30 | 2.60 | 36.0 | 2005-08-13 | 13 | E0 | 0.0 | 0.0 | D | 6.0 | 12.0 | 0.0 | 15.0 | 7.0 | 0.0 | 0.0 | D | 1.0 | Fulham | 2.9 | 3.0 | 2.2 | 2.88 | 3.00 | 2.25 | 8 | R Styles | 2.80 | 3.25 | 2.35 | 2005 | 0506 | 4 | 0 | 0 | draw |
| 4 | 6.0 | 11.0 | 0.0 | 13.0 | 3.0 | 3.0 | West Brom | 5.00 | 3.40 | 1.72 | 4.80 | 3.45 | 1.65 | 55.0 | 23.0 | -0.75 | 1.77 | 1.94 | 4.79 | 1.76 | 2.10 | 3.38 | 1.69 | 1.90 | 2.10 | 5.60 | 1.83 | 2.19 | 3.63 | 1.80 | 36.0 | 2005-08-13 | 13 | E0 | 0.0 | 0.0 | D | 3.0 | 13.0 | 0.0 | 15.0 | 8.0 | 0.0 | 0.0 | D | 2.0 | Man City | 4.2 | 3.2 | 1.7 | 4.50 | 3.25 | 1.67 | 8 | C Foy | 5.00 | 3.25 | 1.75 | 2005 | 0506 | 5 | 0 | 0 | draw |

Now we need to specify which game week we would like to predict. We will then filter the fixture for this game week and append this info to the main DataFrame

```python
round_to_predict = int(input("Which game week would you like to predict? Please input next week's Game Week\n"))
```

    Which game week would you like to predict? Please input next week's Game Week
    4

```python
future_predictions = (fixture.loc[fixture['round'] == round_to_predict, ['Date', 'HomeTeam', 'AwayTeam', 'season']]
                             .pipe(pd.merge, odds, on=['HomeTeam', 'AwayTeam'])
                             .rename(columns={
                                 'f_homeOdds': 'B365H',
                                 'f_awayOdds': 'B365A',
                                 'f_drawOdds': 'B365D'})
                             .assign(season=lambda df: df.season.astype(str)))
```

```python
df_including_future_games = (pd.read_csv('data/epl_data.csv', dtype={'season': str})
                .assign(Date=lambda df: pd.to_datetime(df.Date))
                .pipe(lambda df: df.dropna(thresh=len(df) - 2, axis=1))  # Drop cols with NAs
                .dropna(axis=0)  # Drop rows with NAs
                .sort_values('Date')
                .append(future_predictions, sort=True)
                .reset_index(drop=True)
                .assign(gameId=lambda df: list(df.index + 1),
                            Year=lambda df: df.Date.apply(lambda row: row.year),
                            homeWin=lambda df: df.apply(lambda row: 1 if row.FTHG > row.FTAG else 0, axis=1),
                            awayWin=lambda df: df.apply(lambda row: 1 if row.FTAG > row.FTHG else 0, axis=1),
                            result=lambda df: df.apply(lambda row: 'home' if row.FTHG > row.FTAG else ('draw' if row.FTHG == row.FTAG else 'away'), axis=1)))
```

```python
df_including_future_games.tail(12)
```

|  | AC | AF | AR | AS | AST | AY | AwayTeam | B365A | B365D | B365H | BWA | BWD | BWH | Bb1X2 | BbAH | BbAHh | BbAv<2.5 | BbAv>2.5 | BbAvA | BbAvAHA | BbAvAHH | BbAvD | BbAvH | BbMx<2.5 | BbMx>2.5 | BbMxA | BbMxAHA | BbMxAHH | BbMxD | BbMxH | BbOU | Date | Day | Div | FTAG | FTHG | FTR | HC | HF | HR | HS | HST | HTAG | HTHG | HTR | HY | HomeTeam | IWA | IWD | IWH | LBA | LBD | LBH | Month | Referee | VCA | VCD | VCH | Year | season | gameId | homeWin | awayWin | result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4952 | 4.0 | 8.0 | 0.0 | 12.0 | 2.0 | 1.0 | Burnley | 4.33 | 3.40 | 2.00 | 4.0 | 3.3 | 2.00 | 39.0 | 20.0 | -0.25 | 1.65 | 2.22 | 4.14 | 2.22 | 1.69 | 3.36 | 1.98 | 1.72 | 2.31 | 4.5 | 2.32 | 1.74 | 3.57 | 2.04 | 36.0 | 2018-08-26 | 26.0 | E0 | 2.0 | 4.0 | H | 6.0 | 11.0 | 0.0 | 25.0 | 12.0 | 2.0 | 3.0 | H | 2.0 | Fulham | 4.10 | 3.35 | 1.97 | 3.90 | 3.2 | 2.00 | 8.0 | D Coote | 4.33 | 3.4 | 2.0 | 2018 | 1819 | 4953 | 1 | 0 | home |
| 4953 | 2.0 | 16.0 | 0.0 | 9.0 | 5.0 | 4.0 | Tottenham | 2.90 | 3.30 | 2.62 | 2.9 | 3.2 | 2.55 | 42.0 | 20.0 | -0.25 | 1.79 | 2.03 | 2.86 | 1.72 | 2.18 | 3.27 | 2.56 | 1.84 | 2.10 | 3.0 | 1.76 | 2.25 | 3.40 | 2.67 | 40.0 | 2018-08-27 | 27.0 | E0 | 3.0 | 0.0 | A | 5.0 | 11.0 | 0.0 | 23.0 | 5.0 | 0.0 | 0.0 | D | 2.0 | Man United | 2.75 | 3.25 | 2.60 | 2.75 | 3.2 | 2.55 | 8.0 | C Pawson | 2.90 | 3.3 | 2.6 | 2018 | 1819 | 4954 | 0 | 1 | away |
| 4954 | NaN | NaN | NaN | NaN | NaN | NaN | Liverpool | 1.48 | 5.10 | 7.80 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018-09-01 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Leicester | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018 | 1819 | 4955 | 0 | 0 | away |
| 4955 | NaN | NaN | NaN | NaN | NaN | NaN | Fulham | 3.50 | 3.50 | 2.36 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018-09-02 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Brighton | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018 | 1819 | 4956 | 0 | 0 | away |
| 4956 | NaN | NaN | NaN | NaN | NaN | NaN | Man United | 1.70 | 3.90 | 6.60 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018-09-02 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Burnley | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018 | 1819 | 4957 | 0 | 0 | away |
| 4957 | NaN | NaN | NaN | NaN | NaN | NaN | Bournemouth | 12.00 | 6.80 | 1.32 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018-09-02 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Chelsea | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018 | 1819 | 4958 | 0 | 0 | away |
| 4958 | NaN | NaN | NaN | NaN | NaN | NaN | Southampton | 4.50 | 3.55 | 2.04 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018-09-02 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Crystal Palace | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018 | 1819 | 4959 | 0 | 0 | away |
| 4959 | NaN | NaN | NaN | NaN | NaN | NaN | Huddersfield | 8.20 | 4.40 | 1.54 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018-09-02 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Everton | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018 | 1819 | 4960 | 0 | 0 | away |
| 4960 | NaN | NaN | NaN | NaN | NaN | NaN | Wolves | 2.98 | 3.50 | 2.62 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018-09-02 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | West Ham | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018 | 1819 | 4961 | 0 | 0 | away |
| 4961 | NaN | NaN | NaN | NaN | NaN | NaN | Newcastle | 32.00 | 12.50 | 1.12 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018-09-02 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Man City | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018 | 1819 | 4962 | 0 | 0 | away |
| 4962 | NaN | NaN | NaN | NaN | NaN | NaN | Arsenal | 1.62 | 4.30 | 7.00 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018-09-02 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Cardiff | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018 | 1819 | 4963 | 0 | 0 | away |
| 4963 | NaN | NaN | NaN | NaN | NaN | NaN | Tottenham | 1.68 | 4.30 | 5.90 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018-09-03 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | Watford | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | 2018 | 1819 | 4964 | 0 | 0 | away |

As we can see, what we have done is appended the Game information to our main DataFrame. The rest of the info is left as NAs, but this will be filled when we created our rolling average features. This is a 'hacky' type of way to complete this task, but works well as we can use the same functions that we created in the previous tutorials on this DataFrame. We now need to add the odds from our odds DataFrame, then we can just run our create features functions as usual.

---
## Predicting Next Gameweek's Results
Now that we have our feature DataFrame, all we need to do is split the feature DataFrame up into a training set and next week's games, then use the model we tuned in the last tutorial to create predictions!

```python
features = create_feature_df(df=df_including_future_games)

    Creating all games feature DataFrame
    Creating stats feature DataFrame
    Creating odds feature DataFrame
    Creating market values feature DataFrame
    Filling NAs
    Merging stats, odds and market values into one features DataFrame
    Complete.
```

```python
# Create a feature DataFrame for this week's games.
production_df = pd.merge(future_predictions, features, on=['Date', 'HomeTeam', 'AwayTeam', 'season'])
```

```python
# Create a training DataFrame
training_df = features[~features.gameId.isin(production_df.gameId)]
```

```python
feature_names = [col for col in training_df if col.startswith('f_')]

le = LabelEncoder()
train_y = le.fit_transform(training_df.result)
train_x = training_df[feature_names]
```

```python
lr = LogisticRegression(C=0.01, solver='liblinear')
lr.fit(train_x, train_y)
predicted_probs = lr.predict_proba(production_df[feature_names])
predicted_odds = 1 / predicted_probs
```

```python
# Assign the modelled odds to our predictions df
predictions_df = (production_df.loc[:, ['Date', 'HomeTeam', 'AwayTeam', 'B365H', 'B365D', 'B365A']]
                               .assign(homeModelledOdds=[i[2] for i in predicted_odds],
                                      drawModelledOdds=[i[1] for i in predicted_odds],
                                      awayModelledOdds=[i[0] for i in predicted_odds])
                               .rename(columns={
                                   'B365H': 'BetfairHomeOdds',
                                   'B365D': 'BetfairDrawOdds',
                                   'B365A': 'BetfairAwayOdds'}))
```

```python
predictions_df
```

|  | Date | HomeTeam | AwayTeam | BetfairHomeOdds | BetfairDrawOdds | BetfairAwayOdds | homeModelledOdds | drawModelledOdds | awayModelledOdds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 2018-09-01 | Leicester | Liverpool | 7.80 | 5.10 | 1.48 | 5.747661 | 5.249857 | 1.573478 |
| 1 | 2018-09-02 | Brighton | Fulham | 2.36 | 3.50 | 3.50 | 2.183193 | 3.803120 | 3.584057 |
| 2 | 2018-09-02 | Burnley | Man United | 6.60 | 3.90 | 1.70 | 5.282620 | 4.497194 | 1.699700 |
| 3 | 2018-09-02 | Chelsea | Bournemouth | 1.32 | 6.80 | 12.00 | 1.308366 | 6.079068 | 14.047070 |
| 4 | 2018-09-02 | Crystal Palace | Southampton | 2.04 | 3.55 | 4.50 | 2.202871 | 4.213695 | 3.239122 |
| 5 | 2018-09-02 | Everton | Huddersfield | 1.54 | 4.40 | 8.20 | 1.641222 | 3.759249 | 8.020055 |
| 6 | 2018-09-02 | West Ham | Wolves | 2.62 | 3.50 | 2.98 | 1.999816 | 4.000456 | 4.000279 |
| 7 | 2018-09-02 | Man City | Newcastle | 1.12 | 12.50 | 32.00 | 1.043103 | 29.427939 | 136.231983 |
| 8 | 2018-09-02 | Cardiff | Arsenal | 7.00 | 4.30 | 1.62 | 6.256929 | 4.893445 | 1.572767 |
| 9 | 2018-09-03 | Watford | Tottenham | 5.90 | 4.30 | 1.68 | 5.643663 | 4.338926 | 1.688224 |

Above are the predictions for this Gameweek's matches. In the next tutorial we will explore the errors our model has made, and work on creating a profitable betting strategy.