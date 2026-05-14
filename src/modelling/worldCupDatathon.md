# Betfair’s 2026 FIFA World Cup Datathon

![FIFA World Cup Datathon Banner](../img/FIFA_DATATHON.png)

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/iHjKeNM5Vd)

Note – only existing customers of Betfair, as at 17 May 2026, can participate in the Competition.

---

## The Competition

Think you’ve got what it takes to model the FIFA World Cup? Now’s your chance to showcase your data modelling skills in **Betfair’s 2026 FIFA World Cup Datathon!**  

With **$5,000 in prizes** on offer, this is your opportunity to create a predictive model that accurately **predicts match results** across the World Cup Tournament. Whether you're a seasoned pro or new to soccer analytics, we encourage you to get creative — adapt your skills from other fields, improve an existing model, or start fresh! 

This year’s Datathon takes place over the entire tournament, featuring **72 Group Stage Matches** and **32 Knockout Stage Matches**. Participants will be challenged to produce **probabilities for each Home/Draw/Away result of the group matches AND the Home/Away 'To Qualify' probability for every possible combination of Knockout Stage match**, with performance measured against real-world outcomes to determine model accuracy and leaderboard rankings.

- **Leaderboard updates** will be posted here throughout the competition, so check back often.  
- Join the conversation in the Quants Discord server (**#datathon** channel), where you can discuss models with fellow participants.  
- Don’t forget to complete the [registration form](https://forms.office.com/r/ZG9ea1xQj1) to join the Discord Server.  

For questions and submissions, contact [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

---

## The Specifics

Review the full Terms and Conditions for the 2026 FIFA World Cup Datathon [here](../assets/FIFA_World_Cup_Datathon_2026_TCs.pdf).

The competition will run from **11 June** 2026 until **19 July** 2026 (**excluding weekends**) and will cover **all** matches in the World Cup competition

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

Your goal is create a model or a set of models to generate the probability:

 - For Home / Draw / Away Full-Time Results for all 72 Group Stage Matches
 - For Home / Away To-Qualify Results for all **possible** Knockout Stage Match-Ups

How you build your model is entirely up to you—whether it's an Elo model, regression, Machine Learning, or something else, the creativity is in your hands.

Submit your predictions by **4:59 AEST on the day before the first match (June 11th 2026)**

See the full Terms and Conditions for more competition rules.

---

### Submission Process

Submissions will be evaluated based on the [Log Loss method](https://en.wikipedia.org/wiki/Cross-entropy#Cross-entropy_loss_function_and_logistic_regression). The entrant with the lowest total log loss for the whole tournament will be declared the winner.

All submissions should be emailed to datathon@betfair.com.au

---
 
### Judging

 - Entrants will be ranked in ascending order on their average log loss per race

---

### Historic Data

The historic dataset will be provided by email with 2 business days of registering for the competition
---

### Submission File

Check Back Later

---
 
## Leaderboard (Final)

Check Back Later
---

## FAQs

### What happens if Italy replaces Iran in the final groups?

- There will be an additional 6 matches included in the submission file for Group G where Italy replaces Iran
- There will be an additional 47 Knockout Stage match-ups where Italy replaces Iran

### Can I resubmit my submission if I notice an error?

- Yes, only the last submitted file before the submission deadline will be considered for marking

### What are the guidelines for the probabilities?

- For each match up the probability of all outcomes must sum to 1
- Each result must have a probability between 0 and 1, excluding 0 and 1
- Any probability of 0 will be adjusted to 0.001, corresponding to a price of $1000
- Any probability of 1 will be adjusted to 0.99, corresponding to a price of $1.01

### What happens for knockout matches that don't occur?

- These matches will not be considered for scoring

### What happens in the event of a match being forfeited?

- These matches will not be considered for scoring

### What happens in the event of extra-time?

- Group matches do not go to extra-time
- Knockout matches require the entrant to make a 'To Qualify' probability, which is the final result after Extra Time and any penalty shootouts

### Is the 3rd-Place Match included?

- Yes

### What if I want to use a Machine Learning model?

- The algorithm choice doesn’t matter from a competition perspective. However, you should use a classification model, not a regression model.

---

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/QnQVkCqtd7)