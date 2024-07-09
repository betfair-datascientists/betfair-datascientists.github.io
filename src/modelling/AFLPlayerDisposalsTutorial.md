# AFL Player Disposals Tutorial

There are many possible ways to bet on an AFL match. Whilst Handicaps, Total Points and Match Odds have long been the traditional ways to bet into AFL markets, 'Player Proposition' bets have become the next big thing in AFL wagering. Traditionally, Same Game Multis will have options to pick players to have at least XX disposals, however 'Player Disposal Line' markets have quickly shot-up to be the next biggest market on the Betfair Exchange with regards to AFL. 

A player disposal line will be set at XX.5 disposals which, in theory, has a 50% chance of being over or under the true disposal prediction. The punter then needs to decide when they think the line is right or not, and take a position on either side. This tutorial here will outline how we can use data freely available online to generate predictions for player disposals.

AFL Data is made available from the R package [fitzRoy](https://github.com/jimmyday12/fitzRoy) which requires installation of R and use of the Python R-emulator 'rpy2'. (Direct R code can also be used.) This package pulls data from four separate sites which all have similar data with only a few columns differing between each, however due to the differing ways these sources display team and player names, matching between them can be painful. For the purposes of this tutorial we will use the 'fryzigg' function in fitzRoy which pulls data from [Squiggle](https://squiggle.com.au/), a renowned site for AFL modellers.

## Requirements

- A code editor with Jupyter Notebook functionality (e.g. VS Code)
- Python and R installations

## Downloading Historic Data

```py title="Downloading data using rpy2 and fitzRoy"

import os
import rpy2.situation
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import pandas as pd

# Set the R_HOME environment variable to the path of your R installation
# NOTE: You must have your R installation saved to your system PATH
os.environ['R_HOME'] = 'C:/Users/username/AppData/Local/Programs/R/R-43~1.0'

print(os.environ['R_HOME'])

# Load the necessary R packages 
# These must be installed to your R installation first
fitzRoy = importr('fitzRoy')
dplyr = importr('dplyr')


seasons = []

for i in range(2012,2024,1):
    seasons.append(i)

print(seasons)

api_queries = [
                #'footywire',
               'fryzigg',
               #'afl',
               #'afltables'
               ]

for api in api_queries:

    # Initialize an empty dataframe for storing the data
    robjects.r('this_season <- data.frame()')

    # Loop through each season and fetch the data
    for season in seasons:

        query = 'fetch_player_stats_'+api
        data = getattr(fitzRoy, query)(season=season, round_number=robjects.NULL)
        robjects.globalenv['data'] = data
        robjects.r('this_season <- dplyr::bind_rows(this_season, data)')

    # Retrieve the combined dataframe from R
    this_season = robjects.r('this_season')

    # Extract column names
    column_names = list(this_season.colnames)

    # Convert the R dataframe to a pandas dataframe
    this_season_df = pd.DataFrame(robjects.conversion.rpy2py(this_season))

    # Transpose the dataframe
    this_season_df = this_season_df.T

    # Set the correct column headers
    this_season_df.columns = column_names

    # Reset the index
    this_season_df.reset_index(drop=True, inplace=True)

    # Inspect the dataframe to ensure it's correctly oriented and headers are set
    print(this_season_df.head())

    # Save the dataframe to a CSV file
    this_season_df.to_csv(api+'.csv', index=False)

```

This is the R code to do the same function

```{R}
library(fitzRoy)
library(dplyr)

# Function to fetch data and write to CSV
fetch_and_save_data <- function(fetch_function, seasons, file_name) {
  all_data <- NULL
  for (season in seasons) {
    data <- fetch_function(season = season, round_number = NULL)
    all_data <- bind_rows(all_data, data)
  }
  write.csv(all_data, file_name)
}

# List of fetch functions and corresponding file names
fetch_functions <- list(
  fitzRoy::fetch_player_stats_afltables,
  fitzRoy::fetch_player_stats_footywire,
  fitzRoy::fetch_player_stats_fryzigg,
  fitzRoy::fetch_player_stats_afl
)

file_names <- c('afltables.csv', 'footywire.csv', 'fryzigg.csv', 'afl.csv')

seasons <- 2012:2024

# Loop over fetch functions and file names
for (i in seq_along(fetch_functions)) {
  fetch_and_save_data(fetch_functions[[i]], seasons, file_names[i])
}

```

## Processing the data

Here we will load our csv file from the fryzigg function into a pandas dataframe for processing. 

```py title="Loading our historical data"

import pandas as pd

afl_data = pd.read_csv('fryzigg.csv',low_memory=False)

afl_data = afl_data[[
                                    'venue_name',
                                    'match_id',
                                    'match_home_team',
                                    'match_away_team',
                                    'match_date',
                                    'match_round',
                                    'match_home_team_score',
                                    'match_away_team_score',
                                    'match_margin',
                                    'match_winner',
                                    'match_weather_temp_c',
                                    'match_weather_type',
                                    'player_id',
                                    'player_first_name',
                                    'player_last_name',
                                    'player_team',
                                    'kicks',
                                    'marks',
                                    'handballs',
                                    'disposals',
                                    'effective_disposals',
                                    'disposal_efficiency_percentage',
                                    'goals',
                                    'behinds',
                                    'hitouts',
                                    'tackles',
                                    'rebounds',
                                    'inside_fifties',
                                    'clearances',
                                    'clangers',
                                    'free_kicks_for',
                                    'free_kicks_against',
                                    'contested_possessions',
                                    'uncontested_possessions',
                                    'contested_marks',
                                    'marks_inside_fifty',
                                    'one_percenters',
                                    'bounces',
                                    'goal_assists',
                                    'time_on_ground_percentage',
                                    'afl_fantasy_score',
                                    'centre_clearances',
                                    'stoppage_clearances',
                                    'score_involvements',
                                    'metres_gained',
                                    'turnovers',
                                    'intercepts',
                                    'tackles_inside_fifty',
                                    'contest_def_losses',
                                    'contest_def_one_on_ones',
                                    'contest_off_one_on_ones',
                                    'contest_off_wins',
                                    'def_half_pressure_acts',
                                    'effective_kicks',
                                    'f50_ground_ball_gets',
                                    'ground_ball_gets',
                                    'hitouts_to_advantage',
                                    'intercept_marks',
                                    'marks_on_lead',
                                    'pressure_acts',
                                    'rating_points',
                                    'ruck_contests',
                                    'score_launches',
                                    'shots_at_goal',
                                    'spoils'
                                    ]]

# This creates an unedited copy of the dataframe that will be used for calculating player level data
player_data = afl_data.copy()                                

```

All the data here is split out by player, however, it is clear to anyone that watches AFL, a player's disposal count very much depends on the performance of the whole team. A defender will get a higher number of disposals if the team concedes a lot of forward 50 entries and a lower number if they don't. Here we will apply some functions to group this data by team, both for and against, and then concatenate it with the players individual data before we generate our features ready for training

```py title="Processing the data"

afl_data.rename(columns={'venue_name':'match_venue'}, inplace=True)

# List of columns to calculate the sum for
columns_to_sum = ['kicks', 'marks', 'handballs', 'disposals', 'effective_disposals', 'hitouts', 'tackles', 'rebounds', 'inside_fifties', 'clearances', 'clangers', 'free_kicks_for', 'free_kicks_against', 'contested_possessions', 'uncontested_possessions', 'contested_marks', 'marks_inside_fifty', 'one_percenters', 'bounces', 'goal_assists', 'centre_clearances', 'stoppage_clearances', 'score_involvements', 'metres_gained', 'turnovers', 'intercepts', 'tackles_inside_fifty', 'contest_def_losses', 'contest_def_one_on_ones', 'contest_off_one_on_ones', 'contest_off_wins', 'def_half_pressure_acts', 'effective_kicks', 'f50_ground_ball_gets', 'ground_ball_gets', 'hitouts_to_advantage', 'intercept_marks', 'marks_on_lead', 'pressure_acts', 'score_launches', 'shots_at_goal', 'spoils']

# Calculate sum for each column separately
sum_by_column = {}
for column in columns_to_sum:
    sum_by_column[column] = afl_data.groupby(['match_id', 'player_team'])[column].sum()

# Convert the dictionary to DataFrame
sum_df = pd.DataFrame(sum_by_column)

sum_df = sum_df.add_prefix('team_')

team_data = afl_data[[
                                    'match_venue',
                                    'match_id',
                                    'player_team',
                                    'match_date',
                                    'match_round',
                                    'match_winner',
                                    'match_home_team_score',
                                    'match_away_team_score',
                                    'match_margin',
                                    'match_weather_temp_c',
                                    'match_weather_type',
                                    'match_home_team',
                                    'match_away_team'
                                    ]]
team_data = team_data.drop_duplicates()
team_data = pd.merge(team_data,sum_df,how='left',on=['match_id','player_team'])

def home_away(row):
    if row['match_away_team'] == row['player_team']:
        return 'AWAY'
    else:
        return 'HOME'
    
team_data['home_away'] = team_data.apply(home_away, axis=1)
team_data.drop(columns=['player_team'],inplace=True)

home_team_data_score_data = team_data[team_data['home_away'] == 'HOME']

# Add suffix '_against' to column names that do not begin with 'match_'
for col in home_team_data_score_data.columns:
    if not col.startswith('match_'):
        home_team_data_score_data.rename(columns={col: col + '_for'}, inplace=True)

home_team_data_concede_data = team_data[team_data['home_away'] == 'AWAY']
home_team_data_concede_data.drop(columns=['match_venue',
                                    'match_date',
                                    'match_round',
                                    'match_winner',
                                    'match_home_team_score',
                                    'match_away_team_score',
                                    'match_margin',
                                    'match_weather_temp_c',
                                    'match_weather_type',
                                    'home_away'],inplace=True)


# Add suffix '_against' to column names that do not begin with 'match_'
for col in home_team_data_concede_data.columns:
    if not col.startswith('match_'):
        home_team_data_concede_data.rename(columns={col: col + '_against'}, inplace=True)

home_team_data = pd.merge(home_team_data_score_data,home_team_data_concede_data,how='left',on=['match_id','match_home_team','match_away_team'])
home_team_data.rename(columns={'match_home_team_score':'team_points_for',
                               'match_away_team_score':'team_points_against',
                               'match_home_team':'match_team',
                               'match_away_team':'match_opponent'}, inplace= True)

away_team_data_score_data = team_data[team_data['home_away'] == 'AWAY']

# Add suffix '_against' to column names that do not begin with 'match_'
for col in away_team_data_score_data.columns:
    if not col.startswith('match_'):
        away_team_data_score_data.rename(columns={col: col + '_for'}, inplace=True)

away_team_data_concede_data = team_data[team_data['home_away'] == 'HOME']
away_team_data_concede_data.drop(columns=['match_venue',
                                    'match_date',
                                    'match_round',
                                    'match_winner',
                                    'match_home_team_score',
                                    'match_away_team_score',
                                    'match_margin',
                                    'match_weather_temp_c',
                                    'match_weather_type',
                                    'home_away'],inplace=True)

# Add suffix '_against' to column names that do not begin with 'match_'
for col in away_team_data_concede_data.columns:
    if not col.startswith('match_'):
        away_team_data_concede_data.rename(columns={col: col + '_against'}, inplace=True)

away_team_data = pd.merge(away_team_data_score_data,away_team_data_concede_data,how='left',on=['match_id','match_home_team','match_away_team'])
away_team_data.rename(columns={'match_home_team_score':'team_points_against',
                               'match_away_team_score':'team_points_for',
                               'match_home_team':'match_opponent',
                               'match_away_team':'match_team'}, inplace= True)

afl_data = pd.concat([home_team_data,away_team_data])
afl_data = afl_data[afl_data['team_spoils_for'] > 0]

stat_names = set('_'.join(col.split('_')[1:-1]) for col in afl_data.columns if col.startswith('team_') and (col.endswith('_for') or col.endswith('_against')))

# Calculate the difference and create new columns
for stat in stat_names:
    for_or_against = ['for', 'against']
    for col_suffix in for_or_against:
        col_name = f'team_{stat}_{col_suffix}'
        if col_name in afl_data.columns:
            for_or_against_value = afl_data[f'team_{stat}_{col_suffix}']
            against_col_name = f'team_{stat}_against' if col_suffix == 'for' else f'team_{stat}_for'
            against_value = afl_data[against_col_name]
            diff_col_name = f'team_{stat}_diff'
            afl_data[diff_col_name] = for_or_against_value - against_value

afl_data.to_csv('afl_data.csv',index=False)

```

## Home Ground Advantage

The next section here will be very prescriptive in how we define home ground advantage and neutral grounds. There are instances where a team will play another team at a venue that they both share as home ground and so true home ground advantage is lost (i.e. Richmond v Collingwood at the MCG), and so it may make sense for the purposes of the model to define both of these teams as being home teams (in terms of crowd, travel and ground dimensions). Additionally, we will define a function that calls out as neutral, grounds for which neither team is the home team.

### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.