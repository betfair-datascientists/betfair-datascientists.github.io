# Betfair’s 2025 Tennis Datathon

![Tennis Datathon Banner](../img/TENNIS_DATATHON_BANNER.png)

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/VbxSUYXjsi)

---

## The Competition

Think you’ve got what it takes to model Tennis matches? Now’s your chance to showcase your data modeling skills in Betfair’s 2025 Tennis Datathon!

With **$5,000 in prizes** on offer, this is your opportunity to create a predictive model for the Men's Singles Tournament in the 2025 Canadian National Bank Open. Whether you're a seasoned pro or new to sports modeling, we encourage you to get creative — adapt your skills from other fields, improve an existing model, or start fresh!

This year’s Datathon features the **127 scheduled matches** from the tournament with a total of **8128 match predictions** required (equal to the number of possible matches), and we challenge you to test your skills against others for both **prizes** and **ultimate bragging rights**.

- Leaderboard updates will be posted here throughout the competition, so check back often.
- Join the conversation in the Quants Discord server (**#datathon** channel), where you can discuss models with fellow participants.
- Don't forget to complete the [registration form](https://forms.office.com/r/ZG9ea1xQj1) to join the Discord Server.

For questions and submissions, contact [datathon@betfair.com.au](mailto:datathon@betfair.com.au).

---

## The Specifics

Review the full Terms and Conditions for the 2025 Tennis Datathon [here](../assets/Tennis_Datathon_2025_TCs.pdf).

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

### Competition Rules

Entrants will receive a bespoke set of historical tennis player data for all ATP matches from 2021 to the present.

Your goal is create a model or a set of models to generate a probability for each player to win the match.

How you build your model is entirely up to you—whether it's an Elo model, regression, Machine Learning, or something else, the creativity is in your hands.

Submit your predictions by 4:59pm AEST on 25 July 2025

See the full Terms and Conditions for more competition rules.

---

### Submission Process

Submissions will be evaluated based on the [Log Loss method](https://en.wikipedia.org/wiki/Cross-entropy#Cross-entropy_loss_function_and_logistic_regression). The entrant with the lowest average log loss per match will be declared the winner.

All submissions should be emailed to datathon@betfair.com.au

---

### Judging

 - Entrants will be ranked in ascending order on their average log loss per selection

---

### Historic Data

The dataset for the competition will be provided to participants in the registration email

## Leaderboard

Check back later for leaderboard updates

---

## FAQs

### Can I resubmit my submission if I notice an error?

- Yes, only the last submitted file before the submission deadline will be considered for marking

### What are the guidelines for the rated prices?

- For each match, the sum of the reciprocals for both players must sum to 1
- Each probability must be between 0 and 1, exclusive
- No truncation of decimal points is required

### What happens for matches that don't happen because one of the players was eliminated?

- These matches will not be considered for scoring

### What happens in the event of a walkover or retirement?

- The match will only be considered for scoring if at least 1 set has been completed

---
