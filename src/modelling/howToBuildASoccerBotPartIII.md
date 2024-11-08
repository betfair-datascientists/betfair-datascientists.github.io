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

models = ['ensemble']

# Define common conditions for simplification
home_team_win = ['1&0', '2&1', '2&0', '3&0', '3&1', '3&2', 'Any Other Home Win']
away_team_win = ['0&1', '1&2', '0&2', '0&3', '1&3', '2&3', 'Any Other Away Win']
draw_results = ['0&0','1&1', '2&2', '3&3', 'Any Other Draw', 'The Draw']

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