# How To Build A Betfair Soccer Bot Part 3

This is a continuation of the tutorial - [How To Build A Betfair Soccer Bot Part 2](../modelling/howToBuildASoccerBotPartII.md)

**"I've done my simulations, now how I use it to bet with?"**

The previous tutorial describes how to run simulations on historical stream files using what I call a "shotgun" approach; where we bet on everything (both backing and laying). This part will walkthrough how to analyse the simulation results to determine a profitable angle.

## Is there still profit to be made betting English Premier League?

It's no secret that English Premier League is likely the most modelled sports league in existence but that doesn't mean the markets are 100% efficient on Betfair or elsewhere. There are many theories on why this might be, one being that some punters take positions preplay with the intent to trade inplay. Australian customers aren't allowed to bet inplay without calling up, and even leaving bets inplay may not work in a trading sense due to the voiding of matched bets in the case of a VAR review leaving positions exposed.

However, these trading punters may prioritise flexibility for inplay trading rather than seeking the most efficient preplay prices, creating minor inefficiencies in the preplay market. As a result, preplay money may not fully reflect true probabilities, leaving gaps for value betting. Even a simple model that doesn’t use player-specific information, like the one we've created, can still find an edge by capitalising on these inefficiencies.

## Grouping selections

To do this, we'll need to group selections together so as not to overfit. For market like Over/Under 1.5 Goals, the selection names are always the same and so this is straightforward but for any market where the team name is in the selection id, we'd want to group the selections together using a different characteristic related to each selection. In racing, this might be by grouping together runners by barrier groups, whereas in sports this is usually by utilising the home/away status of each team. In the Match Odds markets, there may not be enough information to accurately determine how good we are at predicting Arsenal but by grouping together we can look at our Home Team bets as a group rather than just a single team.

So the next code block will process our simulation results and initiate a selection grouping column where we can apply changes depending on the home/away status of the team and the market type. Once we've grouped together our markets we'll create some graphs that chart profitability against implied value of our rated price against the price at which we placed our bets. Ideally, we'd like to be able to make profit at any price, but overall that isn't realistic, so we might find that we'll have to introduce some **"edge limits"** to specify where we might not bet at all, depending on the price available in the market.

