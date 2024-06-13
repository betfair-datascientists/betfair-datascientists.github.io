# AFL Player Disposals Tutorial

There are many possible ways to bet on an AFL match. Whilst Handicaps, Total Points and Match Odds have long been the traditional ways to bet into AFL markets, 'Player Proposition' bets have become the next big thing in AFL wagering. Traditionally, Same Game Multis will have options to pick players to have at least XX disposals, however 'Player Disposal Line' markets have quickly shot-up to be the next biggest market on the Betfair Exchange with regards to AFL. 

A player disposal line will be set at XX.5 disposals which, in theory, has a 50% chance of being over or under the true disposal prediction. The punter then needs to decide when they think the line is right or not, and take a position on either side. This tutorial here will outline how we can use data freely available online to generate predictions for player disposals.

AFL Data is made available from the R package (fitzRoy)[https://github.com/jimmyday12/fitzRoy] which requires installation of R and use of the Python R-emulator 'rpy2'. (Direct R code can also be used.) This package pulls data from four separate sites which all have similar data with only a few columns differing between each, however due to the differing ways these sources display team and player names, matching between them can be painful. For the purposes of this tutorial we will use the 'fryzigg' function in fitzRoy which pulls data from (Squiggle)[https://squiggle.com.au/], a renowned site for AFL modellers.

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

