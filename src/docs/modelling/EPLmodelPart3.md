# EPL Machine Learning Walkthrough

# 03. Model Building & Hyperparameter Tuning
Welcome to the third part of this Machine Learning Walkthrough. This tutorial will focus on the model building process, including how to tune hyperparameters. In the [next tutorial], we will create weekly predictions based on the model we have created here.

Specifically, this tutorial will cover a few things:

1. Choosing which Machine Learning algorithm to use from a variety of choices
2. Hyperparameter Tuning
3. Overfitting/Underfitting

---
## Choosing an Algorithm
The best way to decide on specific algorithm to use, is to try them all! To do this, we will define a function which we first used in our AFL Predictions tutorial. This will iterate over a number of algorithms and give us a good indication of which algorithms are suited for this dataset and exercise.

Let's first use grab the features we created in the last tutorial. This may take a minute or two to run.

```python
## Import libraries
from data_preparation_functions import *
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import warnings
from sklearn import linear_model, tree, discriminant_analysis, naive_bayes, ensemble, gaussian_process
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.metrics import log_loss, confusion_matrix
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 100)
```

```python
features = create_feature_df()
    Creating all games feature DataFrame
    Creating stats feature DataFrame
    Creating odds feature DataFrame
    Creating market values feature DataFrame
    Filling NAs
    Merging stats, odds and market values into one features DataFrame
    Complete.
```

To start our modelling process, we need to make a training set, a test set and a holdout set. As we are using cross validation, we will make our training set all of the seasons up until 2017/18, and we will use the 2017/18 season as the test set.

```python
feature_list = [col for col in features.columns if col.startswith("f_")]
betting_features = []

le = LabelEncoder() # Initiate a label encoder to transform the labels 'away', 'draw', 'home' to 0, 1, 2

# Grab all seasons except for 17/18 to use CV with
all_x = features.loc[features.season != '1718', ['gameId'] + feature_list]
all_y = features.loc[features.season != '1718', 'result']
all_y = le.fit_transform(all_y)

# Create our training vector as the seasons except 16/17 and 17/18
train_x = features.loc[~features.season.isin(['1617', '1718']), ['gameId'] + feature_list]
train_y = le.transform(features.loc[~features.season.isin(['1617', '1718']), 'result'])

# Create our holdout vectors as the 16/17 season
holdout_x = features.loc[features.season == '1617', ['gameId'] + feature_list]
holdout_y = le.transform(features.loc[features.season == '1617', 'result'])

# Create our test vectors as the 17/18 season
test_x = features.loc[features.season == '1718', ['gameId'] + feature_list]
test_y = le.transform(features.loc[features.season == '1718', 'result'])
```

```python
# Create a list of standard classifiers
classifiers = [

    #GLM
    linear_model.LogisticRegressionCV(),
    
    #Navies Bayes
    naive_bayes.BernoulliNB(),
    naive_bayes.GaussianNB(),
    
    #Discriminant Analysis
    discriminant_analysis.LinearDiscriminantAnalysis(),
    discriminant_analysis.QuadraticDiscriminantAnalysis(),

    #Ensemble Methods
    ensemble.AdaBoostClassifier(),
    ensemble.BaggingClassifier(),
    ensemble.ExtraTreesClassifier(),
    ensemble.GradientBoostingClassifier(),
    ensemble.RandomForestClassifier(),

    #Gaussian Processes
    gaussian_process.GaussianProcessClassifier(),
    
    #xgboost: http://xgboost.readthedocs.io/en/latest/model.html
#     xgb.XGBClassifier()    
]
```

```python
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
    }).sort_values(by='Mean Log Loss')
    return cv_results
```

```python
algorithm_results = find_best_algorithms(classifiers, all_x, all_y)
```

```python
algorithm_results
```

|  | Mean Log Loss | Log Loss Std | Algorithm |
| --- | --- | --- | --- |
| 0 | 0.966540 | 0.020347 | LogisticRegressionCV |
| 3 | 0.986679 | 0.015601 | LinearDiscriminantAnalysis |
| 1 | 1.015197 | 0.017466 | BernoulliNB |
| 10 | 1.098612 | 0.000000 | GaussianProcessClassifier |
| 5 | 1.101281 | 0.044383 | AdaBoostClassifier |
| 8 | 1.137778 | 0.153391 | GradientBoostingClassifier |
| 7 | 2.093981 | 0.284831 | ExtraTreesClassifier |
| 9 | 2.095088 | 0.130367 | RandomForestClassifier |
| 6 | 2.120571 | 0.503132 | BaggingClassifier |
| 4 | 4.065796 | 1.370119 | QuadraticDiscriminantAnalysis |
| 2 | 5.284171 | 0.826991 | GaussianNB |

