# How to model Soccer: Python Tutorial

## The Task

This notebook will outline how to train a classification model to predict the outcome of a soccer match using a dataset provided by https://www.football-data.co.uk/

1. Reading data from file and get a raw dataset
2. Data cleaning and feature engineering
3. Training a model
4. The tutorial covers the thought process of manipulating the dataset (why and how), some simple data cleaning, feature engineering and training a classification model.

The tutorial **DOES NOT** delve deep into the fundamentals of machine learning, advanced feature engineering or model tuning.

*There are some helpful hints along the way though.*


``` python
# import required libraries

import numpy as np
import pandas as pd
import os

import warnings
warnings.filterwarnings('ignore')
```

---
## Read data from file and get a raw dataset

#### Change the data types - date column.

We need the date column in good order for our tutorial. [Here's the data set](assets/soccerData.csv) we're using for this tutorial.

*In general, it's a good idea to evaluate data types of all columns that we work with to ensure they are correct.*

``` Python
df = pd.read_csv('soccerData.csv')
```

``` Python
df['date']= pd.to_datetime(df['date'])
```

#### Get data columns and create raw dataset

For this tutorial, let's take only a few stats columns to work with.

*Typically we would explore all features and then decide which data to discard.*

1. Goal counts
2. Half Time Goal Counts
3. Corners
4. Total shots
5. Shots on target
6. Fouls
7. Yellow Cards
8. Red Cards

``` Python
raw_match_stats = df[[
                'date',
                'match_id',
                'home_team_name',
                'away_team_name',
                'home_team_goal_count', 
                'away_team_goal_count',
                'home_team_half_time_goal_count',
                'away_team_half_time_goal_count',
                'home_team_shots',
                'away_team_shots',
                'home_team_shots_on_target',
                'away_team_shots_on_target',
                'home_team_fouls',
                'away_team_fouls',
                'home_team_corner_count',
                'away_team_corner_count',
                'home_team_yellow',
                'away_team_yellow',
                'home_team_red',
                'away_team_red'
                ]]
```

#### Clean data

As a cleaning step, we order our data by date and drop rows with NA values.

``` Python
raw_match_stats = raw_match_stats.sort_values(by=['date'], ascending=False)

raw_match_stats = raw_match_stats.dropna(inplace=True)
```

### Raw dataset

This raw dataset is structured so that each match has an individual row and stats for both teams are on that row with columns titles "home" and "away".

Our goal is to build a machine learning (ML) model that can predict the result of a soccer match. Given that we have some match stats, we will aim to use that information to predict a WIN, LOSS or DRAW.

``` Python
raw_match_stats
```

date|match_id|home_team_name|away_team_name|home_team_goal_count|away_team_goal_count|home_team_half_time_goal_count|away_team_half_time_goal_count|home_team_shots|away_team_shots|home_team_shots_on_target|away_team_shots_on_target|home_team_fouls|away_team_fouls|home_team_corner_count|away_team_corner_count|home_team_yellow|away_team_yellow|home_team_red|away_team_red
---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---
6/11/2023|222305|Tottenham|Chelsea|1|4|1|1|8|17|5|8|12|21|1|6|1|5|2|0
5/11/2023|222304|Luton|Liverpool|1|1|0|0|8|24|5|6|7|13|4|7|1|1|0|0
5/11/2023|222303|Nottm Forest|Aston Villa|2|0|1|0|5|13|3|3|6|9|0|10|1|1|0|0
4/11/2023|222299|Everton|Brighton|1|1|1|0|10|7|4|2|15|5|3|3|4|2|0|0
4/11/2023|222296|Fulham|Man Utd|0|1|0|0|18|12|3|5|9|15|9|4|5|2|0|0
...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...|...
19/08/2000|213457|Chelsea|West Ham|4|2|1|0|17|12|10|5|19|14|7|7|1|2|0|0
19/08/2000|213462|Liverpool|Bradford|1|0|0|0|16|3|10|2|8|8|6|1|1|1|0|0
19/08/2000|213463|Sunderland|Arsenal|1|0|0|0|8|14|2|7|10|21|2|9|3|1|0|1
19/08/2000|213464|Tottenham|Ipswich|3|1|2|1|20|15|6|5|14|13|3|4|0|0|0|0
19/08/2000|213456|Charlton|Man City|4|0|2|0|17|8|14|4|13|12|6|6|1|2|0|0


---
## Data cleaning and feature engineering

#### Target variable - Match Result

Our machine learning model aims to predict the result of a match. This "result" is called the "target variable". Our dataset has no columns showing the match result. We will create two columns for the results for each team. One of these would become the target variable for our ML model.

``` Python
# create results columns for both home and away teams (3 - win, 1 = Draw, 0 = Loss).

raw_match_stats.loc[raw_match_stats['home_team_goal_count'] == raw_match_stats['away_team_goal_count'], 'home_team_result'] = 1
raw_match_stats.loc[raw_match_stats['home_team_goal_count'] > raw_match_stats['away_team_goal_count'], 'home_team_result'] = 3
raw_match_stats.loc[raw_match_stats['home_team_goal_count'] < raw_match_stats['away_team_goal_count'], 'home_team_result'] = 0

raw_match_stats.loc[raw_match_stats['home_team_goal_count'] == raw_match_stats['away_team_goal_count'], 'away_team_result'] = 1
raw_match_stats.loc[raw_match_stats['home_team_goal_count'] > raw_match_stats['away_team_goal_count'], 'away_team_result'] = 0
raw_match_stats.loc[raw_match_stats['home_team_goal_count'] < raw_match_stats['away_team_goal_count'], 'away_team_result'] = 3
```

#### Average pre-match stats - Ten match average

Great! Now we have a dataset with many rows of data, with each row representing match stats and the match result (this would become our target variable).

But our goal is to build an ML model that predicts the match result prior to the start of a match. Are the stats from that match what we need to build this ML model? No! When predicting a match outcome BEFORE the start of the match, we are forced to rely on match stats available to us from previous matches.

Therefore, we need a dataset with the match result (target variable) and stats for each team heading into that match. For this tutorial, we will look at the average stats for each team in the ten matches preceding each match.

Lets look at how we can get the average stats for the previous 10 matches for each team at each match.

1. Split the raw_match_stats to two datasets (home_team_stats and away_team_stats).
2. Stack these two datasets so that each row is the stats for a team for one match (team_stats_per_match).
3. At each row of this dataset, get the team name, find the stats for that team during the last 10 matches, and average these stats (avg_stats_per_team).
4. Add these stats to the team_stats_per_match dataset.

*Why did we chose ten matches? Why not 15? Should we average over a time period (matches in the last year perhaps?) rather than a number? What's the least number of matches available for each competing team in the dataset? These are all interesting questions that may improve our model.*

``` Python
# Split the raw_match_stats to two datasets (home_team_stats and away_team_stats)

home_team_stats = raw_match_stats[[
 'date',
 'match_id',
 'home_team_name',
 'home_team_goal_count',
 'home_team_half_time_goal_count',
 'home_team_corner_count',
 'home_team_shots',
 'home_team_shots_on_target',
 'home_team_fouls',
 'home_team_yellow',
 'home_team_red',
 'home_team_result',
 'away_team_goal_count',
 'away_team_half_time_goal_count',
 'away_team_corner_count',
 'away_team_shots',
 'away_team_shots_on_target',
 'away_team_fouls',
 'away_team_yellow',
 'away_team_red']]

home_team_stats = home_team_stats.rename(columns={'home_team_name':'name',
                                                'home_team_goal_count':'goalsScored',
                                                'home_team_half_time_goal_count':'halfTimeGoalsScored',
                                                'home_team_corner_count':'cornerCount',
                                                'home_team_shots':'shots',
                                                'home_team_shots_on_target':'shotsOnTarget',
                                                'home_team_fouls':'foulsConceded',
                                                'home_team_yellow':'yellowConceded',
                                                'home_team_red':'redConceded',
                                                'home_team_result':'result',
                                                'away_team_goal_count':'goalsConceded',
                                                'away_team_half_time_goal_count':'halfTimeGoalsConceded',
                                                'away_team_corner_count':'cornersConceded',
                                                'away_team_shots':'shotsConceded',
                                                'away_team_shots_on_target':'shotsOnTargetConceded',
                                                'away_team_fouls':'foulsReceived',
                                                'away_team_yellow':'yellowOpponent',
                                                'away_team_red':'redOpponent'})

away_team_stats = raw_match_stats[[
 'date',
 'match_id',
 'away_team_name',
 'away_team_goal_count',
 'away_team_half_time_goal_count',
 'away_team_corner_count',
 'away_team_shots',
 'away_team_shots_on_target',
 'away_team_fouls',
 'away_team_yellow',
 'away_team_red',
 'away_team_result',
 'home_team_goal_count',
 'home_team_half_time_goal_count',
 'home_team_corner_count',
 'home_team_shots',
 'home_team_shots_on_target',
 'home_team_fouls',
 'home_team_yellow',
 'home_team_red',]]

away_team_stats = away_team_stats.rename(columns={'away_team_name':'name',
                                                'away_team_goal_count':'goalsScored',
                                                'away_team_half_time_goal_count':'halfTimeGoalsScored',
                                                'away_team_corner_count':'cornerCount',
                                                'away_team_shots':'shots',
                                                'away_team_shots_on_target':'shotsOnTarget',
                                                'away_team_fouls':'foulsConceded',
                                                'away_team_yellow':'yellowConceded',
                                                'away_team_red':'redConceded',
                                                'away_team_result':'result',
                                                'home_team_goal_count':'goalsConceded',
                                                'home_team_half_time_goal_count':'halfTimeGoalsConceded',
                                                'home_team_corner_count':'cornersConceded',
                                                'home_team_shots':'shotsConceded',
                                                'home_team_shots_on_target':'shotsOnTargetConceded',
                                                'home_team_fouls':'foulsReceived',
                                                'home_team_yellow':'yellowOpponent',
                                                'home_team_red':'redOpponent'})

# add an additional column to denote whether the team is playing at home or away - this will help us later
home_team_stats['home_or_away']='Home'
away_team_stats['home_or_away']='Away'

# stack these two datasets so that each row is the stats for a team for one match (team_stats_per_match)
team_stats_per_match = pd.concat([home_team_stats,away_team_stats])
```

``` Python 
# At each row of this dataset, get the team name, find the stats for that team during the last 5 matches, and average these stats (avg_stats_per_team). 

avg_lastTen_stat_columns = [
                    'average_goalsScored_last_ten',
                    'average_halfTimeGoalsScored_last_ten',
                    'average_cornerCount_last_ten',
                    'average_shots_last_ten',
                    'average_shotsOnTarget_last_ten',
                    'average_foulsConceded_last_ten',
                    'average_yellowConceded_last_ten',
                    'average_redConceded_last_ten',
                    'average_result_last_ten',
                    'average_goalsConceded_last_ten',
                    'average_halfTimeGoalsConceded_last_ten',
                    'average_cornersConceded_last_ten',
                    'average_shotsConceded_last_ten',
                    'average_shotsOnTargetConceded_last_ten',
                    'average_foulsReceived_last_ten',
                    'average_yellowOpponent_last_ten',
                    'average_redOpponent_last_ten'
                    ]

lastTen_stats_list = []
for index, row in team_stats_per_match.iterrows():
    team_stats_last_ten_matches = team_stats_per_match.loc[(team_stats_per_match['name']==row['name']) & (team_stats_per_match['date']<row['date'])].sort_values(by=['date'], ascending=False)
    lastTen_stats_list.append(team_stats_last_ten_matches.iloc[0:10,3:-1].mean(axis=0).values[0:18])

avg_lastTen_stats_per_team = pd.DataFrame(lastTen_stats_list, columns=avg_lastTen_stat_columns)
```
#### Average Pre-Match Stats Last 5 Home and Last 5 Away Matches

Often teams can play better at home than away so it's important to consider whether they are playing at home or away. For example in the AFL, the Brisbane Lions are known to be almost unbeatable at the Gabba (there's a reason it's called the Gabbatoir).
As such we need to add some additional features.

``` Python
avg_lastFiveHome_stat_columns=[
                    'average_goalsScored_last_five_home',
                    'average_halfTimeGoalsScored_last_five_home',
                    'average_cornerCount_last_five_home',
                    'average_shots_last_five_home',
                    'average_shotsOnTarget_last_five_home',
                    'average_foulsConceded_last_five_home',
                    'average_yellowConceded_last_five_home',
                    'average_redConceded_last_five_home',
                    'average_result_last_five_home',
                    'average_goalsConceded_last_five_home',
                    'average_halfTimeGoalsConceded_last_five_home',
                    'average_cornersConceded_last_five_home',
                    'average_shotsConceded_last_five_home',
                    'average_shotsOnTargetConceded_last_five_home',
                    'average_foulsReceived_last_five_home',
                    'average_yellowOpponent_last_five_home',
                    'average_redOpponent_last_five_home'
                    ]

lastFive_Home_stats_list = []
team_stats_L5_home_matches = team_stats_per_match[team_stats_per_match['home_or_away'] == 'Home']
for index, row in team_stats_L5_home_matches.iterrows():
    team_stats_last_five_home_matches = team_stats_L5_home_matches.loc[(team_stats_L5_home_matches['name']==row['name']) & (team_stats_L5_home_matches['date']<row['date'])].sort_values(by=['date'], ascending=False)
    lastFive_Home_stats_list.append(team_stats_last_five_home_matches.iloc[0:5,3:-1].mean(axis=0).values[0:18])

avg_lastFiveHome_stats_per_team = pd.DataFrame(lastFive_Home_stats_list, columns=avg_lastFiveHome_stat_columns)
```
```Python
team_stats_L5_home_matches = pd.concat([team_stats_L5_home_matches.reset_index(drop=True), avg_lastFiveHome_stats_per_team], axis=1, ignore_index=False)
```
```Python
avg_lastFiveAway_stat_columns=[
                    'average_goalsScored_last_five_away',
                    'average_halfTimeGoalsScored_last_five_away',
                    'average_cornerCount_last_five_away',
                    'average_shots_last_five_away',
                    'average_shotsOnTarget_last_five_away',
                    'average_foulsConceded_last_five_away',
                    'average_yellowConceded_last_five_away',
                    'average_redConceded_last_five_away',
                    'average_result_last_five_away',
                    'average_goalsConceded_last_five_away',
                    'average_halfTimeGoalsConceded_last_five_away',
                    'average_cornersConceded_last_five_away',
                    'average_shotsConceded_last_five_away',
                    'average_shotsOnTargetConceded_last_five_away',
                    'average_foulsReceived_last_five_away',
                    'average_yellowOpponent_last_five_away',
                    'average_redOpponent_last_five_away'
                    ]

lastFive_away_stats_list = []
team_stats_L5_away_matches = team_stats_per_match[team_stats_per_match['home_or_away'] == 'Away']
for index, row in team_stats_L5_away_matches.iterrows():
    team_stats_last_five_away_matches = team_stats_L5_away_matches.loc[(team_stats_L5_away_matches['name']==row['name']) & (team_stats_L5_away_matches['date']<row['date'])].sort_values(by=['date'], ascending=False)
    lastFive_away_stats_list.append(team_stats_last_five_away_matches.iloc[0:5,3:-1].mean(axis=0).values[0:18])

avg_lastFiveAway_stats_per_team = pd.DataFrame(lastFive_away_stats_list, columns=avg_lastFiveAway_stat_columns)
team_stats_L5_away_matches = pd.concat([team_stats_L5_away_matches.reset_index(drop=True), avg_lastFiveAway_stats_per_team], axis=1, ignore_index=False)
```
```Python
team_stats_L5_home_matches.columns = team_stats_L5_home_matches.columns[:2].tolist() + ['team_1_'+str(col) for col in team_stats_L5_home_matches.columns[2:]]
team_stats_L5_away_matches.columns = team_stats_L5_away_matches.columns[:2].tolist() + ['team_2_'+str(col) for col in team_stats_L5_away_matches.columns[2:]]
```
```Python
home_and_away_stats = pd.merge(team_stats_L5_home_matches,team_stats_L5_away_matches,how='left',on=['date','match_id'])
```

#### Reshape average pre-match stats

Now that we have the average stats for each team going into every match, we can create a dataset similar to the raw_match_stats, where each row represents both teams from one match.

1. Re-segment the home and away teams (name Team 1 and Team 2 rather than home and away).
2. Combine at each match to get a dataset with a row representing each match.

``` Python
team_stats_per_match = pd.concat([team_stats_per_match.reset_index(drop=True), avg_lastTen_stats_per_team], axis=1, ignore_index=False)
# Re-segment the home and away teams.
home_team_stats = team_stats_per_match.iloc[:int(team_stats_per_match.shape[0]/2),:]
away_team_stats = team_stats_per_match.iloc[int(team_stats_per_match.shape[0]/2):,:]

home_team_stats.columns = home_team_stats.columns[:2].tolist() + ['team_1_'+str(col) for col in home_team_stats.columns[2:]]
away_team_stats.columns = away_team_stats.columns[:2].tolist() + ['team_2_'+str(col) for col in away_team_stats.columns[2:]]

# Combine at each match to get a dataset with a row representing each match. 
# drop the NA rows (earliest match for each team, i.e no previous stats)
away_team_stats = away_team_stats.iloc[:, 2:]
match_stats = pd.concat([home_team_stats, away_team_stats.reset_index(drop=True)], axis=1, ignore_index=False)
match_stats = match_stats.dropna().reset_index(drop=True)
```

``` Python
match_stats=pd.merge(match_stats,home_and_away_stats,how='left',on=['date',
                                                                    'match_id',
                                                                    'team_1_name',
                                                                    'team_1_goalsScored',
                                                                    'team_1_halfTimeGoalsScored',
                                                                    'team_1_cornerCount',
                                                                    'team_1_shots',
                                                                    'team_1_shotsOnTarget',
                                                                    'team_1_foulsConceded',
                                                                    'team_1_yellowConceded',
                                                                    'team_1_redConceded',
                                                                    'team_1_result',
                                                                    'team_1_goalsConceded',
                                                                    'team_1_halfTimeGoalsConceded',
                                                                    'team_1_cornersConceded',
                                                                    'team_1_shotsConceded',
                                                                    'team_1_shotsOnTargetConceded',
                                                                    'team_1_foulsReceived',
                                                                    'team_1_yellowOpponent',
                                                                    'team_1_redOpponent',
                                                                    'team_1_home_or_away',
                                                                    'team_2_name',
                                                                    'team_2_goalsScored',
                                                                    'team_2_halfTimeGoalsScored',
                                                                    'team_2_cornerCount',
                                                                    'team_2_shots',
                                                                    'team_2_shotsOnTarget',
                                                                    'team_2_foulsConceded',
                                                                    'team_2_yellowConceded',
                                                                    'team_2_redConceded',
                                                                    'team_2_result',
                                                                    'team_2_goalsConceded',
                                                                    'team_2_halfTimeGoalsConceded',
                                                                    'team_2_cornersConceded',
                                                                    'team_2_shotsConceded',
                                                                    'team_2_shotsOnTargetConceded',
                                                                    'team_2_foulsReceived',
                                                                    'team_2_yellowOpponent',
                                                                    'team_2_redOpponent',
                                                                    'team_2_home_or_away'])
```

## Train ML model

In our ML model, we will use the raw Team 1 and Team 2 average stats as features.

Some questions we could ask ourselves about this dataset are: (and there is no easy answer without some experimentation)

*Would we be better off using the differential between the teams as features?*

*Can we generate any other useful features from the dataset provided?*

*Do we need to weigh the home and away teams because home teams win more often?*

In this tutorial we will:

1. Train a model using 68 feature columns
2. Use a datetime split in training/test data (a random 80/20 split could also be used)
3. Use accuracy to evaluate our models

*It's probably worth evaluating multiple models (several models explained in this tutorial), perhaps use k-fold cross validation, and use metrics other than accuracy to evaluate a model (check the commented out code).*

``` Python
# import required libraries

from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support as score, confusion_matrix, roc_auc_score, classification_report, log_loss

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
```

#### Get data from our dataset

1. Team_1_result column - target variable
2. The raw stats of the two teams (68 columns) - features

*Do we need to scale or normalize the feature columns in order for it to make mathematical sense to a ML model? This depends on the type of model we are training, but it's definitely worth investigating in order to achieve a high performing model.*

*We should also investigate the dataset to check if it's balanced on all classes or if it's skewed towards a particular class (i.e are there an equal number of wins, losses and draws?). If not, would this affect model performance?*

``` Python
match_stats.dropna(inplace=True)

# Define features
features = ['team_1_average_goalsScored_last_ten',
            'team_1_average_halfTimeGoalsScored_last_ten',
            'team_1_average_cornerCount_last_ten',
            'team_1_average_shots_last_ten',
            'team_1_average_shotsOnTarget_last_ten',
            'team_1_average_foulsConceded_last_ten',
            'team_1_average_yellowConceded_last_ten',
            'team_1_average_redConceded_last_ten',
            'team_1_average_result_last_ten',
            'team_1_average_goalsConceded_last_ten',
            'team_1_average_halfTimeGoalsConceded_last_ten',
            'team_1_average_cornersConceded_last_ten',
            'team_1_average_shotsConceded_last_ten',
            'team_1_average_shotsOnTargetConceded_last_ten',
            'team_1_average_foulsReceived_last_ten',
            'team_1_average_yellowOpponent_last_ten',
            'team_1_average_redOpponent_last_ten',
            'team_2_average_goalsScored_last_ten',
            'team_2_average_halfTimeGoalsScored_last_ten',
            'team_2_average_cornerCount_last_ten',
            'team_2_average_shots_last_ten',
            'team_2_average_shotsOnTarget_last_ten',
            'team_2_average_foulsConceded_last_ten',
            'team_2_average_yellowConceded_last_ten',
            'team_2_average_redConceded_last_ten',
            'team_2_average_result_last_ten',
            'team_2_average_goalsConceded_last_ten',
            'team_2_average_halfTimeGoalsConceded_last_ten',
            'team_2_average_cornersConceded_last_ten',
            'team_2_average_shotsConceded_last_ten',
            'team_2_average_shotsOnTargetConceded_last_ten',
            'team_2_average_foulsReceived_last_ten',
            'team_2_average_yellowOpponent_last_ten',
            'team_2_average_redOpponent_last_ten',
            'team_1_average_goalsScored_last_five_home',
            'team_1_average_halfTimeGoalsScored_last_five_home',
            'team_1_average_cornerCount_last_five_home',
            'team_1_average_shots_last_five_home',
            'team_1_average_shotsOnTarget_last_five_home',
            'team_1_average_foulsConceded_last_five_home',
            'team_1_average_yellowConceded_last_five_home',
            'team_1_average_redConceded_last_five_home',
            'team_1_average_result_last_five_home',
            'team_1_average_goalsConceded_last_five_home',
            'team_1_average_halfTimeGoalsConceded_last_five_home',
            'team_1_average_cornersConceded_last_five_home',
            'team_1_average_shotsConceded_last_five_home',
            'team_1_average_shotsOnTargetConceded_last_five_home',
            'team_1_average_foulsReceived_last_five_home',
            'team_1_average_yellowOpponent_last_five_home',
            'team_1_average_redOpponent_last_five_home',
            'team_2_average_goalsScored_last_five_away',
            'team_2_average_halfTimeGoalsScored_last_five_away',
            'team_2_average_cornerCount_last_five_away',
            'team_2_average_shots_last_five_away',
            'team_2_average_shotsOnTarget_last_five_away',
            'team_2_average_foulsConceded_last_five_away',
            'team_2_average_yellowConceded_last_five_away',
            'team_2_average_redConceded_last_five_away',
            'team_2_average_result_last_five_away',
            'team_2_average_goalsConceded_last_five_away',
            'team_2_average_halfTimeGoalsConceded_last_five_away',
            'team_2_average_cornersConceded_last_five_away',
            'team_2_average_shotsConceded_last_five_away',
            'team_2_average_shotsOnTargetConceded_last_five_away',
            'team_2_average_foulsReceived_last_five_away',
            'team_2_average_yellowOpponent_last_five_away',
            'team_2_average_redOpponent_last_five_away'
]

```

#### Split test and training data

We train a model on the training data, and then use test data to evaluate the performance of that model.

``` Python
train_data = match_stats[match_stats['date'] < '2018-07-01']
test_data = match_stats[match_stats['date'] >= '2018-07-01']

X_train = train_data[features]
X_test = test_data[features]
Y_train = train_data['team_1_result']
Y_test = test_data['team_1_result']
```

#### Name and define classifiers

``` Python
names = ["Nearest Neighbors", "Logistic Regression","Linear SVM", "RBF SVM", "Gaussian Process",
         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
         "Naive Bayes", "QDA"]

classifiers = [
    KNeighborsClassifier(3),
    LogisticRegression(),
    SVC(kernel="linear", C=0.025, probability=True),
    SVC(gamma=2, C=1, probability=True),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=1, max_iter=1000),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis()]
```

#### Iterate through all classifiers and get their accuracy score

We can use the best performing model to make our predictions.

*There are several other metrics in the code that have been commented out which might provide helpful insights on model performance.*

``` Python

for name, clf in zip(names, classifiers):
    # Fit the classifier on the training data and make predictions
    clf.fit(X_train, Y_train)
    test_data[name + '_team_1_result'] = clf.predict(X_test)
    accuracy = clf.score(X_test, Y_test)

    # prediction_proba = clf.predict_proba(X_test)
    # logloss = log_loss(y_test,prediction_proba)
    # precision, recall, fscore, support = score(y_test, prediction)
    # conf_martrix = confusion_matrix(y_test, prediction)
    # clas_report = classification_report(y_test, prediction)

    print(name, accuracy)

# Export the predictions to a CSV file
test_data.to_csv('predictions.csv', index=False)
```

``` 
Nearest Neighbors 0.43313373253493015
Logistic Regression 0.5359281437125748
Linear SVM 0.532435129740519
RBF SVM 0.4431137724550898
Gaussian Process 0.4286427145708583
Decision Tree 0.499001996007984
Random Forest 0.49001996007984033
Neural Net 0.5069860279441117
AdaBoost 0.499500998003992
Naive Bayes 0.5149700598802395
QDA 0.4865269461077844
```

--- 
### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.