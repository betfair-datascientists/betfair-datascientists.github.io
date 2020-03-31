# AFL Modelling Walkthrough 

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

Note that all of our features have columns starting with 'f_' so in the [next tutorial](/modelling/AFLmodelPart3), we will grab this feature dataframe and use these features to sport predicting the matches.