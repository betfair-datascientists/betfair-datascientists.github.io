# Betfair’s 2025 A-League Datathon

![A-League Datathon Banner](../img/ALEAGUE_DATATHON_BANNER.png)

## Registration

Registrations open 12:00pm AEDT Monday, February 3rd and close 4:59pm AEDT Thursday, February 27th

Register for the competition by completing the [registration form](https://forms.office.com/r/FCq9BbQ2mM)

---

## The Competition

Think you’ve got what it takes to predict model the Australian Soccer A-League competition? Now’s your chance to showcase your data modeling skills in Betfair’s 2025 A-League Datathon!

With **$5,000 in prizes** on offer, this is your opportunity to create a predictive model for the 2024-2025 A-League Season. Whether you're a seasoned pro or new to sports modeling, we encourage you to get creative — adapt your skills from other fields, improve an existing model, or start fresh!

This year’s Datathon features **24 matches** from the 2024-2025 A-League Regular Season with a total of **1104 predictions** required, and we challenge you to test your skills against others for both **prizes** and **ultimate bragging rights**.

- Leaderboard updates will be posted here throughout the competition, so check back often.
- Join the conversation in the Quants Discord server (#datathon channel), where you can discuss models with fellow participants.
- Don't forget to complete the [registration form](https://forms.office.com/r/ZG9ea1xQj1) to join the Discord Server.

For questions and submissions, contact [datathon@betfair.com.au](mailto:datathon@betfair.com.au).

---

## The Specifics

Review the full Terms and Conditions for the 2025 A-League Datathon [here](../assets/ALeague_Datathon_2025_TCs.pdf).

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

Entrants will receive a bespoke set of historical A-League player data for all matches from the 2016-2017 season to the present and a blank submission file.

Your goal is create a model or a set of models to generate Rated Prices for a selection of market types from the Betfair exchange.

 - BOTH_TEAMS_TO_SCORE
 - CORRECT_SCORE
 - DOUBLE_CHANCE
 - DRAW_NO_BET
 - MATCH_ODDS
 - OVER_UNDER_05
 - OVER_UNDER_15
 - OVER_UNDER_25
 - OVER_UNDER_35
 - OVER_UNDER_45
 - TEAM_A_1
 - TEAM_A_WIN_TO_NIL
 - TEAM_B_1
 - TEAM_B_WIN_TO_NIL

How you build your model is entirely up to you—whether it's an Elo model, regression, Machine Learning, or something else, the creativity is in your hands.

Submit your predictions by 60 minutes prior to match kick-off.

See the full Terms and Conditions for more competition rules.

---

### Submission Process

Submissions will be evaluated based on the [Log Loss method](https://en.wikipedia.org/wiki/Cross-entropy#Cross-entropy_loss_function_and_logistic_regression). The entrant with the lowest average log loss per selection will be declared the winner.

All submissions should be emailed to datathon@betfair.com.au

 - [Blank Submission Template](../assets/ALeague_Datathon_Submission_Template.csv)

**Missed submissions after kick-off?**

 - You’ll be assigned the median log-loss of all other entrants for that selection.

---

### Judging

 - Entrants will be ranked in ascending order on their average log loss per selection

---

### Historic Data

The dataset for the competition:

- [Player Dataset 2016-10-07 to 2025-02-03](../assets/A-League-Player-Data.csv)
- [Goalkeeper Dataset 2016-10-07 to 2025-02-03](../assets/A-League-Goalkeeper-Data.csv)
- [Half Time Scores](../assets/A-League-HalfTimeScores.csv)

The data has been collected from [fbref](www.fbref.com). Weekly updates will be posted here throughout the competition.

 - [Player update 13/02/2025](../assets/A-League-Player-Data-Update-20250213.csv)
 - [Goalkeeper update 13/02/2025](../assets/A-League-Goalkeeper-Data-Update-20250213.csv)
 - [Player update 18/02/2025](../assets/A-League-Player-Data-Update-20250218.csv)
 - [Goalkeeper update 18/02/2025](../assets/A-League-Goalkeeper-Data-Update-20250218.csv)

## Leaderboard

Check back later

---

## FAQs

### Can I resubmit my submission if I notice an error?

- Yes, only the last submitted file will be considered for marking

### What are the guidelines for the rated prices?

- For each Market Type/Match combination, the sum of the reciprocals of all related selections must sum to 1
- Each rated price must be greater than $1.00
- No truncation of decimal points is required
- There is no upper limit for the rated price

### What happens if I miss a match?

- You’ll be assigned the median log loss from other entrants for each prediction

### Who is Team A and who is Team B?

- In Betfair markets, the home team will be denoted as Team A and away team will be denoted as Team B

---