```py title="Grouping Results and creating graphs"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
Here we will initialise a new column called 'selection_group' as a copy of 'selection' and then
apply changes to this column based on our groups.

For Correct Score & Half Time Score markets we will group scores based on whether the score indicates
a home win, away win or a draw, and additionally treat 0-0 scorelines separately as these
selections behave differently again.

For markets like Match Odds and Handicap (e.g. 'TEAM_A_1'), we will identify the home and away
teams from the event name and compare to whether the team name is contained with the selection name

Finally we will generate a series of graphs using pyplot to visualise these profitability curves
and identify where we might place bets to our gain

'''

models = ['ensemble']

# Define common conditions for simplification
home_team_win = ['1&0', '2&1', '2&0', '3&0', '3&1', '3&2', 'Any Other Home Win']
away_team_win = ['0&1', '1&2', '0&2', '0&3', '1&3', '2&3', 'Any Other Away Win']
draw_results = ['1&1', '2&2', '3&3', 'Any Other Draw', 'The Draw']

for model in models:
    print(f'Processing {model}')
    # Load the CSV file with specified data types
    df = pd.read_csv(destination+f'soccer_simulation_{model}_processed.csv')

    # Filter data based on implied values
    df = df[(df[f'{model}_implied_value'] > -0.3) & (df[f'{model}_implied_value'] < 0.3)]

    # Extract home and away teams
    df[['home_team', 'away_team']] = df['fixture'].str.split(' v ', expand=True)
    
    # Initialize the 'selection_group' column with default values
    df['selection_group'] = df['selection'].str.replace(r'/','-')

    # Home win related conditions
    df.loc[
        (df['market_type'].isin(['CORRECT_SCORE', 'HALF_TIME_SCORE', 'HALF_TIME', 'DRAW_NO_BET', 'MATCH_ODDS']) & 
        (df['selection'].isin(home_team_win) | (df['home_team'] == df['selection']))) |
        (df['market_type'].str.contains('TEAM_A') & df['selection'].str.contains(r'\+')) |
        (df['market_type'].str.contains('TEAM_B') & df['selection'].str.contains('-')),
        'selection_group'
    ] = 'Home'

    # Away win related conditions
    df.loc[
        (df['market_type'].isin(['CORRECT_SCORE', 'HALF_TIME_SCORE', 'HALF_TIME', 'DRAW_NO_BET', 'MATCH_ODDS']) & 
        (df['selection'].isin(away_team_win) | (df['away_team'] == df['selection']))) |
        (df['market_type'].str.contains('TEAM_B') & df['selection'].str.contains(r'\+')) |
        (df['market_type'].str.contains('TEAM_A') & df['selection'].str.contains('-')),
        'selection_group'
    ] = 'Away'

    # Draw related conditions
    df.loc[
        df['market_type'].isin(['CORRECT_SCORE', 'HALF_TIME_SCORE', 'HALF_TIME', 'MATCH_ODDS']) & 
        df['selection'].isin(draw_results),
        'selection_group'
    ] = 'Draw'

    # Half-Time/Full-Time related conditions
    df.loc[
        df['market_type'] == 'HALF_TIME_FULL_TIME',
        'selection_group'
    ] = df.apply(lambda row: 
        'Home-Draw' if row['selection'].startswith(row['home_team']) and 'Draw' in row['selection'] else
        'Home-Home' if row['selection'].startswith(row['home_team']) and row['selection'].endswith(row['home_team']) else
        'Home-Away' if row['selection'].startswith(row['home_team']) else
        'Away-Draw' if row['selection'].startswith(row['away_team']) and 'Draw' in row['selection'] else
        'Away-Away' if row['selection'].startswith(row['away_team']) and row['selection'].endswith(row['away_team']) else
        'Away-Home' if row['selection'].startswith(row['away_team']) else
        'Draw-Home' if 'Draw' in row['selection'] and row['selection'].endswith(row['home_team']) else
        'Draw-Away' if 'Draw' in row['selection'] and row['selection'].endswith(row['away_team']) else
        row['selection_group'],
        axis=1
    )

    # Match Odds and BTTS conditions
    df.loc[
        df['market_type'] == 'MATCH_ODDS_AND_BTTS',
        'selection_group'
    ] = df.apply(lambda row: 
        'Away-Yes' if row['selection'].startswith(row['away_team']) and 'Yes' in row['selection'] else
        'Away-No' if row['selection'].startswith(row['away_team']) and 'No' in row['selection'] else
        'Home-Yes' if row['selection'].startswith(row['home_team']) and 'Yes' in row['selection'] else
        'Home-No' if row['selection'].startswith(row['home_team']) and 'No' in row['selection'] else
        row['selection_group'],
        axis=1
    )

    # Match Odds and OU conditions
    df.loc[
        df['market_type'].str.contains('MATCH_ODDS_AND_OU'),
        'selection_group'
    ] = df.apply(lambda row: 
        'Home-Over' if row['home_team'] in row['selection'] and 'Over' in row['selection'] else
        'Home-Under' if row['home_team'] in row['selection'] and 'Under' in row['selection'] else
        'Away-Over' if row['away_team'] in row['selection'] and 'Over' in row['selection'] else
        'Away-Under' if row['away_team'] in row['selection'] and 'Under' in row['selection'] else
        'Draw-Over' if 'Draw' in row['selection'] and 'Over' in row['selection'] else
        'Draw-Under' if 'Draw' in row['selection'] and 'Under' in row['selection'] else
        row['selection_group'],
        axis=1
    )

    df.to_csv(destination+f'soccer_simulation_{model}_grouped.csv')

    # Iterate over each unique combination of 'market_type' and 'side' and 'selection_group'
    for (market_type, side, selection_group), group_df in df.groupby(['market_type', 'side','selection_group']):

        # Drop rows where 'col' or 'profit' is NaN
        group_df = group_df.dropna(subset=[f'{model}_implied_value', 'profit'])

        # Sort by the column in ascending order
        group_df_sorted = group_df.sort_values(by=f'{model}_implied_value', ascending=True)
        
        # Calculate cumulative sum of 'profit'
        group_df_sorted['cumulative_profit'] = group_df_sorted['profit'].cumsum()

        # Find the index of the maximum cumulative profit
        max_index = group_df_sorted['cumulative_profit'].idxmax()
        max_value = group_df_sorted.loc[max_index, 'cumulative_profit']
        max_x_value = group_df_sorted.loc[max_index, f'{model}_implied_value']

        # Plot the cumulative sum with increased figure size
        fig, ax = plt.subplots(figsize=(12, 8))  # Increase the figure size (width x height in inches)
        ax.plot(group_df_sorted[f'{model}_implied_value'], group_df_sorted['cumulative_profit'], label=f'Cumulative Profit ({market_type}, {side}, {selection_group})')
        ax.set_xlabel(f'{model}_implied_value')
        ax.set_ylabel('Cumulative Profit')
        ax.set_title(f'{f'{model}_implied_value'}: Cumulative Profit for {market_type} and {side} and {selection_group}')
        ax.legend()

        # Add a horizontal line at y=0
        ax.axhline(y=0, color='red', linestyle='--', linewidth=1)  # Red dashed line at y=0

        # Set x-ticks to show a maximum of 10 ticks
        num_ticks = min(len(group_df_sorted[f'{model}_implied_value']), 10)
        ticks = np.linspace(group_df_sorted[f'{model}_implied_value'].min(), group_df_sorted[f'{model}_implied_value'].max(), num_ticks)
        ax.set_xticks(ticks)

        # Add text annotations for maximum and filtered minimum x-values
        text_annotation_max = f"Max Profit: {max_value:.2f}\nAt {f'{model}_implied_value'}: {max_x_value:.4f}"
        ax.text(
            0.95, 0.05,  # Position in relative coordinates (x, y) where (0, 0) is bottom-left and (1, 1) is top-right
            text_annotation_max,
            transform=ax.transAxes,  # Transform coordinates to relative plot area
            fontsize=12,
            verticalalignment='bottom',
            horizontalalignment='right',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        )

        # Save the plot as a JPEG file
        filename = destination+f"{market_type}_{side}_{selection_group}_{model}_cumulative_profit.jpeg"
        print(f'Saving {filename}')
        plt.savefig(filename, format='jpeg')
        plt.close()

```

This image here is an example of a market where we could theoretically bet at any price and make a profit

![BOTH_TEAMS_TO_SCORE](../img/BOTH_TEAMS_TO_SCORE_BACK_Yes_ensemble_cumulative_profit.jpeg)

This image here is a market type and grouping where we would need to input an edge limit

![HALF_TIME_RESULT](../img/HALF_TIME_BACK_Home_ensemble_cumulative_profit.jpeg)

Once we've identified our edge from our graphs, then in order to bet these edges, we'll need to be able to generate new rated prices for upcoming matches, and then feed our rated prices into our live (not simulation) flumine class for the upcoming matches. We will start by using the EPL competition ID to find upcoming matches, update our dataset and perform the rolling window calculations

