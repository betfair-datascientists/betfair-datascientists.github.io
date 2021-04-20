# Australian Open Datathon R Tutorial

## Overview
### The Task
This notebook will outline how the Betfair Data Scientists went about modelling the Australian Open for Betfair's Australian Open Datathon. The task is simple: we ask you to predict the winner of every possible Australian Open matchup using data which we provide.

The metric used to determine the winner will be log loss, based on the actual matchups that happen in the Open. For more information on log loss, click [here](http://wiki.fast.ai/index.php/Log_Loss).

For a detailed outline of the task, the prizes, and to sign up, click [here](https://www.betfair.com.au/hub/australian-open-datathon/).

How an outline of our methodology and thought process, read [this](/modelling/howToModelTheAusOpen) article.

### Intention
This notebook will demonstrate how to:

- Process the raw data sets
- Produce simple features
- Run a predictive model on H2O
- Outputs the final predictions for the submissions
- Load the data and required packages

``` r
import numpy as np
import pandas as pd
import os
import gc
import sys
import warnings
warnings.filterwarnings('ignore')
import h2o
from h2o.automl import H2OAutoML


pd.options.display.max_columns = 999
```

``` r
# We are loading both the mens and womens match csvs
df_atp = pd.read_csv("data/ATP_matches.csv")
df_wta = pd.read_csv("data/WTA_matches.csv")
```

---
## Data pre-processing
Filter the matches to hard and indoor hard only due to the fact that Australian Open is on hard surface and we want the models to train specifically for hard surfaces matches

Convert the columns in both datasets to the correct types. For example, we want to make sure the date columns are in the datetime format and numerical columns are either integer or floats. This will help reduce the memory in use and make the feature engineering process easier

``` r
### Include hard and indoor hard only
df_atp = df_atp.loc[df_atp.Court_Surface.isin(['Hard','Indoor Hard'])]
df_wta = df_wta.loc[df_wta.Court_Surface.isin(['Hard','Indoor Hard'])]

### Exclude qualifying rounds
df_atp = df_atp.loc[df_atp.Round_Description != 'Qualifying']
df_wta = df_wta.loc[df_wta.Round_Description != 'Qualifying']

# Store the shape of the data for reference check later
atp_shape = df_atp.shape
wta_shape = df_wta.shape
```

``` r
numeric_columns = ['Winner_Rank', 'Loser_Rank', 'Retirement_Ind',
                   'Winner_Sets_Won', 'Winner_Games_Won', 'Winner_Aces',
                   'Winner_DoubleFaults', 'Winner_FirstServes_Won',
                   'Winner_FirstServes_In', 'Winner_SecondServes_Won',
                   'Winner_SecondServes_In', 'Winner_BreakPoints_Won',
                   'Winner_BreakPoints', 'Winner_ReturnPoints_Won',
                   'Winner_ReturnPoints_Faced', 'Winner_TotalPoints_Won', 'Loser_Sets_Won',
                   'Loser_Games_Won', 'Loser_Aces', 'Loser_DoubleFaults',
                   'Loser_FirstServes_Won', 'Loser_FirstServes_In',
                   'Loser_SecondServes_Won', 'Loser_SecondServes_In',
                   'Loser_BreakPoints_Won', 'Loser_BreakPoints', 'Loser_ReturnPoints_Won',
                   'Loser_ReturnPoints_Faced', 'Loser_TotalPoints_Won']

text_columns = ['Winner', 'Loser',  'Tournament', 'Court_Surface','Round_Description'] 

date_columns = ['Tournament_Date']

# we set the **erros** to coerce so any non-numerical values (text,special characters) will return an NA
df_atp[numeric_columns] = df_atp[numeric_columns].apply(pd.to_numeric,errors = 'coerce')
df_wta[numeric_columns] = df_wta[numeric_columns].apply(pd.to_numeric,errors = 'coerce')


df_atp[date_columns] = df_atp[date_columns].apply(pd.to_datetime) 
df_wta[date_columns] = df_wta[date_columns].apply(pd.to_datetime)
```

---
## Feature Engineering
The raw datasets are constructed in a way that each row will have the seperate stats for both the winner and loser of that match. However, we want to reshape the data so that each row we will only have one player randomly selected from the winner/loser columns and the features are the difference between opponents statistics (Difference of Averages), such as the difference between average first serve % in a single column rather than Player 1’s first serve % and Player 2’s first serve % in two separate columns.

In addition, for the features, we will take the rolling average of the player's most recent 15 matches before the particular tournament starts. For example, if the match is the second round of the Australian Open 2018, the features will be the last 15 matches before the first round of Australian Open 2018. The reason of not including the stats in the first round is that we would not have known the player's stats in the first round for the final submissions

A typical row of the transformed data will look like this – For a match between Player A – Roger Federer and Player B – Rafael Nadal, we will have a bunch of features like the difference in first serve %, difference in ELO rating etc. The target variable will be whether or not Player A wins (1=Player A wins and 0=lose).

The steps we take are:

- Convert the raw data frames into long format:
- Create some new features
- Take the rolling average for each player and each match
    Since we will be only training our models on US Open and Australian Open, we will only be creating features for those matches. However, the rolling average will take into account any hard surface matches before those tournaments

- Calculate the difference of averages for each match in the data frames

---
## Convert the raw data frames into long format:

``` r
# Before we split the data frame into winner and loser, we want to create a feature that captures the total number of games the match takes.
# We have to do it before the split or we will lose this information
df_atp['Total_Games'] = df_atp.Winner_Games_Won + df_atp.Loser_Games_Won
df_wta['Total_Games'] = df_wta.Winner_Games_Won + df_wta.Loser_Games_Won


# Get the column names for the winner and loser stats
winner_cols = [col for col in df_atp.columns if col.startswith('Winner')]
loser_cols = [col for col in df_atp.columns if col.startswith('Loser')]

# create a winner data frame to store the winner stats and a loser data frame for the losers
# In addition to the winner and loser columns, we are adding common columns as well (e.g. tournamnt dates)
common_cols = ['Total_Games','Tournament','Tournament_Date', 'Court_Surface','Round_Description']
df_winner_atp = df_atp[winner_cols + common_cols]
df_loser_atp = df_atp[loser_cols + common_cols]
df_winner_wta = df_wta[winner_cols + common_cols]
df_loser_wta = df_wta[loser_cols + common_cols]

# Create a new column to show whether the player has won or not. 
df_winner_atp["won"] = 1
df_loser_atp["won"] = 0

df_winner_wta["won"] = 1
df_loser_wta["won"] = 0


# Rename the columns for the winner and loser data frames so we can append them later on.
# We will rename the Winner_ / Loser_ columns to Player_

new_column_names = [col.replace('Winner','Player') for col in winner_cols]

df_winner_atp.columns = new_column_names + common_cols + ['won']

# They all should be the same
df_loser_atp.columns  = df_winner_atp.columns
df_winner_wta.columns  = df_winner_atp.columns
df_loser_wta.columns  = df_winner_atp.columns


# append the winner and loser data frames 

df_long_atp= df_winner_atp.append(df_loser_atp)
df_long_wta= df_winner_wta.append(df_loser_wta)
```

So now our data frames are in long format and should looks like this

``` r
df_long_atp.head()
```

|Player|Player_Rank|Player_Sets_Won|Player_Games_Won|Player_Aces|Player_DoubleFaults|Player_FirstServes_Won|Player_FirstServes_In|Player_SecondServes_Won|Player_SecondServes_In|Player_BreakPoints_Won|Player_BreakPoints|Player_ReturnPoints_Won|Player_ReturnPoints_Faced|Player_TotalPoints_Won|Total_Games|Tournament|Tournament_Date|Court_Surface|Round_Description|won| 
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|Edouard Roger-Vasselin|106.0|2.0|12|5.0|2.0|22|30|12|19|4.0|7.0|25.0|59.0|59|19|Chennai|2012-01-02|Hard|First Round|1|
|Dudi Sela|83.0|2.0|12|2.0|0.0|14|17|11|16|6.0|14.0|36.0|58.0|61|13|Chennai|2012-01-02|Hard|First Round|1|
|Go Soeda|120.0|2.0|19|6.0|1.0|48|64|19|39|5.0|11.0|42.0|105.0|109|33|Chennai|2012-01-02|Hard|First Round|1|
|Yuki Bhambri|345.0|2.0|12|1.0|2.0|22|29|9|17|5.0|13.0|34.0|62.0|65|17|Chennai|2012-01-02|Hard|First Round|1|
|Yuichi Sugita|235.0|2.0|12|3.0|1.0|37|51|11|27|3.0|7.0|22.0|54.0|70|19|Chennai|2012-01-02|Hard|First Round|1|

---
## Create some new features
Thinking about the dynamics of tennis, we know that players often will matches by “breaking” the opponent’s serve (i.e. winning a game when the opponent is serving). This is especially important in tennis. Let’s create a feature called Player_BreakPoints_Per_Game, which is the number of breakpoints a player gets per game that they play (even though they can only get breakpoints every second game, we will use total games). Let’s also create a feature called Player_Return_Win_Ratio which is the proportion of points won when returning.

Similarly, “holding” serve is important (i.e. winning a game when you are serving). Let’s create a feature called Player_Serve_Win_Ratio which is the proportion of points won when serving.

Finally, you only win a set of tennis by winning more sets than your opponent. To win a set, you need to win games. Let’s create a feature called Player_Game_Win_Percentage which is the propotion of games that a player wins.

So the four new features we will create are:

- `Player_Serve_Win_Ratio`
- `Player_Return_Win_Ratio`
- `Player_BreakPoints_Per_Return_Game`
- `Player_Game_Win_Percentage`

``` r
# Here, we will define a function so we can apply it to both atp and wta data frames
def get_new_features(df):

    # Input: 
#     df: data frame to get the data from

     # Return: the df with the new features
    
    
    # Point Win ratio when serving
    df['Player_Serve_Win_Ratio'] = (df.Player_FirstServes_Won + df.Player_SecondServes_Won - df.Player_DoubleFaults) \
                                  /(df.Player_FirstServes_In + df.Player_SecondServes_In + df.Player_DoubleFaults)
    # Point win ratio when returning
    df['Player_Return_Win_Ratio'] = df.Player_ReturnPoints_Won / df.Player_ReturnPoints_Faced
    # Breakpoints per receiving game
    df['Player_BreakPoints_Per_Return_Game'] = df.Player_BreakPoints/df.Total_Games  
    df['Player_Game_Win_Percentage'] = df.Player_Games_Won/df.Total_Games

    return df


# Apply the function we just created to the long data frames
df_long_atp = get_new_features(df_long_atp)
df_long_wta = get_new_features(df_long_wta)
```

``` r
# The long table should have exactly twice of the rows of the original data
assert df_long_atp.shape[0] == atp_shape[0]*2
assert df_long_wta.shape[0] == wta_shape[0]*2
```

---
## Take the rolling average for each player and each match
To train our models, we cannot simply use the player stats for that current match. In fact, we wont be able to use any stats from the same tournament. The logic behind this is that when we try to predict the results in 2019, we would not know the stats of any of the matches in the Australian Open 2019 tournament. As a result, we will use the players' past performance. Here, we will do a rolling average of the most recent 15 matches before the tournament.

To do the above, we will follow the steps below:

1. List all the tournament dates for US and Australian Opens
2. Loop through the dates from point 1, for each date, we filter the data to only include matches before that date and take the most recent 15 games
3. Take the average of those 15 games

``` r
# the two tournaments we will be using for training and thus the feature generation
tournaments = ['U.S. Open, New York','Australian Open, Melbourne']

# Store the dates for the loops 
tournament_dates_atp = df_atp.loc[df_atp.Tournament.isin(tournaments)].groupby(['Tournament','Tournament_Date']) \
.size().reset_index()[['Tournament','Tournament_Date']]

tournament_dates_wta = df_wta.loc[df_wta.Tournament.isin(tournaments)].groupby(['Tournament','Tournament_Date']) \
.size().reset_index()[['Tournament','Tournament_Date']]


# We are adding one more date for the final prediction
tournament_dates_atp.loc[-1] = ['Australian Open, Melbourne',pd.to_datetime('2019-01-15')]
tournament_dates_wta.loc[-1] = ['Australian Open, Melbourne',pd.to_datetime('2019-01-15')]
```

Following are the dates for each tournament

``` r
tournament_dates_atp
```

|Tournament|Tournament_Date|
|-|-|
|Australian Open, Melbourne|2012-01-16|
|Australian Open, Melbourne|2013-01-1|
|Australian Open, Melbourne|2014-01-1|
|Australian Open, Melbourne|2015-01-1|
|Australian Open, Melbourne|2016-01-1|
|Australian Open, Melbourne|2017-01-1|
|Australian Open, Melbourne|2018-01-1|
|U.S. Open, New York|2012-08-2|
|U.S. Open, New York|2013-08-2|
|U.S. Open, New York|2014-08-25|
|U.S. Open, New York|2015-08-31|
|U.S. Open, New York|2016-08-29|
|U.S. Open, New York|2017-08-28|
|U.S. Open, New York|2018-08-27|
|Australian Open, Melbourne|2019-01-15|

``` r
tournament_dates_wta
```

|Tournament|Tournament_Date|
|-|-|
|Australian Open, Melbourne|2014-01-13|
|Australian Open, Melbourne|2015-01-19|
|Australian Open, Melbourne|2016-01-18|
|Australian Open, Melbourne|2017-01-16|
|Australian Open, Melbourne|2018-01-15|
|U.S. Open, New York|2014-08-25|
|U.S. Open, New York|2015-08-31|
|U.S. Open, New York|2016-08-29|
|U.S. Open, New York|2017-08-28|
|U.S. Open, New York|2018-08-27|
|Australian Open, Melbourne|2019-01-15|

They look fine but it is interesting that for men's, we have two more years of data from 2012 to 2013

``` r
# Let's define a function to calculate the rolling averages
def get_rolling_features (df, date_df=None,rolling_cols = None, last_cols= None):
    
    # Input: 
#     df: data frame to get the data from
#     date_df: data frame that has the start dates for each tournament
#     rolling_cols: columns to get the rolling averages
#     last_cols: columns to get the last value (most recent)

     # Return: the df with the new features
    
    
    # Sort the data by player and dates so the most recent matches are at the bottom
    df = df.sort_values(['Player','Tournament_Date','Tournament'], ascending=True)
    
    # For each tournament, get the rolling averages of that player's past matches before the tournament start date
    for index, tournament_date in enumerate(date_df.Tournament_Date):
        # create a temp df to store the interim results
        df_temp = df.loc[df.Tournament_Date < tournament_date]
        
        # for ranks, we only take the last one. (comment this out if want to take avg of rank)
        df_temp_last = df_temp.groupby('Player')[last_cols].last().reset_index()
        
        # take the most recent 15 matches for the rolling average
        df_temp = df_temp.groupby('Player')[rolling_cols].rolling(15, min_periods=1).mean().reset_index()
        df_temp = df_temp.groupby('Player').tail(1) # take the last row of the above
        
        df_temp= df_temp.merge(df_temp_last, on='Player', how='left')
        
        if index ==0:
            df_result = df_temp
            df_result['tournament_date_index'] = tournament_date # so we know which tournament this feature is for
        else:
            df_temp['tournament_date_index'] = tournament_date
            df_result = df_result.append(df_temp)
    
    df_result.drop('level_1', axis=1,inplace=True)
    
    return df_result
```

``` r
# columns we are applying the rolling averages on
rolling_cols = ['Player_Serve_Win_Ratio', 'Player_Return_Win_Ratio',
               'Player_BreakPoints_Per_Return_Game', 'Player_Game_Win_Percentage']

# columns we are taking the most recent values on
# For the player rank, we think we can just use the latest rank (before the tournament starts) 
# as it should refect the most recent performance of the player
last_cols = ['Player_Rank']


# Apply the rolling average function to the long data frames (it will take a few mins to run)
df_rolling_atp = get_rolling_features (df_long_atp, tournament_dates_atp, rolling_cols, last_cols= last_cols )
df_rolling_wta = get_rolling_features (df_long_wta, tournament_dates_wta, rolling_cols, last_cols= last_cols)
```

``` r
df_rolling_atp.head(2)
```

|Player|Player_Serve_Win_Ratio|Player_Return_Win_Ratio|Player_BreakPoints_Per_Return_Game|Player_Game_Win_Percentage|Player_Rank|tournament_date_index|
|-|-|-|-|-|-|-|
|Adrian Mannarino|0.623408|0.353397|0.257859|0.447246|87.0|2012-01-16|
|Albert Montanes|0.507246|0.195652|0.000000|0.294118|50.0|2012-01-16|

``` r
df_rolling_wta.head(2)
```

|Player|Player_Serve_Win_Ratio|Player_Return_Win_Ratio|Player_BreakPoints_Per_Return_Game|Player_Game_Win_Percentage|Player_Rank|tournament_date_index|
|-|-|-|-|-|-|-
|Agnieszka Radwanska|0.413333|0.475410|0.350000|0.350000|5.0|2014-01-13|
|Ajla Tomljanovic|0.468457|0.407319|0.242253|0.462634|75.0|2014-01-13|

---
## Calculate the difference of averages for each match in the data frames
In the original data frames, the first column is always the winner and followed by the loser. Same for the player stats. Thus, we cannot simply calculate the difference between winner and loser and create a target variable indicating player 1 will win or not because it will always be the winner in this case (target always = 1). As a result, we need to pick a player randomly so the player might or might not be the winner

In addition, instead of using both the features for player 1 and 2, we will take the difference of averages between the randomised player 1 and 2. The main benefit is that it will reduce the number of features to half

Steps:

1. We will create a random number for each player which only return 0 or 1
2. If it is zero, we will assign the winner to player 1 and loser to player 2
3. We will join the features to the player 1 and 2. The join will be on the player names and the tournament date (tournament_index in the feature data frames)
4. For players who do not have any history, we will fill the stats by zeros and rank by 999

``` r
# Randomise the match_wide dataset so the first player is not always the winner

# set a seed so the random number is reproducable
np.random.seed(2)

# randomise a number 0/1 with 50% chance each
# if 0 then take the winner, 1 then take loser

df_atp['random_number'] = np.random.randint(2, size=len(df_atp))
df_atp['randomised_player_1'] = np.where(df_atp['random_number']==0,df_atp['Winner'],df_atp['Loser'])
df_atp['randomised_player_2'] = np.where(df_atp['random_number']==0,df_atp['Loser'],df_atp['Winner'])

df_wta['random_number'] = np.random.randint(2, size=len(df_wta))
df_wta['randomised_player_1'] = np.where(df_wta['random_number']==0,df_wta['Winner'],df_wta['Loser'])
df_wta['randomised_player_2'] = np.where(df_wta['random_number']==0,df_wta['Loser'],df_wta['Winner'])

# set the target (win/loss) based on the new randomise number
df_atp['player_1_win'] = np.where(df_atp['random_number']==0,1,0)
df_wta['player_1_win'] = np.where(df_wta['random_number']==0,1,0)


print ('After shuffling, the win rate for player 1 for the mens is {}%'.format(df_atp['player_1_win'].mean()*100))
print ('After shuffling, the win rate for player 1 for the womens is {}%'.format(df_wta['player_1_win'].mean()*100))
```

After shuffling, the win rate for player 1 for the mens is 49.64798919857267%
After shuffling, the win rate for player 1 for the womens is 49.697671426733564%
The win rates are close enough to 50%. So we are good to go

``` r
# To get our data frames ready for model training, we will exclude other tournaments from the data now because we have gotten the rolling averages from them and 
# for training, we only need US and Australian Open matches
df_atp = df_atp.loc[df_atp.Tournament.isin(tournaments)]
df_wta = df_wta.loc[df_wta.Tournament.isin(tournaments)]

# now we can remove other stats columns because we will be using the differences
cols_to_keep = ['Winner','Loser','Tournament','Tournament_Date',
                    'player_1_win','randomised_player_1',
                    'randomised_player_2']

df_atp = df_atp[cols_to_keep]
df_wta = df_wta[cols_to_keep]


# Here, we are joining the rolling average data frames to the individual matches. 
# We need to do it twice. One for player 1 and one for player 2

# Get the rolling features for player 1
df_atp = df_atp.merge(df_rolling_atp, how='left',
                      left_on = ['randomised_player_1','Tournament_Date'],
                      right_on = ['Player','tournament_date_index'],
                      validate ='m:1')

df_wta = df_wta.merge(df_rolling_wta, how='left',
                      left_on = ['randomised_player_1','Tournament_Date'],
                      right_on = ['Player','tournament_date_index'],
                      validate ='m:1')

# Get the rolling features for player 2
# we will use '_p1' to denote player 1 and '_p2' for player 2
df_atp = df_atp.merge(df_rolling_atp, how='left',
                      left_on = ['randomised_player_2','Tournament_Date'],
                      right_on = ['Player','tournament_date_index'],
                      validate ='m:1',
                      suffixes=('_p1','_p2'))

df_wta = df_wta.merge(df_rolling_wta, how='left',
                      left_on = ['randomised_player_2','Tournament_Date'],
                      right_on = ['Player','tournament_date_index'],
                      validate ='m:1',
                      suffixes=('_p1','_p2'))
```

``` r
# How many players do not have previous match history
print('{} player_1s do Not have previous match history before the tournament'.format(df_atp.loc[df_atp.Player_p1.isna(),'randomised_player_1'].nunique()))
print('{} player_2s do Not have previous match history before the tournament'.format(df_atp.loc[df_atp.Player_p2.isna(),'randomised_player_2'].nunique()))
```

59 player_1s do Not have previous match history before the tournament
56 player_2s do Not have previous match history before the tournament

``` r
# How many players do not have previous match history
print('{} player_1s do Not have previous match history before the tournament'.format(df_wta.loc[df_wta.Player_p1.isna(),'randomised_player_1'].nunique()))
print('{} player_2s do Not have previous match history before the tournament'.format(df_wta.loc[df_wta.Player_p2.isna(),'randomised_player_2'].nunique()))
```

41 player_1s do Not have previous match history before the tournament
37 player_2s do Not have previous match history before the tournament

``` r
# Most of the missing are for the early years which makes sense as we dont have enough history for them
df_wta.loc[df_wta.Player_p1.isna(),'Tournament_Date'].value_counts()
```

```
2014-01-13    29
2014-08-25     7
2015-08-31     5
2015-01-19     3
2017-08-28     3
2018-01-15     3
2018-08-27     3
Name: Tournament_Date, dtype: int64
```

``` r
df_atp.loc[df_atp.Player_p1.isna(),'Tournament_Date'].value_counts()
```

```
2012-01-16    29
2012-08-27     9
2014-01-13     5
2013-08-26     5
2016-01-18     5
2013-01-14     4
2014-08-25     3
2018-01-15     3
2017-08-28     3
2018-08-27     2
2016-08-29     2
2015-01-19     1
Name: Tournament_Date, dtype: int64
```

Now we have gotten the rolling averages for both player 1 and 2. What we need to do next is to simply calculate their difference.

To calculate the difference, we need to:

1. Split the data frames into two new data frames: Player 1 and Player 2
2. Take the difference between the two data frames

``` r
def get_player_difference(df, diff_cols = None):
        
        # Input: 
#     df: data frame to get the data from
#     diff_cols: columns we take the difference on. For example is diff_cols = win rate. This function will calculate the 
#                difference of the win rates between player 1 and player 2

     # Return: the df with the new features
    
    p1_cols = [i + '_p1' for i in diff_cols] # column names for player 1 stats
    p2_cols = [i + '_p2' for i in diff_cols] # column names for player 2 stats


    # For any missing values, we will fill them by zeros except the ranking where we will use 999
    df['Player_Rank_p1'] = df['Player_Rank_p1'].fillna(999)
    df[p1_cols] = df[p1_cols].fillna(0)
    
    df['Player_Rank_p2'] = df['Player_Rank_p2'].fillna(999)
    df[p2_cols] = df[p2_cols].fillna(0)

    
    new_column_name = [i + '_diff' for i in diff_cols]

    # Take the difference
    df_p1 = df[p1_cols]
    df_p2 = df[p2_cols]
    
    df_p1.columns=new_column_name
    df_p2.columns=new_column_name
    
    df_diff = df_p1 - df_p2
    df_diff.columns = new_column_name
    
    # drop the p1 and p2 columns because We have the differences now
    df.drop(p1_cols + p2_cols, axis=1, inplace=True)
    
    # Concat the df_diff and raw_df
    df = pd.concat([df, df_diff], axis=1)
    
    return df,new_column_name
```

``` r
diff_cols = ['Player_Serve_Win_Ratio',
            'Player_Return_Win_Ratio',
            'Player_BreakPoints_Per_Return_Game',
            'Player_Game_Win_Percentage','Player_Rank']

# Apply the function and get the difference between player 1 and 2
df_atp,_ = get_player_difference(df_atp,diff_cols=diff_cols)
df_wta,_ = get_player_difference(df_wta,diff_cols=diff_cols)

# Make a copy of the data frames in case we need to come back to check the values
df_atp_final = df_atp.copy()
df_wta_final = df_wta.copy()
```

``` r
df_atp_final.head()
```

|Winner|Loser|Tournament|Tournament_Date|player_1_win|randomised_player_1|randomised_player_2|Player_p1|tournament_date_index_p1|Player_p2|tournament_date_index_p2|Player_Serve_Win_Ratio_diff|Player_Return_Win_Ratio_diff|Player_BreakPoints_Per_Return_Game_diff|Player_Game_Win_Percentage_diff|Player_Rank_diff|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|Juan Martin del Potro|Adrian Mannarino|Australian Open, Melbourne|2012-01-16|1|Juan Martin del Potro|Adrian Mannarino|Juan Martin del Potro|2012-01-16|Adrian Mannarino|2012-01-16|0.035030|-0.021271|-0.025975|0.103479|-76.0|
|Pere Riba|Albert Montanes|Australian Open, Melbourne|2012-01-16|1|Pere Riba|Albert Montanes|Pere Riba|2012-01-16|Albert Montanes|2012-01-16|-0.156369|0.008893|0.066667|-0.094118|39.0|
|Tomas Berdych|Albert Ramos-Vinolas|Australian Open, Melbourne|2012-01-16|0|Albert Ramos-Vinolas|Tomas Berdych|Albert Ramos-Vinolas|2012-01-16|NaN|NaT|0.498027|0.380092|0.414815|0.394444|-934.0|
|Rafael Nadal|Alex Kuznetsov|Australian Open, Melbourne|2012-01-16|0|Alex Kuznetsov|Rafael Nadal|NaN|NaT|Rafael Nadal|2012-01-16|-0.670139|-0.423057|-0.445623|-0.574767|997.0|
|Roger Federer|Alexander Kudryavtsev|Australian Open, Melbourne|2012-01-16|0|Alexander Kudryavtsev|Roger Federer|NaN|NaT|Roger Federer|2012-01-16|-0.721415|-0.449516|-0.360255|-0.668090|996.0|

---
## Modelling
We will trian two models here, one for mens and one for womens.

For training, we will use all available data from the second year (too many missing values in the first year) up until 2017.

For validation, we will test the model on the 2018 Australian Open data

This setup allows us to 'mimic' the final prediction (using historical matches to predict 2019 results)

``` r
df_train_atp = df_atp_final.loc[(df_atp_final.Tournament_Date != '2018-01-15') # excluding Aus Open 2018, and
                                & (df_atp_final.Tournament_Date > '2012-01-16')] # excluding first year
df_valid_atp = df_atp_final.loc[df_atp_final.Tournament_Date == '2018-01-15'] # Australian Open 2018 only

df_train_wta = df_wta_final.loc[(df_wta_final.Tournament_Date != '2018-01-15') # excluding Aus Open 2018, and
                                & (df_wta_final.Tournament_Date > '2014-01-13')] # excluding first year
```

``` r
df_train_atp.head()
```

|Winner|Loser|Tournament|Tournament_Date|player_1_win|randomised_player_1|randomised_player_2|Player_p1|tournament_date_index_p1|Player_p2|tournament_date_index_p2|Player_Serve_Win_Ratio_diff|Player_Return_Win_Ratio_diff|Player_BreakPoints_Per_Return_Game_diff|Player_Game_Win_Percentage_diff|Player_Rank_diff|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|Daniel Brands|Adrian Ungur|U.S. Open, New York|2012-08-27|0|Adrian Ungur|Daniel Brands|NaN|NaT|Daniel Brands|2012-08-27|-0.535211|-0.300000|-0.043478|-0.434783|870.0|
|Richard Gasquet|Albert Montanes|U.S. Open, New York|2012-08-27|1|Richard Gasquet|Albert Montanes|Richard Gasquet|2012-08-27|Albert Montanes|2012-08-27|0.080003|0.077451|0.180847|0.131108|-37.0|
|Martin Klizan|Alejandro Falla|U.S. Open, New York|2012-08-27|1|Martin Klizan|Alejandro Falla|Martin Klizan|2012-08-27|Alejandro Falla|2012-08-27|0.077117|-0.044716|-0.087362|0.068180|-2.0|
|Andy Murray|Alex Bogomolov Jr.|U.S. Open, New York|2012-08-27|1|Andy Murray|Alex Bogomolov Jr.|Andy Murray|2012-08-27|Alex Bogomolov Jr.|2012-08-27|0.039641|0.031701|0.094722|0.059010|-69.0|
|Tommy Robredo|Andreas Seppi|U.S. Open, New York|2012-08-27|1|Tommy Robredo|Andreas Seppi|Tommy Robredo|2012-08-27|Andreas Seppi|2012-08-27|-0.026814|0.006442|-0.009930|-0.067780|151.0|

``` r
# target variable
target= 'player_1_win'

# features being fed into the models
feats = ['Player_Serve_Win_Ratio_diff',
         'Player_Return_Win_Ratio_diff',
         'Player_BreakPoints_Per_Return_Game_diff',
         'Player_Game_Win_Percentage_diff',
         'Player_Rank_diff']

print(feats)
```

---
## H2O model for ATP

``` r
h2o.init()

# Convert to an h2o frame
df_train_atp_h2o = h2o.H2OFrame(df_train_atp)
df_valid_atp_h2o = h2o.H2OFrame(df_valid_atp)


# For binary classification, response should be a factor
df_train_atp_h2o[target] = df_train_atp_h2o[target].asfactor()
df_valid_atp_h2o[target] = df_valid_atp_h2o[target].asfactor()

# Run AutoML for 20 base models (limited to 1 hour max runtime by default)
aml_atp = h2o.automl.H2OAutoML(max_runtime_secs=300,
                           max_models=100,
                           stopping_metric='logloss',
                           sort_metric='logloss',
                           balance_classes=True,
                           seed=183
                          )
aml_atp.train(x=feats, y=target, training_frame=df_train_atp_h2o,validation_frame=df_valid_atp_h2o)

# View the AutoML Leaderboard
lb = aml_atp.leaderboard
lb.head()
```

|model_id|auc|logloss|mean_per_class_error|rmse|mse|
|-|-|-|-|-|-|
|GBM_5_AutoML_20181221_094949|0.790281|0.554852|0.281363|0.431379|0.186088|
|GBM_grid_1_AutoML_20181221_094949_model_15|0.789329|0.556804|0.29856|0.431931|0.186564|
|GBM_grid_1_AutoML_20181221_094949_model_7|0.788013|0.557808|0.295899|0.432968|0.187461|
|StackedEnsemble_BestOfFamily_AutoML_20181221_094949|0.788131|0.558028|0.285321|0.432849|0.187358|
|GBM_grid_1_AutoML_20181221_094949_model_20|0.785633|0.561094|0.283932|0.43479|0.189043|
|StackedEnsemble_AllModels_AutoML_20181221_094949|0.784411|0.561587|0.293244|0.434667|0.188935|
|GBM_grid_1_AutoML_20181221_094949_model_25|0.785311|0.561783|0.291912|0.434888|0.189127|
|GBM_grid_1_AutoML_20181221_094949_model_17|0.774832|0.570883|0.295836|0.439375|0.193051|
|DeepLearning_1_AutoML_20181221_094949|0.779388|0.572823|0.311737|0.438479|0.192264|
|GBM_grid_1_AutoML_20181221_094949_model_14|0.7718|0.578867|0.285835|0.441373|0.19481|

``` r
H2O model for WTA
```

``` r
# Convert to an h2o frame
df_train_wta_h2o = h2o.H2OFrame(df_train_wta)
df_valid_wta_h2o = h2o.H2OFrame(df_valid_wta)


# For binary classification, response should be a factor
df_train_wta_h2o[target] = df_train_wta_h2o[target].asfactor()
df_valid_wta_h2o[target] = df_valid_wta_h2o[target].asfactor()

# Run AutoML for 20 base models (limited to 1 hour max runtime by default)
aml_wta = h2o.automl.H2OAutoML(max_runtime_secs=300,
                           max_models=100,
                           stopping_metric='logloss',
                           sort_metric='logloss',
                           balance_classes=True,
                           seed=183
                          )
aml_wta.train(x=feats, y=target, training_frame=df_train_wta_h2o,validation_frame=df_valid_wta_h2o)

# View the AutoML Leaderboard
lb = aml_wta.leaderboard
lb.head()
```

|model_id|auc|logloss|mean_per_class_error|rmse|mse|
|-|-|-|-|-|-|
|StackedEnsemble_AllModels_AutoML_20181221_095400|0.726046|0.60827|0.321222|0.457117|0.208956|
|StackedEnsemble_BestOfFamily_AutoML_20181221_095400|0.724911|0.609329|0.337847|0.457659|0.209452|
|DeepLearning_grid_1_AutoML_20181221_095400_model_3|0.729152|0.612669|0.315971|0.45641|0.20831|
|GBM_grid_1_AutoML_20181221_095400_model_7|0.721204|0.615763|0.336848|0.460885|0.212415|
|GBM_5_AutoML_20181221_095400|0.719252|0.616535|0.319179|0.461055|0.212572|
|GBM_grid_1_AutoML_20181221_095400_model_15|0.715921|0.619263|0.318673|0.462215|0.213643|
|GLM_grid_1_AutoML_20181221_095400_model_1|0.726048|0.622989|0.366124|0.463099|0.214461|
|GBM_grid_1_AutoML_20181221_095400_model_17|0.709261|0.624902|0.34876|0.465628|0.216809|
|GBM_grid_1_AutoML_20181221_095400_model_18|0.70946|0.625704|0.393556|0.466147|0.217293|
|DeepLearning_grid_1_AutoML_20181221_095400_model_2|0.713419|0.628008|0.311334|0.463638|0.21496|

---
## Use the models to predict and make submissions
Now let's use the models we just created to make the submissions

``` r
df_predict_atp = pd.read_csv("data/men_dummy_submission_file.csv")
df_predict_wta = pd.read_csv("data/women_dummy_submission_file.csv", encoding='latin1') # for womens, there are some names need a different encoding
```

``` r
df_predict_wta.head(2)
```

|player_1|player_2|player_1_win_probability|
|-|-|-|
|Simona Halep|Angelique Kerber|0.5|
|Simona Halep|Caroline Wozniacki|0.5|

---
## Get the features for the predict df
We need to join the features to the 2019 players

``` r
# Before we join the features by the names and the dates, we need to convert any non-english characters to english first
translationTable = str.maketrans("éàèùâêîôûçñá", "eaeuaeioucna")


df_predict_atp['player_1'] = df_predict_atp.player_1.apply(lambda x: x.translate(translationTable))
df_predict_atp['player_2'] = df_predict_atp.player_2.apply(lambda x: x.translate(translationTable))
df_predict_wta['player_1'] = df_predict_wta.player_1.apply(lambda x: x.translate(translationTable))
df_predict_wta['player_2'] = df_predict_wta.player_2.apply(lambda x: x.translate(translationTable))


# Also we need to convert the names into lower cases 
df_predict_atp['player_1'] =df_predict_atp['player_1'].str.lower() 
df_predict_atp['player_2'] =df_predict_atp['player_2'].str.lower() 
df_predict_wta['player_1'] =df_predict_wta['player_1'].str.lower() 
df_predict_wta['player_2'] =df_predict_wta['player_2'].str.lower() 

df_rolling_atp['Player'] = df_rolling_atp['Player'].str.lower() 
df_rolling_wta['Player'] = df_rolling_wta['Player'].str.lower() 


# Lastly, some players have slightly difference names in the submission data and the match data. So we are editing them here manually
df_predict_atp.loc[df_predict_atp.player_1=='jaume munar','player_1'] = 'jaume antoni munar clar'
df_predict_atp.loc[df_predict_atp.player_2=='jaume munar','player_2'] = 'jaume antoni munar clar'

df_predict_wta.loc[df_predict_wta.player_1=='daria kasatkina','player_1'] = 'darya kasatkina'
df_predict_wta.loc[df_predict_wta.player_2=='daria kasatkina','player_2'] = 'darya kasatkina'
df_predict_wta.loc[df_predict_wta.player_1=='lesia tsurenko','player_1'] = 'lesya tsurenko'
df_predict_wta.loc[df_predict_wta.player_2=='lesia tsurenko','player_2'] = 'lesya tsurenko'
df_predict_wta.loc[df_predict_wta.player_1=='danielle collins','player_1'] = 'danielle rose collins'
df_predict_wta.loc[df_predict_wta.player_2=='danielle collins','player_2'] = 'danielle rose collins'
df_predict_wta.loc[df_predict_wta.player_1=='anna karolina schmiedlova','player_1'] = 'anna schmiedlova'
df_predict_wta.loc[df_predict_wta.player_2=='anna karolina schmiedlova','player_2'] = 'anna schmiedlova'
df_predict_wta.loc[df_predict_wta.player_1=='georgina garcia perez','player_1'] = 'georgina garcia-perez'
df_predict_wta.loc[df_predict_wta.player_2=='georgina garcia perez','player_2'] = 'georgina garcia-perez'
```

``` r
# create and tournament date column and set it to 2019 so we can join the lastest features
df_predict_atp['Tournament_Date'] = pd.to_datetime('2019-01-15')
df_predict_wta['Tournament_Date'] = pd.to_datetime('2019-01-15')

# Get the rolling features for player 1
df_predict_atp = df_predict_atp.merge(df_rolling_atp, how='left',
                     left_on = ['player_1','Tournament_Date'],
                     right_on = ['Player','tournament_date_index'],validate ='m:1')
df_predict_wta = df_predict_wta.merge(df_rolling_wta, how='left',
                     left_on = ['player_1','Tournament_Date'],
                     right_on = ['Player','tournament_date_index'],validate ='m:1')


# Get the rolling features for player 2
# For duplicate columns, we will use '_p1' to denote player 1 and '_p2' for player 2
df_predict_atp = df_predict_atp.merge(df_rolling_atp, how='left',
                     left_on = ['player_2','Tournament_Date'],
                     right_on = ['Player','tournament_date_index'],validate ='m:1',suffixes=('_p1','_p2'))
df_predict_wta = df_predict_wta.merge(df_rolling_wta, how='left',
                     left_on = ['player_2','Tournament_Date'],
                     right_on = ['Player','tournament_date_index'],validate ='m:1',suffixes=('_p1','_p2'))
```

``` r
df_predict_atp.head(2)
```

|player_1|player_2|player_1_win_probability|Tournament_Date|Player_p1|Player_Serve_Win_Ratio_p1|Player_Return_Win_Ratio_p1|Player_BreakPoints_Per_Return_Game_p1|Player_Game_Win_Percentage_p1|Player_Rank_p1|tournament_date_index_p1|Player_p2|Player_Serve_Win_Ratio_p2|Player_Return_Win_Ratio_p2|Player_BreakPoints_Per_Return_Game_p2|Player_Game_Win_Percentage_p2|Player_Rank_p2|tournament_date_index_p2|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|novak djokovic|rafael nadal|0.5|2019-01-15|novak djokovic|0.685903|0.426066|0.42378|0.640857|2.0|2019-01-15|rafael nadal|0.622425|0.401028|0.334270|0.570833|1.0|2019-01-15|
|novak djokovic|roger federer|0.5|2019-01-15|novak djokovic|0.685903|0.426066|0.42378|0.640857|2.0|2019-01-15|roger federer|0.620070|0.389781|0.269224|0.564244|3.0|2019-01-15|

``` r
# How many players do not have previous match history
print('{} player_1s do Not have previous match history before the tournament in the mens'.format(df_predict_atp.loc[df_predict_atp.Player_p1.isna(),'player_1'].nunique()))
print('{} player_2s do Not have previous match history before the tournament in the mens'.format(df_predict_atp.loc[df_predict_atp.Player_p2.isna(),'player_2'].nunique()))
```

3 player_1s do Not have previous match history before the tournament in the mens
3 player_2s do Not have previous match history before the tournament in the mens

``` r
# How many players do not have previous match history
print('{} player_1s do Not have previous match history before the tournament in the womens'.format(df_predict_wta.loc[df_predict_wta.Player_p1.isna(),'player_1'].nunique()))
print('{} player_2s do Not have previous match history before the tournament in the womens'.format(df_predict_wta.loc[df_predict_wta.Player_p2.isna(),'player_2'].nunique()))
```

0 player_1s do Not have previous match history before the tournament in the womens
0 player_2s do Not have previous match history before the tournament in the womens

``` r
print(df_predict_atp.loc[df_predict_atp.Player_p1.isna(),'player_1'].unique().tolist())
['christian garin', 'pedro sousa', 'hugo dellien']
```

``` r
print(df_predict_wta.loc[df_predict_wta.Player_p1.isna(),'player_1'].unique().tolist())
[]
```

We will do the differencing again for the prediction data frames exactly like what we did for training

``` r
# Apply the function and get the difference between player 1 and 2
df_predict_atp,_ = get_player_difference(df_predict_atp,diff_cols=diff_cols)
df_predict_wta,_ = get_player_difference(df_predict_wta,diff_cols=diff_cols)
```

---
## Make the prediction

``` r
df_predict_atp_h2o = h2o.H2OFrame(df_predict_atp[feats])
df_predict_wta_h2o = h2o.H2OFrame(df_predict_wta[feats])

atp_preds = aml_atp.predict(df_predict_atp_h2o)['p1'].as_data_frame()
wta_preds = aml_wta.predict(df_predict_wta_h2o)['p1'].as_data_frame()

df_predict_atp['player_1_win_probability'] = atp_preds
df_predict_wta['player_1_win_probability'] = wta_preds
```

``` r
atp_submission = df_predict_atp[['player_1','player_2','player_1_win_probability']]
wta_submission = df_predict_wta[['player_1','player_2','player_1_win_probability']]
```

``` r
atp_submission.head()
```

|player_1|player_2|player_1_win_probability|
|-|-|-|
|novak djokovic|rafael nadal|0.571588|
|novak djokovic|roger federer|0.662511|
|novak djokovic|juan martin del potro|0.544306|
|novak djokovic|alexander zverev|0.709483|
|novak djokovic|kevin anderson|0.687195|

``` r
wta_submission.head()
```

|player_1|player_2|player_1_win_probability|
|-|-|-|
|simona halep|angelique kerber|0.455224|
|simona halep|caroline wozniacki|0.546276|
|simona halep|elina svitolina|0.408014|
|simona halep|naomi osaka|0.285125|
|simona halep|sloane stephens|0.576643|

Let's look at who has the highest win rate from our models

``` r
atp_submission.groupby('player_1')['player_1_win_probability'].mean() \
.reset_index().sort_values('player_1_win_probability',ascending=False).head()
```

|player_1|player_1_win_probability|
|-|-|
|novak djokovic|0.846377|
|juan martin del potro|0.787337|
|karen khachanov|0.782963|
|rafael nadal|0.778707|
|roger federer|0.767337|

``` r
wta_submission.groupby('player_1')['player_1_win_probability'].mean() \
.reset_index().sort_values('player_1_win_probability',ascending=False).head()
```

|player_1|player_1_win_probability|
|-|-|
|madison keys|0.750580|
|naomi osaka|0.749195|
|caroline wozniacki|0.722409|
|kiki bertens|0.713904|
|aryna sabalenka|0.707368|

Now we can output the predictions as csvs

``` r
atp_submission.to_csv('submission/atp_submission_python.csv',index=False)
wta_submission.to_csv('submission/wta_submission_pthon.csv',index=False)
```

``` r
atp_submission.shape
```

(16256, 3)