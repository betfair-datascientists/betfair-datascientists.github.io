# AFL Modelling Walkthrough 

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
Now that we have a model up and running, the next steps are to implement the model on a week to week basis. In the [next tutorial](/modelling/AFLmodelPart4) we will be predicting the 2018 round of footy.