```py title="Boilerplate code"

'''
Here's our boilerplate code again to ensure all the required packages are imported and variables defined
'''

# Import libraries
import pandas as pd
from datetime import datetime,timedelta
import numpy as np
import pickle
import betfairlightweight
import json

import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

# Specify destination for files
destination = 'C:/Users/motykam/OneDrive - Betfair Pty Ltd/Documents/Scripts/Soccer-Goals-Model/'

# Set a list of important columns to keep
column_list = ['date','name','match_id','home_or_away']

# Specify column lists to use later
MATCH_INFO_COLUMNS = ['date_home','match_id','name_home','name_away','goalsScored_home','goalsScored_away','halfTimeGoalsScored_home','halfTimeGoalsScored_away']
DROP_COLUMNS = ['home_or_away_home','date_away','home_or_away_away','goalsConceded_home','goalsConceded_away','halfTimeGoalsConceded_home','halfTimeGoalsConceded_away']

# Define model weights (these should sum to 1 for proper ensembling)
model_weights = {'GradientBoostingClassifier': 0.25, 
                 'RandomForestClassifier': 0.25,
                 'LGBMClassifier': 0.25,
                 'KNeighborsClassifier': 0.15,
                 'LogisticsRegression': 0.1}

model_names = ["KNeighborsClassifier", "LogisticsRegression", "RandomForestClassifier", "GradientBoostingClassifier","LGBMClassifier"]

prefixes = ['home','away']
suffixes = ['','_ht']

new_column_names = []

```

```py title="Pull upcoming EPL Matches"

'''
This function here will login to the Betfair API to find upcoming EPL matches, and then download required markets to a dataframe.
The streaming API doesn't support filtering on competition id so by gathering market_ids here we can just feed them into our streaming_market_filter later

We also generate additional rows to add to our dataset for upcoming matches to calculate the rolling figure calculations
It's important to ensure that your data is up-to-date
'''

def pull_upcoming_fixtures(days_ahead):

    with open("credentials.json") as f:
        cred = json.load(f)
        my_username = cred["username"]
        my_password = cred["password"]
        my_app_key = cred["app_key"]

    trading = betfairlightweight.APIClient(username=my_username,
                                        password=my_password,
                                        app_key=my_app_key
                                        )

    trading.login_interactive()

    # Define a market filter
    epl_event_filter = betfairlightweight.filters.market_filter(
        competition_ids=["10932509"],
        market_start_time={
            "to": (datetime.datetime.now() + datetime.timedelta(days=days_ahead)).strftime("%Y-%m-%dT%TZ")},
        market_type_codes=['BOTH_TEAMS_TO_SCORE','CORRECT_SCORE','DOUBLE_CHANCE','DRAW_NO_BET','FIRST_HALF_GOALS_05','FIRST_HALF_GOALS_15','FIRST_HALF_GOALS_25','HALF_TIME','HALF_TIME_FULL_TIME','HALF_TIME_SCORE','MATCH_ODDS','MATCH_ODDS_AND_BTTS','MATCH_ODDS_AND_OU_25','MATCH_ODDS_AND_OU_35','OVER_UNDER_05','OVER_UNDER_15','OVER_UNDER_25','OVER_UNDER_35','OVER_UNDER_45','TEAM_A_1','TEAM_A_OVER_UNDER_05','TEAM_A_OVER_UNDER_15','TEAM_A_OVER_UNDER_25','TEAM_A_WIN_TO_NIL','TEAM_B_1','TEAM_B_OVER_UNDER_05','TEAM_B_OVER_UNDER_15','TEAM_B_OVER_UNDER_25','TEAM_B_WIN_TO_NIL']
        )

    # Get a list of all thoroughbred events as objects
    epl_events = trading.betting.list_market_catalogue(
        filter=epl_event_filter,
        market_projection=['EVENT','MARKET_DESCRIPTION'],
        max_results=200 
    )

    # Create a DataFrame with all the events by iterating over each event object
    epl_events_upcoming = pd.DataFrame({
        "event_name": [market_cat_object.event.name for market_cat_object in epl_events],
        "event_id": [market_cat_object.event.id for market_cat_object in epl_events],
        "open_date": [market_cat_object.event.open_date for market_cat_object in epl_events],
        "market_name": [market_cat_object.market_name for market_cat_object in epl_events],
        "market_id": [market_cat_object.market_id for market_cat_object in epl_events],
        "market_type" : [market_cat_object.description.market_type for market_cat_object in epl_events]
    })

    # Remove daily goals and matches too far ahead
    epl_events_upcoming = epl_events_upcoming[epl_events_upcoming["event_name"].str.contains(" v ", case=False, na=False)]

    # Find the maximum match_id from our existing dataset
    existing_df = pd.read_csv("englishPremierLeague.csv")
    max_match_id = existing_df["match_id"].max()

    upcoming_fixtures = epl_events_upcoming[["open_date","event_name"]]
    upcoming_fixtures.drop_duplicates(inplace=True)

    # Create the new DataFrame
    upcoming_matches = pd.DataFrame({
        "date": upcoming_fixtures["open_date"].dt.date,
        "match_id": range(max_match_id + 1, max_match_id + 1 + len(upcoming_fixtures)), 
        "home_team_name": upcoming_fixtures["event_name"].str.split(" v ").str[0], 
        "away_team_name": upcoming_fixtures["event_name"].str.split(" v ").str[1],
        "home_team_goal_count": 0,
        "away_team_goal_count": 0,
        "home_team_half_time_goal_count": 0,
        "away_team_half_time_goal_count": 0,
        "home_team_shots": 0,
        "away_team_shots": 0,
        "home_team_shots_on_target": 0,
        "away_team_shots_on_target": 0,
        "home_team_fouls": 0,
        "away_team_fouls": 0,
        "home_team_corner_count": 0,
        "away_team_corner_count": 0,
        "home_team_yellow": 0,
        "away_team_yellow": 0,
        "home_team_red": 0,
        "away_team_red": 0,
    })

    upcoming_matches['date'] = pd.to_datetime(upcoming_matches['date'])

    return epl_events_upcoming, upcoming_matches
```

