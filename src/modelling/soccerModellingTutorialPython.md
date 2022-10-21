# How to model the 2021 Euro & Copa America: Python Tutorial
This tutorial was written as part of the 2021 Euro & Copa America Datathon competition
## The Task

This notebook will outline how to train a simple classification model to predict the outcome of a soccer match using the dataset provided for the datathon.

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

We need the date column in good order for our tutorial. [Here's a sample of the data set](assets/datathon_initial_form_data - SAMPLE.csv) we're using for this tutorial.

*In general, it's a good idea to evaluate data types of all columns that we work with to ensure they are correct.*

``` Python
df = pd.read_csv('soccerData.csv')
```

``` Python
df['date_GMT']= pd.to_datetime(df['date_GMT'])
```

#### Get data columns and create raw dataset

For this tutorial, let's take only a few stats columns to work with.

*Typically we would explore all features and then decide which data to discard.*

1. Goal counts
2. Corners
3. Total shots
4. Shots on target
5. Fouls
6. Possession

``` Python
raw_match_stats = df[[
 'date_GMT',
 'home_team_name',
 'away_team_name',
 'home_team_goal_count',
 'away_team_goal_count',
 'home_team_corner_count',
 'away_team_corner_count',
 'home_team_shots',
 'away_team_shots',
 'home_team_shots_on_target',
 'away_team_shots_on_target',
 'home_team_fouls',
 'away_team_fouls',
 'home_team_possession',
 'away_team_possession',]]
```

#### Clean data

As a cleaning step, we order our data by date and drop rows with NA values.

``` Python
raw_match_stats = raw_match_stats.sort_values(by=['date_GMT'], ascending=False)

raw_match_stats = raw_match_stats.dropna()
```

### Raw dataset

This raw dataset is structured so that each match has an individual row and stats for both teams are on that row with columns titles "home" and "away".

Our goal is to build a machine learning (ML) model that can predict the result of a soccer match. Given that we have some match stats, we will aim to use that information to predict a WIN, LOSS or DRAW.

``` Python
raw_match_stats
```

| date_GMT            | home_team_name   | away_team_name | home_team_goal_count | away_team_goal_count | home_team_corner_count | away_team_corner_count | home_team_shots | away_team_shots | home_team_shots_on_target | away_team_shots_on_target | home_team_fouls | away_team_fouls | home_team_possession | away_team_possession |
|---------------------|------------------|----------------|----------------------|----------------------|------------------------|------------------------|-----------------|-----------------|---------------------------|---------------------------|-----------------|-----------------|----------------------|----------------------|
| 2021-03-31 18:45:00 | Spain            | Kosovo         | 3                    | 1                    | 9.0                    | 2.0                    | 25.0            | 4.0             | 9.0                       | 2.0                       | 9.0             | 10.0            | 80.0                 | 20.0                 |
| 2021-03-31 18:45:00 | Scotland         | Faroe Islands  | 4                    | 0                    | 1.0                    | 5.0                    | 14.0            | 8.0             | 8.0                       | 3.0                       | 9.0             | 13.0            | 65.0                 | 35.0                 |
| 2021-03-31 18:45:00 | Switzerland      | Finland        | 3                    | 2                    | 5.0                    | 2.0                    | 21.0            | 6.0             | 9.0                       | 3.0                       | 11.0            | 7.0             | 63.0                 | 37.0                 |
| 2021-03-31 18:45:00 | Lithuania        | Italy          | 0                    | 2                    | 4.0                    | 5.0                    | 8.0             | 29.0            | 3.0                       | 11.0                      | 14.0            | 13.0            | 34.0                 | 66.0                 |
| 2021-03-31 18:45:00 | Northern Ireland | Bulgaria       | 0                    | 0                    | 12.0                   | 2.0                    | 16.0            | 4.0             | 5.0                       | 2.0                       | 17.0            | 17.0            | 70.0                 | 30.0                 |
| ...                 | ...              | ...            | ...                  | ...                  | ...                    | ...                    | ...             | ...             | ...                       | ...                       | ...             | ...             | ...                  | ...                  |
| 2014-06-14 16:00:00 | Colombia         | Greece         | 3                    | 0                    | 4.0                    | 4.0                    | 9.0             | 13.0            | 5.0                       | 8.0                       | 20.0            | 13.0            | 44.0                 | 56.0                 |
| 2014-06-13 22:00:00 | Chile            | Australia      | 3                    | 1                    | 3.0                    | 1.0                    | 7.0             | 12.0            | 5.0                       | 3.0                       | 10.0            | 18.0            | 59.0                 | 41.0                 |
| 2014-06-13 19:00:00 | Spain            | Netherlands    | 1                    | 5                    | 4.0                    | 1.0                    | 8.0             | 6.0             | 5.0                       | 6.0                       | 6.0             | 18.0            | 61.0                 | 39.0                 |
| 2014-06-13 16:00:00 | Mexico           | Cameroon       | 1                    | 0                    | 2.0                    | 5.0                    | 7.0             | 12.0            | 3.0                       | 4.0                       | 10.0            | 10.0            | 55.0                 | 45.0                 |
| 2014-06-12 20:00:00 | Brazil           | Croatia        | 3                    | 1                    | 7.0                    | 3.0                    | 13.0            | 10.0            | 5.0                       | 4.0                       | 5.0             | 19.0            | 63.0                 | 37.0                 |

---
## Data cleaning and feature engineering

#### Target variable - Match Result

Our machine learning model aims to predict the result of a match. This "result" is called the "target variable". Our dataset has no columns showing the match result. We will create two columns for the results for each team. One of these would become the target variable for our ML model.

``` Python
# create results columns for both home and away teams (W - win, D = Draw, L = Loss).

raw_match_stats.loc[raw_match_stats['home_team_goal_count'] == raw_match_stats['away_team_goal_count'], 'home_team_result'] = 'D'
raw_match_stats.loc[raw_match_stats['home_team_goal_count'] > raw_match_stats['away_team_goal_count'], 'home_team_result'] = 'W'
raw_match_stats.loc[raw_match_stats['home_team_goal_count'] < raw_match_stats['away_team_goal_count'], 'home_team_result'] = 'L'

raw_match_stats.loc[raw_match_stats['home_team_goal_count'] == raw_match_stats['away_team_goal_count'], 'away_team_result'] = 'D'
raw_match_stats.loc[raw_match_stats['home_team_goal_count'] > raw_match_stats['away_team_goal_count'], 'away_team_result'] = 'L'
raw_match_stats.loc[raw_match_stats['home_team_goal_count'] < raw_match_stats['away_team_goal_count'], 'away_team_result'] = 'W'
```

#### Average pre-match stats - Five match average

Great! Now we have a dataset with many rows of data, with each row representing match stats and the match result (this would become our target variable).

But our goal is to build an ML model that predicts the match result prior to the start of a match. Are the stats from that match what we need to build this ML model? No! When predicting a match outcome BEFORE the start of the match, we are forced to rely on match stats available to us from previous matches.

Therefore, we need a dataset with the match result (target variable) and stats for each team heading into that match. For this tutorial, we will look at the average stats for each team in the five matches preceding each match.

Lets look at how we can get the average stats for the previous 5 matches for each team at each match.

1. Split the raw_match_stats to two datasets (home_team_stats and away_team_stats).
2. Stack these two datasets so that each row is the stats for a team for one match (team_stats_per_match).
3. At each row of this dataset, get the team name, find the stats for that team during the last 5 matches, and average these stats (avg_stats_per_team).
4. Add these stats to the team_stats_per_match dataset.

*Why did we chose five matches? Why not 10? Should we average over a time period (matches in the last year perhaps?) rather than a number? What's the least number of matches available for each competing team in the dataset? These are all interesting questions that may improve our model.*

``` Python
# Split the raw_match_stats to two datasets (home_team_stats and away_team_stats)

home_team_stats = raw_match_stats[[
 'date_GMT',
 'home_team_name',
 'home_team_goal_count',
 'home_team_corner_count',
 'home_team_shots',
 'home_team_shots_on_target',
 'home_team_fouls',
 'home_team_possession',
 'home_team_result',]]

away_team_stats = raw_match_stats[[
 'date_GMT',
 'away_team_name',
 'away_team_goal_count',
 'away_team_corner_count',
 'away_team_shots',
 'away_team_shots_on_target',
 'away_team_fouls',
 'away_team_possession',
 'away_team_result',]]

# rename "home_team" and "away_team" columns
home_team_stats.columns = [col.replace('home_team_','') for col in home_team_stats.columns]
away_team_stats.columns = [col.replace('away_team_','') for col in away_team_stats.columns]

# stack these two datasets so that each row is the stats for a team for one match (team_stats_per_match)
team_stats_per_match = home_team_stats.append(away_team_stats)
```

``` Python
# At each row of this dataset, get the team name, find the stats for that team during the last 5 matches, and average these stats (avg_stats_per_team). 

avg_stat_columns = ['goals_per_match','corners_per_match','shots_per_match','shotsOnTarget_per_match','fouls_per_match', 'possession_per_match']
stats_list = []
for index, row in team_stats_per_match.iterrows():
    team_stats_last_five_matches = team_stats_per_match.loc[(team_stats_per_match['name']==row['name']) & (team_stats_per_match['date_GMT']<row['date_GMT'])].sort_values(by=['date_GMT'], ascending=False)
    stats_list.append(team_stats_last_five_matches.iloc[0:5,:].mean(axis=0).values[0:6])

avg_stats_per_team = pd.DataFrame(stats_list, columns=avg_stat_columns)
```

``` Python 
# Add these stats to the team_stats_per_match dataset.

team_stats_per_match = pd.concat([team_stats_per_match.reset_index(drop=True), avg_stats_per_team], axis=1, ignore_index=False)
```

#### Reshape average pre-match stats

Now that we have the average stats for each team going into every match, we can create a dataset similar to the raw_match_stats, where each row represents both teams from one match.

1. Re-segment the home and away teams (name Team 1 and Team 2 rather than home and away).
2. Combine at each match to get a dataset with a row representing each match.

``` Python
# Re-segment the home and away teams.

home_team_stats = team_stats_per_match.iloc[:int(team_stats_per_match.shape[0]/2),:]
away_team_stats = team_stats_per_match.iloc[int(team_stats_per_match.shape[0]/2):,:]

home_team_stats.columns = ['team_1_'+str(col) for col in home_team_stats.columns]
away_team_stats.columns = ['team_2_'+str(col) for col in away_team_stats.columns]
```

``` Python
# Combine at each match to get a dataset with a row representing each match. 
# drop the NA rows (earliest match for each team, i.e no previous stats)

match_stats = pd.concat([home_team_stats, away_team_stats.reset_index(drop=True)], axis=1, ignore_index=False)
match_stats = match_stats.dropna().reset_index(drop=True)
```

#### Find the difference of stats between teams

In our ML model, we will take the difference between Team 1 and Team 2 average stats as features. 6 new columns are created for this.

*Would we be better off using the raw stats for each team as features?*

*Can we generate any other useful features from the dataset provided?*

*Do we need to weigh the home and away teams because home teams win more often?*

``` Python
# create columns with average stat differences between the two teams

match_stats['goals_per_match_diff'] = (match_stats['team_1_goals_per_match'] - match_stats['team_2_goals_per_match'])
match_stats['corners_per_match_diff'] = (match_stats['team_1_corners_per_match'] - match_stats['team_2_corners_per_match'])
match_stats['shots_per_match_diff'] = (match_stats['team_1_shots_per_match'] - match_stats['team_2_shots_per_match'])
match_stats['shotsOnTarget_per_match_diff'] = (match_stats['team_1_shotsOnTarget_per_match'] - match_stats['team_2_shotsOnTarget_per_match'])
match_stats['fouls_per_match_diff'] = (match_stats['team_1_fouls_per_match'] - match_stats['team_2_fouls_per_match'])
match_stats['possession_per_match_diff'] = (match_stats['team_1_possession_per_match'] - match_stats['team_2_possession_per_match'])
```

``` Python
match_stats
```

| team_1_date_GMT     | team_1_name      | team_1_goal_count | team_1_corner_count | team_1_shots | team_1_shots_on_target | team_1_fouls | team_1_possession | team_1_result | team_1_goals_per_match | ... | team_2_shots_per_match | team_2_shotsOnTarget_per_match | team_2_fouls_per_match | team_2_possession_per_match | goals_per_match_diff | corners_per_match_diff | shots_per_match_diff | shotsOnTarget_per_match_diff | fouls_per_match_diff | possession_per_match_diff |
|---------------------|------------------|-------------------|---------------------|--------------|------------------------|--------------|-------------------|---------------|------------------------|-----|------------------------|--------------------------------|------------------------|-----------------------------|----------------------|------------------------|----------------------|------------------------------|----------------------|---------------------------|
| 2021-03-31 18:45:00 | Spain            | 3                 | 9.0                 | 25.0         | 9.0                    | 9.0          | 80.0              | W             | 2.2                    | ... | 6.6                    | 2.4                            | 12.2                   | 45.0                        | 1.8                  | 3.4                    | 5.2                  | 2.4                          | -1.6                 | 24.6                      |
| 2021-03-31 18:45:00 | Scotland         | 4                 | 1.0                 | 14.0         | 8.0                    | 9.0          | 65.0              | W             | 0.8                    | ... | 9.0                    | 3.8                            | 14.0                   | 46.8                        | -0.2                 | 2.2                    | 4.6                  | 2.4                          | -0.2                 | 2.0                       |
| 2021-03-31 18:45:00 | Switzerland      | 3                 | 5.0                 | 21.0         | 9.0                    | 11.0         | 63.0              | W             | 1.8                    | ... | 7.6                    | 2.2                            | 10.2                   | 36.0                        | 0.2                  | 2.6                    | 5.2                  | 3.6                          | 3.2                  | 15.8                      |
| 2021-03-31 18:45:00 | Lithuania        | 0                 | 4.0                 | 8.0          | 3.0                    | 14.0         | 34.0              | L             | 0.8                    | ... | 15.6                   | 5.4                            | 11.4                   | 64.4                        | -1.6                 | -4.6                   | -7.2                 | -3.0                         | 0.2                  | -17.2                     |
| 2021-03-31 18:45:00 | Northern Ireland | 0                 | 12.0                | 16.0         | 5.0                    | 17.0         | 70.0              | D             | 0.8                    | ... | 8.8                    | 3.2                            | 16.2                   | 48.6                        | -0.2                 | 0.4                    | 0.0                  | -0.2                         | -7.0                 | -2.8                      |
| ...                 | ...              | ...               | ...                 | ...          | ...                    | ...          | ...               | ...           | ...                    | ... | ...                    | ...                            | ...                    | ...                         | ...                  | ...                    | ...                  | ...                          | ...                  | ...                       |
| 2014-06-19 16:00:00 | Colombia         | 2                 | 5.0                 | 8.0          | 5.0                    | 12.0         | 40.0              | W             | 3.0                    | ... | 19.0                   | 8.0                            | 12.0                   | 56.0                        | 1.0                  | -4.0                   | -10.0                | -3.0                         | 8.0                  | -12.0                     |
| 2014-06-18 22:00:00 | Cameroon         | 0                 | 4.0                 | 12.0         | 2.0                    | 11.0         | 43.0              | L             | 0.0                    | ... | 10.0                   | 4.0                            | 19.0                   | 37.0                        | -1.0                 | 2.0                    | 2.0                  | 0.0                          | -9.0                 | 8.0                       |
| 2014-06-18 19:00:00 | Spain            | 0                 | 7.0                 | 18.0         | 9.0                    | 14.0         | 63.0              | L             | 1.0                    | ... | 7.0                    | 5.0                            | 10.0                   | 59.0                        | -2.0                 | 1.0                    | 1.0                  | 0.0                          | -4.0                 | 2.0                       |
| 2014-06-18 16:00:00 | Australia        | 2                 | 3.0                 | 6.0          | 3.0                    | 17.0         | 50.0              | L             | 1.0                    | ... | 6.0                    | 6.0                            | 18.0                   | 39.0                        | -4.0                 | 0.0                    | 6.0                  | -3.0                         | 0.0                  | 2.0                       |
| 2014-06-17 19:00:00 | Brazil           | 0                 | 4.0                 | 12.0         | 7.0                    | 14.0         | 50.0              | D             | 3.0                    | ... | 7.0                    | 3.0                            | 10.0                   | 55.0                        | 2.0                  | 5.0                    | 6.0                  | 2.0                          | -5.0                 | 8.0                       |

---
## Train ML model

In this tutorial we will:

1. Train a model using 6 feature columns
2. Use an 80/20 split in training/test data
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
2. The difference of stats between teams (6 columns) - features

*Do we need to scale or normalize the feature columns in order for it to make mathematical sense to a ML model? This depends on the type of model we are training, but it's definitely worth investigating in order to achieve a high performing model.*

*We should also investigate the dataset to check if it's balanced on all classes or if it's skewed towards a particular class (i.e are there an equal number of wins, losses and draws?). If not, would this affect model performance?*

``` Python
target = match_stats[['team_1_result']].replace(['W','L','D'],[0,1,2])

features = match_stats[['goals_per_match_diff', 'corners_per_match_diff',
       'shots_per_match_diff', 'shotsOnTarget_per_match_diff',
       'fouls_per_match_diff', 'possession_per_match_diff']]
```

#### Split test and training data

We train a model on the training data, and then use test data to evaluate the performance of that model.

``` Python
X_train,X_test,y_train,y_test = train_test_split(features, target, test_size=0.2, stratify = target)
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
        clf.fit(X_train, y_train)
        accuracy = clf.score(X_test, y_test)
        
        # prediction_proba = clf.predict_proba(X_test)
        # logloss = log_loss(y_test,prediction_proba)
        # precision, recall, fscore, support = score(y_test, prediction)
        # conf_martrix = confusion_matrix(y_test, prediction)
        # clas_report = classification_report(y_test, prediction)
        
        print(name, accuracy)
```

``` 
Nearest Neighbors 0.49295774647887325
Logistic Regression 0.5714285714285714
Linear SVM 0.5694164989939637
RBF SVM 0.46680080482897385
Gaussian Process 0.5633802816901409
Decision Tree 0.5432595573440644
Random Forest 0.5533199195171026
Neural Net 0.5573440643863179
AdaBoost 0.5573440643863179
Naive Bayes 0.5331991951710262
QDA 0.5674044265593562
```

--- 
### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.