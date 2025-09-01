# Betfair’s 2025 Brownlow Medal Datathon

![Brownlow Datathon Banner](../img/BROWNLOW_MEDAL_DATATHON.png)

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/VbxSUYXjsi)

## The Competition

Think you’ve got what it takes to predict who wins the biggest individual prize in footy? Now’s your chance to showcase your data modeling skills in Betfair’s 2025 Brownlow Medal Datathon!

With **$5,000 in prizes** on offer, this is your opportunity to create a predictive model for the Brownlow Medal count on the Betfair Exchange. Whether you're a seasoned pro or new to player prop modelling, we encourage you to get creative—adapt your skills from other fields, improve an existing model, or start fresh!

This year’s Brownlow Medal Datathon will concern only the count on the night, tentatively scheduled for Monday 22nd September 2025, and we challenge you to test your skills against others for both **prizes** and **ultimate bragging rights**.

- Only a final leaderboard will be posted here, follow along in the Discord server for updates during the count!
- Join the conversation in the Quants Discord server (#datathon channel), where you can discuss models with fellow participants.
- Don't forget to complete the [registration form](https://forms.office.com/r/ZG9ea1xQj1) to join the Discord Server.

For questions and submissions, contact [datathon@betfair.com.au](mailto:datathon@betfair.com.au).

---

## The Specifics

Review the full Terms and Conditions for the 2025 Brownlow Medal Datathon [here](../assets/Greyhound_Datathon_2025_TCs.pdf).

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

The aim of this competition is to predict **how many votes** a player will receive from the umpires in every given match in the 2025 AFL season!
With 23 players per team across 23 rounds, that's a total of **9522 predictions** across the season!

The individual match predictions must meet the following criteria:

 - The individual player predictions must be between 0 and 3 (inclusive)
 - The total predictions across all 46 players in an individual match must equal exactly 6
 - Predictions are not required to be whole numbers, decimals are allowed

Submissions are by due by 2:59pm AEST on the day of count (Monday 22nd September 2025)

---

### Submission Process

The submission template will be provided here no later than 8th September 2025

Entrants should not edit the template in any way except to add the predicted number of votes for each player.

---

### Judging

Submissions will be evaluated based on the [Root Mean Square Error Method ](https://en.wikipedia.org/wiki/Root_mean_square_deviation). 

The score for each model will be the average RMSE for each individual prediction and the model with the lowest score will be deemed the winner

---

### Historic Data

Registrants will be provided with a historic dataset from the fitzRoy R package.

## Leaderboard

Check Back Later

---

## FAQs

### Can I resubmit my submission if I notice an error?

- Yes, only the final entry received before the deadline will be used for scoring

### What are the guidelines for the rated prices?

 - The individual player predictions must be between 0 and 3 (inclusive)
 - The total predictions across all 46 players in an individual match must equal exactly 6
 - Predictions are not required to be whole numbers, decimals are allowed

### What if my values don't sum to 6 across the match?

- Predictions will be adjusted automatically to sum to 6 before scoring

### What if I want to use a Machine Learning model?

- The algorithm choice doesn’t matter from a competition perspective. However, you should use a regression model, not a classification model.

### What happens if I miss a match?

- Each player will be assigned the prediction of 6/46

---

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/VbxSUYXjsi)

---

### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.