```py title="Generate Future Rated Prices"
'''
This function pulls our previous functions for calculating the rolling windows and applies them again to the upcoming matches
'''
def generate_rolling_windows_upcoming(upcoming_matches):

    raw_match_stats = load_data()
    raw_match_stats = pd.concat([raw_match_stats,upcoming_matches])
    raw_match_stats = championshipPoints(raw_match_stats)
    team_match_stats = separate_home_and_away(raw_match_stats)
    team_match_stats = calculate_differential(team_match_stats)
    team_data_all_sorted, team_rolling_columns = calculate_rolling_median(team_match_stats)
    team_stats_rolling_dataframe = rejoin_home_away_data(team_data_all_sorted,column_list,team_rolling_columns)
    team_stats_rolling_dataframe,feature_columns = reshape_dataframe(MATCH_INFO_COLUMNS,DROP_COLUMNS,team_stats_rolling_dataframe)
    upcoming_matches_rolling_windows = team_stats_rolling_dataframe[team_stats_rolling_dataframe['date_home'] >= datetime.now() - timedelta(days=1)]

    return upcoming_matches_rolling_windows,feature_columns

'''
This function loads our pickle files and applies them to generate the class probabilities for the new matches
'''
def apply_models_to_new_data_with_ensemble(model_names, new_data, model_weights):
    # Separate match information and feature columns
    final_predictions = new_data[MATCH_INFO_COLUMNS]
    feature_data = new_data.drop(columns=MATCH_INFO_COLUMNS)

    for prefix in prefixes:

        for suffix in suffixes:

            # Initialize a list to hold the weighted predictions
            weighted_predictions = None
        
            # Loop over each model
            for model_name in model_names:
                # Load the model
                with open(f"{model_name}_{prefix}{suffix}.pickle", "rb") as file:
                    model = pickle.load(file)

                model_predictions = model.predict_proba(feature_data)
                
                # Weight the predictions by the model's weight
                if weighted_predictions is None:
                    weighted_predictions = model_predictions * model_weights.get(model_name, 0)
                else:
                    weighted_predictions += model_predictions * model_weights.get(model_name, 0)

            # Normalize the weighted predictions (to make sure they sum to 1 for each instance)
            weighted_predictions /= np.sum(list(model_weights.values()))

            # Add the ensemble predictions as new columns to the final DataFrame
            for i in range(weighted_predictions.shape[1]):
                final_predictions[f"{prefix}_{i}{suffix}"] = weighted_predictions[:, i]

    return final_predictions

'''
This function takes our class probabilities and then calculates the market rated prices
'''
def generate_rated_prices(goal_predictions):
    # List of indices representing the number of goals for which we want to calculate the probability
    full_time_indices = range(8) # 0,1,2,3,4,5,6,7
    half_time_indices = range(6) # 0,1,2,3,4,5

    # Generate new columns efficiently using vectorized operations
    for i in full_time_indices:
        for j in full_time_indices:
            home_col = f'home_{i}'
            away_col = f'away_{j}'
            new_col_name = f'{home_col}_x_{away_col}'
            goal_predictions[new_col_name] = goal_predictions[home_col].fillna(0) * goal_predictions[away_col].fillna(0)
            new_column_names.append(new_col_name)

    for i in half_time_indices:
        for j in half_time_indices:
            home_ht_col = f'home_{i}_ht'
            away_ht_col = f'away_{j}_ht'
            new_col_name = f'{home_ht_col}_x_{away_ht_col}'
            goal_predictions[new_col_name] = goal_predictions[home_ht_col].fillna(0) * goal_predictions[away_ht_col].fillna(0)
            new_column_names.append(new_col_name)

    # Final DataFrame with only the relevant columns (Match Information plus the probability of each scoreline)
    goal_predictions = goal_predictions[MATCH_INFO_COLUMNS + [col for col in goal_predictions.columns if '_x_' in col]]
    goal_predictions.to_csv('upcoming_scoreline_predictions.csv', index=False)

    rated_prices = process_model_predictions(goal_predictions)
    rated_prices.to_csv('upcoming_rated_prices.csv', index=False)

    return rated_prices

```

Now that we've generated our rated prices, lets go back to our simulation results to determine which markets we want to bet into, which selections and the minimum and maximum acceptable prices for which we'll bet. 

The below is an example of some market types, selections and value ranges that could be used to place bets.
Where we've determined that we don't need to set a value boundary, then we'll set the min/max prices to 1.01/1000.
If we do need to define a value boundary, we'll do the calculations individually for each market_type/selection_group