We can see that LogisticRegression seems to perform the best out of all the algorithms, and some algorithms have a very high log loss. This is most likely due to overfitting. It would definitely be useful to condense our features down to reduce the dimensionality of the dataset.

---
## Hyperparameter Tuning
For now, however, we will use logistic regression. Let's first try and tune a logistic regression model with cross validation. To do this, we will use [grid search](https://en.wikipedia.org/wiki/Hyperparameter_optimization). Grid search essentially tries out each combination of values and finds the model with the lowest error metric, which in our case is log loss. 'C' in logistic regression determines the amount of regularization. Lower values increase regularization.

```python
# Define our parameters to run a grid search over
lr_grid = {
    "C": [0.0001, 0.01, 0.05, 0.2, 1],
    "solver": ["newton-cg", "lbfgs", "liblinear"]
}

kfold = StratifiedKFold(n_splits=5)

gs = GridSearchCV(LogisticRegression(), param_grid=lr_grid, cv=kfold, scoring='neg_log_loss')
gs.fit(all_x, all_y)
print("Best log loss: {}".format(gs.best_score_ *-1))
best_lr_params = gs.best_params_

  Best log loss: 0.9669551970849734
```
    
---
## Defining a Baseline
We should also define a baseline, as we don't really know if our log loss is good or bad. Randomly assigning a 1/3 chance to each selection yields a log loss of log3 = 1.09. However, what we are really interested in, is how our model performs relative to the odds. So let's find the log loss of the odds.

```python
# Finding the log loss of the odds
log_loss(all_y, 1 / all_x[['f_awayOdds', 'f_drawOdds', 'f_homeOdds']])

  0.9590114943474463
```

This is good news: our algorithm almost beats the bookies in terms of log loss. It would be great if we could beat this result.

---
## Analysing the Errors Made
Now that we have a logistic regression model tuned, let's see what type of errors it made. To do this we will look at the confusion matrix produced when we predict our holdout set.

```python
lr = LogisticRegression(**best_lr_params) # Instantiate the model
lr.fit(train_x, train_y) # Fit our model
lr_predict = lr.predict(holdout_x) # Predict the holdout values
```

```python
# Create a confusion matrix
c_matrix = (pd.DataFrame(confusion_matrix(holdout_y, lr_predict), columns=le.classes_, index=le.classes_)
 .rename_axis('Actual')
 .rename_axis('Predicted', axis='columns'))

c_matrix
```

| Predicted | away | draw | home |
| --- | --- | --- | --- |
| Actual |  |  |  |
| away | 77 | 0 | 32 |
| draw | 26 | 3 | 55 |
| home | 33 | 7 | 147 |


As we can see, when we predicted 'away' as the result, we correctly predicted 79 / 109 results, a hit rate of 70.6%. However, when we look at our draw hit rate, we only predicted 6 / 84 correctly, meaning we only had a hit rate of around 8.3%. For a more in depth analysis of our predictions, please skip to the Analysing Predictions & Staking Strategies section of the tutorial.

Before we move on, however, let's use our model to predict the 17/18 season and compare how we went with the odds.

```python
# Get test predictions

test_lr = LogisticRegression(**best_lr_params)
test_lr.fit(all_x, all_y)
test_predictions_probs = lr.predict_proba(test_x)
test_predictions = lr.predict(test_x)

test_ll = log_loss(test_y, test_predictions_probs)
test_accuracy = (test_predictions == test_y).mean()

print("Our predictions for the 2017/18 season have a log loss of: {0:.5f} and an accuracy of: {1:.2f}".format(test_ll, test_accuracy))
```
    Our predictions for the 2017/18 season have a log loss of: 0.95767 and an accuracy of: 0.56
    
```python
# Get accuracy and log loss based on the odds
odds_ll = log_loss(test_y, 1 / test_x[['f_awayOdds', 'f_drawOdds', 'f_homeOdds']])

odds_predictions = test_x[['f_awayOdds', 'f_drawOdds', 'f_homeOdds']].apply(lambda row: row.idxmin()[2:6], axis=1).values
odds_accuracy = (odds_predictions == le.inverse_transform(test_y)).mean()

print("Odds predictions for the 2017/18 season have a log loss of: {0:.5f} and an accuracy of: {1:.3f}".format(odds_ll, odds_accuracy))
```
    Odds predictions for the 2017/18 season have a log loss of: 0.94635 and an accuracy of: 0.545
    
---
## Results
There we have it! The odds predicted 54.5% of EPL games correctly in the 2017/18 season, whilst our model predicted 54% correctly. This is a decent result for the first iteration of our model. In future iterations, we could wait a certain number of matches each season and calculate EMAs for on those first n games. This may help the issue of players switching clubs and teams becoming relatively stronger/weaker compared to previous seasons.