# Modelling the Brownlow

This walkthrough will provide a brief, yet effective tutorial on how to model the Brownlow medal. We will use data from 2010 to 2018, which includes Supercoach points and other useful stats.

The output will be the number of votes predicted for each player in each match, and we will aggregate these to create aggregates for each team and for the whole competition. No doubt we'll have Mitchell right up the top, and if we don't, then we know we've done something wrong!

```python
# Import modules libraries
import pandas as pd
import h2o
from h2o.automl import H2OAutoML
import numpy as np
from sklearn.preprocessing import StandardScaler
import os
import pickle

# Change notebook settings
pd.options.display.max_columns = None
pd.options.display.max_rows = 300
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
```

---
## EDA - Read in the data
I have collated this data using the fitzRoy R package and merging the afltables dataset with the footywire dataset, so that we can Supercoach and other advanced stats with Brownlow votes. Let's read in the data and have a sneak peak at what it looks like.

```python
brownlow_data = pd.read_csv('data/afl_brownlow_data.csv')

brownlow_data.tail(3)
```

|  | date | season | round | venue | ID | match_id | player | jumper_no | team | opposition | status | team_score | opposition_score | margin | brownlow_votes | CP | UP | ED | DE | CM | GA | MI5 | one_perc | BO | TOG | K | HB | D | M | G | B | T | HO | I50 | CL | CG | R50 | FF | FA | AF | SC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 76585 | 2018-08-26 | 2018 | 23 | Etihad Stadium | 12312 | 9708.0 | M Wood | 32 | North Melbourne | St Kilda | Away | 117 | 94 | 23 | NaN | 0 | 3 | 2 | 66.7 | 0 | 0 | 2 | 0 | 0 | 34 | 3 | 0 | 3 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 24 | 25 |
| 76586 | 2018-08-26 | 2018 | 23 | Etihad Stadium | 11755 | 9708.0 | S Wright | 19 | North Melbourne | St Kilda | Away | 117 | 94 | 23 | NaN | 10 | 17 | 22 | 75.9 | 0 | 0 | 0 | 0 | 1 | 83 | 16 | 13 | 29 | 8 | 0 | 0 | 2 | 0 | 3 | 0 | 4 | 4 | 1 | 0 | 107 | 96 |
| 76587 | 2018-08-26 | 2018 | 23 | Etihad Stadium | 11724 | 9708.0 | J Ziebell | 7 | North Melbourne | St Kilda | Away | 117 | 94 | 23 | NaN | 9 | 8 | 11 | 73.3 | 0 | 0 | 2 | 4 | 0 | 94 | 12 | 3 | 15 | 6 | 3 | 1 | 2 | 0 | 1 | 0 | 0 | 0 | 2 | 0 | 89 | 109 |

It looks like we've got about 76,000 rows of data and have stats like hitouts, clangers, effective disposals etc. Let's explore some certain scenarios. Using my domain knowledge of footy, I can hypothesise that if a player kicks 5 goals, he is pretty likely to poll votes. Similarly, if a player gets 30 possessions and 2+ goals, he is also probably likely to poll votes. Let's have a look at the mean votes for players for both of these situations. 

### Exploring votes if a bag is kicked (5+ goals)

```python
brownlow_data.query('G >= 5').groupby('season').brownlow_votes.mean()
print("Mean votes is a player has kicked a bag:", brownlow_data.query('G >= 5').brownlow_votes.mean())

    season
    2010    1.420455
    2011    1.313433
    2012    1.413333
    2013    1.253731
    2014    1.915254
    2015    1.765625
    2016    1.788732
    2017    2.098361
    2018    0.000000
    Name: brownlow_votes, dtype: float64

    Mean votes is a player has kicked a bag: 1.4708818635607321
```

### Exploring votes if the player has 30+ possies & 2+ goals 

```python
brownlow_data.query('G >= 2 and D >= 30').groupby('season').brownlow_votes.mean()
print("Mean votes if a player has 30 possies and kicks 2+ goals:", brownlow_data.query('G >= 2 and D >= 30').brownlow_votes.mean())

    season
    2010    1.826923
    2011    1.756410
    2012    2.118421
    2013    2.000000
    2014    2.253731
    2015    2.047619
    2016    2.103448
    2017    2.050000
    2018    0.000000
    Name: brownlow_votes, dtype: float64

    Mean votes if a player has 30 possies and kicks 2+ goals: 1.8741379310344828
```

As suspected, the average votes for these two situations is 1.87! That's huge. Let's get an idea of the average votes for each player. It should be around 6/44, as there are always 6 votes per match and around 44 players per match.

```python
brownlow_data.brownlow_votes.mean()
    0.12347341475121326
```

So the average vote is 0.12. Let's see how this changes is the player is a captain. I have collected data on if players are captains from wikipedia and collated it into a csv. Let's load this in and create a "Is the player captain" feature, then check the average votes for captains.

### Create Is Player Captain Feature

```python
captains = pd.read_csv('data/captains.csv').set_index('player')

def is_captain_for_that_season(captains_df, player, year):
    
    if player in captains_df.index:
        # Get years they were captain
        seasons = captains_df.loc[player].season.split('-')
        if len(seasons) == 1:
            seasons_captain = list(map(int, seasons))
        elif len(seasons) == 2:
            if seasons[1] == '':
                seasons_captain = list(range(int(seasons[0]), 2019))
            else:
                seasons_captain = list(range(int(seasons[0]), int(seasons[1]) + 1))
        
        if year in seasons_captain:
            return 1
    return 0

brownlow_data['is_captain'] = brownlow_data.apply(lambda x: is_captain_for_that_season(captains, x.player, x.season), axis='columns')
```

```python
brownlow_data.query('is_captain == 1').groupby('season').brownlow_votes.mean()
print("Mean votes if a player is captain:", brownlow_data.query('is_captain == 1').brownlow_votes.mean())

    season
    2010    0.408497
    2011    0.429936
    2012    0.274194
    2013    0.438725
    2014    0.519663
    2015    0.447222
    2016    0.347826
    2017    0.425806
    2018    0.000000
    Name: brownlow_votes, dtype: float64

    Mean votes if a player is captain: 0.36661698956780925
```
    
This is significantly higher than if they aren't captain. What would be interesting is to look at the average difference in votes between when they were captain and when they weren't, to try and find if there is a 'captain bias' in brownlow votes. Go ahead and try. For now, we're going to move onto feature creation

