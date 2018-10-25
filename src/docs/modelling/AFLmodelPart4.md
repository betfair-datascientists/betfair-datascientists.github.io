# AFL Modelling Walkthrough 

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