|Market Type|Selection Type|Side|Min EV|Max EV|
|--------------------|---------|----|-------|-------|
|BOTH_TEAMS_TO_SCORE|No|LAY|-|-|
|CORRECT_SCORE|0-0|LAY|-|-0.0325|
|CORRECT_SCORE|Away|LAY|-|0.08|
|CORRECT_SCORE|Home|BACK|-|0.08|
|CORRECT_SCORE|Draw|BACK|-|0|
|DOUBLE_CHANCE|Draw-Away|LAY|-|-|
|DOUBLE_CHANCE|Home-Draw|BACK|-0.08|0.11|
|DRAW_NO_BET|Away|LAY|-|0.02|
|FIRST_HALF_GOALS_05|Under 0.5 Goals|LAY|-|-|
|FIRST_HALF_GOALS_15|Under 1.5 Goals|LAY|-|-|
|FIRST_HALF_GOALS_25|Under 2.5 Goals|LAY|-|-|
|HALF_TIME_SCORE|0-0|LAY|-0.05|-|
|HALF_TIME_SCORE|Draw|BACK|-0.01|-|
|HALF_TIME_SCORE|Away|LAY|-0.07|0.11|
|HALF_TIME_FULL_TIME|Draw-Home|BACK|-0.06|-|
|HALF_TIME_FULL_TIME|Away-Away|LAY|-|-|
|MATCH_ODDS|Away|LAY|-|-|
|MATCH_ODDS|Home|BACK|-|-|
|MATCH_ODDS_AND_OU_25|Draw/Under|LAY|-|-|
|MATCH_ODDS_AND_OU_25|Home/Over|BACK|-0.05|-|
|OVER_UNDER_05|Under 0.5 Goals|LAY|-0.03|-|
|OVER_UNDER_15|Over 1.5 Goals|BACK|-0.05|0.1|
|OVER_UNDER_25|Over 2.5 Goals|BACK|-0.05|0.1|
|OVER_UNDER_35|Over 3.5 Goals|BACK|-0.05|0.1|
|OVER_UNDER_45|Over 4.5 Goals|BACK|-0.05|0.1|
|OVER_UNDER_55|Over 5.5 Goals|BACK|-0.05|0.1|
|TEAM_A_1|Home +1|BACK|-|-|
|TEAM_A_1|Draw|LAY|-|-|
|TEAM_A_OVER_UNDER_05|Over 0.5 Goals|BACK|-|0.07|
|TEAM_A_OVER_UNDER_15|Over 1.5 Goals|BACK|-0.05|-|
|TEAM_A_OVER_UNDER_25|Over 2.5 Goals|BACK|-0.05|-|
|TEAM_B_1|Draw|BACK|-|-|
|TEAM_B_1|Away|LAY|-|-|