---
# Feature Creation
Let's make a range of features, including:

- Ratios of each statistic per game
- If the player is a captain
- If they kicked a bag (4/5+)
- If they kicked 2 and had 30+ possies

First we will make features of ratios. What is important is not how many of a certain stat a player has, but how much of that stat a player has *relative* to everyone else in the same match. It doesn't matter if Dusty Martin has 31 possessions if Tom Mitchell has had 50 - Mitchell is probably more likely to poll (assuming all else is equal). So rather than using the actual number of possessions for example, we can divide these possessions by the total amount of possessions in the game. To do this we'll use pandas groupby and transform methods.

### Create Ratios As Features

```python
%%time

# Get a list of stats of which to create ratios for
ratio_cols = ['CP', 'UP', 'ED', 'DE', 'CM', 'GA', 'MI5', 'one_perc', 'BO', 'TOG', 
               'K', 'HB', 'D', 'M', 'G', 'B', 'T', 'HO', 'I50', 'CL', 'CG', 'R50', 
               'FF', 'FA', 'AF', 'SC']

# Create a ratios df
ratios = (brownlow_data.copy()
          .loc[:, ['match_id'] + ratio_cols]
          .groupby('match_id')
          .transform(lambda x: x / x.sum()))

feature_cols = ['date', 'season', 'round', 'venue', 'ID', 'match_id', 'player', 'jumper_no', 'team', 
                'opposition', 'status', 'team_score', 'opposition_score', 'margin', 'brownlow_votes']

# Create a features df - join the ratios to this df
features = (brownlow_data[feature_cols].copy()
               .join(ratios))

    Wall time: 11.3 s
```
    
```python
features.head()
```

|  | date | season | round | venue | ID | match_id | player | jumper_no | team | opposition | status | team_score | opposition_score | margin | brownlow_votes | CP | UP | ED | DE | CM | GA | MI5 | one_perc | BO | TOG | K | HB | D | M | G | B | T | HO | I50 | CL | CG | R50 | FF | FA | AF | SC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 2010-03-28 | 2010 | 1 | Domain Stadium | 11807 | 5096.0 | T Armstrong | 38 | Adelaide | Fremantle | Away | 62 | 118 | -56 | 0.0 | 0.013393 | 0.016304 | 0.015517 | 0.025529 | 0.0 | 0.0 | 0.00 | 0.013333 | 0.000000 | 0.020516 | 0.013441 | 0.014599 | 0.014049 | 0.022599 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.011494 | 0.000000 | 0.036145 | 0.018868 | 0.000000 | 0.037037 | 0.011568 | 0.005456 |
| 1 | 2010-03-28 | 2010 | 1 | Domain Stadium | 3968 | 5096.0 | N Bock | 44 | Adelaide | Fremantle | Away | 62 | 118 | -56 | 0.0 | 0.008929 | 0.025362 | 0.022414 | 0.023875 | 0.0 | 0.0 | 0.00 | 0.080000 | 0.000000 | 0.027169 | 0.032258 | 0.012165 | 0.021711 | 0.016949 | 0.038462 | 0.000000 | 0.026549 | 0.029851 | 0.022989 | 0.000000 | 0.024096 | 0.018868 | 0.037037 | 0.000000 | 0.024422 | 0.021825 |
| 2 | 2010-03-28 | 2010 | 1 | Domain Stadium | 11712 | 5096.0 | M Cook | 8 | Adelaide | Fremantle | Away | 62 | 118 | -56 | 0.0 | 0.035714 | 0.025362 | 0.031034 | 0.026746 | 0.0 | 0.0 | 0.00 | 0.013333 | 0.034483 | 0.021625 | 0.021505 | 0.031630 | 0.026820 | 0.022599 | 0.000000 | 0.045455 | 0.008850 | 0.014925 | 0.011494 | 0.028986 | 0.048193 | 0.056604 | 0.000000 | 0.037037 | 0.020887 | 0.019703 |
| 3 | 2010-03-28 | 2010 | 1 | Domain Stadium | 11700 | 5096.0 | P Dangerfield | 32 | Adelaide | Fremantle | Away | 62 | 118 | -56 | 0.0 | 0.049107 | 0.016304 | 0.017241 | 0.015605 | 0.0 | 0.0 | 0.04 | 0.026667 | 0.172414 | 0.022734 | 0.021505 | 0.029197 | 0.025543 | 0.016949 | 0.038462 | 0.090909 | 0.026549 | 0.000000 | 0.022989 | 0.072464 | 0.024096 | 0.018868 | 0.074074 | 0.037037 | 0.024422 | 0.028190 |
| 4 | 2010-03-28 | 2010 | 1 | Domain Stadium | 85 | 5096.0 | M Doughty | 11 | Adelaide | Fremantle | Away | 62 | 118 | -56 | 0.0 | 0.017857 | 0.021739 | 0.025862 | 0.027526 | 0.0 | 0.0 | 0.00 | 0.053333 | 0.000000 | 0.025229 | 0.010753 | 0.031630 | 0.021711 | 0.016949 | 0.000000 | 0.000000 | 0.026549 | 0.000000 | 0.011494 | 0.000000 | 0.036145 | 0.037736 | 0.000000 | 0.000000 | 0.018959 | 0.018490 |

### Kicked A Bag Feature

```python
features['kicked_a_bag'] = brownlow_data.G.apply(lambda x: 1 if x >= 5 else 0)
```

### Is Captain Feature

```python
features['is_captain'] = features.apply(lambda x: is_captain_for_that_season(captains, x.player, x.season), axis='columns')
```

### Won the Game Feature

```python
features['team_won'] = np.where(features.margin > 0, 1, 0)
```

### 30+ & 2+ Goals Feature

```python
features['got_30_possies_2_goals'] = np.where((brownlow_data.G >= 2) & (brownlow_data.D >= 30), 1, 0)
```
### Previous Top 10 Finish Feature
I have a strong feeling that past performance may be a predictor of future performance in the brownlow. For example, last year Dusty Martin won the Brownlow. The umpires may have a bias towards Dusty this year because he is known to be on their radar as being a good player. Let's create a feature which is categorical and is 1 if the player has previously finished in the top 10. Let's create a function for this and then apply it to the afltables dataset, which has data back to 1897. We will then create a lookup table for the top 10 for each season and merge this table with our current features df.

