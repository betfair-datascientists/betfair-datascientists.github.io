# Betfair’s 2023 AFL Datathon

## The Competition

Do you think you have what it takes to predict the scores in AFL matches?

Betfair is giving you the chance to show off your data modelling skills by building a predictive model for the final rounds of the 2023 AFL Home and Away Season!

With over $5,000 in prizes up for grabs, we’re challenging you to use your modelling skills to your advantage, be that by building your first predictive sports model, improving on an existing design or have a go at something different by adapting your data skills from other fields.

This year’s AFL Season will run until August 27th, presenting a perfect opportunity for keen sports and data enthusiasts to get involved and put your skills to the test against the masses in order to compete for both prizes and ultimate glory!

Submissions close at 4:59pm AEST on Thursday July 7 2023 - time to get modelling!

Weekly leaderboard updates will be published here throughout the competition so be sure to check back to follow your model’s competition ranking.

Please direct all questions and submissions to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

## Previous AFL Modelling Meet-Up
![png](../img/AFL-Meet-Up.png)

Check out our Online Meet-Up with Stats Insider on modelling the AFL [here](https://www.youtube.com/watch?v=8Zq87d1AVyI&list=PLvw8KRdyfOY19ys_5lpSpcbjpy_PBoZEZ&index=21)

## The Specifics

The Terms and Conditions for the 2023 AFL Datathon Competition can be viewed [here](../assets/Betfairs_TCs_2023_Datathon.pdf)

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

Prize winners will be announced, and all prizes will be distributed at the conclusion of the tournament

### Competition Rules 

The 2023 AFL Datathon will see entrants provided with a bespoke set of historic AFL data from the 2022 AFL Season and the first 14 rounds of the 2023 AFL Season
The goal from there is to use the provided data (or any other data) to build your own model to predict the score of every team in each of the remaining 72 matches in rounds 17-24.

How you go about building the model is entirely up to you – do you want to build an Elo model, a regression-based model, a Machine Learning algorithm or something entirely different? Get as innovative with it as you want!

Your set of predictions will be due before the first match of round 17 – all submissions must be emailed to datathon@betfair.com.au before 4:59pm AEST Thursday July 7th 2023.
See the Terms and Conditions for full competition rules.

### Submissions & Judging

The Datathon will be judged using the root-mean-square-error (RMSE) method. The winner will be the Competition Entrant with the lowest RMSE over all matches that take place between Round 17 and Round 24; 72 in total.

One submission file template will be provided to Competition Entrants along with the data set upon registration. Submissions must follow the template set out in the submission file template provided and must be submitted in a csv format.

For each Home and Away Match, each entrant is required to predict **the total match score of each team in the match.** This prediction will then be used against the actual score to calculate the model’s RMSE.

Please name submission file using the following formatting:

- 	AFL_Datathon_2023_Submission_Form_{Model_Name}.csv; 

To submit your model entry, please send it through to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

### Registration

Register [here](https://forms.gle/WnABDhEz9gHeBRbS6) to receive your submission form and AFL dataset. Additional data can be sourced by utilising the [fitzRoy R package](https://github.com/jimmyday12/fitzRoy)