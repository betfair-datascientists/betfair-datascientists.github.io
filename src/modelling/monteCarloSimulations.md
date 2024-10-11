# Monte Carlo Simulations in Python - Brownlow Medal

Monte Carlo simulations are a way to estimate outcomes by running a model many times with random inputs to see the range of possible results. It’s useful when you have uncertainty or variability, like in sports or finance.

Imagine you're trying to predict how many goals a team will score in a match, but there are many factors you can't control, like weather or player form. Instead of guessing a single outcome, you run a simulation where you randomly vary these factors based on their likelihood (like rolling dice). After running the simulation thousands of times, you can see the most common results and the likelihood of different outcomes.

It's called Monte Carlo because it’s similar to gambling in a casino, where random events affect the result.

In this tutorial we will run through a basic python script for running Monte Carlo simulations on an entry submitted for the 2024 Brownlow Medal Datathon.
In this datathon we predicted the expected votes each player would receive in each match as the output of a regression model. This output however, did not generate a rated price for a player to win the whole event or to poll the most votes in their team.

## Data File

 - [Brownlow Medal Predictions](src/modelling/assets/Brownlow_Medal_Datathon_2024_Submission_Form.csv)

## Using the Poisson distribution. 

Monte Carlo simulations the probability of each class occurring to generate outcomes, and so we need to calculate the probability of each class occurring from our regression value.

