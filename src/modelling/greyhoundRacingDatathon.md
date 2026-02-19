# Betfair’s 2026 Greyhound Racing Datathon

![Greyhound Racing Datathon Banner](../img/RACING_DATATHON.png)

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/mUmj35mFHb)

Note – only existing customers of Betfair, as at 18 February 2026, can participate in the Competition.

---

## The Competition

Think you’ve got what it takes to model **Greyhound Racing** H2H markets? Now’s your chance to showcase your data modelling skills in **Betfair’s 2026 Greyhound Racing Datathon!**  

With **$5,000 in prizes** on offer, this is your opportunity to create a predictive model that accurately **prices up Head-To-Head markets** across Australian Greyhound racing. Whether you're a seasoned pro or new to racing analytics, we encourage you to get creative — adapt your skills from other fields, improve an existing model, or start fresh!  

This year’s Datathon takes place over **3 weeks**, featuring a curated selection of **real Greyhound races**. Participants will be challenged to produce **probabilities for each runner in every possible head to head combination**, with performance measured against real-world outcomes to determine model accuracy and leaderboard rankings.

- **Leaderboard updates** will be posted here throughout the competition, so check back often.  
- Join the conversation in the Quants Discord server (**#datathon** channel), where you can discuss models with fellow participants.  
- Don’t forget to complete the [registration form](https://forms.office.com/r/ZG9ea1xQj1) to join the Discord Server.  

For questions and submissions, contact [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

---

## The Specifics

Review the full Terms and Conditions for the 2026 Greyhound Racing Datathon [here](../assets/Greyhound_Racing_Datathon_2026_TCs.pdf).

The competition will run from **10 March** 2026 until **25 March** 2026 (**excluding weekends**) and will cover **all** Australian Greyhound Racing (excluding WA) where the first race at the meeting is scheduled to occur after 5:00pm AEDT.

### Prizes

**$5,000 in prizes** are up for grabs! Here's the breakdown of the prize pool:

| Place | Prize     |
|-------|-----------|
| 1     | $2,500.00 |
| 2     | $1,000.00 |
| 3     | $500.00   |
| 4     | $250.00   |
| 5     | $250.00   |
| 6     | $100.00   |
| 7     | $100.00   |
| 8     | $100.00   | 
| 9     | $100.00   | 
| 10    | $100.00   |
| **Total Prize Pool** | **$5,000.00** |

Winners will be announced at the end of the competition, with prizes distributed shortly afterward.

---
 
### Competition Rules

Entrants must have been provided a Topaz API key by the Betfair Australia Automation Team to access the historic dataset.

Your goal is create a model or a set of models to generate the probability that one dog will finish ahead of another dog in the race, repeated for all possible combinations in the race (up to 56 combinations per race). The sum of the probabilities for both dogs in each head-to-head match up must equal 1 and must be between 0 and 1, excluding 0 and 1. If either runner is scratched or if both runners fail to finish the race, then that match up will be excluded from scoring.

How you build your model is entirely up to you—whether it's an Elo model, regression, Machine Learning, or something else, the creativity is in your hands.

Submit your predictions by **4:59 AEDT on the day of the race**

See the full Terms and Conditions for more competition rules.

---

### Submission Process

Submissions will be evaluated based on the [Log Loss method](https://en.wikipedia.org/wiki/Cross-entropy#Cross-entropy_loss_function_and_logistic_regression). The entrant with the lowest average log loss per race will be declared the winner.

All submissions should be emailed to datathon@betfair.com.au

**Code to generate submission file will be provided**

---
 
### Judging

 - Entrants will be ranked in ascending order on their average log loss per race

---

### Historic Data

Participants are required to utilise their Topaz API key to download the historic dataset. A temporary Topaz key may be provided upon request.

---
 
## Leaderboard

Check back later

---

## FAQs

### Can I resubmit my submission if I notice an error?

- Yes, only the last submitted file before the submission deadline will be considered for marking

### What are the guidelines for the probabilities?

- For each match up the probability of both dogs must sum to 1
- Each dog must have a probability between 0 and 1, excluding 0 and 1
- Any probability of 0 will be adjusted to 0.001, corresponding to a price of $1000
- Any probability of 1 will be adjusted to 0.99, corresponding to a price of $1.01

### What happens for races that are abandoned or postponed?

- These races will not be considered for scoring

### What happens in the event of a scratching?

- That runner will be removed from the race, and all combinations relating to that runner will be removed from scoring

### What happens if one or both dogs fail to complete the race?

- If one dog fails to complete the race and other dog completes the race, then the latter will be assigned the winner
- If both dogs fail to complete the race, then the match up will be excluded from scoring

### What happens in the event of a dead heat?

- If there is a dead heat, the result for both runners will be assigned as 0.5 and log loss calculated accordingly

### Why are WA races excluded?

- Due to the later loading times of the WA markets, it is necessary to exclude them to allow the submission templates to be loaded and available by 12pm daily

### What if I want to use a Machine Learning model?

- The algorithm choice doesn’t matter from a competition perspective. However, you should use a classification model, not a regression model.

### What happens if I miss a race?

- The entrant will be assigned the median value of all other participants for the race. You must submit at least 90% of races to remain eligible for a prize.

---

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/QnQVkCqtd7)