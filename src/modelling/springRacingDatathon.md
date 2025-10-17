# Betfair’s 2025 Spring Racing Datathon

![Spring Racing Datathon Banner](../img/RACING_DATATHON.png)

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/QnQVkCqtd7)

---

## The Competition

Think you’ve got what it takes to model **Thoroughbred Racing** markets? Now’s your chance to showcase your data modeling skills in **Betfair’s 2025 Spring Racing Datathon!**  

With **$5,000 in prizes** on offer, this is your opportunity to create a predictive model that accurately **prices up Place markets** across Victorian Thoroughbred racing. Whether you're a seasoned pro or new to racing analytics, we encourage you to get creative — adapt your skills from other fields, improve an existing model, or start fresh!  

This year’s Datathon takes place over **3 weeks**, featuring a curated selection of **real Thoroughbred races**. Participants will be challenged to produce **probabilities for each runner in the Place market**, with performance measured against real-world outcomes to determine model accuracy and leaderboard rankings.

- **Leaderboard updates** will be posted here throughout the competition, so check back often.  
- Join the conversation in the Quants Discord server (**#datathon** channel), where you can discuss models with fellow participants.  
- Don’t forget to complete the [registration form](https://forms.office.com/r/ZG9ea1xQj1) to join the Discord Server.  

For questions and submissions, contact [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

---

## The Specifics

Review the full Terms and Conditions for the 2025 Spring Racing Datathon [here](../assets/Spring_Racing_Datathon_2025_TCs.pdf).

The competition will run from **10 November** 2025 until **29 November** 2025 (**excluding Sundays**) and will cover **all** Victorian Thoroughbred Racing

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

Entrants will receive a bespoke set of thoroughbred racing data from a variety of sources and **this will be updated daily.**

Your goal is create a model or a set of models to generate a probability for each horse to place. The sum of the probabilities for all horses in each race must equal the number of winners in the **PLACE** market on the Betfair Exchange. If the number of runners at the time of market loading is **less than 8**, then the PLACE market will pay **two winners, otherwise three winners will be paid.** In the event of scratchings that reduce the number of runners to less than 8, the initial number of winners in the PLACE market will remain unchanged.

How you build your model is entirely up to you—whether it's an Elo model, regression, Machine Learning, or something else, the creativity is in your hands.

Submit your predictions by **60 minutes prior to the first race of the day.**

See the full Terms and Conditions for more competition rules.

---

### Submission Process

Submissions will be evaluated based on the [Log Loss method](https://en.wikipedia.org/wiki/Cross-entropy#Cross-entropy_loss_function_and_logistic_regression). The entrant with the lowest average log loss per race will be declared the winner.

All submissions should be emailed to datathon@betfair.com.au

---
 
### Judging

 - Entrants will be ranked in ascending order on their average log loss per race

---

### Historic Data

The dataset for the competition will be provided to participants in the registration email and daily updates will be provided here

---
 
## Leaderboard

**Check Back Later**
---

## FAQs

### Can I resubmit my submission if I notice an error?

- Yes, only the last submitted file before the submission deadline will be considered for marking

### What are the guidelines for the rated prices?

- For each match, the sum of the reciprocals for all horses must sum to the number of winners in the PLACE market (either 2 or 3)
- Each probability must be between 0 and 1, exclusive
- Any probability of 0 will be adjusted to 0.001 (equivalent to maximum Betfair Price of $1000)
- Any probability of 1 will be adjusted to 0.99 (equivalent to minimum Betfair Price of $1.01)
- No truncation of decimal points is required

### What happens for races that are abandoned or postponed?

- These races will not be considered for scoring

### What happens in the event of a scratching?

- That runner will be removed from the race, and all remaining probabilities will be normalised

### What happens in the event of a dead heat?

- If there is a dead heat, such that the number of actual winners exceeds the market number of winners, the binary result will be divided by the number of runners for the final place.
- e.g. If there is a dead heat for 3rd place between 2 runners, the horses placed 1st and 2nd will be assigned 1, the two runners in 3rd will be assigned a result of 0.5 and all other runners will receive 0. This replicates the process used for market settlement on the Betfair Exchange

### What if I want to use a Machine Learning model?

- The algorithm choice doesn’t matter from a competition perspective. However, you should use a classification model, not a regression model.

### What happens if I miss a race?

- The entrant will be assigned the median value of all other participants for the race. You must submit at least 90% of races to remain eligible for a prize.

---

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/QnQVkCqtd7)