We need to use the Poisson distribution to calculate the probability that our player will poll 1, 2, or 3 votes. (for more info on the Poisson distribution see [here](https://en.wikipedia.org/wiki/Poisson_distribution))

In excel, the probabilities of each class would be (where x is the regression value):

|number of votes|excel formula|
|---|-------------------------|
| 3 |1 - POISSON.DIST(2,x,TRUE)|
| 2 |POISSON.DIST(2,x,FALSE)|
| 1 |POISSON.DIST(1,x,FALSE)|

We use the **TRUE** parameter for calculating the value for 3 because the Poisson distribution assumes a non-zero probability of values more than 3, where we know that for the brownlow medal that isn't possible.
This method assigns the probability of the player polling 4 votes by adding it to the probability of the player polling 3 votes. The values should then be normalised across all players in the match so that the sum of the 3,2,1 votes equals exactly 1 (as only player per match can receive these votes). 

The probability of the player polling 0 votes will then be **1 - Pr(3) - Pr(2) - Pr(1)**

In Python, this looks like:

```py title="Creating Poisson Predictions"

import pandas as pd
from scipy.stats import poisson

# Load the CSV file
df = pd.read_csv('Brownlow_Medal_Datathon_2024_Submission_Form.csv')

# Define Poisson functions for different vote counts
df['poisson_3_votes'] = 1 - poisson.cdf(2, df['brownlow_votes'])
df['poisson_2_votes'] = poisson.pmf(2, df['brownlow_votes'])
df['poisson_1_votes'] = poisson.pmf(1, df['brownlow_votes'])

# Calculate votes, grouped by match_id
df['3_votes'] = df['poisson_3_votes'] / df.groupby('match_id')['poisson_3_votes'].transform('sum')
df['2_votes'] = df['poisson_2_votes'] / df.groupby('match_id')['poisson_2_votes'].transform('sum')
df['1_votes'] = df['poisson_1_votes'] / df.groupby('match_id')['poisson_1_votes'].transform('sum')

# Calculate 0_votes
df['0_votes'] = 1 - df['3_votes'] - df['2_votes'] - df['1_votes']

# Drop columns with 'poisson' in the name
df = df.drop(columns=[col for col in df.columns if 'poisson' in col])

# Save the modified DataFrame to a new CSV file
df.to_csv('brownlow_datathon_poisson.csv', index=False)

print("CSV file has been saved with new columns.")

```

Now that we've generated the probabilities for each class, we will perform the simulations to predict the number of votes each player will poll across the entire season.
We will then use the results of these simulations to generate rated prices for some of the markets offered for the Brownlow medal count.

```py title="Monte Carlo Simulations"

import pandas as pd
import numpy as np
from tqdm import tqdm

# Load the CSV file
df = pd.read_csv('brownlow_datathon_poisson.csv')

# Define the number of Monte Carlo simulations
num_simulations = 10000

# Dictionary to store the results
results = {}

'''
The code here can handle multiple models (if you've trained multiple variations of a model for example)
It will easily handle just one model of course
'''

# Group the data by 'model'
models = df['model'].unique()

for model in models:
    print(f'Running simulations for {model}')
    model_df = df[df['model'] == model]
    
    # Get unique match_ids and player_ids
    match_ids = model_df['match_id'].unique()
    player_ids = model_df['player_id'].unique()

    # Initialize a DataFrame to store simulation results
    simulation_results = pd.DataFrame()

    # Run the Monte Carlo simulations with a progress bar
    for simulation_number in tqdm(range(num_simulations), desc=f"Simulating model {model}"):
        # Initialize vote counts for this simulation
        vote_totals = {player_id: 0 for player_id in player_ids}
        
        # Simulate votes for each match
        for match_id in match_ids:
            match_df = model_df[model_df['match_id'] == match_id]
            
            '''
            We had already normalised across the markets but sometimes floating point errors can causing some rounding issues
            So we normalise again just to ensure we don't hit any errors.
            '''
            p_3_votes = match_df['3_votes'] / match_df['3_votes'].sum()
            p_2_votes = match_df['2_votes'] / match_df['2_votes'].sum()
            p_1_votes = match_df['1_votes'] / match_df['1_votes'].sum()

            # Select one player for 3 votes, 2 votes, and 1 vote
            player_3_votes = np.random.choice(match_df['player_id'], p=p_3_votes)
            player_2_votes = np.random.choice(match_df['player_id'], p=p_2_votes)
            player_1_votes = np.random.choice(match_df['player_id'], p=p_1_votes)
            
            # Update vote totals
            vote_totals[player_3_votes] += 3
            vote_totals[player_2_votes] += 2
            vote_totals[player_1_votes] += 1

        # Store the results for this simulation
        simulation_row = {player_id: vote_totals[player_id] for player_id in player_ids}
        simulation_row['Simulation'] = simulation_number
        simulation_row['Model'] = model
        simulation_results = simulation_results. _append(simulation_row, ignore_index=True)

    # Save the results to a CSV file
    output_file = f'AFL-Brownlow/simulation_results_{model}.csv'
    simulation_results.to_csv(output_file, index=False)

    print(f'Simulation results for {model} saved to {output_file}')

```

## Creating rated prices for our model

Now let's walk through a subset of markets offered on the exchange on the day of the Brownlow:

 - Winner
 - Top X Finish (3, 5, 10, 20)
 - Poll X Votes (1, 10, 15, 20)
 - Player to Poll Over/Under X Votes
 - Player to Poll Most Votes in Team
 - H2H Player Match-Ups
 - Team to Poll Most Votes

We'll create a dictionary of lists which will contain each team as the key and a list of player_ids as the value.
We'll also create a dataframe containing the player ids and the players' full names so we can match to the Betfair data.

```py title="Grouping players by teams"
import pandas as pd

# Load the CSV file into a dataframe
df = pd.read_csv('Brownlow_Medal_Datathon_2024_Submission_Form.csv')

# Step 1: Replace spaces with underscores in 'player_team' column
df['player_team'] = df['player_team'].str.replace(' ', '_')

# Step 2: Create a list of unique 'player_team' values
unique_teams = df['player_team'].unique()

# Step 3: Iterate over unique teams and get unique 'player_id' values for each team
team_player_ids = {}
for team in unique_teams:
    # Create a sub-dataframe for each team
    sub_df = df[df['player_team'] == team]
    
    # Get the list of unique player_ids for that team
    unique_player_ids = sub_df['player_id'].unique().tolist()
    
    # Store in dictionary with team as key
    team_player_ids[team] = unique_player_ids

df['runner_name'] = df['player_first_name'] + ' ' + df['player_last_name']
player_ids_df = df[['player_id','runner_name']].drop_duplicates()
player_ids_df['player_id'] = player_ids_df['player_id'].astype(str)

```
---
## Team To Poll Most Votes

```py title="Team To Poll Most Votes"

counter = 0

for model in models:
    sim_df = pd.read_csv(f'simulation_results_{model}.csv')

    # The column names are player_ids, so this line fixes any issues with player_ids being turned into floats
    sim_df.columns = sim_df.columns.str.replace(r'\.0$', '', regex=True)

    # Initialize a dictionary to hold the team scores
    team_scores = {team: [] for team in team_player_ids.keys()}
    # Initialize a counter for each team to store the number of times they were the highest scorer
    team_highest_count = {team: 0 for team in team_player_ids.keys()}

    # Iterate through each row of the DataFrame
    for index, row in sim_df.iterrows():
        # Calculate the sum of votes for each team in the current row
        team_scores_for_row = []  # Temporary list to hold scores for this row
        for team, player_ids in team_player_ids.items():
            # Convert player_ids to strings since sim_df columns are strings
            player_ids_str = [str(player_id) for player_id in player_ids]
            
            # Filter the player_ids to only include those present in sim_df columns
            valid_player_ids = [player_id for player_id in player_ids_str if player_id in sim_df.columns]
            
            # Sum votes for all valid players in the team
            team_score = row[valid_player_ids].sum() if valid_player_ids else 0
            team_scores_for_row.append(team_score)

        # Find the maximum score in the row
        max_score = max(team_scores_for_row)

        # Count how many teams have the max score
        count_of_max = team_scores_for_row.count(max_score)

        # Add 1 / count to each team with the highest score
        for team_index, score in enumerate(team_scores_for_row):
            if score == max_score:
                team_highest_count[list(team_player_ids.keys())[team_index]] += 1 / count_of_max

    # Convert the team_highest_count dictionary to a list of values
    team_highest_count_values = [team_highest_count[team] for team in team_player_ids.keys()]

    # Create a DataFrame with team names and their highest count
    df_team_highest_count = pd.DataFrame({
        'Model': model,
        'market_name': 'Team To Poll Most Votes (Incl. Ineligible)',
        'runner_name': list(team_player_ids.keys()),
        'rated_price': team_highest_count_values
    })

    df_team_highest_count['rated_price'] = [
        1000 if count == 0 else 1 / (count / num_simulations) 
        for count in team_highest_count_values
    ]
    df_team_highest_count['runner_name'] = df_team_highest_count['runner_name'].str.replace('_', ' ')

    if counter == 0:
        df_team_highest_count.to_csv('teamToPollMostVotes.csv', header=True, index=False, mode="w")
    else:
        df_team_highest_count.to_csv('teamToPollMostVotes.csv', header=False, index=False, mode="a")
    
    counter += 1
    print(f'model {counter} processed')

```
## To Poll Most Votes in Team

This section here is very prescriptive, and could certainly be condensed into a more efficient way.
However, I've given the full, unabridged code to carefully outline exactly what is being done here.

```py title="Most Votes in Team"

# Remove specific player IDs from the relevant teams in team_player_ids
# This is done because some of these markets have excluded certain players
if 'Brisbane' in team_player_ids:
    if 12061 in team_player_ids['Brisbane']:
        team_player_ids['Brisbane'].remove(12061)

if 'Carlton' in team_player_ids:
    if 12685 in team_player_ids['Carlton']:
        team_player_ids['Carlton'].remove(12685)
    if 12269 in team_player_ids['Carlton']:
        team_player_ids['Carlton'].remove(12269)

if 'Collingwood' in team_player_ids:
    if 12948 in team_player_ids['Collingwood']:
        team_player_ids['Collingwood'].remove(12948)

if 'Essendon' in team_player_ids:
    if 12249 in team_player_ids['Essendon']:
        team_player_ids['Essendon'].remove(12249)

counter = 0

for model in models:

    df = pd.read_csv(f'simulation_results_{model}.csv')
    df.columns = df.columns.str.replace(r'\.0$', '', regex=True)

    # Initialise the dictionary to store every selection across this market type in the format f'{market_name} - {runner_name}'
    players = {
        "Adelaide - Any Other Player":0,
        "Adelaide - Ben Keays":0,
        "Adelaide - Izak Rankine":0,
        "Adelaide - Jordan Dawson":0,
        "Adelaide - Rory Laird":0,
        "Brisbane Without Neale - Any Other Player":0,
        "Brisbane Without Neale - Cam Rayner":0,
        "Brisbane Without Neale - Dayne Zorko":0,
        "Brisbane Without Neale - Hugh McCluggage":0,
        "Brisbane Without Neale - Joe Daniher":0,
        "Brisbane Without Neale - Josh Dunkley":0,
        "Carlton Without Cripps/Walsh - Any Other Player":0,
        "Carlton Without Cripps/Walsh - Charlie Curnow":0,
        "Carlton Without Cripps/Walsh - George Hewett":0,
        "Carlton Without Cripps/Walsh - Harry McKay":0,
        "Carlton Without Cripps/Walsh - Tom De Koning":0,
        "Collingwood Without N Daicos - Any Other Player":0,
        "Collingwood Without N Daicos - Jack Crisp":0,
        "Collingwood Without N Daicos - Jordan De Goey":0,
        "Collingwood Without N Daicos - Josh Daicos":0,
        "Collingwood Without N Daicos - Scott Pendlebury":0,
        "Collingwood Without N Daicos - Will Hoskin Elliott":0,
        "Essendon Without Merrett - Any Other Player":0,
        "Essendon Without Merrett - Jye Caldwell":0,
        "Essendon Without Merrett - Nic Martin":0,
        "Essendon Without Merrett - Sam Durham":0,
        "Fremantle - Andrew Brayshaw":0,
        "Fremantle - Any Other Player":0,
        "Fremantle - Caleb Serong":0,
        "Fremantle - Hayden Young":0,
        "Geelong - Any Other Player":0,
        "Geelong - Jeremy Cameron":0,
        "Geelong - Max Holmes":0,
        "Geelong - Patrick Dangerfield":0,
        "Geelong - Tom Stewart":0,
        "Gold Coast - Any Other Player":0,
        "Gold Coast - Matt Rowell":0,
        "Gold Coast - Noah Anderson":0,
        "Gold Coast - Sam Flanders":0,
        "GWS - Any Other Player":0,
        "GWS - Jesse Hogan":0,
        "GWS - Lachie Whitfield":0,
        "GWS - Toby Greene":0,
        "GWS - Tom Green":0,
        "Hawthorn - Any Other Player":0,
        "Hawthorn - Dylan Moore":0,
        "Hawthorn - Jai Newcombe":0,
        "Hawthorn - James Sicily":0,
        "Hawthorn - James Worpel":0,
        "Hawthorn - Will Day":0,
        "Melbourne - Any Other Player":0,
        "Melbourne - Christian Petracca":0,
        "Melbourne - Jack Viney":0,
        "Melbourne - Max Gawn":0,
        "North Melbourne - Any Other Player":0,
        "North Melbourne - Harry Sheezel":0,
        "North Melbourne - Luke Davies Uniacke":0,
        "North Melbourne - Tristan Xerri":0,
        "Port Adelaide - Any Other Player":0,
        "Port Adelaide - Connor Rozee":0,
        "Port Adelaide - Jason Horne Francis":0,
        "Port Adelaide - Ollie Wines":0,
        "Port Adelaide - Zak Butters":0,
        "Richmond - Any Other Player":0,
        "Richmond - Daniel Rioli":0,
        "Richmond - Jayden Short":0,
        "Richmond - Liam Baker":0,
        "Richmond - Nick Vlastuin":0,
        "Richmond - Shai Bolton":0,
        "Richmond - Tim Taranto":0,
        "Richmond - Toby Nankervis":0,
        "St Kilda - Any Other Player":0,
        "St Kilda - Jack Sinclair":0,
        "St Kilda - Jack Steele":0,
        "St Kilda - Nasiah Wanganeen Milera":0,
        "St Kilda - Rowan Marshall":0,
        "Sydney - Any Other Player":0,
        "Sydney - Chad Warner":0,
        "Sydney - Errol Gulden":0,
        "Sydney - Isaac Heeney":0,
        "West Coast - Any Other Player":0,
        "West Coast - Elliot Yeo":0,
        "West Coast - Harley Reid":0,
        "West Coast - Jake Waterman":0,
        "West Coast - Tim Kelly":0,
        "Western Bulldogs - Adam Treloar":0,
        "Western Bulldogs - Any Other Player":0,
        "Western Bulldogs - Ed Richards":0,
        "Western Bulldogs - Marcus Bontempelli":0,
        "Western Bulldogs - Tom Liberatore":0
    }

    for team, player_ids in team_player_ids.items():  # Iterate over the dictionary keys (teams) and their values (player IDs)

        # Create a DataFrame for the team with columns corresponding to the player_ids (converted to strings)
        team_df = df[[str(player_id) for player_id in player_ids]]

        for _, row in team_df.iterrows():

            team_sorted_players = row.sort_values(ascending=False)

            # Find the maximum value in the row
            max_value = team_sorted_players.max()

            # Count how many times the maximum value occurs in this row
            winners = (team_sorted_players == max_value).sum()

            for player_id, player_value in team_sorted_players.items():
                if player_value == max_value:
                    if team == 'Adelaide':
                        if player_id == '12171':    players['Adelaide - Rory Laird'] += 1 / winners
                        elif player_id == '12519':	players['Adelaide - Jordan Dawson'] += 1 / winners
                        elif player_id == '12797':	players['Adelaide - Izak Rankine'] += 1 / winners
                        elif player_id == '12441':	players['Adelaide - Ben Keays'] += 1 / winners
                        else: players['Adelaide - Any Other Player'] += 1 / winners
                    if team == 'Brisbane':
                        if player_id == '12421':	players['Brisbane Without Neale - Josh Dunkley'] += 1 / winners
                        elif player_id == '12205':	players['Brisbane Without Neale - Joe Daniher'] += 1 / winners
                        elif player_id == '12526':	players['Brisbane Without Neale - Hugh McCluggage'] += 1 / winners
                        elif player_id == '12082':	players['Brisbane Without Neale - Dayne Zorko'] += 1 / winners
                        elif player_id == '12594':	players['Brisbane Without Neale - Cam Rayner'] += 1 / winners
                        else:	players['Brisbane Without Neale - Any Other Player'] += 1 / winners
                    if team == 'Carlton':
                        if player_id == '12681':	players['Carlton Without Cripps/Walsh - Tom De Koning'] += 1 / winners
                        elif player_id == '12575':	players['Carlton Without Cripps/Walsh - Harry McKay'] += 1 / winners
                        elif player_id == '12417':	players['Carlton Without Cripps/Walsh - George Hewett'] += 1 / winners
                        elif player_id == '12428':	players['Carlton Without Cripps/Walsh - Charlie Curnow'] += 1 / winners
                        else:	players['Carlton Without Cripps/Walsh - Any Other Player'] += 1 / winners
                    if team == 'Collingwood':
                        if player_id == '12029':	players['Collingwood Without N Daicos - Will Hoskin Elliott'] += 1 / winners
                        elif player_id == '11506':	players['Collingwood Without N Daicos - Scott Pendlebury'] += 1 / winners
                        elif player_id == '12582':	players['Collingwood Without N Daicos - Josh Daicos'] += 1 / winners
                        elif player_id == '12333':	players['Collingwood Without N Daicos - Jordan De Goey'] += 1 / winners
                        elif player_id == '12067':	players['Collingwood Without N Daicos - Jack Crisp'] += 1 / winners
                        else:	players['Collingwood Without N Daicos - Any Other Player'] += 1 / winners
                    if team == 'Essendon':
                        if player_id == '12926':	players['Essendon Without Merrett - Sam Durham'] += 1 / winners
                        elif player_id == '12950':	players['Essendon Without Merrett - Nic Martin'] += 1 / winners
                        elif player_id == '12752':	players['Essendon Without Merrett - Jye Caldwell'] += 1 / winners
                        else:	players['Essendon Without Merrett - Any Other Player'] += 1 / winners
                    if team == 'Fremantle':
                        if player_id == '12777':	players['Fremantle - Hayden Young'] += 1 / winners
                        elif player_id == '12786':	players['Fremantle - Caleb Serong'] += 1 / winners
                        elif player_id == '12596':	players['Fremantle - Andrew Brayshaw'] += 1 / winners
                        else:	players['Fremantle - Any Other Player'] += 1 / winners
                    if team == 'Geelong':
                        if player_id == '12514':	players['Geelong - Tom Stewart'] += 1 / winners
                        elif player_id == '11706':	players['Geelong - Patrick Dangerfield'] += 1 / winners
                        elif player_id == '12882':	players['Geelong - Max Holmes'] += 1 / winners
                        elif player_id == '12022':	players['Geelong - Jeremy Cameron'] += 1 / winners
                        else:	players['Geelong - Any Other Player'] += 1 / winners
                    if team == 'Gold_Coast':
                        if player_id == '12825':	players['Gold Coast - Sam Flanders'] += 1 / winners
                        elif player_id == '12767':	players['Gold Coast - Noah Anderson'] += 1 / winners
                        elif player_id == '12769':	players['Gold Coast - Matt Rowell'] += 1 / winners
                        else:	players['Gold Coast - Any Other Player'] += 1 / winners
                    if team == 'GWS':
                        if player_id == '12766':	players['GWS - Tom Green'] += 1 / winners
                        elif player_id == '12026':	players['GWS - Toby Greene'] += 1 / winners
                        elif player_id == '12147':	players['GWS - Lachie Whitfield'] += 1 / winners
                        elif player_id == '12326':	players['GWS - Jesse Hogan'] += 1 / winners
                        else:	players['GWS - Any Other Player'] += 1 / winners
                    if team == 'Hawthorn':
                        if player_id == '12794':	players['Hawthorn - Will Day'] += 1 / winners
                        elif player_id == '12626':	players['Hawthorn - James Worpel'] += 1 / winners
                        elif player_id == '12342':	players['Hawthorn - James Sicily'] += 1 / winners
                        elif player_id == '12913':	players['Hawthorn - Jai Newcombe'] += 1 / winners
                        elif player_id == '12710':	players['Hawthorn - Dylan Moore'] += 1 / winners
                        else:	players['Hawthorn - Any Other Player'] += 1 / winners
                    if team == 'Melbourne':
                        if player_id == '11972':	players['Melbourne - Max Gawn'] += 1 / winners
                        elif player_id == '12152':	players['Melbourne - Jack Viney'] += 1 / winners
                        elif player_id == '12437':	players['Melbourne - Christian Petracca'] += 1 / winners
                        else:	players['Melbourne - Any Other Player'] += 1 / winners
                    if team == 'North_Melbourne':
                        if player_id == '12789':	players['North Melbourne - Tristan Xerri'] += 1 / winners
                        elif player_id == '12599':	players['North Melbourne - Luke Davies Uniacke'] += 1 / winners
                        elif player_id == '13030':	players['North Melbourne - Harry Sheezel'] += 1 / winners
                        else:	players['North Melbourne - Any Other Player'] += 1 / winners
                    if team == 'Port_Adelaide':
                        if player_id == '12693':	players['Port Adelaide - Zak Butters'] += 1 / winners
                        elif player_id == '12155':	players['Port Adelaide - Ollie Wines'] += 1 / winners
                        elif player_id == '12955':	players['Port Adelaide - Jason Horne Francis'] += 1 / winners
                        elif player_id == '12696':	players['Port Adelaide - Connor Rozee'] += 1 / winners
                        else:	players['Port Adelaide - Any Other Player'] += 1 / winners
                    if team == 'Richmond':
                        if player_id == '12379':	players['Richmond - Toby Nankervis'] += 1 / winners
                        elif player_id == '12512':	players['Richmond - Tim Taranto'] += 1 / winners
                        elif player_id == '12542':	players['Richmond - Shai Bolton'] += 1 / winners
                        elif player_id == '12180':	players['Richmond - Nick Vlastuin'] += 1 / winners
                        elif player_id == '12668':	players['Richmond - Liam Baker'] += 1 / winners
                        elif player_id == '12425':	players['Richmond - Jayden Short'] += 1 / winners
                        elif player_id == '12409':	players['Richmond - Daniel Rioli'] += 1 / winners
                        else:	players['Richmond - Any Other Player'] += 1 / winners
                    if team == 'St_Kilda':
                        if player_id == '12572':	players['St Kilda - Rowan Marshall'] += 1 / winners
                        elif player_id == '12947':	players['St Kilda - Nasiah Wanganeen Milera'] += 1 / winners
                        elif player_id == '12377':	players['St Kilda - Jack Steele'] += 1 / winners
                        elif player_id == '12337':	players['St Kilda - Jack Sinclair'] += 1 / winners
                        else:	players['St Kilda - Any Other Player'] += 1 / winners
                    if team == 'Sydney':
                        if player_id == '12331':	players['Sydney - Isaac Heeney'] += 1 / winners
                        elif player_id == '12864':	players['Sydney - Errol Gulden'] += 1 / winners
                        elif player_id == '12799':	players['Sydney - Chad Warner'] += 1 / winners
                        else:	players['Sydney - Any Other Player'] += 1 / winners
                    if team == 'West_Coast':
                        if player_id == '12605':	players['West Coast - Tim Kelly'] += 1 / winners
                        elif player_id == '12609':	players['West Coast - Jake Waterman'] += 1 / winners
                        elif player_id == '13112':	players['West Coast - Harley Reid'] += 1 / winners
                        elif player_id == '12093':	players['West Coast - Elliot Yeo'] += 1 / winners
                        else:	players['West Coast - Any Other Player'] += 1 / winners
                    if team == 'Western_Bulldogs':
                        if player_id == '11904':	players['Western Bulldogs - Tom Liberatore'] += 1 / winners
                        elif player_id == '12277':	players['Western Bulldogs - Marcus Bontempelli'] += 1 / winners
                        elif player_id == '12612':	players['Western Bulldogs - Ed Richards'] += 1 / winners
                        elif player_id == '12058':	players['Western Bulldogs - Adam Treloar'] += 1 / winners
                        else:	players['Western Bulldogs - Any Other Player'] += 1 / winners

    player_team_votes = pd.DataFrame.from_dict(players,orient='index')
    player_team_votes['Model'] = model

    # We reset the index because the market_name and runner_name are in the index
    player_team_votes = player_team_votes.reset_index()
    player_team_votes[['market_name', 'runner_name']] = player_team_votes['index'].str.split(' - ', expand=True)
    player_team_votes = player_team_votes.rename(columns={0: 'rated_price'})
    player_team_votes = player_team_votes[['Model','market_name','runner_name','rated_price']]

    # Calculate rated_price
    player_team_votes['rated_price'] = 1/(player_team_votes['rated_price']/num_simulations)

    if counter == 0:
        player_team_votes.to_csv('pollMostVotesInTeam.csv',header=True,index=True,mode="w")
    else:
        player_team_votes.to_csv('pollMostVotesInTeam.csv',header=False,index=True,mode="a")
    
    counter += 1
    print(f'model {counter} processed')

```
## Player Lines
```py title="Player Vote Lines"

counter = 0

for model in models:

    df = pd.read_csv(f'simulation_results_{model}.csv')
    df.columns = df.columns.str.replace(r'\.0$', '', regex=True)

    lines = {
    'Caleb Serong - Over 23.5 Votes':0,
    'Caleb Serong - Under 23.5 Votes':0,
    'Errol Gulden - Over 22.5 Votes':0,
    'Errol Gulden - Under 22.5 Votes':0,
    'Isaac Heeney - Over 26.5 Votes':0,
    'Isaac Heeney - Under 26.5 Votes':0,
    'Lachie Neale - Over 27.5 Votes':0,
    'Lachie Neale - Under 27.5 Votes':0,
    'Marcus Bontempelli - Over 24.5 Votes':0,
    'Marcus Bontempelli - Under 24.5 Votes':0,
    'Nick Daicos - Over 31.5 Votes':0,
    'Nick Daicos - Under 31.5 Votes':0,
    'Patrick Cripps - Over 32.5 Votes':0,
    'Patrick Cripps - Under 32.5 Votes':0,
    'Tom Green - Over 21.5 Votes':0,
    'Tom Green - Under 21.5 Votes':0,
    'Zach Merrett - Over 23.5 Votes':0,
    'Zach Merrett - Under 23.5 Votes':0,
    'Zak Butters - Over 20.5 Votes':0,
    'Zak Butters - Under 20.5 Votes':0
    }

    # Iterate over each row (simulation)
    for _, row in df.iterrows():

        for player_id, total_votes in row.items():
            if player_id == '12786' and total_votes > 23.5:
                lines['Caleb Serong - Over 23.5 Votes'] += 1
            if player_id == '12786' and total_votes < 23.5:
                lines['Caleb Serong - Under 23.5 Votes'] += 1
            if player_id == '12864' and total_votes > 22.5:
                lines['Errol Gulden - Over 22.5 Votes'] += 1
            if player_id == '12864' and total_votes < 22.5:
                lines['Errol Gulden - Under 22.5 Votes'] += 1
            if player_id == '12331' and total_votes > 26.5:
                lines['Isaac Heeney - Over 26.5 Votes'] += 1
            if player_id == '12331' and total_votes < 26.5:
                lines['Isaac Heeney - Under 26.5 Votes'] += 1
            if player_id == '12061' and total_votes > 27.5:
                lines['Lachie Neale - Over 27.5 Votes'] += 1
            if player_id == '12061' and total_votes < 27.5:
                lines['Lachie Neale - Under 27.5 Votes'] += 1
            if player_id == '12277' and total_votes > 24.5:
                lines['Marcus Bontempelli - Over 24.5 Votes'] += 1
            if player_id == '12277' and total_votes < 24.5:
                lines['Marcus Bontempelli - Under 24.5 Votes'] += 1
            if player_id == '12948' and total_votes > 31.5:
                lines['Nick Daicos - Over 31.5 Votes'] += 1
            if player_id == '12948' and total_votes < 31.5:
                lines['Nick Daicos - Under 31.5 Votes'] += 1
            if player_id == '12269' and total_votes > 32.5:
                lines['Patrick Cripps - Over 32.5 Votes'] += 1
            if player_id == '12269' and total_votes < 32.5:
                lines['Patrick Cripps - Under 32.5 Votes'] += 1
            if player_id == '12766' and total_votes > 21.5:
                lines['Tom Green - Over 21.5 Votes'] += 1
            if player_id == '12766' and total_votes < 21.5:
                lines['Tom Green - Under 21.5 Votes'] += 1
            if player_id == '12249' and total_votes > 23.5:
                lines['Zach Merrett - Over 23.5 Votes'] += 1
            if player_id == '12249' and total_votes < 23.5:
                lines['Zach Merrett - Under 23.5 Votes'] += 1
            if player_id == '12693' and total_votes > 20.5:
                lines['Zak Butters - Over 20.5 Votes'] += 1
            if player_id == '12693' and total_votes < 20.5:
                lines['Zak Butters - Over 20.5 Votes'] += 1

    lines = pd.DataFrame.from_dict(lines,orient='index')
    lines['Model'] = model

    # We reset the index because the market_name and runner_name are in the index
    lines = lines.reset_index()
    lines[['market_name', 'runner_name']] = lines['index'].str.split(' - ', expand=True)
    lines = lines.rename(columns={0: 'rated_price'})
    lines = lines[['Model','market_name','runner_name','rated_price']]

    lines['rated_price'] = 1/(lines['rated_price']/num_simulations)

    if counter == 0:
        lines.to_csv('playerVoteLines.csv',header=True,index=True,mode="w")
    else:
        lines.to_csv('playerVoteLines.csv',header=False,index=True,mode="a")
    
    counter += 1
    print(f'model {counter} processed')

```
## Player Head-To-Head
```py title="Head to Head Markets"

# Create lists for each market match up
Keays_Rayner= ['12441','12594']
Serong_Merrett= ['12786','12249']
Zorko_Whitfield= ['12082','12147']
Moore_Sinclair= ['12710','12337']
Reid_Dempsey= ['13112','12976']
Sheezel_Flanders= ['13030','12825']
Yeo_Worpel= ['12093','12626']
Heeney_Neale= ['12331','12061']
Warner_Anderson= ['12799','12767']
Dangerfield_Greene= ['11706','12026']

# Create a list of lists
head_to_head_markets = [Keays_Rayner,Serong_Merrett,Zorko_Whitfield,Moore_Sinclair,Reid_Dempsey,Sheezel_Flanders,Yeo_Worpel,Heeney_Neale,Warner_Anderson,Dangerfield_Greene]

counter = 0

for model in models:

    df = pd.read_csv(f'simulation_results_{model}.csv')
    df.columns = df.columns.str.replace(r'\.0$', '', regex=True)

    # Initialise a dictionary with every market_name and runner_name
    head_to_head = {
        'Ben Keays v Cam Rayner - Ben Keays' : 0,
        'Ben Keays v Cam Rayner - Cam Rayner' : 0,
        'Caleb Serong v Zach Merrett - Caleb Serong' : 0,
        'Caleb Serong v Zach Merrett - Zach Merrett' : 0,
        'Dayne Zorko v Lachie Whitfield - Dayne Zorko' : 0,
        'Dayne Zorko v Lachie Whitfield - Lachie Whitfield' : 0,
        'Dylan Moore v Jack Sinclair - Dylan Moore' : 0,
        'Dylan Moore v Jack Sinclair - Jack Sinclair' : 0,
        'Harley Reid v Oliver Dempsey - Harley Reid' : 0,
        'Harley Reid v Oliver Dempsey - Oliver Dempsey' : 0,
        'Harry Sheezel v Sam Flanders - Harry Sheezel' : 0,
        'Harry Sheezel v Sam Flanders - Sam Flanders' : 0,
        'James Worpel v Elliot Yeo - Elliot Yeo' : 0,
        'James Worpel v Elliot Yeo - James Worpel' : 0,
        'Lachie Neale v Isaac Heeney - Isaac Heeney' : 0,
        'Lachie Neale v Isaac Heeney - Lachie Neale' : 0,
        'Noah Anderson v Chad Warner - Chad Warner' : 0,
        'Noah Anderson v Chad Warner - Noah Anderson' : 0,
        'Patrick Dangerfield v Toby Greene - Patrick Dangerfield' : 0,
        'Patrick Dangerfield v Toby Greene - Toby Greene' : 0
    }

    for market in head_to_head_markets:

        market_df = df[market]

        for _, row in market_df.iterrows():

            market_sorted_head_to_head = row.sort_values(ascending=False)

            max_value = market_sorted_head_to_head.max()

            winners = (market_sorted_head_to_head == max_value).sum()

            for player_id, player_value in market_sorted_head_to_head.items():
                if player_value == max_value:

                    if player_id == '12441': head_to_head['Ben Keays v Cam Rayner - Ben Keays'] += 1 / winners
                    if player_id == '12786': head_to_head['Caleb Serong v Zach Merrett - Caleb Serong'] += 1 / winners
                    if player_id == '12082': head_to_head['Dayne Zorko v Lachie Whitfield - Dayne Zorko'] += 1 / winners
                    if player_id == '12710': head_to_head['Dylan Moore v Jack Sinclair - Dylan Moore'] += 1 / winners
                    if player_id == '13112': head_to_head['Harley Reid v Oliver Dempsey - Harley Reid'] += 1 / winners
                    if player_id == '13030': head_to_head['Harry Sheezel v Sam Flanders - Harry Sheezel'] += 1 / winners
                    if player_id == '12093': head_to_head['James Worpel v Elliot Yeo - Elliot Yeo'] += 1 / winners
                    if player_id == '12331': head_to_head['Lachie Neale v Isaac Heeney - Isaac Heeney'] += 1 / winners
                    if player_id == '12799': head_to_head['Noah Anderson v Chad Warner - Chad Warner'] += 1 / winners
                    if player_id == '11706': head_to_head['Patrick Dangerfield v Toby Greene - Patrick Dangerfield'] += 1 / winners
                    if player_id == '12594': head_to_head['Ben Keays v Cam Rayner - Cam Rayner'] += 1 / winners
                    if player_id == '12249': head_to_head['Caleb Serong v Zach Merrett - Zach Merrett'] += 1 / winners
                    if player_id == '12147': head_to_head['Dayne Zorko v Lachie Whitfield - Lachie Whitfield'] += 1 / winners
                    if player_id == '12337': head_to_head['Dylan Moore v Jack Sinclair - Jack Sinclair'] += 1 / winners
                    if player_id == '12976': head_to_head['Harley Reid v Oliver Dempsey - Oliver Dempsey'] += 1 / winners
                    if player_id == '12825': head_to_head['Harry Sheezel v Sam Flanders - Sam Flanders'] += 1 / winners
                    if player_id == '12626': head_to_head['James Worpel v Elliot Yeo - James Worpel'] += 1 / winners
                    if player_id == '12061': head_to_head['Lachie Neale v Isaac Heeney - Lachie Neale'] += 1 / winners
                    if player_id == '12767': head_to_head['Noah Anderson v Chad Warner - Noah Anderson'] += 1 / winners
                    if player_id == '12026': head_to_head['Patrick Dangerfield v Toby Greene - Toby Greene'] += 1 / winners

    head_to_head = pd.DataFrame.from_dict(head_to_head,orient='index')

    head_to_head['Model'] = model

    # We reset the index because the market_name and runner_name are in the index
    head_to_head = head_to_head.reset_index()
    head_to_head[['market_name', 'runner_name']] = head_to_head['index'].str.split(' - ', expand=True)
    head_to_head = head_to_head.rename(columns={0: 'rated_price'})
    head_to_head = head_to_head[['Model','market_name','runner_name','rated_price']]

    head_to_head['rated_price'] = 1/(head_to_head['rated_price']/num_simulations)

    if counter == 0:
        head_to_head.to_csv('headToHeadVotes.csv',header=True,index=True,mode="w")
    else:
        head_to_head.to_csv('headToHeadVotes.csv',header=False,index=True,mode="a")
    
    counter += 1
    print(f'model {counter} processed')

```
## Winner & Top X Finish
```py title="Winner & Top X markets"

counter = 0

for model in models:

    df = pd.read_csv(f'simulation_results_{model}.csv')
    df.columns = df.columns.str.replace(r'\.0$', '', regex=True)

    # Drop the 'Model' and 'Simulation' columns
    df.drop(columns=['Model', 'Simulation'], errors='ignore', inplace=True)

    top_rank_counts = {pid: {'Winner': 0, 'Top 3 (Incl. Ineligible)': 0, 'Top 5 (Incl. Ineligible)': 0, 'Top 10 (Incl. Ineligible)': 0, 'Top 20 (Incl. Ineligible)': 0} for pid in df.columns}

    # Iterate over each row (simulation)
    for _, row in df.iterrows():
        # Isolate the numeric values (votes) and sort them in descending order
        numeric_votes = row.astype(float)  # Convert the row to numeric, ignoring non-numeric values
        sorted_players = numeric_votes.sort_values(ascending=False)

        # Get the top ranks (1, 3, 5, 10, 20)
        for rank, (player_id, player_value) in enumerate(sorted_players.items(), 1):
            # Count the number of players with the same value as the current player up to the current rank
            rank_count = (sorted_players[:rank] == player_value).sum()

            if rank == 1:
                top_rank_counts[player_id]['Winner'] += 1 / rank_count
            if rank <= 3:
                top_rank_counts[player_id]['Top 3 (Incl. Ineligible)'] += 1 / rank_count
            if rank <= 5:
                top_rank_counts[player_id]['Top 5 (Incl. Ineligible)'] += 1 / rank_count
            if rank <= 10:
                top_rank_counts[player_id]['Top 10 (Incl. Ineligible)'] += 1 / rank_count
            if rank <= 20:
                top_rank_counts[player_id]['Top 20 (Incl. Ineligible)'] += 1 / rank_count

    # Convert the result dictionaries into DataFrames for easy viewing
    top_rank_df = pd.DataFrame(top_rank_counts).T
    top_rank_df['Model'] = model

    top_rank_df = top_rank_df.reset_index()
    top_rank_df = top_rank_df.merge(player_ids_df,how='left',left_on=['index'],right_on=['player_id'])

    market_labels = ['winner', 'top3', 'top5', 'top10', 'top20']  # Market labels
    markets = []

    # Loop through the market labels and create DataFrames
    for i, label in enumerate(market_labels):
        market_df = pd.DataFrame({
            'Model': top_rank_df['Model'],
            'market_name': top_rank_df.columns[i + 1],
            'runner_name': top_rank_df['runner_name'],
            'rated_price': top_rank_df[top_rank_df.columns[i + 1]]
        })
        markets.append(market_df)

    # Concatenate all the DataFrames into one
    final_rank_df = pd.concat(markets, ignore_index=True)

    # This is the list of players disqualified from winning the medal
    disqualified_players = [
        'Isaac Heeney',
        'Toby Greene',
        'Izak Rankine',
        'Kysaiah Pickett',
        'Tom Liberatore',
        'Dan Houston',
        'Harley Reid',
        'Nat Fyfe'
    ]

    # Calculate the sum of 'rated_price' for specified runner names where market_name is 'Winner'
    rated_price_sum = final_rank_df[
        (final_rank_df['runner_name'].isin(disqualified_players)) &
        (final_rank_df['market_name'] == 'Winner')
    ]['rated_price'].sum()

    # Calculate winner_simulations
    winner_simulations = num_simulations - rated_price_sum

    def calculate_rated_price(row):
        try:
            if row['market_name'] == 'Winner':
                return 1 / (row['rated_price'] / winner_simulations)
            else:
                return 1 / (row['rated_price'] / num_simulations)
        except ZeroDivisionError:
            return 1000

    # This function will create rated prices for all markets (including removing disqualified players from the Winner prices)
    final_rank_df['rated_price'] = final_rank_df.apply(calculate_rated_price, axis=1)

    # Write results to CSV
    if counter == 0:
        final_rank_df.to_csv('winnerTopXMarkets.csv', header=True, index=True, mode="w")
    else:
        final_rank_df.to_csv('winnerTopXMarkets.csv', header=False, index=True, mode="a")

    counter += 1
    print(f'model {counter} processed')
```
## To Poll X Votes

```py title="To Poll X Votes markets"

counter = 0

for model in models:

    df = pd.read_csv(f'simulation_results_{model}.csv')
    df.columns = df.columns.str.replace(r'\.0$', '', regex=True)

    # Drop the 'Model' and 'Simulation' columns
    df.drop(columns=['Model', 'Simulation'], errors='ignore', inplace=True)

    vote_sum_counts = {pid: {'To Poll a Vote': 0, 'To Poll 10 Votes': 0, 'To Poll 15 Votes': 0, 'To Poll 20 Votes': 0} for pid in df.columns}

    # Iterate over each row (simulation)
    for _, row in df.iterrows():
        # Isolate the numeric values (votes) and sort them in descending order
        numeric_votes = row.astype(float)  # Convert the row to numeric, ignoring non-numeric values
        sorted_players = numeric_votes.sort_values(ascending=False)

        # Process the sum of votes for each player
        for player_id, total_votes in row.items():
            if float(total_votes) >= 1:
                vote_sum_counts[player_id]['To Poll a Vote'] += 1
            if float(total_votes) >= 10:
                vote_sum_counts[player_id]['To Poll 10 Votes'] += 1
            if float(total_votes) >= 15:
                vote_sum_counts[player_id]['To Poll 15 Votes'] += 1
            if float(total_votes) >= 20:
                vote_sum_counts[player_id]['To Poll 20 Votes'] += 1

    vote_sum_df = pd.DataFrame(vote_sum_counts).T
    vote_sum_df['Model'] = model

    # Reset index for vote_sum_df and merge with player_ids_df
    vote_sum_df = vote_sum_df.reset_index()
    vote_sum_df = vote_sum_df.merge(player_ids_df, how='left', left_on=['index'], right_on=['player_id'])

    # Market labels
    market_labels = ['To Poll a Vote', 'To Poll 10 Votes', 'To Poll 15 Votes', 'To Poll 20 Votes']
    markets = []

    # Loop through the market labels and create DataFrames
    for i, label in enumerate(market_labels):
        market_df = pd.DataFrame({
            'Model': vote_sum_df['Model'],
            'market_name': vote_sum_df.columns[i + 1],  # i + 1 to skip the 'Model' column
            'runner_name': vote_sum_df['runner_name'],
            'rated_price': vote_sum_df[vote_sum_df.columns[i + 1]]
        })
        markets.append(market_df)

    # Concatenate all the DataFrames into one
    final_vote_df = pd.concat(markets, ignore_index=True)
    final_vote_df['rated_price'] = 1/(final_vote_df['rated_price']/num_simulations)

    # Write results to CSV
    if counter == 0:
        final_vote_df.to_csv('toPollXVotesMarkets.csv', header=True, index=True, mode="w")
    else:
        final_vote_df.to_csv('toPollXVotesMarkets.csv', header=False, index=True, mode="a")

    counter += 1
    print(f'model {counter} processed')
```

## Combine Ratings and Join to Betfair markets

Now just combine all our csv files and then join to our market data that we've pulled from the Betfair API - [API File](src/modelling/assets/brownlow_market_prices.csv)

```py title="Combine Files"

monte_carlo_rated_prices = [final_vote_df,final_rank_df,head_to_head,lines,player_team_votes,df_team_highest_count]

all_rated_prices = pd.concat(monte_carlo_rated_prices,ignore_index=True)
all_rated_prices['runner_name'] = all_rated_prices['runner_name'].str.replace('-',' ')
all_rated_prices.to_csv('all_rated_prices.csv',index=False)

brownlow_prices = pd.read_csv('brownlow_market_prices.csv')
brownlow_prices['runner_name'] = brownlow_prices['runner_name'].str.replace('-',' ')
brownlow_prices['runner_name'] = brownlow_prices['runner_name'].str.replace('McClugagge','McCluggage')
brownlow_rated_prices = brownlow_prices.merge(all_rated_prices,how='left',on=['market_name','runner_name'])

# Replace 'inf' with 1000
brownlow_rated_prices['rated_price'] = brownlow_rated_prices['rated_price'].replace('inf', 1000).astype(float)

# Cap values greater than 1000 to 1000
brownlow_rated_prices['rated_price'] = brownlow_rated_prices['rated_price'].where(brownlow_rated_prices['rated_price'] <= 1000, 1000)

# Drop disqualified players
brownlow_rated_prices = brownlow_rated_prices.drop(
    brownlow_rated_prices[
        (brownlow_rated_prices['market_name'] == 'Winner') & 
        (brownlow_rated_prices['best_back_price'] == 1.01)
    ].index
)
# Calculate Implied Value compared to market prices
brownlow_rated_prices['implied_value'] = 1 / brownlow_rated_prices['rated_price'] - 1 / brownlow_rated_prices['best_back_price']
brownlow_rated_prices.to_csv('brownlow_rated_prices.csv',index=False)

```

## Conclusion

This code does take quite a lot of time to setup however the process is powerful and can be used across any market on the exchange.
While the Brownlow is a once yearly event, if you took the time to set this up for Match Odds or Handicap markets, it can be used on a more regular basis!

--- 
### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.