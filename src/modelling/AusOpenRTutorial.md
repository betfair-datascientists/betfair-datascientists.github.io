# Australian Open Datathon R Tutorial

## Overview
### The Task
This notebook will outline how the Betfair Data Scientists went about modelling the Australian Open for Betfair's Australian Open Datathon. The task is simple: we ask you to predict the winner of every possible Australian Open matchup using data which we provide.

The metric used to determine the winner will be log loss, based on the actual matchups that happen in the Open. For more information on log loss, click [here](http://wiki.fast.ai/index.php/Log_Loss).

How an outline of our methodology and thought process, read [this](/modelling/howToModelTheAusOpen) article.

---
## Exploring the Data
First we need to get an idea of what the data looks like. Let's read the men's data in and get an idea of what it looks like. Note that you will need to install all the packages listed below unless you already have them.

Note that for this tutorial I will be using `dplyr`, if you are not familiar with the syntax I encourage you to read up on [the basics](https://cran.r-project.org/web/packages/dplyr/vignettes/dplyr.html).

``` r
# Import libraries
library(dplyr)
library(readr)
library(tidyr)
library(RcppRoll)
library(tidyselect)
library(lubridate)
library(stringr)
library(zoo)
library(purrr)
library(h2o)
library(DT)
mens = readr::read_csv('data/ATP_matches.csv', na = ".") # NAs are indicated by .
mens %>%
  datatable(rownames = FALSE, extensions = 'Scroller', 
            options = list(dom = "t", 
            scrollY = 450,
            scroller = TRUE,
            scrollX = 600,
            fixedColumns = TRUE)) %>%
  formatRound(columns=pluck(., "x", "data") %>% colnames(), digits=3)
```

| Winner | Loser | Tournament | Tournament_Date | Court_Surface | Round_Description | Winner_Rank | Loser_Rank | Retirement_Ind | Winner_Sets_Won | ... | Loser_DoubleFaults | Loser_FirstServes_Won | Loser_FirstServes_In | Loser_SecondServes_Won | Loser_SecondServes_In | Loser_BreakPoints_Won | Loser_BreakPoints | Loser_ReturnPoints_Won | Loser_ReturnPoints_Faced | Loser_TotalPoints_Won |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Edouard Roger-Vasselin | Eric Prodon | Chennai | 2-Jan-12 | Hard | First Round | 106 | 97 | 0 | 2 | ... | 3 | 21 | 33 | 13 | 26 | 1 | 3 | 15 | 49 | 49 |
| Dudi Sela | Fabio Fognini | Chennai | 2-Jan-12 | Hard | First Round | 83 | 48 | 0 | 2 | ... | 4 | 17 | 32 | 5 | 26 | 0 | 1 | 8 | 33 | 30 |
| Go Soeda | Frederico Gil | Chennai | 2-Jan-12 | Hard | First Round | 120 | 102 | 0 | 2 | ... | 2 | 45 | 70 | 18 | 35 | 2 | 4 | 36 | 103 | 99 |
| Yuki Bhambri | Karol Beck | Chennai | 2-Jan-12 | Hard | First Round | 345 | 101 | 0 | 2 | ... | 1 | 15 | 33 | 13 | 29 | 2 | 3 | 15 | 46 | 43 |
| Yuichi Sugita | Olivier Rochus | Chennai | 2-Jan-12 | Hard | First Round | 235 | 67 | 0 | 2 | ... | 0 | 19 | 32 | 13 | 22 | 1 | 7 | 30 | 78 | 62 |
| Benoit Paire | Pere Riba | Chennai | 2-Jan-12 | Hard | First Round | 95 | 89 | 0 | 2 | ... | 5 | 13 | 20 | 12 | 32 | 0 | 1 | 9 | 44 | 34 |
| Victor Hanescu | Sam Querrey | Chennai | 2-Jan-12 | Hard | First Round | 90 | 93 | 0 | 2 | ... | 8 | 29 | 41 | 7 | 24 | 1 | 3 | 17 | 57 | 53 |
| Yen-Hsun Lu | Thiemo de Bakker | Chennai | 2-Jan-12 | Hard | First Round | 82 | 223 | 0 | 2 | ... | 0 | 20 | 32 | 10 | 24 | 1 | 1 | 19 | 57 | 49 |
| Andreas Beck | Vasek Pospisil | Chennai | 2-Jan-12 | Hard | First Round | 98 | 119 | 0 | 2 | ... | 3 | 39 | 57 | 16 | 38 | 1 | 5 | 24 | 74 | 79 |
| Ivan Dodig | Vishnu Vardhan | Chennai | 2-Jan-12 | Hard | First Round | 36 | 313 | 0 | 2 | ... | 5 | 41 | 59 | 13 | 27 | 2 | 8 | 34 | 101 | 88 |
| David Goffin | Xavier Malisse | Chennai | 2-Jan-12 | Hard | First Round | 174 | 49 | 0 | 2 | ... | 1 | 31 | 43 | 19 | 34 | 1 | 4 | 27 | 85 | 77 |
| David Goffin | Andreas Beck | Chennai | 2-Jan-12 | Hard | Second Round | 174 | 98 | 0 | 2 | ... | 0 | 43 | 71 | 14 | 27 | 2 | 8 | 27 | 82 | 84 |
| Dudi Sela | Benoit Paire | Chennai | 2-Jan-12 | Hard | Second Round | 83 | 95 | 0 | 2 | ... | 5 | 40 | 58 | 21 | 46 | 1 | 7 | 26 | 87 | 87 |
| Stan Wawrinka | Edouard Roger-Vasselin | Chennai | 2-Jan-12 | Hard | Second Round | 17 | 106 | 0 | 2 | ... | 0 | 43 | 70 | 16 | 34 | 4 | 6 | 28 | 82 | 87 |
| Go Soeda | Ivan Dodig | Chennai | 2-Jan-12 | Hard | Second Round | 120 | 36 | 0 | 2 | ... | 2 | 31 | 41 | 11 | 28 | 1 | 4 | 23 | 73 | 65 |
| Milos Raonic | Victor Hanescu | Chennai | 2-Jan-12 | Hard | Second Round | 31 | 90 | 0 | 2 | ... | 1 | 25 | 38 | 5 | 14 | 0 | 4 | 15 | 56 | 45 |
| Yuichi Sugita | Yen-Hsun Lu | Chennai | 2-Jan-12 | Hard | Second Round | 235 | 82 | 0 | 2 | ... | 4 | 34 | 45 | 12 | 34 | 2 | 9 | 38 | 93 | 84 |
| Janko Tipsarevic | Yuki Bhambri | Chennai | 2-Jan-12 | Hard | Second Round | 9 | 345 | 0 | 2 | ... | 2 | 12 | 22 | 9 | 17 | 0 | 1 | 8 | 41 | 29 |
| Janko Tipsarevic | David Goffin | Chennai | 2-Jan-12 | Hard | Quarter-finals | 9 | 174 | 0 | 2 | ... | 5 | 34 | 51 | 19 | 40 | 1 | 2 | 18 | 67 | 71 |
| Milos Raonic | Dudi Sela | Chennai | 2-Jan-12 | Hard | Quarter-finals | 31 | 83 | 0 | 2 | ... | 2 | 23 | 31 | 19 | 28 | 0 | 3 | 16 | 69 | 58 |
| Go Soeda | Stan Wawrinka | Chennai | 2-Jan-12 | Hard | Quarter-finals | 120 | 17 | 0 | 2 | ... | 4 | 18 | 34 | 13 | 31 | 3 | 7 | 31 | 74 | 62 |
| Nicolas Almagro | Yuichi Sugita | Chennai | 2-Jan-12 | Hard | Quarter-finals | 10 | 235 | 0 | 2 | ... | 1 | 36 | 65 | 30 | 40 | 3 | 12 | 45 | 123 | 111 |
| Janko Tipsarevic | Go Soeda | Chennai | 2-Jan-12 | Hard | Semi-finals | 9 | 120 | 0 | 2 | ... | 1 | 21 | 33 | 10 | 28 | 1 | 1 | 10 | 44 | 41 |
| Milos Raonic | Nicolas Almagro | Chennai | 2-Jan-12 | Hard | Semi-finals | 31 | 10 | 0 | 2 | ... | 0 | 31 | 45 | 8 | 15 | 0 | 3 | 12 | 54 | 51 |
| Milos Raonic | Janko Tipsarevic | Chennai | 2-Jan-12 | Hard | Finals | 31 | 9 | 0 | 2 | ... | 2 | 59 | 83 | 34 | 55 | 0 | 4 | 25 | 113 | 118 |
| Igor Andreev | Adrian Mannarino | Brisbane | 2-Jan-12 | Hard | First Round | 115 | 87 | 0 | 2 | ... | 3 | 24 | 35 | 13 | 25 | 1 | 3 | 21 | 70 | 58 |
| Alexandr Dolgopolov | Alejandro Falla | Brisbane | 2-Jan-12 | Hard | First Round | 15 | 74 | 0 | 2 | ... | 3 | 16 | 33 | 12 | 25 | 3 | 7 | 33 | 75 | 61 |
| Tatsuma Ito | Benjamin Mitchell | Brisbane | 2-Jan-12 | Hard | First Round | 122 | 227 | 0 | 2 | ... | 6 | 30 | 44 | 7 | 24 | 0 | 2 | 13 | 52 | 50 |
| Kei Nishikori | Cedrik-Marcel Stebe | Brisbane | 2-Jan-12 | Hard | First Round | 25 | 81 | 0 | 2 | ... | 2 | 27 | 49 | 23 | 41 | 3 | 6 | 28 | 75 | 78 |
| Denis Istomin | Florian Mayer | Brisbane | 2-Jan-12 | Hard | First Round | 73 | 23 | 1 | 1 | ... | 1 | 28 | 38 | 11 | 17 | 0 | 2 | 15 | 56 | 54 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |  | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| Malek Jaziri | Fernando Verdasco | Paris | 29-Oct-18 | Indoor Hard | Second Round | 55 | 27 | 0 | 2 | ... | 6 | 46 | 60 | 16 | 35 | 3 | 13 | 39 | 104 | 101 |
| Alexander Zverev | Frances Tiafoe | Paris | 29-Oct-18 | Indoor Hard | Second Round | 5 | 44 | 0 | 2 | ... | 4 | 26 | 40 | 16 | 36 | 2 | 10 | 27 | 72 | 69 |
| Dominic Thiem | Gilles Simon | Paris | 29-Oct-18 | Indoor Hard | Second Round | 8 | 31 | 0 | 2 | ... | 1 | 13 | 26 | 12 | 25 | 2 | 2 | 23 | 59 | 48 |
| Novak Djokovic | Joao Sousa | Paris | 29-Oct-18 | Indoor Hard | Second Round | 2 | 48 | 0 | 2 | ... | 2 | 25 | 35 | 6 | 22 | 1 | 10 | 27 | 74 | 58 |
| Karen Khachanov | Matthew Ebden | Paris | 29-Oct-18 | Indoor Hard | Second Round | 18 | 39 | 1 | 2 | ... | 6 | 8 | 18 | 5 | 20 | 1 | 2 | 10 | 30 | 23 |
| John Isner | Mikhail Kukushkin | Paris | 29-Oct-18 | Indoor Hard | Second Round | 9 | 54 | 0 | 2 | ... | 1 | 54 | 80 | 24 | 39 | 0 | 1 | 13 | 90 | 91 |
| Kevin Anderson | Nikoloz Basilashvili | Paris | 29-Oct-18 | Indoor Hard | Second Round | 6 | 22 | 0 | 2 | ... | 7 | 43 | 54 | 30 | 49 | 0 | 3 | 26 | 106 | 99 |
| Marin Cilic | Philipp Kohlschreiber | Paris | 29-Oct-18 | Indoor Hard | Second Round | 7 | 43 | 0 | 2 | ... | 1 | 19 | 34 | 12 | 20 | 1 | 1 | 17 | 55 | 48 |
| Jack Sock | Richard Gasquet | Paris | 29-Oct-18 | Indoor Hard | Second Round | 23 | 28 | 0 | 2 | ... | 4 | 18 | 33 | 16 | 29 | 0 | 4 | 19 | 59 | 53 |
| Grigor Dimitrov | Roberto Bautista Agut | Paris | 29-Oct-18 | Indoor Hard | Second Round | 10 | 25 | 0 | 2 | ... | 0 | 34 | 48 | 11 | 20 | 2 | 4 | 27 | 76 | 72 |
| Damir Dzumhur | Stefanos Tsitsipas | Paris | 29-Oct-18 | Indoor Hard | Second Round | 52 | 16 | 0 | 2 | ... | 3 | 14 | 26 | 15 | 30 | 2 | 2 | 17 | 52 | 46 |
| Dominic Thiem | Borna Coric | Paris | 29-Oct-18 | Indoor Hard | Third Round | 8 | 13 | 0 | 2 | ... | 1 | 39 | 57 | 16 | 38 | 2 | 2 | 27 | 88 | 82 |
| Novak Djokovic | Damir Dzumhur | Paris | 29-Oct-18 | Indoor Hard | Third Round | 2 | 52 | 1 | 2 | ... | 4 | 15 | 28 | 7 | 18 | 0 | 0 | 8 | 28 | 30 |
| Alexander Zverev | Diego Schwartzman | Paris | 29-Oct-18 | Indoor Hard | Third Round | 5 | 19 | 0 | 2 | ... | 2 | 22 | 37 | 12 | 24 | 0 | 4 | 18 | 58 | 52 |
| Roger Federer | Fabio Fognini | Paris | 29-Oct-18 | Indoor Hard | Third Round | 3 | 14 | 0 | 2 | ... | 6 | 22 | 32 | 15 | 37 | 1 | 5 | 16 | 54 | 53 |
| Marin Cilic | Grigor Dimitrov | Paris | 29-Oct-18 | Indoor Hard | Third Round | 7 | 10 | 0 | 2 | ... | 1 | 37 | 55 | 14 | 32 | 1 | 5 | 22 | 71 | 73 |
| Karen Khachanov | John Isner | Paris | 29-Oct-18 | Indoor Hard | Third Round | 18 | 9 | 0 | 2 | ... | 4 | 67 | 80 | 19 | 38 | 0 | 0 | 17 | 100 | 103 |
| Kei Nishikori | Kevin Anderson | Paris | 29-Oct-18 | Indoor Hard | Third Round | 11 | 6 | 0 | 2 | ... | 1 | 26 | 33 | 11 | 19 | 0 | 0 | 11 | 51 | 48 |
| Jack Sock | Malek Jaziri | Paris | 29-Oct-18 | Indoor Hard | Third Round | 23 | 55 | 0 | 2 | ... | 6 | 13 | 21 | 10 | 24 | 0 | 0 | 9 | 41 | 32 |
| Karen Khachanov | Alexander Zverev | Paris | 29-Oct-18 | Indoor Hard | Quarter-finals | 18 | 5 | 0 | 2 | ... | 7 | 26 | 47 | 4 | 21 | 1 | 3 | 10 | 36 | 40 |
| Dominic Thiem | Jack Sock | Paris | 29-Oct-18 | Indoor Hard | Quarter-finals | 8 | 23 | 0 | 2 | ... | 5 | 44 | 59 | 19 | 37 | 2 | 10 | 34 | 97 | 97 |
| Roger Federer | Kei Nishikori | Paris | 29-Oct-18 | Indoor Hard | Quarter-finals | 3 | 11 | 0 | 2 | ... | 0 | 21 | 37 | 16 | 26 | 0 | 1 | 12 | 56 | 49 |
| Novak Djokovic | Marin Cilic | Paris | 29-Oct-18 | Indoor Hard | Quarter-finals | 2 | 7 | 0 | 2 | ... | 0 | 38 | 55 | 11 | 28 | 2 | 5 | 29 | 85 | 78 |
| Karen Khachanov | Dominic Thiem | Paris | 29-Oct-18 | Indoor Hard | Semi-finals | 18 | 8 | 0 | 2 | ... | 0 | 19 | 29 | 8 | 26 | 1 | 3 | 15 | 47 | 42 |
| Novak Djokovic | Roger Federer | Paris | 29-Oct-18 | Indoor Hard | Semi-finals | 2 | 3 | 0 | 2 | ... | 2 | 69 | 93 | 25 | 46 | 1 | 2 | 29 | 113 | 123 |
| Karen Khachanov | Novak Djokovic | Paris | 29-Oct-18 | Indoor Hard | Finals | 18 | 2 | 0 | 2 | ... | 1 | 30 | 43 | 14 | 28 | 1 | 5 | 20 | 66 | 64 |
| Jaume Antoni Munar Clar | Frances Tiafoe | Milan | 5-Nov-18 | Indoor Hard | NA | 76 | 40 | 0 | 3 | ... | 3 | 21 | 29 | 6 | 17 | 0 | 2 | 5 | 46 | 32 |
| Frances Tiafoe | Hubert Hurkacz | Milan | 5-Nov-18 | Indoor Hard | NA | 40 | 85 | 0 | 3 | ... | 4 | 35 | 48 | 10 | 19 | 1 | 7 | 22 | 78 | 67 |
| Hubert Hurkacz | Jaume Antoni Munar Clar | Milan | 5-Nov-18 | Indoor Hard | NA | 85 | 76 | 0 | 3 | ... | 1 | 43 | 63 | 15 | 35 | 3 | 9 | 29 | 80 | 87 |
| Andrey Rublev | Liam Caruana | Milan | 5-Nov-18 | Indoor Hard | NA | 68 | NA | 0 | 3 | ... | 1 | 28 | 39 | 4 | 14 | 1 | 3 | 18 | 57 | 50 |

As we can see, we have a `Winner` column, a `Loser` column, as well as other columns detailing the match details, and other columns which have the stats for that match. As we have a `Winner` column, if we use the current data structure to train a model we will leak the result. The model will simply learn that the actual winner comes from the `Winner` column, rather than learning from other features that we can create, such as `First Serve %`.

To avoid this problem, let's reshape the data from wide to long, then shuffle the data. For this, we will define a function, `split_winner_loser_columns`, which splits the raw data frame into two data frames, appends them together, and then shuffles the data.

Let's also remove all Grass and Clay matches from our data, as we will be modelling the Australian Open which is a hardcourt surface.

Additionally, we will add a few columns, such as `Match_Id` and `Total_Games`. These will be useful later.

``` r
split_winner_loser_columns <- function(df) {
  # This function splits the raw data into two data frames and appends them together then shuffles them
  # This output is a data frame with only one player's stats on each row (i.e. in long format)
  
  # Grab a df with only the Winner's stats
  winner = df %>% 
    select(-contains("Loser")) %>% # Select only the Winner columns + extra game info columns as a df
    rename_at( # Rename all columns containing "Winner" to "Player" 
      vars(contains("Winner")),
      ~str_replace(., "Winner", "Player")
    ) %>%
    mutate(Winner = 1) # Create a target column
  
  # Repeat the process with the loser's stats
  loser = df %>%
    select(-contains("Winner")) %>%
    rename_at(
      vars(contains("Loser")),
      ~str_replace(., "Loser", "Player")
    ) %>%
    mutate(Winner = 0)
  
  set.seed(183) # Set seed to replicate results - 183 is the most games played in a tennis match (Isner-Mahut)
  
  # Create a df that appends both the Winner and loser df together
  combined_df = winner %>% 
    rbind(loser) %>% # Append the loser df to the Winner df
    slice(sample(1:n())) %>% # Randomise row order
    arrange(Match_Id) %>% # Arrange by Match_Id
    return()
}
```

``` r
# Read in men and womens data; randomise the data to avoid result leakage
mens = readr::read_csv('data/ATP_matches.csv', na = ".") %>%
  filter(Court_Surface == "Hard" | Court_Surface == "Indoor Hard") %>% # Filter to only use hardcourt games
  mutate(Match_Id = row_number(), # Add a match ID column to be used as a key
         Tournament_Date = dmy(Tournament_Date), # Change Tournament to datetime
         Total_Games = Winner_Games_Won + Loser_Games_Won) %>% # Add a total games played column
  split_winner_loser_columns() # Change the data frame from wide to long
mens %>%
  datatable(rownames = FALSE, extensions = 'Scroller', 
            options = list(dom = "t", 
            scrollY = 450,
            scroller = TRUE,
            scrollX = 600,
            fixedColumns = TRUE)) %>%
  formatRound(columns=pluck(., "x", "data") %>% colnames(), digits=3)
```

| Player | Tournament | Tournament_Date | Court_Surface | Round_Description | Player_Rank | Retirement_Ind | Player_Sets_Won | Player_Games_Won | Player_Aces | ... | Player_SecondServes_Won | Player_SecondServes_In | Player_BreakPoints_Won | Player_BreakPoints | Player_ReturnPoints_Won | Player_ReturnPoints_Faced | Player_TotalPoints_Won | Match_Id | Total_Games | Winner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Eric Prodon | Chennai | 2012-01-02 | Hard | First Round | 97 | 0 | 0 | 7 | 2 | ... | 13 | 26 | 1 | 3 | 15 | 49 | 49 | 1 | 19 | 0 |
| Edouard Roger-Vasselin | Chennai | 2012-01-02 | Hard | First Round | 106 | 0 | 2 | 12 | 5 | ... | 12 | 19 | 4 | 7 | 25 | 59 | 59 | 1 | 19 | 1 |
| Dudi Sela | Chennai | 2012-01-02 | Hard | First Round | 83 | 0 | 2 | 12 | 2 | ... | 11 | 16 | 6 | 14 | 36 | 58 | 61 | 2 | 13 | 1 |
| Fabio Fognini | Chennai | 2012-01-02 | Hard | First Round | 48 | 0 | 0 | 1 | 1 | ... | 5 | 26 | 0 | 1 | 8 | 33 | 30 | 2 | 13 | 0 |
| Frederico Gil | Chennai | 2012-01-02 | Hard | First Round | 102 | 0 | 1 | 14 | 5 | ... | 18 | 35 | 2 | 4 | 36 | 103 | 99 | 3 | 33 | 0 |
| Go Soeda | Chennai | 2012-01-02 | Hard | First Round | 120 | 0 | 2 | 19 | 6 | ... | 19 | 39 | 5 | 11 | 42 | 105 | 109 | 3 | 33 | 1 |

---
## Feature Creation
Now that we have a fairly good understanding of what the data looks like, let's add some features. To do this we will define a function. Ideally we want to add features which will provide predictive power to our model. 

Thinking about the dynamics of tennis, we know that players often will matches by "breaking" the opponent's serve (i.e. winning a game when the opponent is serving). This is especially important in mens tennis. Let's create a feature called `F_Player_BreakPoints_Per_Game`, which is the number of breakpoints a player gets per game that they play (even though they can only get breakpoints every second game, we will use total games). Let's also create a feature called `F_Player_Return_Win_Ratio` which is the proportion of points won when returning.

Similarly, "holding" serve is important (i.e. winning a game when you are serving). Let's create a feature called `F_Player_Serve_Win_Ratio` which is the proportion of points won when serving.

Finally, you only win a set of tennis by winning more sets than your opponent. To win a set, you need to win games. Let's create a feature called `F_Player_Game_Win_Percentage` which is the propotion of games that a player wins.

``` r
add_ratio_features <- function(df) {
  # This function adds ratio features to a long df
  df %>%
    mutate(
      # Point Win ratio when serving
      F_Player_Serve_Win_Ratio = (Player_FirstServes_Won + Player_SecondServes_Won - Player_DoubleFaults) / 
        (Player_FirstServes_In + Player_SecondServes_In + Player_DoubleFaults), 
      # Point win ratio when returning
      F_Player_Return_Win_Ratio = Player_ReturnPoints_Won / Player_ReturnPoints_Faced, 
      # Breakpoints per receiving game
      F_Player_BreakPoints_Per_Game = Player_BreakPoints / Total_Games, 
      F_Player_Game_Win_Percentage = Player_Games_Won / Total_Games
    ) %>%
    mutate_at(
      vars(colnames(.), -contains("Rank"), -Tournament_Date), # Replace all NAs with0 apart from Rank, Date
      ~ifelse(is.na(.), 0, .)
    ) %>%
    return()
}
mens = mens %>%
  add_ratio_features() # Add features
```

Now that we have added our features, we need to create rolling averages for them. We cannot simply use current match statistics, as they will leak the result to the model. Instead, we need to use past match statistics to predict future matches. Here we will use a rolling mean with a window of 15. If the player hasn't played 15 games, we will instead use a cumulative mean. We will also lag the result so as to not leak the result.

This next chunk of code simply takes all the columns starting with F_ and calculates these means.

``` r
mens = mens %>% 
  group_by(Player) %>% # Group by player
  mutate_at( # Create a rolling mean with window 15 for each player. 
    vars(starts_with("F_")), # If the player hasn't played 15 games, use a cumulative mean
    ~coalesce(rollmean(., k = 15, align = "right", fill = NA_real_), cummean(.)) %>% lag()
  ) %>%
  ungroup()
```

---
## Creating a Training Feature Matrix
In predictive modelling language - features are data metrics we use to predict an outcome or target variable. We have several choices to make before we get to the prediction phase. What are the features? How do we structure the outcome variable? What does each row mean? Do we use all data or just a subset? We narrowed it down to two options

We can train the model on every tennis match in the data set, or
We can only train the model on Australian Open matches.
Doing Option 1 would mean we have a lot more data to build a strong model, but it might be challenging to work around the constraints described in the tournament structure.

Doing Option 2 fits better from that angle but leaves us with very few matches to train our model on.
 
We have decided to go with an option that combines strengths from both approaches, by training the model on matches from the Aus Open and the US Open because both grand slams are played on the same surface - hard court.

However, we also need to train our model in the same way that will be used to predict the 2019 Australian Open. When predicting the 2nd round, we won't have data from the 1st round. So we will need to build our training feature matrix with this in mind. We should extract features for a player from past games at the start of the tournament and apply them to every matchup that that player plays.

To do this, we will create a function, `extract_latest_features_for_tournament`, which maps over our feature data frame for the dates in the first round of a tournament and grabs features.

First, we need the Australian Open and US Open results - let's grab these and then apply our function.

``` r
# Get Australian Open and US Open Results
aus_us_open_results = 
  mens %>%
  filter((Tournament == "Australian Open, Melbourne" | Tournament == "U.S. Open, New York")
         & Round_Description != "Qualifying" & Tournament_Date != "2012-01-16") %>% # Filter out qualifiers
  select(Match_Id, Player, Tournament, Tournament_Date, Round_Description, Winner)
# Create a function which extracts features for each tournament
extract_latest_features_for_tournament = function(df, dte) {
  
  df %>% # Filter for the 1st round
    filter(Tournament_Date == dte, Round_Description == "First Round", Tournament_Date != "2012-01-16") %>% 
    group_by(Player) %>% # Group by player
    select_at(
      vars(Match_Id, starts_with("F_"), Player_Rank) # Grab the players' features
    ) %>%
    rename(F_Player_Rank = Player_Rank) %>%
    ungroup() %>%
    mutate(Feature_Date = dte) %>%
    select(Player, Feature_Date, everything())
}
# Create a feature matrix in long format
feature_matrix_long = 
  aus_us_open_results %>%
  distinct(Tournament_Date) %>% # Pull all Tournament Dates
  pull() %>%
  map_dfr(
    ~extract_latest_features_for_tournament(mens, .) # Get the features
  ) %>%
  filter(Feature_Date != "2012-01-16") %>% # Filter out the first Aus Open
  mutate_at( # Replace NAs with the mean
    vars(starts_with("F_")),
    ~ifelse(is.na(.), mean(., na.rm = TRUE), .)
  )
```

Now that we have a feature matrix in long format, we need to convert it to wide format so that the features are on the same row. To do this we will define a function `gather_df`, which converts the data frame from long to wide.
Let's also join the results to the matrix and convert the `Winner` column to a factor. Finally, we will take the difference of player1 and player2's features, so as to reduce the dimensionality of the model.

``` r
gather_df <- function(df) {
  # This function puts the df back into its original format of each row containing stats for both players
  df %>%
    arrange(Match_Id) %>%
    filter(row_number() %% 2 != 0) %>% # Filter for every 2nd row, starting at the 1st index. e.g. 1, 3, 5
    rename_at( # Rename columns to player_1
      vars(contains("Player")),
      ~str_replace(., "Player", "player_1")
    ) %>%
    inner_join(df %>%
                 filter(row_number() %% 2 == 0) %>%
                 rename_at(
                   vars(contains("Player")), # Rename columns to player_2
                   ~str_replace(., "Player", "player_2")
                 ) %>%
                 select(Match_Id, contains("Player")),
               by=c('Match_Id')
    ) %>%
    select(Match_Id, player_1, player_2, Winner, everything()) %>%
    return()
}
# Joining results to features
feature_matrix_wide = aus_us_open_results %>%
  inner_join(feature_matrix_long %>% 
               select(-Match_Id), 
             by = c("Player", "Tournament_Date" = "Feature_Date")) %>%
  gather_df() %>%
  mutate(
    F_Serve_Win_Ratio_Diff = F_player_1_Serve_Win_Ratio - F_player_2_Serve_Win_Ratio,
    F_Return_Win_Ratio_Diff = F_player_1_Return_Win_Ratio - F_player_2_Return_Win_Ratio,
    F_Game_Win_Percentage_Diff = F_player_1_Game_Win_Percentage - F_player_2_Game_Win_Percentage,
    F_BreakPoints_Per_Game_Diff = F_player_1_BreakPoints_Per_Game - F_player_2_BreakPoints_Per_Game,
    F_Rank_Diff = (F_player_1_Rank - F_player_2_Rank),
    Winner = as.factor(Winner)
  ) %>%
  select(Match_Id, player_1, player_2, Tournament, Tournament_Date, Round_Description, Winner, contains("Diff"))
train = feature_matrix_wide
train %>%
  datatable(rownames = FALSE, extensions = 'Scroller', 
            options = list(dom = "t", 
            scrollY = 450,
            scroller = TRUE,
            scrollX = 600,
            fixedColumns = TRUE)) %>%
  formatRound(columns=pluck(., "x", "data") %>% colnames(), digits=3)
```

| Match_Id | player_1 | player_2 | Tournament | Tournament_Date | Round_Description | Winner | F_Serve_Win_Ratio_Diff | F_Return_Win_Ratio_Diff | F_Game_Win_Percentage_Diff | F_BreakPoints_Per_Game_Diff | F_Rank_Diff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1139 | Adrian Ungur | Daniel Brands | U.S. Open, New York | 2012-08-27 | First Round | 0 | 0.03279412 | -0.014757229 | 0.002877458 | 0.073938088 | -13 |
| 1140 | Albert Montanes | Richard Gasquet | U.S. Open, New York | 2012-08-27 | First Round | 0 | -0.08000322 | -0.077451342 | -0.131108056 | -0.180846832 | 97 |
| 1141 | Martin Klizan | Alejandro Falla | U.S. Open, New York | 2012-08-27 | First Round | 1 | 0.07711693 | -0.044715517 | 0.068179841 | -0.087361962 | 1 |
| 1142 | Alex Bogomolov Jr. | Andy Murray | U.S. Open, New York | 2012-08-27 | First Round | 0 | -0.03964074 | -0.031700826 | -0.059010072 | -0.094721700 | 69 |
| 1143 | Tommy Robredo | Andreas Seppi | U.S. Open, New York | 2012-08-27 | First Round | 1 | -0.02681392 | 0.006442134 | -0.067779660 | -0.009930089 | 151 |
| 1144 | Ryan Harrison | Benjamin Becker | U.S. Open, New York | 2012-08-27 | First Round | 1 | 0.04251983 | 0.018604623 | 0.026486753 | -0.003548973 | -24 |

---
## Creating the Feature Matrix for the 2019 Australian Open
Now that we have our training set, `train`, we need to create a feature matrix to create predictions on. To do this, we need to generate features again. We could simply append a player list to our raw data frame, create a mock date and then use the `extract_latest_features_for_tournament` function that we used before. 
Instead, we're going to create a lookup table for each unique player in the 2019 Australian Open. We will need to get their last 15 games and then find the mean for each feature so that our features are the same.

Let's first explore what the dummy submission file looks like, then use it to get the unique players.

``` r
read_csv('data/men_dummy_submission_file.csv') %>% glimpse()
```

As we can see, the dummy submission file contains every potential match up for the Open. This will be updated a few days before the Open starts with the actual players playing. Let's now create the lookup feature table.

``` r
# Get a vector of unique players in this years' open using the dummy submission file
unique_players = read_csv('data/men_dummy_submission_file.csv') %>% pull(player_1) %>% unique()
# Get the last 15 games played for each unique player and find their features
lookup_feature_table = read_csv('data/ATP_matches.csv', na = ".") %>%
  filter(Court_Surface == "Hard" | Court_Surface == "Indoor Hard") %>%
  mutate(Match_Id = row_number(), # Add a match ID column to be used as a key
         Tournament_Date = dmy(Tournament_Date), # Change Tournament to datetime
         Total_Games = Winner_Games_Won + Loser_Games_Won) %>% # Add a total games played column
  # clean_missing_data() %>% # Clean missing data
  split_winner_loser_columns() %>% # Change the data frame from wide to long
  add_ratio_features() %>%
  filter(Player %in% unique_players) %>%
  group_by(Player) %>%
  top_n(15, Match_Id) %>%
  summarise(
    F_Player_Serve_Win_Ratio = mean(F_Player_Serve_Win_Ratio),
    F_Player_Return_Win_Ratio = mean(F_Player_Return_Win_Ratio),
    F_Player_BreakPoints_Per_Game = mean(F_Player_BreakPoints_Per_Game),
    F_Player_Game_Win_Percentage = mean(F_Player_Game_Win_Percentage),
    F_Player_Rank = last(Player_Rank)
  )
```

Now let's create features for every single combination. To do this we'll join our `lookup_feature_table` to the `player_1` and `player_2` columns in the `dummy_submission_file`.

``` r
# Create feature matrix for the Australian Open for all player 1s
features_player_1 = read_csv('data/men_dummy_submission_file.csv') %>%
  select(player_1) %>%
  inner_join(lookup_feature_table, by=c("player_1" = "Player")) %>%
  rename(F_player_1_Serve_Win_Ratio = F_Player_Serve_Win_Ratio,
         F_player_1_Return_Win_Ratio = F_Player_Return_Win_Ratio,
         F_player_1_BreakPoints_Per_Game = F_Player_BreakPoints_Per_Game,
         F_player_1_Game_Win_Percentage = F_Player_Game_Win_Percentage,
         F_player_1_Rank = F_Player_Rank)
# Create feature matrix for the Australian Open for all player 2s
features_player_2 = read_csv('data/men_dummy_submission_file.csv') %>%
  select(player_2) %>%
  inner_join(lookup_feature_table, by=c("player_2" = "Player")) %>%
  rename(F_player_2_Serve_Win_Ratio = F_Player_Serve_Win_Ratio,
         F_player_2_Return_Win_Ratio = F_Player_Return_Win_Ratio,
         F_player_2_BreakPoints_Per_Game = F_Player_BreakPoints_Per_Game,
         F_player_2_Game_Win_Percentage = F_Player_Game_Win_Percentage,
         F_player_2_Rank = F_Player_Rank)
# Join the two dfs together and subtract features to create Difference features
aus_open_2019_features = features_player_1 %>% 
  bind_cols(features_player_2) %>%
  select(player_1, player_2, everything()) %>%
  mutate(
    F_Serve_Win_Ratio_Diff = F_player_1_Serve_Win_Ratio - F_player_2_Serve_Win_Ratio,
    F_Return_Win_Ratio_Diff = F_player_1_Return_Win_Ratio - F_player_2_Return_Win_Ratio,
    F_Game_Win_Percentage_Diff = F_player_1_Game_Win_Percentage - F_player_2_Game_Win_Percentage,
    F_BreakPoints_Per_Game_Diff = F_player_1_BreakPoints_Per_Game - F_player_2_BreakPoints_Per_Game,
    F_Rank_Diff = (F_player_1_Rank - F_player_2_Rank)
  ) %>%
  select(player_1, player_2, contains("Diff"))
aus_open_2019_features  %>%
  datatable(rownames = FALSE, extensions = 'Scroller', 
            options = list(dom = "t",
                          scrollY = 450,
                          scroller = TRUE,
                          scrollX = 600,
                          fixedColumns = TRUE)) %>%
  formatRound(columns=pluck(., "x", "data") %>% colnames(), digits=3)
```

| player_1 | player_2 | F_Serve_Win_Ratio_Diff | F_Return_Win_Ratio_Diff | F_Game_Win_Percentage_Diff | F_BreakPoints_Per_Game_Diff | F_Rank_Diff |
| --- | --- | --- | --- | --- | --- | --- |
| Novak Djokovic | Rafael Nadal | 0.06347805 | 0.02503802 | 0.07002382 | 0.08951024 | 1 |
| Novak Djokovic | Roger Federer | 0.06583364 | 0.03628491 | 0.07661295 | 0.15455628 | -1 |
| Novak Djokovic | Juan Martin del Potro | 0.01067079 | 0.03436023 | 0.06382353 | 0.11259979 | -2 |
| Novak Djokovic | Alexander Zverev | 0.11117863 | 0.03125651 | 0.11055585 | 0.08661036 | -3 |
| Novak Djokovic | Kevin Anderson | 0.02132375 | 0.10449337 | 0.11184503 | 0.23684083 | -4 |
| Novak Djokovic | Marin Cilic | 0.08410746 | 0.02434916 | 0.07653035 | 0.08355134 | -5 |

---
## Generating 2019 Australian Open Predictions
Now that we have our features, we can finally train our model and generate predictions for the 2019 Australian Open. Due to its simplicity, we will use h2o's Auto Machine Learning function `h2o.automl`. This will train a heap of different models and optimise the hyperparameters, as well as creating stacked ensembles automatically for us. We will use optimising by log loss.

First, we must create h2o frames for our training and feature data frames. Then we will run `h2o.automl`. Note that we can set the `max_runtime_secs` parameter. As this is a notebook, I have set it for 30 seconds - but I suggest you give it 10 minutes to create the best model. We can then create our predictions and assign them back to our `aus_open_2019_features` data frame. Finally, we will group_by player and find the best player, on average.

``` r
## Setup H2O
h2o.init(ip = "localhost",
         port = 54321,
         enable_assertions = TRUE,
         nthreads = 2,
         max_mem_size = "24g"
         
)
## Sending file to h2o
train_h2o = feature_matrix_wide %>%
  select(contains("Diff"), Winner) %>%
  as.h2o(destination_frame = "train_h2o")
aus_open_2019_features_h2o = aus_open_2019_features %>%
  select(contains("Diff")) %>%
  as.h2o(destination_frame = "aus_open_2019_features_h2o")
## Running Auto ML 
mens_model = h2o.automl(y = "Winner",
                        training_frame = train_h2o,
                        max_runtime_secs = 30,
                        max_models = 100,
                        stopping_metric = "logloss",
                        sort_metric = "logloss",
                        balance_classes = TRUE,
                        seed = 183) # Set seed to replicate results - 183 is the most games played in a tennis match (Isner-Mahut)
## Predictions on test frame
predictions = h2o.predict(mens_model@leader, aus_open_2019_features_h2o) %>%
  as.data.frame()
aus_open_2019_features$prob_player_1 = predictions$p1
aus_open_2019_features$prob_player_2 = predictions$p0
h2o.shutdown(prompt = FALSE)
```
Now let's find the best player by taking the mean of the prediction probability by player.
``` r
aus_open_2019_features %>% 
  select(player_1, starts_with("F_"), prob_player_1) %>%
  group_by(player_1) %>%
  summarise_all(mean) %>%
  arrange(desc(prob_player_1)) %>%
  datatable(rownames = FALSE, extensions = 'Scroller', 
            options = list(dom = "t",
                          scrollY = 450,
                          scroller = TRUE,
                          scrollX = 600,
                          fixedColumns = TRUE)) %>%
  formatRound(columns=pluck(., "x", "data") %>% colnames(), digits=3)
```

| player_1 | F_Serve_Win_Ratio_Diff | F_Return_Win_Ratio_Diff | F_Game_Win_Percentage_Diff | F_BreakPoints_Per_Game_Diff | F_Rank_Diff | prob_player_1 |
| --- | --- | --- | --- | --- | --- | --- |
| Novak Djokovic | 0.1109364627 | 0.076150615 | 0.1483970690 | 0.17144300 | NA | 0.8616486 |
| Karen Khachanov | 0.0960639298 | 0.061436164 | 0.1059967623 | 0.04544955 | NA | 0.8339594 |
| Juan Martin del Potro | 0.1003931993 | 0.042025222 | 0.0847985439 | 0.05943767 | NA | 0.8218308 |
| Rafael Nadal | 0.0480432305 | 0.051531252 | 0.0790179917 | 0.08181694 | NA | 0.8032543 |
| Gilles Simon | 0.0646937767 | 0.084843307 | 0.0901401318 | 0.08675350 | NA | 0.7985995 |
| Roger Federer | 0.0452014997 | 0.040992497 | 0.0725719954 | 0.01817046 | NA | 0.7962289 |
| Kei Nishikori | 0.0777155934 | 0.018720226 | 0.0800648870 | 0.02740276 | NA | 0.7843631 |
| Marin Cilic | 0.0285413602 | 0.053017465 | 0.0736687072 | 0.08883055 | NA | 0.7804876 |
| Tomas Berdych | 0.0471654691 | 0.047289449 | 0.0737401748 | 0.10584114 | NA | 0.7739211 |
| Daniil Medvedev | 0.0275430665 | 0.031121856 | 0.0721948279 | 0.01803757 | NA | 0.7543269 |
| Stefanos Tsitsipas | 0.0470382377 | 0.023825850 | 0.0577628626 | 0.02105227 | NA | 0.7511674 |
| Dominic Thiem | 0.0258904189 | 0.032481624 | 0.0483707080 | 0.05857158 | NA | 0.7451547 |
| Alexander Zverev | 0.0006199716 | 0.044811275 | 0.0380134371 | 0.08423392 | NA | 0.7374897 |
| Kyle Edmund | 0.0558006240 | 0.011963627 | 0.0478850676 | 0.05142186 | NA | 0.7304873 |
| Pablo Carreno Busta | 0.0321878318 | 0.029862068 | 0.0413674481 | -0.00229784 | NA | 0.7302043 |
| Borna Coric | 0.0762084129 | -0.010097922 | 0.0413621283 | -0.01924267 | NA | 0.7268124 |
| Kevin Anderson | 0.0907358428 | -0.027171681 | 0.0381421997 | -0.06362578 | NA | 0.7260799 |
| David Goffin | -0.0034821911 | 0.037247336 | 0.0162572061 | 0.05603565 | NA | 0.7155908 |
| Fernando Verdasco | 0.0229261365 | 0.032884054 | 0.0521212576 | 0.04668854 | NA | 0.7120831 |
| Roberto Bautista Agut | 0.0047641170 | 0.049939608 | 0.0218975349 | 0.07331023 | NA | 0.7009891 |
| Milos Raonic | 0.0849726089 | -0.028732182 | 0.0385944327 | -0.08009382 | NA | 0.6986865 |
| Fabio Fognini | -0.0394792678 | 0.047935185 | 0.0226546894 | 0.06213496 | NA | 0.6982031 |
| Hyeon Chung | 0.0042489153 | 0.047722133 | 0.0158096386 | 0.04823304 | NA | 0.6958943 |
| Jack Sock | -0.0099659903 | 0.026454984 | 0.0186547428 | 0.02307214 | NA | 0.6757770 |
| Diego Schwartzman | -0.0317130675 | 0.032098381 | 0.0006215006 | 0.05621187 | NA | 0.6631067 |
| John Millman | 0.0016290285 | 0.042676556 | 0.0119857356 | 0.06228135 | NA | 0.6603912 |
| Nikoloz Basilashvili | -0.0099968609 | 0.005561102 | 0.0473876170 | 0.03661962 | NA | 0.6602628 |
| John Isner | 0.1346946527 | -0.070556940 | 0.0161348609 | -0.11425009 | NA | 0.6598097 |
| Gael Monfils | -0.0074254934 | 0.024286746 | 0.0295568649 | 0.04007519 | NA | 0.6449506 |
| Richard Gasquet | 0.0296009556 | -0.011382437 | 0.0013138324 | -0.03972967 | NA | 0.6442043 |
| ... | ... | ... | ... | ... | ... | ... |
| Laslo Djere | -0.042300822 | -0.0150684095 | -0.064667709 | -0.0349151578 | NA | 0.3606923 |
| David Ferrer | -0.036179509 | 0.0532782117 | 0.012751020 | 0.0914824480 | NA | 0.3488057 |
| Bradley Klahn | -0.001248083 | -0.0444982448 | -0.025987040 | -0.1181295700 | NA | 0.3487806 |
| Marcel Granollers | -0.031011830 | -0.0094056152 | -0.049853664 | 0.0136841358 | NA | 0.3460035 |
| Ricardas Berankis | -0.022557215 | -0.0103782963 | -0.047937290 | -0.0468488990 | NA | 0.3454980 |
| Radu Albot | -0.040829057 | 0.0076150564 | -0.034891704 | 0.0443672533 | NA | 0.3420615 |
| Jordan Thompson | -0.068554906 | 0.0261969117 | -0.044349181 | 0.0206636045 | NA | 0.3358572 |
| Thomas Fabbiano | -0.060583307 | 0.0275756029 | -0.025883493 | 0.0709707306 | NA | 0.3319778 |
| Roberto Carballes Baena | -0.054016396 | -0.0091521177 | -0.019093050 | 0.0347187874 | NA | 0.3312105 |
| Paolo Lorenzi | -0.038613500 | -0.0212206827 | -0.052602703 | 0.0199474025 | NA | 0.3299791 |
| Guido Andreozzi | -0.038614385 | -0.0133763922 | 0.029549861 | 0.0636745661 | NA | 0.3288762 |
| Peter Polansky | 0.007461636 | -0.0163389196 | -0.024034159 | -0.0442144260 | NA | 0.3216756 |
| Ernests Gulbis | -0.062827089 | -0.0134699552 | -0.027633425 | -0.0518663252 | NA | 0.3123511 |
| Thiago Monteiro | 0.001235931 | -0.0288349103 | -0.043831840 | -0.0654744344 | NA | 0.3122069 |
| Casper Ruud | 0.016838968 | -0.0178511679 | 0.015234507 | 0.0219131874 | NA | 0.3119321 |
| Marco Trungelliti | -0.022148774 | -0.0005658242 | 0.048542554 | 0.1243537739 | NA | 0.3092636 |
| Jiri Vesely | -0.050204009 | -0.0351868278 | -0.042887646 | -0.0160467165 | NA | 0.3089287 |
| Guillermo Garcia-Lopez | -0.090076100 | -0.0108663630 | -0.048712763 | -0.0124446402 | NA | 0.3080898 |
| Michael Mmoh | -0.063802934 | -0.0079053251 | -0.011112236 | -0.0332042032 | NA | 0.2822330 |
| Jason Kubler | -0.124758873 | -0.0202756806 | -0.013998570 | 0.1020895301 | NA | 0.2814246 |
| Ruben Bemelmans | -0.029036164 | -0.0138846550 | -0.032256254 | -0.0363563402 | NA | 0.2772185 |
| Bjorn Fratangelo | -0.014149222 | 0.0033574304 | -0.019931504 | -0.0360199607 | NA | 0.2652527 |
| Pablo Andujar | -0.042869833 | -0.0488261697 | -0.070057834 | -0.0164918910 | NA | 0.2647100 |
| Christian Garin | -0.046150875 | 0.0235799476 | -0.006209664 | 0.0736304057 | NA | 0.2631607 |
| Ivo Karlovic | 0.071597162 | -0.1093833837 | 0.001410787 | -0.1237762218 | NA | 0.2500242 |
| Juan Ignacio Londero | -0.026454456 | -0.0715665271 | -0.016749898 | -0.0363353678 | NA | 0.2351747 |
| Ramkumar Ramanathan | -0.005371622 | -0.0606138479 | -0.041631884 | -0.0005573405 | NA | 0.2272977 |
| Reilly Opelka | 0.025704824 | -0.0607219257 | -0.015474944 | -0.0720809006 | NA | 0.2262993 |
| Carlos Berlocq | -0.063580460 | 0.0074576369 | -0.054277974 | -0.0165235079 | NA | 0.2112275 |
| Pedro Sousa | -0.197333352 | -0.0734557562 | -0.161962722 | -0.1023311674 | NA | 0.1502313 |

---
### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.