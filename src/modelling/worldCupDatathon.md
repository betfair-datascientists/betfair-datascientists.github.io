# Betfair’s 2026 FIFA World Cup Datathon

![FIFA World Cup Datathon Banner](../img/FIFA_DATATHON.png)

## Registration

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/iHjKeNM5Vd)

Note – only existing customers of Betfair, as at 17 May 2026, can participate in the Competition.

**Registrations close at 4:59pm AEST on Monday June 8th 2026.**

---

## The Competition

Think you’ve got what it takes to model the FIFA World Cup? Now’s your chance to showcase your data modelling skills in **Betfair’s 2026 FIFA World Cup Datathon!**  

With **$5,000 in prizes** on offer, this is your opportunity to create a predictive model that accurately **predicts match results** across the World Cup Tournament. Whether you're a seasoned pro or new to soccer analytics, we encourage you to get creative — adapt your skills from other fields, improve an existing model, or start fresh! 

This year’s Datathon takes place over the entire tournament, featuring **72 Group Stage Matches** and **32 Knockout Stage Matches**. 

Participants will be challenged to produce 

 - **probabilities for each Home/Draw/Away result of the group matches**; AND 
 - **the Home/Away 'To Qualify' probability for every possible combination of Knockout Stage match**
 
Performance will be measured against real-world outcomes to determine model accuracy and leaderboard rankings.

- **Leaderboard updates** will be posted here throughout the competition, so check back often.  
- Join the conversation in the Quants Discord server (**#datathon** channel), where you can discuss models with fellow participants.  
- You can join the Discord Server [here](https://forms.office.com/r/ZG9ea1xQj1).  

For questions and submissions, contact [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

---

## The Specifics

Review the full Terms and Conditions for the 2026 FIFA World Cup Datathon [here](../assets/FIFA_World_Cup_Datathon_2026_TCs.pdf).

The competition will run from **12 June** 2026 until **20 July** 2026 and will cover **all** matches in the World Cup competition

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
 - For Home / Away To-Qualify Results for all **possible** Knockout Stage Match-Ups (1128)

How you build your model is entirely up to you—whether it's an Elo model, regression, Machine Learning, or something else, the creativity is in your hands.

Submit your predictions by **4:59 AEST on the day before the first match (June 11th 2026)**

See the full Terms and Conditions for more competition rules.

---

### Submission Process

Submissions will be evaluated based on the [Log Loss method](https://en.wikipedia.org/wiki/Cross-entropy#Cross-entropy_loss_function_and_logistic_regression). The entrant with the lowest total log loss for the whole tournament will be declared the winner.

All submissions should be emailed to datathon@betfair.com.au

---
 
### Judging

 Entrants will be ranked in ascending order on their total log loss across all matches that take place

---

### Historic Data

The historic dataset will be provided by email with 2 business days of registering for the competition

---
 
## Leaderboard

| Model | Log Loss | Rank |
|-----------------------------------------|------|------|
|Cregh|56.564|1|
|LogLobster|56.666|2|
|LMac|56.828|3|
|GoalSniper|58.027|4|
|TerrySpanks|58.042|5|
|Nightingale|58.558|6|
|jnik|58.815|7|
|AirRaider|59.044|8|
|Shiverm3ginger|59.094|9|
|IfISpeakIAmInBigTrouble|59.165|10|
|PopovickingOff|59.348|11|
|blend|59.381|12|
|TeslaKnight3701|59.445|13|
|WorldYup|59.541|14|
|VARgorithm|59.643|15|
|willingly|59.773|16|
|Dandmm|59.785|17|
|SokkahModlol|59.889|18|
|TheLassoWay|60.025|19|
|Amade|60.134|20|
|camow7|60.265|21|
|Jumbalumba|60.44|22|
|footyprophet|60.608|23|
|Garrincha|60.703|24|
|FightAndWin|60.891|25|
|Watptv|61.396|26|
|Garbage1368|61.511|27|
|Ca7618|61.863|28|
|Connor|62.058|29|
|assumethecrown|62.685|30|
|ACoupleOfDimmies|62.804|31|
|Tdot|62.805|32|
|MyWorldCupModel|62.904|33|
|Gisele|63.088|34|
|JacksArmy|63.263|35|
|smarm|63.537|36|
|Swish|63.64|37|
|tomket|63.893|38|
|DrinkCard|63.902|39|
|SnoopBall|64.509|40|
|NetResults|64.883|41|
|ThePuddictor|65.167|42|


---

## FAQs

### What happens if Italy replaces Iran in the final groups?

- There will be an additional 3 matches included in the submission file for Group G where Italy replaces Iran
- There will be an additional 47 Knockout Stage match-ups where Italy replaces Iran

### How is Log Loss calculated?

- Log Loss for each selection is defined as -1 * (R * LN(P) + (1-R) * LN(1-P)) where R is the binary result and P is the submitted probability
- There will be 3 log loss values for each group stage match and 2 for each knockout match for a total of 280 log loss values

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

To enter the Competition, an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/iHjKeNM5Vd)

Registrations close at 4:59pm AEST on Monday June 8th 2026.