```py title="Calculate Min/Max Prices for upcoming markets"

'''
This function will calculate our upper and lower price limits
'''

def set_min_max_prices(rated_prices,epl_events_upcoming):
    
    # Initialise certain columns as required with placeholder values
    rated_prices['home_team'] = rated_prices['fixture'].str.split(' v ').str[0]
    rated_prices['away_team'] = rated_prices['fixture'].str.split(' v ').str[1]
    rated_prices['min_price'] = 1.01
    rated_prices['max_price'] = 1000
    rated_prices['side'] = None

    df = pd.merge(rated_prices, epl_events_upcoming, how="left",left_on=["fixture","market_name"],right_on=["event_name","market_name"])
    df = df[['event_date',
                                            'home_team',
                                            'away_team',
                                            'fixture',
                                            'market_type',
                                            'market_name',
                                            'market_id',
                                            'runner_name',
                                            'rated_price',
                                            'min_price',
                                            'max_price',
                                            'side'
                                            ]]
    df = df.dropna(subset=['market_type'])

    # Set our side

    df.loc[
        (
            (df['market_type'].isin(['BOTH_TEAMS_TO_SCORE']) & df['runner_name'].isin(['No'])) |
            (df['market_type'].isin(['CORRECT_SCORE']) & df['runner_name'].isin(['0 - 0','0 - 1','0 - 2','0 - 3','1 - 2','1 - 3','2 - 3','Any Other Away Win'])) |
            (df['market_type'].isin(['DOUBLE CHANCE']) & df['runner_name'].isin(['Draw or Away'])) |
            (df['market_type'].isin(['DRAW_NO_BET']) & (df['runner_name'] == df['away_team'])) |
            (df['market_type'].isin(['FIRST_HALF_GOALS_05']) & df['runner_name'].isin(['Under 0.5 Goals'])) |
            (df['market_type'].isin(['FIRST_HALF_GOALS_15']) & df['runner_name'].isin(['Under 1.5 Goals'])) |
            (df['market_type'].isin(['FIRST_HALF_GOALS_25']) & df['runner_name'].isin(['Under 2.5 Goals'])) |
            (df['market_type'].isin(['HALF_TIME_SCORE']) & df['runner_name'].isin(['0 - 0','0 - 1','0 - 2','1 - 2'])) |
            (df['market_type'].isin(['MATCH_ODDS']) & (df['runner_name'] == df['away_team'])) |
            (df['market_type'].isin(['MATCH_ODDS_AND_OU_25']) & df['runner_name'].isin(['Draw/Under 2.5 Goals'])) |
            (df['market_type'].isin(['OVER_UNDER_05']) & df['runner_name'].isin(['Under 0.5 Goals'])) |
            (df['market_type'].isin(['TEAM_A_1']) & df['runner_name'].isin(['Draw']))
        ),
        'side'
    ] = 'LAY'

    df['side'] = df.apply(lambda row: 'LAY' if row['market_type'] == 'TEAM_B_1' and '+' in row['runner_name'] else row['side'], axis=1)
    df['side'] = df.apply(lambda row: 'LAY' if row['market_type'] == 'HALF_TIME_FULL_TIME' and row['runner_name'].count(row['away_team']) == 2 else row['side'], axis=1)

    df.loc[
        (
            (df['market_type'].isin(['CORRECT_SCORE']) & df['runner_name'].isin(['1 - 0','2 - 0','3 - 0','2 - 1','2 - 0','3 - 1','3 - 2','Any Other Home Win','1 - 1','2 - 2','3 - 3', 'Any Other Draw'])) |
            (df['market_type'].isin(['DOUBLE CHANCE']) & df['runner_name'].isin(['Home or Draw'])) |
            (df['market_type'].isin(['HALF_TIME_SCORE']) & df['runner_name'].isin(['1 - 1','2 - 2'])) |
            (df['market_type'].isin(['MATCH_ODDS']) & (df['runner_name'] == df['home_team'])) |
            (df['market_type'].isin(['OVER_UNDER_15']) & df['runner_name'].isin(['Over 1.5 Goals'])) |
            (df['market_type'].isin(['OVER_UNDER_25']) & df['runner_name'].isin(['Over 2.5 Goals'])) |
            (df['market_type'].isin(['OVER_UNDER_35']) & df['runner_name'].isin(['Over 3.5 Goals'])) |
            (df['market_type'].isin(['OVER_UNDER_45']) & df['runner_name'].isin(['Over 4.5 Goals'])) |
            (df['market_type'].isin(['OVER_UNDER_55']) & df['runner_name'].isin(['Over 5.5 Goals'])) |
            (df['market_type'].isin(['TEAM_A_OVER_05']) & df['runner_name'].isin(['Over 0.5 Goals'])) |
            (df['market_type'].isin(['TEAM_A_OVER_15']) & df['runner_name'].isin(['Over 1.5 Goals'])) |
            (df['market_type'].isin(['TEAM_A_OVER_25']) & df['runner_name'].isin(['Over 2.5 Goals'])) |
            (df['market_type'].isin(['TEAM_B_1']) & df['runner_name'].isin(['Draw']))
        ),
        'side'
    ] = 'BACK'

    df['side'] = df.apply(lambda row: 'BACK' if row['market_type'] == 'TEAM_A_1' and '+' in row['runner_name'] else row['side'], axis=1)
    df['side'] = df.apply(lambda row: 'BACK' if row['market_type'] == 'HALF_TIME_FULL_TIME' and 'Draw/' in row['runner_name'] and row['runner_name'].count(row['home_team']) == 1 else row['side'], axis=1)
    df['side'] = df.apply(lambda row: 'BACK' if row['market_type'] == 'MATCH_ODDS_AND_OU_25' and 'OVer' in row['runner_name'] and row['runner_name'].count(row['home_team']) == 1 else row['side'], axis=1)

    # Discard any markets/selections that we're not interested in
    df.dropna(subset=['side'],inplace=True)

    # Set any prices that we have limits for
    df['max_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 + 3.25 * row['rated_price'])
                        if row['market_type'] == 'CORRECT_SCORE' and row['runner_name'] == '0 - 0' else row['max_price'],axis=1)
    df['max_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 - 8 * row['rated_price'])
                        if row['market_type'] == 'CORRECT_SCORE' and row['runner_name'] in ['0 - 1','0 - 2','0 - 3','1 - 2','1 - 3','2 - 3','Any Other Away Win'] else row['max_price'],axis=1)
    df['max_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 - 8 * row['rated_price'])
                        if row['market_type'] == 'CORRECT_SCORE' and row['runner_name'] in ['1 - 0','2 - 0','3 - 0','2 - 1','3 - 1','3 - 2','Any Other Home Win'] else row['max_price'],axis=1)
    df['max_price'] = df.apply(lambda row: row['rated_price']
                        if row['market_type'] == 'CORRECT_SCORE' and row['runner_name'] in ['1 - 1','2 - 2','Any Other Draw'] else row['max_price'],axis=1)
    df['max_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 - 11 * row['rated_price'])
                        if row['market_type'] == 'DOUBLE_CHANCE' and row['runner_name'] == 'Home or Draw' else row['max_price'],axis=1)
    df['min_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 + 8 * row['rated_price'])
                        if row['market_type'] == 'DOUBLE_CHANCE' and row['runner_name'] == 'Home or Draw' else row['min_price'],axis=1)
    df['max_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 - 2 * row['rated_price'])
                        if row['market_type'] == 'DRAW_NO_BET' else row['max_price'],axis=1)
    df['min_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 + 5 * row['rated_price'])
                        if row['market_type'] == 'HALF_TIME_SCORE' and row['runner_name'] == '0 - 0' else row['min_price'],axis=1)
    df['min_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 + 1 * row['rated_price'])
                        if row['market_type'] == 'CORRECT_SCORE' and row['runner_name'] in ['1 - 1','2 - 2'] else row['min_price'],axis=1)
    df['max_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 - 11 * row['rated_price'])
                        if row['market_type'] == 'CORRECT_SCORE' and row['runner_name'] in ['0 - 1','0 - 2','1 - 2'] else row['max_price'],axis=1)
    df['min_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 + 7 * row['rated_price'])
                        if row['market_type'] == 'CORRECT_SCORE' and row['runner_name'] in ['0 - 1','0 - 2','1 - 2'] else row['min_price'],axis=1)
    df['min_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 + 6 * row['rated_price'])
                        if row['market_type'] == 'HALF_TIME_FULL_TIME' and 'Draw/' in row['runner_name'] and row['runner_name'].count(row['home_team']) == 1 else row['min_price'], axis=1)
    df['min_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 + 5 * row['rated_price']) 
                        if row['market_type'] == 'MATCH_ODDS_AND_OU_25' and 'OVer' in row['runner_name'] and row['runner_name'].count(row['home_team']) == 1 else row['min_price'], axis=1)
    df['min_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 + 3 * row['rated_price'])
                        if row['market_type'] == 'OVER_UNDER_05' else row['min_price'],axis=1)
    df['min_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 + 5 * row['rated_price'])
                        if row['market_type'] in ['OVER_UNDER_15','OVER_UNDER_25','OVER_UNDER_35','OVER_UNDER_45','OVER_UNDER_55'] else row['min_price'],axis=1)
    df['max_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 - 10 * row['rated_price'])
                        if row['market_type'] in ['OVER_UNDER_15','OVER_UNDER_25','OVER_UNDER_35','OVER_UNDER_45','OVER_UNDER_55'] else row['max_price'],axis=1)
    df['min_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 + 5 * row['rated_price'])
                        if row['market_type'] in ['OVER_UNDER_15','OVER_UNDER_25','OVER_UNDER_35','OVER_UNDER_45','OVER_UNDER_55'] else row['min_price'],axis=1)
    df['max_price'] = df.apply(lambda row: (100 * row['rated_price'])/(100 - 10 * row['rated_price'])
                        if row['market_type'] in ['OVER_UNDER_15','OVER_UNDER_25','OVER_UNDER_35','OVER_UNDER_45','OVER_UNDER_55'] else row['max_price'],axis=1)
    
    '''
    These calculations can result in negative values
    e.g. where we've set an upper boundary of 7% but the implied probability of the rated price is only 4%
    So we'll set any negative values to 1000
    '''
    df['max_price'] = df.apply(lambda row: 1000
                        if row['max_price'] < 0 else row['max_price'], axis=1)
    

    df.sort_values(by=['event_date','fixture','market_type','runner_name'],inplace=True)

    return df
```