```python
afltables = pd.read_csv('data/afltables_stats.csv').query('Season >= 2000')

def replace_special_characters(name):
    name = name.replace("'", "").replace("-", " ").lower()
    name_split = name.split()
    
    if len(name_split) > 2:
        first_name = name_split[0]
        last_name = name_split[-1]
        name = first_name + ' ' + last_name
    
    name_split_2 = name.split()
    name = name_split_2[0][0] + ' ' + name_split_2[1]
    return name.title()

afltables = (afltables.assign(player=lambda df: df['First.name'] + ' ' + df.Surname)
                .assign(player=lambda df: df.player.apply(replace_special_characters))
                .rename(columns={'Brownlow.Votes': 'brownlow_votes', 'Season': 'season', 'Playing.for': 'team'}))
```

```python
### Create Top 10 rank look up table

brownlow_votes_yearly = (afltables.groupby(['season', 'player', 'team'], as_index=False)
                                  .brownlow_votes
                                  .sum())

brownlow_votes_yearly['yearly_rank'] = (brownlow_votes_yearly.groupby('season')
                                                             .brownlow_votes
                                                             .rank(method='max', ascending=False))

# Filter to only get a dataframe since 2000 and only the top 10 players from each season
brownlow_votes_top_10 = brownlow_votes_yearly.query('yearly_rank < 11 & season >= 2000')

brownlow_votes_top_10.head(3)

def how_many_times_top_10(top_10_df, player, year):
    times = len(top_10_df[(top_10_df.player == player) & (top_10_df.season < year)])
    return times

features['times_in_top_10'] = features.apply(lambda x: how_many_times_top_10(brownlow_votes_top_10, x.player, x.season), axis=1) 
```

|  | season | player | team | brownlow_votes | yearly_rank |
| --- | --- | --- | --- | --- | --- |
| 27 | 2000.0 | A Koutoufides | Carlton | 19.0 | 4.0 |
| 36 | 2000.0 | A Mcleod | Adelaide | 20.0 | 3.0 |
| 105 | 2000.0 | B Ratten | Carlton | 18.0 | 6.0 |

### Average Brownlow Votes Per Game Last Season Feature

```python
# Create a brownlow votes lookup table
brownlow_votes_lookup_table = (brownlow_data.groupby(['player', 'team', 'season'], as_index=False)
                                    .brownlow_votes
                                    .mean()
                                    .assign(next_season=lambda df: df.season + 1)
                                    .rename(columns={
                                        'brownlow_votes': 'ave_votes_last_season'
                                    }))

# Have a look at Cripps to check if it's working
brownlow_votes_lookup_table[brownlow_votes_lookup_table.player == 'P Cripps']

# Merge it to our features df
features_with_votes_last_season = (pd.merge(features, brownlow_votes_lookup_table.drop(columns='season'),
                                            
                                             left_on=['player', 'team', 'season'], 
                                             right_on=['player', 'team', 'next_season'],
                                             how='left')
                                  .drop(columns=['next_season'])
                                  .fillna(0))
```

|  | player | team | season | ave_votes_last_season | next_season |
| --- | --- | --- | --- | --- | --- |
| 4377 | P Cripps | Carlton | 2014 | 0.000000 | 2015 |
| 4378 | P Cripps | Carlton | 2015 | 0.300000 | 2016 |
| 4379 | P Cripps | Carlton | 2016 | 0.857143 | 2017 |
| 4380 | P Cripps | Carlton | 2017 | 0.333333 | 2018 |
| 4381 | P Cripps | Carlton | 2018 | 0.000000 | 2019 |

### Historic Performance Relative To Model Feature
It is well known that some players are good Brownlow performers. For whatever reason, they always poll much better than their stats may suggest. Lance Franklin and Bontempelli are probably in this category. Perhaps these players have an X-factor that Machine Learning models struggle to pick up on. To get around this, let's create a feature which looks at the player's performance relative to the model's prediction. To do this, we'll need to train and predict 7 different models - from 2011 to 2017.

