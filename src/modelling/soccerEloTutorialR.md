# Using an Elo approach to model soccer in R

## Elo modelling

[Elo modelling](https://en.wikipedia.org/wiki/Elo_rating_system) is a commonly-used approach towards creating rating systems in sport. Originally devised by Arpad Elo for ranking chess players, the popularity of Elo modelling has grown massively since its first official use in the 1960s to the point where it is now widely used to model just about every professional sporting code across the globe.

From a set of Elo ratings we can construct win/loss probabilities for given match-ups between two teams using a simple formula which takes the difference between the two teams' ratings and outputs the probability of each team winning or losing the match. A very basic yet very effective approach!

To read more the inner workings of Elo models, [take a read of this article](https://www.betfair.com.au/hub/tennis-elo-modelling/) for a detailed run-down of how the mathematics behind an Elo rating system works in the context of tennis matches.

---
## Elo Models & Soccer

Elo-based systems lend themselves particularly well to modelling soccer, so much so that publicly available Elo ratings systems ([www.eloratings.net](https://www.eloratings.net) for international soccer for example)  have been adopted by professional bodies to help seed tournaments and create fairer fixtures.

This tutorial aims to serve as guide of how to build a basic soccer Elo model with a particular focus on the 2021 editions of the Euro and Copa America, as they will serve as the subject of [Betfair's Datathon](https://www.betfair.com.au/hub/betfair-euro-copa-america-datathon/).

To follow along with this tutorial you will need two things:

1. This code is written in R, and hence you will need to have [R](https://www.r-project.org) and [RStudio](https://www.rstudio.com) running on your system if you wish to follow along.
2. You will also need the historical data set provided for Betfair's 2021 Euro & Copa America Datathon. For full access to the data set including international soccer fixtures from 2014 to 2021 you can [register for the Datathon here](https://www.betfair.com.au/hub/betfair-euro-copa-america-datathon/), or alternatively if you are reading this tutorial after the Datathon has concluded, please reach out to [datathon@betfair.com.au](mailto:datathon@betfair.com.au) for data access. In the meantime, [click here for a sample of the data](assets/datathon_initial_form_data - SAMPLE.csv) which will be enough to allow the code to run effectively.

!!! note "Betfair Datathon"
    If you're interested in competing in the 2021 Euro & Copa America Datathon competition make sure you [head to the Hub](https://www.betfair.com.au/hub/betfair-euro-copa-america-datathon/), register and download the bespoke data set provided and get your model submitted before 11 June for your chance to win part of the prize pool. 

Let's get started!

---
## Load Packages & Import Data

The first thing to do is load the packages that will be required to run the Elo model and to read in the historic data from wherever it is stored on your machine.

The main package to take notice of here is the `elo` package. As the name suggests, this package is for running Elo models.
The `MLmetrics` package will be used towards the end of the tutorial to back-test the accuracy of our model.

```{r message=FALSE}
library(readr)
library(dplyr)
library(lubridate)
library(elo)
library(MLmetrics)

raw_data <- read_csv("datathon_initial_form_data.csv")
```

When exploring a new data set, it is always good practice to first get an idea of the what is included in the data set.

```{r}
colnames(raw_data)
```

Something noticeable is that the data set does not have a feature included to indicate the result of each match. Let's start by creating two new columns: one showing the result from the home team's perspective and another from the away team's perspective.

We'll also create a feature to show the margin of the match, i.e. the absolute goal difference between the two sides.

```{r}
raw_data <- raw_data %>% 
  mutate(home_result = case_when(home_team_goal_count > away_team_goal_count ~ 1,
                                 home_team_goal_count < away_team_goal_count ~ 0,
                                 home_team_goal_count == away_team_goal_count ~ 0.5),
  away_result = case_when(home_team_goal_count < away_team_goal_count ~ 1,
                          home_team_goal_count > away_team_goal_count ~ 0,
                          home_team_goal_count == away_team_goal_count ~ 0.5),
  margin = abs(home_team_goal_count - away_team_goal_count))
```

Let's also make sure the date_GMT column is formatted correctly as a date. We can do that using the `parse_date_time` function from the `lubridate` package.

``` {r}

raw_data <- raw_data %>% 
  mutate(date_GMT = parse_date_time(raw_data$date_GMT , "mdY_HM"))

```

---
## Running the Elo Model

Now comes the fun part - setting the Elo model in action!

There are a number of steps we could have taken before getting to this point to make the model a touch more complex (and possibly more accurate as a result), however in the interest of keeping this tutorial as accessible and easy to follow as possible let's jump straight into running an Elo model based on our data set.

To run the Elo model we will need to use the `elo.run` function from the `elo` package. The `elo.run` function requires we input a formula as an argument which tells the function which columns list the two teams, which column is our target/outcome variable, as well as any other features we want to include in our model.

We can use the `home_result` column we've created to identify the result from the home team's perspective.

We can also input a k value which essentially dictates the maximum number of Elo points that can be won or lost in a single match.

Here we could set k to be a constant (such as 30), however to add an extra layer of (very slight) complexity, we can instead choose to use a variable k value which is dictated by the margin of the match using a formula of `k = 30 + 30*margin`. This means that for every goal the margin increases by, the k value will increase by 30, starting with a base k value of 30 for draws (`margin equals 0`). The idea here is simply to help account for and reward/punish teams winning/losing by bigger margins compared to closer matches.

```{r}
elo_model <- elo.run(data = raw_data,
                     formula = home_result ~ home_team_name + away_team_name + k(30 + 30*margin))
```

Let's take a look at the last few matches in our training sample to get a better view of the Elo model in action.

``` {r}
elo_results <- elo_model %>%
  as.data.frame()

elo_results %>% tail(n = 10)
```

We can also now check out what the latest Elo rankings for each team in the data set! Let's look at the top 20.

Keep in mind that teams start with an Elo rating of 1500, so any team with an Elo greater 1500 can be considered above average, while those with Elo ratings below 1500 are therefore below average.

``` {r}

final_elos <- final.elos(elo_model)
final_elos %>% sort(decreasing = TRUE) %>% head(n = 20)

```

---
## Accounting for Draws

Something that we need to acknowledge both generally and also in relation to the Euro & Copa America Datathon is that Elo models are best suited to sporting contexts with binary outcomes - i.e. win or lose - however in most soccer fixture we also have the possibility of a draw to account for. We are still able to ensure that Elo ratings update appropriately after a draw using 0.5 wins to denote the situation in which a draw occurs, but when it comes to making probabilistic win predictions using the Elo ratings (see p.A column above for example) things get a little more confusing.

For the Euro & Copa America Datathon, we also need to consider the fact that draws are a possibility during group stage match-ups, therefore we need to develop a workaround option to include draw probabilities.

One way to do this - and the method that will be adopted for this tutorial - is to find the historic rate at which two teams of a certain Elo prediction split ending up drawing their matches. For example, how often do matches in which an Elo model deems Team A an 80% chance of winning and Team B a 20% chance of winning result in a draw? How about a 70%-30% split? We can find these draw rates for a range of probability points between 0 and 1 and use them to redistribute win/loss probabilities accordingly.

Let's start the process by finding historic draw rates. We will bucket matches at 5% increments according to the home team's probability of winning the match according to the model.

``` {r}

draw_rates <- data.frame(win_prob = elo_model$elos[,3],
                        win_loss_draw = elo_model$elos[,4]) %>%
  mutate(prob_bucket = abs(round((win_prob)*20)) / 20) %>%   # Round the predicted win probabilities to the nearest 0.05
  group_by(prob_bucket) %>%
  summarise(draw_prob = sum(ifelse(win_loss_draw == 0.5, 1, 0)) / n())   # Calculate the rate their was a draw for this win prob - elo package codes a draw as a 0.5

draw_rates %>% head(n=20)

```

We now have data which will help us deem how likely a match-up between two teams is to end up in a draw!

The next step is to merge this data in with our existing data set. We also need to include the win/loss probabilities for each match that we've already found using our Elo model so that we may tweak them to include for the possibility of a draw. We'll also pull in the actual Elo ratings for each team for completeness.

``` {r}

data_with_probabilities <- raw_data %>% 
  select(tournament, date_GMT, home_team_name, away_team_name, home_result, away_result) %>%   # Remove some redundant columns
  mutate(home_elo = elo_results$elo.A - elo_results$update.A,    # Add in home team's elo rating (need to subtract the points update to obtain pre-match rating)
         away_elo = elo_results$elo.B - elo_results$update.B,    # Add in away team's elo rating (need to subtract the points update to obtain pre-match rating)
         home_prob = elo_results$p.A,                            # Add in home team's win/loss probability
         away_prob = 1 - home_prob) %>%                          # Add in away team's win/loss probability
  mutate(prob_bucket = round(20*home_prob)/20) %>%               # Bucket the home team's win/loss probability into a rounded increment of 0.05
  left_join(draw_rates, by = "prob_bucket") %>%                  # Join in our historic draw rates using the probability buckets
    relocate(draw_prob, .after = home_prob) %>% 
  select(-prob_bucket)

```

Having now brought the draw probability for each match into the data frame, we need to redistribute the win and loss probabilities so that `Pr(win) + Pr(draw) + Pr(loss)` sums to exactly 1. We can do this by simply subtracting the draw probability from each of the win and loss probabilities in a proportional manner. See below:

```{r}

data_with_probabilities <- data_with_probabilities %>% 
  mutate(home_prob = home_prob - home_prob * draw_prob,          # Redistribute home team's probabilities proportionally to create win/draw/loss probabilities
         away_prob = away_prob - away_prob * draw_prob)          # Redistribute away team's probabilities proportionally to create win/draw/loss probabilities

data_with_probabilities %>% 
  select(home_team_name, away_team_name, home_prob, draw_prob, away_prob) %>% 
  tail(n=10)

```

And there you have it! We've now come up with win, draw and loss probabilities for each match-up in our data set!

Keep in mind that if we were to be focusing on knockout matches (i.e. where no draws are possible), we could have just skipped the previous few steps as we already had binary win-loss probabilities as direct outputs from our Elo model.

---
## Back Testing

The last step in our modelling process is to back test against a subset of our data to get an idea of our model's accuracy.

We can use the `MLmetrics` package to run a [log loss](https://towardsdatascience.com/understanding-binary-cross-entropy-log-loss-a-visual-explanation-a3ac6025181a) function on our subset. 

Let's look at how the model performed when we limit the data set to include only the most recent matches from early 2021.

``` {r}

matches_2021 <- data_with_probabilities %>% 
  filter(year(date_GMT) == 2021) %>%                      # Filter down to only 2021 matches
  mutate(home_win = ifelse(home_result == 1, 1, 0),       # Include new columns which show the true outcome of the match
         draw = ifelse(home_result == 0.5, 1, 0),
         away_win = ifelse(away_result == 1, 1, 0)) %>% 
  select(date_GMT, home_team_name, away_team_name, home_prob, draw_prob, away_prob, home_win, draw, away_win)


# Run the multinomial log loss function from MLmetrics to output a log loss score for our sample
MultiLogLoss(
  y_pred = matches_2021[,c("home_prob", "draw_prob", "away_prob")] %>% as.matrix(),
  y_true = matches_2021[,c("home_win", "draw", "away_win")] %>% as.matrix()
)

```

A pretty good result for such a simple Elo model!

---
## Making Future Predictions

Okay, so now our Elo model is set in place, we have the latest set of Elo ratings for each team and we've back tested our model. We can now apply our model to future matches to obtain probabilities for match-ups that are yet to occur.

Again we can do this using the `elo` package. This time we will use the function `elo.prob`, which takes two teams and outputs the probability of the first team winning the match-up. Like before, this function only considers win/loss outcomes to be possible, so if we were to also be looking to generate draw probabilities for a future match-up, we can just go through the exact same process as we did previously (i.e. make a binary win/loss prediction, merge in historic draw rates for various probabilities, redistribute accordingly).

Let's just keep this simple for now though and focus on win and loss probabilities. We'll put together a small dataframe of matches and see what our model thinks - we've gone for hypothetical match-ups of Brazil v Argentina, England v France, Spain v Germany and an obligatory 2006 World Cup rematch of Australia v Italy.

``` {r}

future_matches <- data.frame(
  team_a = c("Brazil", "England", "Spain", "Australia"),
  team_b = c("Argentina", "France", "Germany", "Italy"))  %>% 
  mutate(elo_a = final_elos[team_a],
         elo_b = final_elos[team_b],
         team_a_win_prob = elo.prob(elo.A = elo_a,
                                    elo.B = elo_b)
  )

future_matches

```

---
## Conclusions & Areas for Improvement

Elo modelling can be a surprisingly accurate modelling technique given how simple it is to implement. This tutorial gives a very basic framework from which you are free to build a more intricate model with more detailed inputs and features.

Some things that you might want to consider adding to this Elo model:

- Home ground advantage
- Key match statistics (i.e. shots on target, possession %, etc.)
- Whether the match was a dead rubber (teams may take the foot off the gas if they don't need to win to advance to the next stage of a tournament)
- Selected team line-ups (were key players missing?)

Remember, an Elo model can be as complex or as simple as you want it to be - in some cases it might be better to keep it basic!

We hope you've found this tutorial useful - if you have any questions regarding predictive data modelling please reach out to [automation@betfair.com.au](mailto:automation@betfair.com.au).

Good luck in the [Datathon](https://www.betfair.com.au/hub/betfair-euro-copa-america-datathon/)!

---
### Disclaimer 

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.