# How to model the Australian Open

Betfair’s Data Scientists Team are putting together a collection of articles on How to Build a Model and submit an entry to the [Betfair Aus Open Datathon](https://www.betfair.com.au/hub/australian-open-datathon/).

This article will outline their thought process and share their approach. Subsequent articles will be posted with code examples that outline how this approach can be put into practice.

---
## Tools for creating our model

We will be providing a step by step tutorial in two languages – Python and R.

These are the two most popular languages used in data science nowadays. Both code examples will follow identical approaches.

---
## Tournament structure

The Datathon structure requires contestants to predict every possible tournament match-up only using data that is available at the start of the tournament.

This means we can’t use information from previous rounds (data from Round 1 matches for potential Round 2 matches and so on). For example, if we were to just train our model on all the tennis matches in the data set, our model would have been trained assuming that it had the result from previous rounds in the Australian Open.

But this isn’t the case, so we need to account for this nuance of the competition. We need to ensure that we don’t include previous round data from the same tournament in the way we structure our features for predicting results.

---
## How to set up data and features

In predictive modelling language – features are data metrics we use to predict an outcome or target variable. We have several choices to make before we get to the prediction phase. What are the features? How do we structure the outcome variable? What does each row mean? Do we use all data or just a subset? We narrowed it down to two options

!!! Note "Training the model"
    - **We can train the model on every tennis match in the data set** or
    - **We can only train the model on Australian Open matches**

    Doing **Option 1** would mean we have a lot more data to build a strong model, but it might be challenging to work around the constraints described in the tournament structure.

    Doing **Option 2** fits better from that angle but leaves us with very few matches to train our model on.

In the end, we decided to go with an option that combines strengths from both approaches, by training the model on matches from the Aus Open and the US Open because both grand slams are played on the same surface – hard court.

Next decision is to decide the features (or the metrics we feed into the model, which makes the decision on who the winner is going to be).

We don’t have a definitive list of features that we will use, but we will most likely keep the number of features quite low (between 4-5).

!!! Note "Features set"
    Likely features may include:

    - **ELO**
    - **First serve %**
    - **Winners-unforced error ratio**

We will also use the difference between opponents' statistics (Difference of Averages), such as the difference between average first serve % in a single column rather than Player 1’s first serve % and Player 2’s first serve % in two separate columns. This will reduce the dimensionality of the model.

A typical row of the transformed data will look like this – For a match between Player A – Roger Federer and Player B – Rafael Nadal, we will have a bunch of features like the difference in first serve %, the difference in ELO rating etc.

---
## Target variable

Our target variable (what we are trying to predict) is whether player A wins or not against player B. In machine learning terms this is a classification problem.

The output will be a probability number between 0 and 1. A number closer to 0 means Player B is likely to win, and a number closer to 1 will mean Player A is likely to win.

Another positive of a probabilistic outcome is that they can easily be converted to odds, and can also be compared with the historical Betfair odds that have been provided, and test if our model would have been profitable for previous seasons.

---
## Sports modelling nuances

Sports data is inherently complex to model. Generally when predicting something, like “will it rain today”, you have information for that day, such as the temperature, which you can use in formulating your prediction.

However with sports data, you cannot use the majority of information that is provided in the raw dataset, such as aces, winners, etc, as this will create what is called feature leakage – using data from after the event, which you won’t have access to before the event, to predict the result.

You will also need to use historic results in such a way that will have predictive power for the sports event that you are trying to predict. This means that you run into little nuances like needing to use rolling averages, as well as whether to model each match on a single row or multiple rows. In the next article in this series, we will show you how we tackle this problem using code examples that anyone can replicate.

!!! Note "Betfair's Aus Open Datathon"
    Make sure you register for our [Australian Open Datathon](https://www.betfair.com.au/hub/australian-open-datathon/) to receive 7 years of match data for tournments all around the world, along with historic Aus Open price data. Submit a model and you'll also be in the running to take home some of the $15k prize pool!