```py title="Call functions"

# Call our functions to generate the dataframe for flumine
def generate_flumine_dataframe():
    epl_events_upcoming, upcoming_matches = pull_upcoming_fixtures(2)
    upcoming_matches_rolling_windows,feature_columns = generate_rolling_windows_upcoming(upcoming_matches)
    upcoming_matches_rolling_windows[feature_columns] = scaler.fit_transform(upcoming_matches_rolling_windows[feature_columns])
    goal_predictions = apply_models_to_new_data_with_ensemble(model_names, upcoming_matches_rolling_windows, model_weights)
    rated_prices = generate_rated_prices(goal_predictions)
    final_flumine_dataframe = set_min_max_prices(rated_prices,epl_events_upcoming)
    print(final_flumine_dataframe)

    return final_flumine_dataframe

final_flumine_dataframe = generate_flumine_dataframe()
final_flumine_dataframe.to_csv('flumine_dataframe_upcoming_matches.csv',index=False)

```

```py title="Define Flumine Strategy"
# Import libraries for logging in
import betfairlightweight
from flumine import Flumine, clients
import json
import pandas as pd
import os
import csv
import time

# Import libraries and logging
from flumine import BaseStrategy 
from flumine.order.trade import Trade
from flumine.order.order import MarketOnCloseOrder
from flumine.markets.market import Market
from betfairlightweight.filters import streaming_market_filter
from betfairlightweight.resources import MarketBook
from flumine.events.events import TerminationEvent
import logging
from datetime import datetime

from flumine.controls.loggingcontrols import LoggingControl
from flumine.order.ordertype import OrderTypes
from flumine.worker import BackgroundWorker

logging.basicConfig(filename = 'soccer_bot.log', level=logging.CRITICAL, format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

FIELDNAMES = [
    "bet_id",
    "strategy_name",
    "market_id",
    "selection_id",
    "trade_id",
    "date_time_placed",
    "price",
    "price_matched",
    "size",
    "size_matched",
    "profit",
    "side",
    "elapsed_seconds_executable",
    "order_status",
    "market_note",
    "trade_notes",
    "order_notes",
]

def bflw_trading():

    with open('credentials.json') as f:
        cred = json.load(f)
        username = cred['username']
        password = cred['password']
        app_key = cred['app_key']

    # Define the betfairlightweight client
    trading = betfairlightweight.APIClient(username, password, app_key=app_key)

    return trading

def process_runner_books(runner_books):
    # Grab the prices for each runner from the win market
    '''
    This function processes the runner books and returns a DataFrame with the best back/lay prices + vol for each runner
    :param runner_books:
    :return:
    '''
    
    best_back_prices = [runner_book.ex.available_to_back[0]['price']
        if runner_book.ex.available_to_back
        else 1.01
        for runner_book
        in runner_books]
    
    best_lay_prices = [runner_book.ex.available_to_lay[0]['price']
        if runner_book.ex.available_to_lay
        else 1000
        for runner_book
        in runner_books]
    
    selection_ids = [runner_book.selection_id for runner_book in runner_books]

    df = pd.DataFrame({
        'selection_id': selection_ids,
        'best_back_price': best_back_prices,
        'best_lay_price':best_lay_prices
    })
    return df

# Function to process the runner catalogue to gather all selection names
def process_runner_catalogue(market_book: MarketBook):

    runners_df = process_runner_books(market_book.runners)

    for runner in market_book.runners:
        runner_name = next((rd.name for rd in market_book.market_definition.runners if rd.selection_id == runner.selection_id), None)
        # rstrip() removes any trailing white spaces
        runners_df.loc[runner.selection_id, 'runner_name'] = runner_name.rstrip().title()

    return runners_df

def load_model_ratings():

    soccer_ratings = pd.read_csv('flumine_dataframe_upcoming_matches.csv')
    soccer_markets = soccer_ratings['market_id'].unique().tolist()

    return soccer_ratings, soccer_markets

class SoccerModel(BaseStrategy):

    def __init__(self, context, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = context

    def check_market_book(self, market: Market, market_book: MarketBook) -> bool:
        # process_market_book only executed if this returns True
        if market_book.status not in ["INPLAY","CLOSED"]:
            return True

    def process_market_book(self, market: Market, market_book: MarketBook) -> None:

        try:
            runners_df = process_runner_catalogue(market_book)
            runners_df['market_id'] = market.market_id
            market_df = pd.merge(runners_df,self.context['model_prices'],how="left",on=['market_id','runner_name'])
            market_df['selection_id'] = market_df['selection_id'].astype(int)
            market_df.set_index('selection_id',inplace=True)

            if market.seconds_to_start < 300 and not market_book.inplay:

                for runner in market_book.runners:

                    if market_df.loc[runner.selection_id, 'min_price'] == 'BACK':
                    
                        if market_df.loc[runner.selection_id, 'min_price'] <= market_df.loc[runner.selection_id, 'best_back_price'] and market_df.loc[runner.selection_id, 'max_price'] >= market_df.loc[runner.selection_id, 'best_back_price']:

                            if runner.selection_id in market_df.index:

                                trade = Trade(
                                    market_id=market_book.market_id,
                                    selection_id=runner.selection_id,
                                    handicap=runner.handicap,
                                    strategy=self,
                                )
                                order = trade.create_order(
                                    side="BACK",
                                    order_type=LimitOrder(
                                    price = market_df.loc[runner.selection_id, 'best_back_price'],
                                    size = round(100/market_df.loc[runner.selection_id, 'best_back_price'],2),
                                    persistence_type='LAPSE'
                                    )
                                )
                                market.place_order(order)
                        
                    if market_df.loc[runner.selection_id, 'min_price'] == 'LAY':
                    
                        if market_df.loc[runner.selection_id, 'min_price'] <= market_df.loc[runner.selection_id, 'best_back_price'] and market_df.loc[runner.selection_id, 'max_price'] >= market_df.loc[runner.selection_id, 'best_back_price']:

                            if runner.selection_id in market_df.index:

                                trade = Trade(
                                    market_id=market_book.market_id,
                                    selection_id=runner.selection_id,
                                    handicap=runner.handicap,
                                    strategy=self,
                                )
                                order = trade.create_order(
                                    side="LAY",
                                    order_type=LimitOrder(
                                    price = market_df.loc[runner.selection_id, 'best_back_price'],
                                    size = round(100/market_df.loc[runner.selection_id, 'best_back_price'],2),
                                    persistence_type='LAPSE'
                                    )
                                )
                                market.place_order(order)
        
        except AttributeError:
            pass

class LiveLoggingControl(LoggingControl):
    NAME = "BACKTEST_LOGGING_CONTROL"

    def __init__(self, *args, **kwargs):
        super(LiveLoggingControl, self).__init__(*args, **kwargs)
        self._setup()

    def _setup(self):
        if os.path.exists("soccer_model.csv"):
            logging.info("Results file exists")
        else:
            with open("soccer_model.csv", "w") as m:
                csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                csv_writer.writeheader()

    def _process_cleared_orders_meta(self, event):
        orders = event.event
        with open("soccer_model.csv", "a") as m:
            for order in orders:
                if order.order_type.ORDER_TYPE == OrderTypes.LIMIT:
                    size = order.order_type.size
                else:
                    size = order.order_type.liability
                if order.order_type.ORDER_TYPE == OrderTypes.MARKET_ON_CLOSE:
                    price = None
                else:
                    price = order.order_type.price
                try:
                    order_data = {
                        "bet_id": order.bet_id,
                        "strategy_name": order.trade.strategy,
                        "market_id": order.market_id,
                        "selection_id": order.selection_id,
                        "trade_id": order.trade.id,
                        "date_time_placed": order.responses.date_time_placed,
                        "price": price,
                        "price_matched": order.average_price_matched,
                        "size": size,
                        "size_matched": order.size_matched,
                        "profit": 0 if not order.cleared_order else order.cleared_order.profit,
                        "side": order.side,
                        "elapsed_seconds_executable": order.elapsed_seconds_executable,
                        "order_status": order.status.value,
                        "market_note": order.trade.market_notes,
                        "trade_notes": order.trade.notes_str,
                        "order_notes": order.notes_str,
                    }
                    csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                    csv_writer.writerow(order_data)
                except Exception as e:
                    logger.error(
                        "_process_cleared_orders_meta: %s" % e,
                        extra={"order": order, "error": e},
                    )

        logger.info("Orders updated", extra={"order_count": len(orders)})

# Function that stops automation running at the end of the day
def terminate(
    context: dict, flumine, today_only: bool = True, seconds_closed: int = 600
) -> None:
    """terminate framework if no markets
    live today.
    """
    markets = list(flumine.markets.markets.values())
    markets_today = [
        m
        for m in markets
        if m.market_start_datetime.date() == datetime.datetime.now().date()
        and (
            m.elapsed_seconds_closed is None
            or (m.elapsed_seconds_closed and m.elapsed_seconds_closed < seconds_closed)
        )
    ]
    if today_only:
        market_count = len(markets_today)
    else:
        market_count = len(markets)
    if market_count == 0:
        # logger.info("No more markets available, terminating framework")
        flumine.handler_queue.put(TerminationEvent(flumine))

if __name__ == "__main__":

    # Credentials to login and logging in 
    trading = bflw_trading()
    client = clients.BetfairClient(trading, interactive_login=True, min_bet_validation = False)

    soccer_ratings, soccer_markets = load_model_ratings()

    framework = Flumine(client=client)
    # Define the betting strategy
    soccer_strategy = SoccerModel(
        market_filter=streaming_market_filter(
            market_ids=soccer_markets
        ),
        max_order_exposure=100,  # Max bet sizes of $100
        max_trade_count=1,  # Max of trade/bet attempt per selection
        max_live_trade_count=1,  # Max of 1 unmatched Bet per selection
        max_selection_exposure=100,
        context = {'model_prices':soccer_ratings}
    )

    framework.add_strategy(soccer_strategy)

    framework.add_logging_control(LiveLoggingControl())

        # Add the stopped to our framework
    framework.add_worker(
        BackgroundWorker(
            framework,
            terminate,
            func_kwargs={"today_only": True, "seconds_closed": 1200},
            interval=60,
            start_delay=60,
        )
    )

```
## Final Step

Running the below line of code will start the flumine instance and place real bets, so run this at your own risk

```py title="GO FLUMINE BOT"

framework.run()

```

### Conclusion

Hopefully this 3-part tutorial has been informative and insightful and provided lots of ideas for different strategies! Soccer/Football is the most popular sport across the Betfair Exchange and so there are numerous possibilities across different leagues to create a new strategy! If you have any questions, including about accessing historic pricing data, Australian and NZ customers can email us at automation@betfair.com.au!

### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.