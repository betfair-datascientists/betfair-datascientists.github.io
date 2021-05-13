# How to model the 2021 Euro & Copa America: R Tutorial

## The Task

This notebook will outline how to train a simple classification model to predict the outcome of a soccer match using the dataset provided for the datathon.

1. Reading data from file and get a raw dataset
2. Data cleaning and feature engineering
3. Training a model

The tutorial covers the thought process of manipulating the dataset (why and how), some simple data cleaning, feature engineering and training a classification model.

The tutorial **DOES NOT** delve deep into the fundamentals of machine learning, advanced feature engineering or model tuning.

*There are some helpful hints along the way though.*

!!! note "Betfair Datathon"
    If you're interested in competing in the 2021 Euro & Copa America Datathon competition make sure you [head to the Hub](https://www.betfair.com.au/hub/betfair-euro-copa-america-datathon/), register and download the bespoke data set provided and get your model submitted before 11 June for your chance to win part of the prize pool. 


```{r}
# import required libraries
library(tidyverse)
library(lubridate)
library(caTools) # calculate rolling average 
```

---
## Read data from file and get a raw dataset
#### Change the data types - date column.

We need the date column in good order for our tutorial. [Here's a sample of the data set](assets/datathon_initial_form_data - SAMPLE.csv) we're using for this tutorial.

*In general, it's a good idea to evaluate data types of all columns that we work with to ensure they are correct.*

```{r}
df = read_csv("SoccerData.csv", guess_max = 2000)
df = df %>% mutate(date_GMT = parse_date_time(date_GMT, '%b %d %Y - %I:%M%p', tz = "GMT"))
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

```{r}
raw_match_stats = df %>%
  select(
  date_GMT,
  home_team_name,
  away_team_name,
  home_team_goal_count,
  away_team_goal_count,
  home_team_corner_count,
  away_team_corner_count,
  home_team_shots,
  away_team_shots,
  home_team_shots_on_target,
  away_team_shots_on_target,
  home_team_fouls,
  away_team_fouls,
  home_team_possession,
  away_team_possession
  )
```

#### Clean data
As a cleaning step, we order our data by date and drop rows with NA values.

```{r}
raw_match_stats = raw_match_stats %>%
  arrange(desc(date_GMT)) %>%
  drop_na() %>%
  mutate(game_id = 1:n())
```

#### Raw dataset
This raw dataset is structured so that each match has an individual row and stats for both teams are on that row with columns titles "home" and "away".

Our goal is to build a machine learning (ML) model that can predict the result of a soccer match. Given that we have some match stats, we will aim to use that information to predict a WIN, LOSS or DRAW.

```{r}
raw_match_stats
```

---
## Data cleaning and feature engineering

#### Target variable - Match Result

Our machine learning model aims to predict the result of a match. This "result" is called the "target variable". Our dataset has no columns showing the match result. We will create two columns for the results for each team. One of these would become the target variable for our ML model.

```{r}
# create results columns for both home and away teams (W - win, D = Draw, L = Loss).
raw_match_stats = raw_match_stats %>%
  mutate(home_team_result = case_when(home_team_goal_count == away_team_goal_count ~ "D",
                                      home_team_goal_count > away_team_goal_count ~ "W",
                                      home_team_goal_count < away_team_goal_count ~ "L"),
         away_team_result = case_when(home_team_goal_count == away_team_goal_count ~ "D",
                                      home_team_goal_count > away_team_goal_count ~ "L",
                                      home_team_goal_count < away_team_goal_count ~ "W"))
```

#### Average pre-match stats - Five match average

Great! Now we have a dataset with many rows of data, with each row representing match stats and the match result (this would become our target variable).

But our goal is to build an ML model that predicts the match result prior to the start of a match. Are the stats from that match what we need to build this ML model? No! When predicting a match outcome BEFORE the start of the match, we are forced to rely on match stats available to us from previous matches.

Therefore, we need a dataset with the match result (target variable) and stats for each team heading into that match. For this tutorial, we will look at the average stats for each team in the five matches preceding each match.

Lets look at how we can get the average stats for the previous 5 matches for each team at each match.

1. Split the raw_match_stats to two datasets (home_team_stats and away_team_stats).
2. Stack these two datasets so that each row is the stats for a team for one match (team_stats_per_match).
3. At each row of this dataset, get the team name, find the stats for that team during the 4. last 5 matches, and average these stats (avg_stats_per_team).
Add these stats to the team_stats_per_match dataset.

*Why did we chose five matches? Why not 10? Should we average over a time period (matches in the last year perhaps?) rather than a number? What's the least number of matches available for each competing team in the dataset? These are all interesting questions that may improve our model.*

```{r}
# Split the raw_match_stats to two datasets (home_team_stats and away_team_stats). 
home_team_stats = raw_match_stats %>%
  select(game_id,
         date_GMT,
         starts_with("home_team"))
away_team_stats = raw_match_stats %>%
  select(game_id,
         date_GMT,
         starts_with("away_team"))
# rename "home_team" and "away_team" columns
home_team_stats = rename_with(home_team_stats, ~gsub("home_team_", "", .x))
away_team_stats = rename_with(away_team_stats, ~gsub("away_team_", "", .x))
# Stack these two datasets so that each row is the stats for a team for one match (team_stats_per_match). 
team_stats_per_match = home_team_stats %>%
  bind_rows(away_team_stats)
```

```{r}
# At each row of this dataset, get the team name, find the stats for that team during the last 5 matches, and average these stats (avg_stats_per_team). 
avg_stats_per_team <- team_stats_per_match %>%
  group_by(name) %>%
  filter(n() > 1) %>%     # remove countries with only 1 match
  arrange(date_GMT) %>%
  mutate_at(
  vars(
  goal_count,
  corner_count,
  shots,
  shots_on_target,
  fouls,
  possession
  ),
  ## Columns for which we want a rolling mean
  .funs = ~ runmean(
  x = dplyr::lag(.x),
  k = 5,
  endrule = "mean",
  align = "right"
  )## Rolling mean for last 5 matches
  ) %>%
  rename(
  goals_per_match = goal_count,
  corners_per_match = corner_count,
  shots_per_match = shots,
  shotsOnTarget_per_match = shots_on_target,
  fouls_per_match = fouls,
  possession_per_match = possession
  )
```

#### Reshape average pre-match stats

Now that we have the average stats for each team going into every match, we can create a dataset similar to the raw_match_stats, where each row represents both teams from one match.

1. Re-segment the home and away teams (name Team 1 and Team 2 rather than home and away).
2. Combine at each match to get a dataset with a row representing each match.

```{r}
# Add these stats to the home/away dataset
home_team_stats <- home_team_stats %>% 
  left_join(avg_stats_per_team)  %>%
  arrange(game_id) %>%
  rename_with(~paste0("team_1_", .))
away_team_stats <- away_team_stats %>% 
  left_join(avg_stats_per_team)  %>%
  arrange(game_id) %>%
  rename_with(~paste0("team_2_", .))
```

```{r}
# Combine at each match to get a dataset with a row representing each match. 
# drop the NA rows ( earliest match for each team, i.e no previous stats)
match_stats = home_team_stats %>%
  bind_cols(away_team_stats) %>%
  drop_na()
```

#### Find the difference of stats between teams
In our ML model, we will take the difference between Team 1 and Team 2 average stats as features. 6 new columns are created for this.

*Would we be better off using the raw stats for each team as features?*

*Can we generate any other useful features from the dataset provided?*

*Do we need to weigh the home and away teams because home teams win more often?*

```{r}
# create columns with average stat differences between the two teams
match_stats = match_stats %>%
  mutate(goals_per_match_diff = team_1_goals_per_match - team_2_goals_per_match,
         corners_per_match_diff = team_1_corners_per_match - team_2_corners_per_match,
         shots_per_match_diff = team_1_shots_per_match - team_2_shots_per_match,
         shotsOnTarget_per_match_diff = team_1_shotsOnTarget_per_match - team_2_shotsOnTarget_per_match,
         fouls_per_match_diff = team_1_fouls_per_match - team_2_fouls_per_match,
         possession_per_match_diff = team_1_possession_per_match - team_2_possession_per_match)
```

```{r}
match_stats
```

---
## Train ML model

In this tutorial we will:

1. Train a model using 6 feature columns
2. Use an 80/20 split in training/test data
3. Use accuracy to evaluate our models

*It's probably worth evaluating multiple models (several models explained in this tutorial), perhaps use k-fold cross validation, and use metrics other than accuracy to evaluate a model (check the commented out code).*

```{r}
library(tidymodels)
library(discrim)
library(kknn) # kknn
library(kernlab) # svm
library(naivebayes) #naive bayes
library(rpart) # decision tree
library(nnet) # logistic regression and neural net
library(ranger) # random forest (modified by multiclass)
library(xgboost) # xgboost
```

---
## Get data from our dataset

1. Team_1_result column - target variable
2. The difference of stats between teams (6 columns) - features

*Do we need to scale or normalize the feature columns in order for it to make mathematical sense to a ML model? This depends on the type of model we are training, but it's definitely worth investigating in order to achieve a high performing model.*

*We should also investigate the dataset to check if it's balanced on all classes or if it's skewed towards a particular class (i.e are there an equal number of wins, losses and draws?). If not, would this affect model performance?*

```{r}
# form a dataset with only target and features
model_data = match_stats %>%
  mutate(target = factor(recode(team_1_result, W = 0, D = 1, L = 2))) %>%
  select(
    target,
    goals_per_match_diff,
    corners_per_match_diff,
    shots_per_match_diff,
    shotsOnTarget_per_match_diff,
    fouls_per_match_diff,
    possession_per_match_diff
  )
```

#### Split test and training data

We train a model on the training data, and then use test data to evaluate the performance of that model.

```{r}
# For more details of using tidymodels package, check https://www.tidymodels.org/
# split test and train data
set.seed(2021)
data_split <- initial_split(model_data, strata = target, prop = 0.8)
# create a recipe for data pre-processing
model_recipe <- 
  recipe(target ~ ., data = model_data) %>%
  step_zv(all_predictors())  %>%
  step_corr(all_predictors()) %>%
  prep()
```

#### Name and define classifiers


```{r}
# Define the models
## knn model
knn_model <- 
  nearest_neighbor() %>% 
  set_engine("kknn") %>% 
  set_mode("classification")
## svm model
svm_model <- 
  svm_rbf() %>%
  set_engine("kernlab") %>%
  set_mode("classification") 
## logistic regression model
lr_model <- 
  multinom_reg() %>% 
  set_engine("nnet") %>% 
  set_mode("classification")
## naive bayes
nb_model <- 
  naive_Bayes() %>% 
  set_engine("naivebayes") %>% 
  set_mode("classification")
## decision tree model
tree_model <- 
  decision_tree() %>% 
  set_engine("rpart") %>% 
  set_mode("classification")
# random forest
rf_model <- 
  rand_forest() %>% 
  set_engine("ranger") %>% 
  set_mode("classification")
# boosted tree (xgboost)
xgb_model <- 
  boost_tree() %>% 
  set_engine("xgboost") %>% 
  set_mode("classification")
# single layer neural network
nn_model <- 
  mlp() %>% 
  set_engine("nnet") %>% 
  set_mode("classification")
```

#### Iterate through all classifiers and get their accuracy score

We can use the best performing model to make our predictions.

*There are several other metrics in the code that have been commented out which might provide helpful insights on model performance.*

```{r}
accuracy_results <-
  map_dfr(
    .x = list(knn_model,
              lr_model,
              nb_model,
              nn_model,
              rf_model,
              svm_model,
              tree_model,
              xgb_model),
    .f = function(the_model) {
      # create a work flow with recipe and model
      the_workflow <- workflow() %>%
        add_recipe(model_recipe) %>%
        add_model(the_model)
      
      # fit the model with training data and evaluate with test data
      the_fit <- the_workflow %>%
        last_fit(data_split)
      
      tibble(model_name = class(the_model)[1],
             accuracy = the_fit %>% collect_metrics() %>% filter(.metric == "accuracy") %>% select(.estimate) %>% pull)
    }
  )
## Displaying accuracy of the models set in descending order
accuracy_results %>%
  arrange(desc(accuracy))
```

---
### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.