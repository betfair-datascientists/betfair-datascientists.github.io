# FIFA 2022 Soccer World Cup Datathon

## The Competition

Do you think you have what it takes to predict the outcome of a soccer match-up?

Betfair is giving you the chance to show off your data modelling skills by building a predictive model for the 2022 FIFA Soccer World Cup!

With over $5,000 in prizes up for grabs, we’re challenging you to use your modelling skills to your advantage, be that by building your first predictive sports model, improving on an existing design or have a go something different by adapting your data skills from other fields.This year’s Soccer World Cup tournament will run from November 20th to December 18th, presenting a perfect opportunity for keen sports and data enthusiasts to get involved and put your skills to the test against the masses in order to compete for both cash prizes and ultimate glory!

Submissions close at 4:59pm AEDT on Friday November 18th - time to get modelling! 

Please register your interest [here](https://docs.google.com/forms/d/1ApCKQ-NkwNx4OeCyc1yBH667YinZTfNSWjOJqgJdVnM). Datasets and submission files will be provided by email once registrations have been received.

Daily leaderboard updates will be published here throughout the tournament so be sure to check back to follow your model’s competition ranking.

Please direct all questions and submissions to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)


See the [Terms and Conditions](/modelling/assets/Betfair_TCs_2022_Datathon.pdf) for full competition rules


## Prizes

Over $5,000 in prize money is up for grabs!
See the list below for the prize money each placing at the end of the competition will receive:

| Place | Prize
---|---
1st | $2500
2nd | $1000
3rd | $500
4th | $250
5th | $250
6th | $100
7th | $100
8th | $100
9th | $100
10th | $100
Total Prize Pool | $5000

Prizewinners will be announced and all prizes will be distributed at the conclusion of the tournament via bank transfer (upon receiving bank account details from eligible prize-winners).

## Competition Rules

The 2022 FIFA Soccer World Cup Datathon will see entrants provided with a bespoke set of historic soccer form data covering major international tournaments dating back to 2000 as well as a selection of relevant international friendly matches.

The goal from there is to use the provided data (or any other data) to build your own model to predict the outcome of every possible match-up in both the group stage (Win-Draw-Loss) and knockout stages (Win-Loss).

How you go about building the model is entirely up to you – do you want to build an Elo model, a regression-based model, a Machine Learning algorithm or something entirely different? Get as innovative with it as you want!

Your set of predictions will be due before the tournament kicks off – all submissions must be emailed to [datathon@betfair.com.au](mailto:datathon@betfair.com.au) before 4:59pm AEDT Friday November 18th 2022.

## Submission & Judging

The Datathon will be judged using the log loss method (cross entropy). The winner will be the Competition Entrant with the lowest mean (average) log loss over all matches that actually take place throughout the tournament (48 in the Group Stage and 16 in the Knockout Stages).

One submission file template will be provided to Competition Entrants along with the data set upon registration – one for the group stage and the knockout stages. Submissions must follow the template set out in the submission file template provided and must be submitted in a csv format.

For the group stage, Competition Entrants will be required to submit probabilities of a win, draw or loss for a given team in each scheduled match.
Additionally, Competition Entrants will be required to submit probabilities of a win or loss (no draws) for a given team in every possible match-up that could occur within the knockout stage of the tournament (i.e. the 496 possible combinations of teams who could play off head-to-head in the knockout stages)

Please name submission file using the following formatting:
•	{model_name}_submission_file.csv; 

To submit your model entry, please send it through to [datathon@betfair.com.au](mailto:datathon@betfair.com.au).

--- 
### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.