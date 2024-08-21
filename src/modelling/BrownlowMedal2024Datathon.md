# Betfair’s 2024 Brownlow Medal Datathon

### Registration

Registrations open at 12:00pm AEST on 26 August 2024, registrations close at 4:59pm AEST on 20 September 2024.

To enter the Competition (Competition Entrant), an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/EKGM2RV6kR)

## The Competition

Do you think you have what it takes to predict how many Brownlow votes a player will be awarded in an AFL match?

Betfair is giving you the chance to show off your data modelling skills by building a predictive model for the 2024 Brownlow Medal Count.

With $5,000 in prizes up for grabs, we’re challenging you to use your modelling skills to your advantage, be that by building your first predictive sports model, improving on an existing design or have a go at something different by adapting your data skills from other fields.

This year's AFL Brownlow Medal Datathon, over all rounds in the 2024 Home and Away season, presents the perfect opportunity for keen sports and data enthusiasts to get involved. Put your skills to the test against the masses to compete for both prizes and ultimate glory!

Submissions close at at 2:59pm AEST on the day of the count - Monday September 23rd, 2024.

Leaderboard updates will be published in the Discord Server throughout the count so be sure to check the #datathon channel in the Discord server. [Join The Discord Conversation](https://forms.office.com/r/ZG9ea1xQj1)

A final leaderboard will be posted here following the completion of the count.

Please direct all questions and submissions to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

## The Specifics

The Terms and Conditions for the 2024 Brownlow Medal Datathon can be viewed [here](../assets/Brownlow_Medal_2024_TCs.pdf)

### Prizes
$5,000 in prizes are up for grabs!
See the list below for the prizes each placing at the end of the competition will receive:

| Place | Prize |
| --- | --- |
| 1 | $2,500.00 |
| 2 | $1,000.00 |
| 3 | $500.00 |
| 4 | $250.00 |
| 5 | $250.00 |
| 6 | $100.00 |
| 7 | $100.00 |
| 8 | $100.00 | 
| 9 | $100.00 | 
| 10 | $100.00 |
| Total Prize Pool | $5,000.00 | 

Prize winners will be announced, and all prizes will be distributed at the conclusion of the medal count.

### Competition Rules 

The 2024 Brownlow Medal Datathon will see entrants provided with a bespoke set of historic AFL data for all matches from the AFL 2015 season until the present day which includes the Brownlow medal votes for all games up until Round 24, 2023.
The goal from there is to use the provided data (or any other data) to build your own model to predict the number of votes every player named in the final squad of 23 for each team will receive.

How you go about building the model is entirely up to you – do you want to build an Elo model, a regression-based model, a Machine Learning algorithm or something entirely different? Get as innovative with it as you want!

Your set of predictions will be due by 2:59pm AEST on Monday September 23rd, 2024 – all submissions must be emailed to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

See the Terms and Conditions for full competition rules.

## Submission File Template

The submission file templates will be emailed to each person upon registration and will also be posted here.

## Submissions & Judging

The Datathon will be judged using the [root-mean-square-error](https://en.wikipedia.org/wiki/Root-mean-square_deviation) (RMSE) method. The winner will be the Competition Entrant with the lowest average RMSE per player over all matches in the 2024 AFL Home and Away Season

One submission file template will be provided to Competition Entrants along with the data set upon registration. Submissions must follow the template set out in the submission file template provided and must be submitted in a csv format, not .numbers or .xlsx.

For each player named in the final squad of 23 for each team in that round, each entrant is required to predict **the total number of Brownlow votes that a player will be awarded.** This prediction will then be used against the player's actual vote count to calculate the model’s RMSE.

With 207 matches and 23 players per side, this is a whopping 9522 predictions!

Please name submission file using the following formatting:

- 	Brownlow_Medal_Datathon_2024_Submission_Form_{Model_Name}.csv;

To submit your model entry, please send it through to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

## Leaderboard - Final

Check back later

## FAQs

**Will I receive a confirmation email once I submit my entry?**

No

**If I notice an error with my submission, can I resubmit?**

Yes, only the last entry received before the submission deadline will be considered for scoring

**What are the guidelines for my predictions?**

 - Each player must have a prediction input between 0 and 3 (inclusive).
 - Any players with a blank prediction will be assigned 0.
 - Predictions are not required to be an integer, decimal predictions are acceptable (and tend to perform better in challenges like this)
 - The sum of all predictions for each match must equal 6, as this is the number of votes awarded per match. 

**What happens if a player is suspended and deemed ineligible for the award?**

A prediction must still be submitted

**If I wanted to use a Machine-Learning Model, what algorithm should I use?**

The actual algorithm used from a rules perspective does not matter. However, any model used should be a regression model, not a classification model.

**What happens if my predictions do not sum to 6 for a match?**

Your predictions will be normalised so that the predictions for the match sum to 6.

### Registration

Registrations open at 12:00pm AEST on 26 August 2024, registrations close at 4:59pm AEST on 20 September 2024.

To enter the Competition (Competition Entrant), an Eligible Participant must register their details by filling out the [registration form](https://forms.office.com/r/EKGM2RV6kR)