To create a model for each season, we will use h2o's AutoML. If you're new to h2o, please read about it [here.](http://docs.h2o.ai/h2o/latest-stable/h2o-docs/automl.html) It can be used in both R and Python.

The metric we will use for loss in Mean Absolute Error (MAE).

As we are using regression, some values are negative. We will convert these negative values to 0 as it doesn't make sense to poll negative brownlow votes. Similarly, some matches won't predict exactly 6 votes, so we will scale these predictions so that we predict exactly 6 votes for each match.

So that you don't have to train these models yourself, I have saved the models and we will load them in. If you are keen to train the models yourself, simply uncomment out the code below and run the cell. To bulk uncomment, highlight the rows and press ctrl + '/'

```python
h2o.init()

# Uncomment the code below if you want to train the models yourself - otherwise, we will load them in the load cell from disk

## Join to our features df

# aml_yearly_model_objects = {}
# yearly_predictions_dfs = {}

# feature_cols = ['margin', 'CP', 'UP', 'ED', 'DE',
#        'CM', 'GA', 'MI5', 'one_perc', 'BO', 'TOG', 'K', 'HB', 'D', 'M', 'G',
#        'B', 'T', 'HO', 'I50', 'CL', 'CG', 'R50', 'FF', 'FA', 'AF', 'SC']

# for year in range(2011, 2018):
#     # Filter the data to only include past data
#     train_historic = brownlow_data[brownlow_data.season < year].copy()
    
#     # Convert to an h2o frame
#     train_h2o_historic = h2o.H2OFrame(train_historic)
    
#     # Create an AutoML object
#     aml = H2OAutoML(max_runtime_secs=30,
#                    balance_classes=True,
#                    seed=42)
    
#     # Train the model
#     aml.train(y='brownlow_votes', x=feature_cols, training_frame=train_h2o_historic)
    
#     # save the model
#     model_path = h2o.save_model(model=aml.leader, path="models", force=True)
    
#     # Get model id
#     model_name = aml.leaderboard[0, 'model_id']
    
#     # Rename the model on disk
#     os.rename(f'models/{model_name}', f'models/yearly_model_{year}')
    
#     # Append the best model to a list
#     aml_yearly_model_objects[year] = aml.leader
    
#     # Make predictions on test set for that year
#     test_historic = brownlow_data[brownlow_data.season == year].copy()
#     test_h2o_historic = h2o.H2OFrame(test_historic)

#     preds = aml.predict(test_h2o_historic).as_data_frame()
#     test_historic['predicted_votes'] = preds.values
    
#     # Convert negative predictions to 0
#     test_historic['predicted_votes_neg_to_0'] = test_historic.predicted_votes.apply(lambda x: 0 if x < 0 else x)
    
#     # Create a total match votes column - which calculates the number of votes predicted in each game when the predictions 
#     # are unscaled
#     test_historic['unscaled_match_votes'] = test_historic.groupby('match_id').predicted_votes_neg_to_0.transform('sum')
    
#     # Scale predictions
#     test_historic['predicted_votes_scaled'] = test_historic.predicted_votes_neg_to_0 / test_historic.unscaled_match_votes * 6
    
#     # Aggregate the predictions
#     test_grouped = (test_historic.groupby(['player', 'team'], as_index=False)
#                                  .sum()
#                                  .sort_values(by='brownlow_votes', ascending=False)
#                                  .assign(mae=lambda df: abs(df.predicted_votes_scaled - df.brownlow_votes)))
    
#     test_grouped['error'] = test_grouped.predicted_votes_scaled - test_grouped.brownlow_votes
#     test_grouped['next_year'] = year + 1
    
#     # Add this years predictions df to a dictionary to use later
#     yearly_predictions_dfs[year] = test_grouped

# preds_errors = None

# for key, value in yearly_predictions_dfs.items():
#     if preds_errors is None:
#         preds_errors = value[['player', 'season', 'next_year', 'brownlow_votes', 'predicted_votes_scaled', 'error']]
#     else:
#         preds_errors = preds_errors.append(value[['player', 'season', 'next_year', 'brownlow_votes', 'predicted_votes_scaled', 'error']], sort=True)
        
# with open('data/prediction_errors_df.pickle', 'wb') as handle:
#     pickle.dump(yearly_predicted_errors, handle)
```

Checking whether there is an H2O instance running at http://localhost:54321. connected.   

| H2O cluster uptime: | 1 hour 28 mins |
| --- | --- |
| H2O cluster timezone: | Australia/Hobart |
| H2O data parsing timezone: | UTC |
| H2O cluster version: | 3.20.0.4 |
| H2O cluster version age: | 1 month and 18 days  |
| H2O cluster name: | H2O_from_python_WardJ_tt2ak5 |
| H2O cluster total nodes: | 1 |
| H2O cluster free memory: | 7.018 Gb |
| H2O cluster total cores: | 4 |
| H2O cluster allowed cores: | 4 |
| H2O cluster status: | locked, healthy |
| H2O connection url: | http://localhost:54321 |
| H2O connection proxy: | None |
| H2O internal security: | False |
| H2O API Extensions: | Algos, AutoML, Core V3, Core V4 |
| Python version: | 3.6.4 final |

```python
# Load predictions error df    
with open('data/prediction_errors_df.pickle', 'rb') as handle:
    preds_errors = pickle.load(handle)

# Look at last years predictions
preds_errors.query('next_year == 2018').sort_values(by='brownlow_votes', ascending=False).head(20)
```

|  | brownlow_votes | error | next_year | player | predicted_votes_scaled | season |
| --- | --- | --- | --- | --- | --- | --- |
| 139 | 36.0 | -4.915157 | 2018 | D Martin | 31.084843 | 44374 |
| 486 | 33.0 | -4.413780 | 2018 | P Dangerfield | 28.586220 | 42357 |
| 619 | 25.0 | 0.072223 | 2018 | T Mitchell | 25.072223 | 44374 |
| 279 | 23.0 | -9.296209 | 2018 | J Kennedy | 13.703791 | 38323 |
| 376 | 22.0 | -7.621336 | 2018 | L Franklin | 14.378664 | 44374 |
| 278 | 21.0 | -3.016176 | 2018 | J Kelly | 17.983824 | 42357 |
| 519 | 20.0 | -4.182915 | 2018 | R Sloane | 15.817085 | 44374 |
| 410 | 19.0 | -7.740142 | 2018 | M Bontempelli | 11.259858 | 44374 |
| 483 | 18.0 | -4.522835 | 2018 | O Wines | 13.477165 | 44374 |
| 121 | 17.0 | -4.446749 | 2018 | D Beams | 12.553251 | 38323 |
| 390 | 16.0 | -3.620094 | 2018 | L Parker | 12.379906 | 44374 |
| 561 | 15.0 | -5.846506 | 2018 | S Pendlebury | 9.153494 | 32272 |
| 463 | 15.0 | -4.402600 | 2018 | N Fyfe | 10.597400 | 42357 |
| 42 | 15.0 | -4.787914 | 2018 | B Ebert | 10.212086 | 44374 |
| 651 | 15.0 | 0.824510 | 2018 | Z Merrett | 15.824510 | 42357 |
| 578 | 14.0 | 2.300607 | 2018 | T Adams | 16.300607 | 44374 |
| 34 | 14.0 | -5.796604 | 2018 | B Brown | 8.203396 | 44374 |
| 172 | 14.0 | -1.650752 | 2018 | D Zorko | 12.349248 | 42357 |
| 184 | 14.0 | -1.233663 | 2018 | G Ablett | 12.766337 | 28238 |
| 389 | 14.0 | -2.099613 | 2018 | L Neale | 11.900387 | 42357 |

Look at that! A simply Machine Learning ensemble model, using AutoML predicted last year's winner! That's impressive. As we can see it also predicted Bontempelli would only score 11.26, when he actually scored 19 - a huge discrepency. Let's use this as a feature.

```python
features_with_historic_perf_relative_to_model = \
    (features_with_votes_last_season.pipe(pd.merge, preds_errors[['player', 'next_year', 'error']],
                                          left_on=['player', 'season'],
                                          right_on=['player', 'next_year'],
                                          how='left')
                                     .fillna(0)
                                     .rename(columns={'error': 'error_last_season'})
                                     .drop_duplicates(subset=['player', 'round', 'SC']))
```

---
## Filtering the data to only include the top 20 SC for each match
Logically, it is extremely unlikely that a player will poll votes if their Supercoach score is not in the top 20 players. By eliminating the other 20+ players, we can reduce the noise in the data, as we are almost certain the players won't poll from the bottom half. Let's explore how many players poll if they're not in the top 20, and then filter our df if this number is not significant.

```python
# Find number of players who vote when in top 15 SC

brownlow_data['SC_rank_match'] = brownlow_data.groupby('match_id').SC.rank(method='max', ascending=False)

brownlow_data.query('SC_rank_match > 20 and season > 2014').brownlow_votes.value_counts()

    0.0    18330
    1.0       14
    2.0        8
    3.0        2
    Name: brownlow_votes, dtype: int64
```

Since 2014, there have only been 24 players who have voted and not been in the top 20 SC.

```python
features_with_sc_rank = features_with_historic_perf_relative_to_model.copy()

features_with_sc_rank['SC_rank_match'] = features_with_sc_rank.groupby('match_id').SC.rank(method='max', ascending=False)

# Filter out rows with a SC rank of below 20
features_with_sc_rank_filtered = features_with_sc_rank.query('SC_rank_match <= 20')
```

```python
# Filter out 2010 and 2011 as we used these seasons to create historic model performance features
features_last_before_train = features_with_sc_rank_filtered.query('season != 2010 and season != 2011').reset_index(drop=True)

features_last_before_train.head(3)
```

|  | date | season | round | venue | ID | match_id | player | jumper_no | team | opposition | status | team_score | opposition_score | margin | brownlow_votes | CP | UP | ED | DE | CM | GA | MI5 | one_perc | BO | TOG | K | HB | D | M | G | B | T | HO | I50 | CL | CG | R50 | FF | FA | AF | SC | kicked_a_bag | is_captain | team_won | got_30_possies_2_goals | times_in_top_10 | ave_votes_last_season | next_year | error_last_season | SC_rank_match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 2012-03-31 | 2012 | 1 | Metricon Stadium | 11985 | 5347.0 | I Callinan | 37 | Adelaide | Gold Coast | Away | 137 | 68 | 69 | 0.0 | 0.031359 | 0.018947 | 0.016071 | 0.015745 | 0.0 | 0.000000 | 0.12 | 0.000000 | 0.000000 | 0.023333 | 0.031674 | 0.012270 | 0.023438 | 0.026042 | 0.068966 | 0.217391 | 0.041322 | 0.0 | 0.017241 | 0.013699 | 0.042553 | 0.000000 | 0.000000 | 0.032258 | 0.030593 | 0.026962 | 0 | 0 | 1 | 0 | 0 | 0.000000 | 2012.0 | 0.042048 | 14.0 |
| 1 | 2012-03-31 | 2012 | 1 | Metricon Stadium | 11700 | 5347.0 | P Dangerfield | 32 | Adelaide | Gold Coast | Away | 137 | 68 | 69 | 0.0 | 0.048780 | 0.023158 | 0.037500 | 0.026451 | 0.0 | 0.000000 | 0.04 | 0.009804 | 0.090909 | 0.025556 | 0.029412 | 0.036810 | 0.032552 | 0.015625 | 0.068966 | 0.000000 | 0.016529 | 0.0 | 0.051724 | 0.123288 | 0.042553 | 0.000000 | 0.000000 | 0.032258 | 0.027503 | 0.028173 | 0 | 0 | 1 | 0 | 0 | 0.333333 | 2012.0 | -2.983636 | 12.0 |
| 2 | 2012-03-31 | 2012 | 1 | Metricon Stadium | 2381 | 5347.0 | R Douglas | 26 | Adelaide | Gold Coast | Away | 137 | 68 | 69 | 0.0 | 0.020906 | 0.033684 | 0.021429 | 0.019901 | 0.0 | 0.083333 | 0.04 | 0.049020 | 0.000000 | 0.023056 | 0.031674 | 0.015337 | 0.024740 | 0.031250 | 0.034483 | 0.130435 | 0.057851 | 0.0 | 0.043103 | 0.000000 | 0.031915 | 0.014493 | 0.064516 | 0.000000 | 0.033684 | 0.030597 | 0 | 0 | 1 | 0 | 0 | 0.000000 | 2012.0 | 1.724915 | 10.0 |

---
## Modeling The 2017 Brownlow

Now that we have all of our features, we can simply create a training set (2012-2016), and a test set (2017), and make our predictions for last year! We will use AutoML for this process again. Again, rather than waiting for the model to train, I will save the model so you can simply load it in. We will also scale our features. We can then see how our model went in predicting last year's brownlow, creating a baseline for this years' predictions. We will then predict this year's vote count.

```python
train_baseline = features_last_before_train.query("season < 2017")
holdout = features_last_before_train.query("season == 2017")

scale_cols = ['team_score', 'opposition_score', 'margin', 'CP', 'UP', 'ED', 'DE',
       'CM', 'GA', 'MI5', 'one_perc', 'BO', 'K', 'HB', 'D', 'M', 'G',
       'B', 'T', 'HO', 'I50', 'CL', 'CG', 'R50', 'FF', 'FA', 'AF', 'SC']

other_feature_cols = ['is_captain', 'kicked_a_bag', 'team_won', 'got_30_possies_2_goals', 'times_in_top_10', 
                      'ave_votes_last_season', 'error_last_season', 'SC_rank_match']

all_feature_cols = scale_cols + other_feature_cols

# Scale features
scaler = StandardScaler()

train_baseline_scaled = train_baseline.copy()
train_baseline_scaled[scale_cols] = scaler.fit_transform(train_baseline[scale_cols])

holdout_scaled = holdout.copy()
holdout_scaled[scale_cols] = scaler.transform(holdout[scale_cols])

# Convert categorical columns to categoricals
train_baseline_h2o = h2o.H2OFrame(train_baseline_scaled)
holdout_h2o = h2o.H2OFrame(holdout_scaled)

for col in ['is_captain', 'kicked_a_bag', 'team_won', 'got_30_possies_2_goals']:
    train_baseline_h2o[col] = train_baseline_h2o[col].asfactor()
    holdout_h2o[col] = holdout_h2o[col].asfactor()
```

    C:\Users\wardj\AppData\Local\Continuum\anaconda3\lib\site-packages\h2o\utils\shared_utils.py:177: FutureWarning: Method .as_matrix will be removed in a future version. Use .values instead.
      data = _handle_python_lists(python_obj.as_matrix().tolist(), -1)[1]

    Parse progress: |█████████████████████████████████████████████████████████| 100%
    Parse progress: |█████████████████████████████████████████████████████████| 100%
    
Below I have commented out training and saving the 2017 model. Rather than training it again, we will just load it in. Uncomment this part out if you want to train it yourself.

```python
# aml_2017_model = H2OAutoML(max_runtime_secs = 60*3,
#                    balance_classes=True,
#                    seed=42)

# aml_2017_model.train(y='brownlow_votes', x=all_feature_cols, training_frame=train_baseline_h2o)
```

```python
# save the model
# model_path = h2o.save_model(model=aml_2017_model.leader, path="models", force=True)

# Get model id
# model_name = aml_2017_model.leaderboard[0, 'model_id']

# Rename the model on disk
# os.rename(f'models/{model_name}', f'models/brownlow_2017_model_v1')

# Load model in
aml_2017_model = h2o.load_model('models/brownlow_2017_model_v1')
```

```python
# Predict the 2017 brownlow count
preds_final_2017_model = aml_2017_model.predict(holdout_h2o)

# Scale these predictions - change negatives to 0s and scale so each game predicts 6 votes total
holdout = (holdout.assign(predicted_votes=preds_final_2017_model.as_data_frame().values)
                  .assign(predicted_votes_neg_to_0=lambda df: df.predicted_votes.apply(lambda x: 0 if x <0 else x))
                  .assign(unscaled_match_votes=lambda df: df.groupby('match_id').predicted_votes_neg_to_0.transform('sum'))
                  .assign(predicted_votes_scaled=lambda df: df.predicted_votes_neg_to_0 / df.unscaled_match_votes * 6))

# Create an aggregate votes df and show the average SC points and goals scored
agg_predictions_2017 = (holdout.groupby(['player', 'team'], as_index=False)
                        .agg({
                            'brownlow_votes': sum,
                            'predicted_votes_scaled': sum,
                            'SC': 'mean',
                            'G': 'mean'})
                        .sort_values(by='brownlow_votes', ascending=False)
                        .assign(mae=lambda df: abs(df.brownlow_votes - df.predicted_votes_scaled))
                        .reset_index(drop=True))
```
    stackedensemble prediction progress: |████████████████████████████████████| 100%

```python
agg_predictions_2017.head(15)
```

|  | player | team | brownlow_votes | predicted_votes_scaled | SC | G | mae |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | D Martin | Richmond | 36.0 | 37.271060 | 0.037862 | 0.064869 | 1.271060 |
| 1 | P Dangerfield | Geelong | 33.0 | 39.288122 | 0.042441 | 0.070819 | 6.288122 |
| 2 | T Mitchell | Hawthorn | 25.0 | 28.629859 | 0.036040 | 0.016928 | 3.629859 |
| 3 | L Franklin | Sydney | 22.0 | 16.353733 | 0.034640 | 0.149203 | 5.646267 |
| 4 | J Kelly | GWS | 21.0 | 19.565321 | 0.034652 | 0.033772 | 1.434679 |
| 5 | R Sloane | Adelaide | 20.0 | 21.417347 | 0.037068 | 0.034821 | 1.417347 |
| 6 | J Kennedy | Sydney | 20.0 | 13.671891 | 0.032014 | 0.030508 | 6.328109 |
| 7 | M Bontempelli | Western Bulldogs | 19.0 | 17.461889 | 0.033233 | 0.040498 | 1.538111 |
| 8 | D Beams | Brisbane | 17.0 | 15.414730 | 0.034848 | 0.044998 | 1.585270 |
| 9 | O Wines | Port Adelaide | 16.0 | 12.973973 | 0.031601 | 0.021967 | 3.026027 |
| 10 | N Fyfe | Fremantle | 15.0 | 11.926030 | 0.033761 | 0.031680 | 3.073970 |
| 11 | S Pendlebury | Collingwood | 15.0 | 10.845214 | 0.033855 | 0.013660 | 4.154786 |
| 12 | B Ebert | Port Adelaide | 15.0 | 7.633526 | 0.032795 | 0.008431 | 7.366474 |
| 13 | L Parker | Sydney | 15.0 | 14.680079 | 0.031366 | 0.030311 | 0.319921 |
| 14 | Z Merrett | Essendon | 15.0 | 21.063889 | 0.033737 | 0.015362 | 6.063889 |

So whilst our model predicted Dangerfield to win, it was pretty damn accurate! Let's find the MAE for the top 100, 50, 25, and 10, and then compare it to 2018's MAE in week, when the Brownlow has been counted.

```python
for top_x in [10, 25, 50, 100]:
    temp_mae = round(agg_predictions_2017.iloc[:top_x].mae.mean(), 3)
    print(f"The Average Mean Absolute Error for the top {top_x} is {temp_mae}")
```
    The Average Mean Absolute Error for the top 10 is 3.216
    The Average Mean Absolute Error for the top 25 is 2.931
    The Average Mean Absolute Error for the top 50 is 3.15
    The Average Mean Absolute Error for the top 100 is 2.577

---  
## Modelling This Year's Brownlow
Let's now predict this year's vote count. These predictions will be on the front page of the GitHub.

```python
train = features_last_before_train.query("season < 2018")
test = features_last_before_train.query("season == 2018")

# Scale features
scaler = StandardScaler()

train_scaled = train.copy()
train_scaled[scale_cols] = scaler.fit_transform(train[scale_cols])

test_scaled = test.copy()
test_scaled[scale_cols] = scaler.transform(test[scale_cols])
```

```python
# Convert categorical columns to categoricals

train_h2o = h2o.H2OFrame(train_scaled)
test_h2o = h2o.H2OFrame(test_scaled)

for col in ['is_captain', 'kicked_a_bag', 'team_won', 'got_30_possies_2_goals']:
    train_h2o[col] = train_h2o[col].asfactor()
    test_h2o[col] = test_h2o[col].asfactor()
```

    C:\Users\wardj\AppData\Local\Continuum\anaconda3\lib\site-packages\h2o\utils\shared_utils.py:177: FutureWarning: Method .as_matrix will be removed in a future version. Use .values instead.
      data = _handle_python_lists(python_obj.as_matrix().tolist(), -1)[1]
    
    Parse progress: |█████████████████████████████████████████████████████████| 100%
    Parse progress: |█████████████████████████████████████████████████████████| 100%

```python
# Train the model - this part is commented out as we will just load our model from disk

# aml = H2OAutoML(max_runtime_secs = 60*3,
#                    balance_classes=True,
#                    seed=42)

# aml.train(y='brownlow_votes', x=all_feature_cols, training_frame=train_h2o)
```

```python
# # save the model
# model_path = h2o.save_model(model=aml.leader, path="models", force=True)

# # Get model id
# model_name = aml.leaderboard[0, 'model_id']

# # Rename the model on disk
# os.rename(f'models/{model_name}', f'models/brownlow_2018_model_v1')

# Load model in
aml = h2o.load_model('models/brownlow_2018_model_v1')
```

```python
# Predict the 2018 brownlow count
preds_final_2018_model = aml.predict(test_h2o)

# Scale these predictions - change negatives to 0s and scale so each game predicts 6 votes total
test = (test.assign(predicted_votes=preds_final_2018_model.as_data_frame().values)
                  .assign(predicted_votes_neg_to_0=lambda df: df.predicted_votes.apply(lambda x: 0 if x <0 else x))
                  .assign(unscaled_match_votes=lambda df: df.groupby('match_id').predicted_votes_neg_to_0.transform('sum'))
                  .assign(predicted_votes_scaled=lambda df: df.predicted_votes_neg_to_0 / df.unscaled_match_votes * 6))

# Create an aggregate votes df and show the average SC points and goals scored
agg_predictions_2018 = (test.groupby(['player', 'team'], as_index=False)
                        .agg({
                            'predicted_votes_scaled': sum,
                            'match_id': 'count'}) # shows how many games they played
                        .sort_values(by='predicted_votes_scaled', ascending=False)
                        .reset_index(drop=True))
```

    stackedensemble prediction progress: |████████████████████████████████████| 100%
    
```python
# Show the top 25 predictions

agg_predictions_2018.head(25)
```

|  | player | team | predicted_votes_scaled | match_id |
| --- | --- | --- | --- | --- |
| 0 | T Mitchell | Hawthorn | 35.484614 | 20 |
| 1 | M Gawn | Melbourne | 21.544278 | 22 |
| 2 | D Martin | Richmond | 20.444488 | 19 |
| 3 | B Grundy | Collingwood | 19.543511 | 22 |
| 4 | C Oliver | Melbourne | 19.009628 | 20 |
| 5 | J Macrae | Western Bulldogs | 18.931594 | 17 |
| 6 | P Dangerfield | Geelong | 18.621242 | 21 |
| 7 | D Beams | Brisbane | 17.621222 | 15 |
| 8 | E Yeo | West Coast | 16.015638 | 20 |
| 9 | L Neale | Fremantle | 15.495083 | 21 |
| 10 | A Gaff | West Coast | 15.165629 | 18 |
| 11 | D Heppell | Essendon | 15.083797 | 19 |
| 12 | J Selwood | Geelong | 14.989096 | 18 |
| 13 | S Sidebottom | Collingwood | 14.863136 | 18 |
| 14 | N Fyfe | Fremantle | 14.692243 | 11 |
| 15 | J Kennedy | Sydney | 14.404489 | 16 |
| 16 | Z Merrett | Essendon | 13.632131 | 18 |
| 17 | M Crouch | Adelaide | 13.503858 | 16 |
| 18 | R Laird | Adelaide | 13.274869 | 19 |
| 19 | P Cripps | Carlton | 13.240568 | 21 |
| 20 | G Ablett | Geelong | 13.018950 | 15 |
| 21 | L Franklin | Sydney | 12.792476 | 13 |
| 22 | J Lloyd | Sydney | 12.174224 | 20 |
| 23 | J Kelly | GWS | 11.982157 | 14 |
| 24 | C Ward | GWS | 11.892443 | 19 |

```python
print(agg_predictions_2018.head(15))
```

player|team|predicted\_votes\_scaled|match\_id
-----|-----|-----|-----
0|T Mitchell|Hawthorn|35.484614
1|M Gawn|Melbourne|21.544278
2|D Martin|Richmond|20.444488
3|B Grundy|Collingwood|19.543511
4|C Oliver|Melbourne|19.009628
5|J Macrae|Western Bulldogs|18.931594
6|P Dangerfield|Geelong|18.621242
7|D Beams|Brisbane|17.621222
8|E Yeo|West Coast|16.015638
9|L Neale|Fremantle|15.495083
10|A Gaff|West Coast|15.165629
11|D Heppell|Essendon|15.083797
12|J Selwood|Geelong|14.989096
13|S Sidebottom|Collingwood|14.863136
14|N Fyfe|Fremantle|14.692243
    
Now that we have the top 25, let's also look at the top 3 from each team.

```python
agg_predictions_2018.sort_values(by=['team', 'predicted_votes_scaled'], ascending=[True, False]).groupby('team').head(3)
```

|  | player | team | predicted_votes_scaled | match_id |
| --- | --- | --- | --- | --- |
| 17 | M Crouch | Adelaide | 13.503858 | 16 |
| 18 | R Laird | Adelaide | 13.274869 | 19 |
| 51 | B Gibbs | Adelaide | 7.783425 | 18 |
| 7 | D Beams | Brisbane | 17.621222 | 15 |
| 46 | D Zorko | Brisbane | 8.123915 | 14 |
| 55 | S Martin | Brisbane | 7.243428 | 19 |
| 19 | P Cripps | Carlton | 13.240568 | 21 |
| 50 | K Simpson | Carlton | 7.864995 | 18 |
| 88 | E Curnow | Carlton | 3.725292 | 19 |
| 3 | B Grundy | Collingwood | 19.543511 | 22 |
| 13 | S Sidebottom | Collingwood | 14.863136 | 18 |
| 31 | A Treloar | Collingwood | 10.487535 | 11 |
| 11 | D Heppell | Essendon | 15.083797 | 19 |
| 16 | Z Merrett | Essendon | 13.632131 | 18 |
| 57 | D Smith | Essendon | 6.838857 | 20 |
| 9 | L Neale | Fremantle | 15.495083 | 21 |
| 14 | N Fyfe | Fremantle | 14.692243 | 11 |
| 74 | M Walters | Fremantle | 5.120949 | 12 |
| 23 | J Kelly | GWS | 11.982157 | 14 |
| 24 | C Ward | GWS | 11.892443 | 19 |
| 25 | S Coniglio | GWS | 11.785273 | 20 |
| 6 | P Dangerfield | Geelong | 18.621242 | 21 |
| 12 | J Selwood | Geelong | 14.989096 | 18 |
| 20 | G Ablett | Geelong | 13.018950 | 15 |
| 80 | J Witts | Gold Coast | 4.617273 | 13 |
| 85 | J Lyons | Gold Coast | 4.043711 | 14 |
| 114 | B Fiorini | Gold Coast | 2.798683 | 6 |
| 0 | T Mitchell | Hawthorn | 35.484614 | 20 |
| 39 | L Breust | Hawthorn | 9.286521 | 16 |
| 45 | J Gunston | Hawthorn | 8.341824 | 19 |
| 1 | M Gawn | Melbourne | 21.544278 | 22 |
| 4 | C Oliver | Melbourne | 19.009628 | 20 |
| 32 | J Hogan | Melbourne | 10.198873 | 13 |
| 26 | S Higgins | North Melbourne | 11.327596 | 19 |
| 37 | B Brown | North Melbourne | 9.550205 | 13 |
| 42 | B Cunnington | North Melbourne | 8.857294 | 17 |
| 27 | O Wines | Port Adelaide | 11.118795 | 16 |
| 36 | R Gray | Port Adelaide | 9.606960 | 17 |
| 54 | J Westhoff | Port Adelaide | 7.355449 | 21 |
| 2 | D Martin | Richmond | 20.444488 | 19 |
| 30 | J Riewoldt | Richmond | 10.557749 | 15 |
| 59 | T Cotchin | Richmond | 6.741732 | 12 |
| 41 | S Ross | St Kilda | 9.093395 | 17 |
| 48 | J Steven | St Kilda | 8.099164 | 17 |
| 90 | J Steele | St Kilda | 3.617769 | 16 |
| 15 | J Kennedy | Sydney | 14.404489 | 16 |
| 21 | L Franklin | Sydney | 12.792476 | 13 |
| 22 | J Lloyd | Sydney | 12.174224 | 20 |
| 8 | E Yeo | West Coast | 16.015638 | 20 |
| 10 | A Gaff | West Coast | 15.165629 | 18 |
| 38 | J Redden | West Coast | 9.368163 | 16 |
| 5 | J Macrae | Western Bulldogs | 18.931594 | 17 |
| 40 | M Bontempelli | Western Bulldogs | 9.272771 | 16 |
| 44 | L Hunter | Western Bulldogs | 8.349606 | 17 |

If you're looking for a round by round breakdown, just have a look at the test dataframe.

```python
test[['date', 'round', 'player', 'team', 'opposition', 'margin', 'SC', 'predicted_votes_scaled']].tail(25)
```

|  | date | round | player | team | opposition | margin | SC | predicted_votes_scaled |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 27231 | 2018-08-26 | 23 | R Lobb | GWS | Melbourne | -45 | 0.027576 | 0.007501 |
| 27232 | 2018-08-26 | 23 | H Perryman | GWS | Melbourne | -45 | 0.025758 | 0.000000 |
| 27233 | 2018-08-26 | 23 | D Shiel | GWS | Melbourne | -45 | 0.026364 | 0.000000 |
| 27234 | 2018-08-26 | 23 | A Tomlinson | GWS | Melbourne | -45 | 0.026667 | 0.000000 |
| 27235 | 2018-08-26 | 23 | C Ward | GWS | Melbourne | -45 | 0.035455 | 0.332057 |
| 27236 | 2018-08-26 | 23 | L Austin | St Kilda | North Melbourne | -23 | 0.027853 | 0.003928 |
| 27237 | 2018-08-26 | 23 | J Geary | St Kilda | North Melbourne | -23 | 0.025129 | 0.000000 |
| 27238 | 2018-08-26 | 23 | S Gilbert | St Kilda | North Melbourne | -23 | 0.025734 | 0.000000 |
| 27239 | 2018-08-26 | 23 | R Marshall | St Kilda | North Melbourne | -23 | 0.028156 | 0.103389 |
| 27240 | 2018-08-26 | 23 | B Paton | St Kilda | North Melbourne | -23 | 0.023918 | 0.000000 |
| 27241 | 2018-08-26 | 23 | S Ross | St Kilda | North Melbourne | -23 | 0.039055 | 0.300392 |
| 27242 | 2018-08-26 | 23 | J Steele | St Kilda | North Melbourne | -23 | 0.042386 | 1.094723 |
| 27243 | 2018-08-26 | 23 | J Steven | St Kilda | North Melbourne | -23 | 0.046624 | 1.119684 |
| 27244 | 2018-08-26 | 23 | R Clarke | North Melbourne | St Kilda | 23 | 0.021193 | 0.050859 |
| 27245 | 2018-08-26 | 23 | B Cunnington | North Melbourne | St Kilda | 23 | 0.032698 | 0.212364 |
| 27246 | 2018-08-26 | 23 | M Daw | North Melbourne | St Kilda | 23 | 0.022404 | 0.021889 |
| 27247 | 2018-08-26 | 23 | T Dumont | North Melbourne | St Kilda | 23 | 0.049046 | 2.042550 |
| 27248 | 2018-08-26 | 23 | T Goldstein | North Melbourne | St Kilda | 23 | 0.037844 | 0.347199 |
| 27249 | 2018-08-26 | 23 | S Higgins | North Melbourne | St Kilda | 23 | 0.039358 | 0.508419 |
| 27250 | 2018-08-26 | 23 | N Hrovat | North Melbourne | St Kilda | 23 | 0.025129 | 0.012548 |
| 27251 | 2018-08-26 | 23 | J Macmillan | North Melbourne | St Kilda | 23 | 0.024220 | 0.000000 |
| 27252 | 2018-08-26 | 23 | J Waite | North Melbourne | St Kilda | 23 | 0.025734 | 0.057826 |
| 27253 | 2018-08-26 | 23 | M Williams | North Melbourne | St Kilda | 23 | 0.023312 | 0.000000 |
| 27254 | 2018-08-26 | 23 | S Wright | North Melbourne | St Kilda | 23 | 0.029064 | 0.093219 |
| 27255 | 2018-08-26 | 23 | J Ziebell | North Melbourne | St Kilda | 23 | 0.033000 | 0.031010 |

And there we have it! In a single notebook we have made a fairly good Brownlow predictive model. Enjoy.

---
### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.