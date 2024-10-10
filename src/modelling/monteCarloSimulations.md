# Monte Carlo Simulations in Python - Brownlow Medal

Monte Carlo simulations are a way to estimate outcomes by running a model many times with random inputs to see the range of possible results. It’s useful when you have uncertainty or variability, like in sports or finance.

Imagine you're trying to predict how many goals a team will score in a match, but there are many factors you can't control, like weather or player form. Instead of guessing a single outcome, you run a simulation where you randomly vary these factors based on their likelihood (like rolling dice). After running the simulation thousands of times, you can see the most common results and the likelihood of different outcomes.

It's called Monte Carlo because it’s similar to gambling in a casino, where random events affect the result.

In this tutorial we will run through a basic python script for running Monte Carlo simulations on an entry submitted for the 2024 Brownlow Medal Datathon.
In this datathon we predicted the expected votes each player would receive in each match as the output of a regression model. This output however, did not generate a rated price for a player to win the whole event or to poll the most votes in their team.

## Data File

 - (Brownlow Medal Predictions)[src/modelling/assets/Brownlow_Medal_Datathon_2024_Submission_Form.csv]

## Using the Poisson distribution. 

Monte Carlo simulations the probability of each class occurring to generate outcomes, and so we need to calculate the probability of each class occurring from our regression value.

We need to use the Poisson distribution to calculate the probability that our player will poll 1, 2, or 3 votes. (for more info on the Poisson distribution see (here)[https://en.wikipedia.org/wiki/Poisson_distribution])

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
            
            # Normalize the probabilities so they sum to 1
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

