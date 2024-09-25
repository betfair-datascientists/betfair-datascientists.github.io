# Betfair’s 2024 Brownlow Medal Datathon

![png](../img/BROWNLOW_DATATHON_BANNER.png)

### Registration

Registrations have closed

## The Competition

Do you think you have what it takes to predict how many Brownlow votes a player will be awarded in an AFL match?

Betfair is giving you the chance to show off your data modelling skills by building a predictive model for the 2024 Brownlow Medal Count.

With $5,000 in prizes up for grabs, we’re challenging you to use your modelling skills to your advantage, be that by building your first predictive sports model, improving on an existing design or have a go at something different by adapting your data skills from other fields.

This year's AFL Brownlow Medal Datathon, over all rounds in the 2024 Home and Away season, presents the perfect opportunity for keen sports and data enthusiasts to get involved. Put your skills to the test against the masses to compete for both prizes and ultimate glory!

Submissions close at at 2:59pm AEST on the day of the count - Monday September 23rd, 2024.

Leaderboard updates will be published in the Discord Server throughout the count so be sure to check the #datathon channel in the [Discord server](https://forms.office.com/r/ZG9ea1xQj1)

A final leaderboard will be posted here following the completion of the count.

Please direct all questions and submissions to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

## How To Build A Model

Check out our tutorial on modelling the [Brownlow Medal](../modelling/brownlowModelTutorial.ipynb) and this article on [How a Data Scientist models the Brownlow medal](../modelling/modellingTheBrownlowMedal.md) written by Liam from [Crow Data Science](https://www.crowdatascience.com/)

## The Specifics

The Terms and Conditions for the 2024 Brownlow Medal Datathon can be viewed [here](../assets/Brownlow_Medal_Datathon_2024_TCs.pdf)

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


## Submissions & Judging

The Datathon will be judged using the [root-mean-square-error](https://en.wikipedia.org/wiki/Root-mean-square_deviation) (RMSE) method. The winner will be the Competition Entrant with the lowest average RMSE per player over all matches in the 2024 AFL Home and Away Season

One submission file template will be provided to Competition Entrants along with the data set upon registration. Submissions must follow the template set out in the submission file template provided and must be submitted in a csv format, not .numbers or .xlsx.

For each player named in the final squad of 23 for each team in that round, each entrant is required to predict **the total number of Brownlow votes that a player will be awarded.** This prediction will then be used against the player's actual vote count to calculate the model’s RMSE.

With 207 matches and 23 players per side, this is a whopping 9522 predictions!

Please name submission file using the following formatting:

- 	Brownlow_Medal_Datathon_2024_Submission_Form_{Model_Name}.csv;

To submit your model entry, please send it through to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

## Leaderboard - Final

|model|RMSE|Rank|PrizeRank|
|-------------------------|-------|----|---------|
Leisurinho|0.36457|1|1|
Countach|0.36464|2|2|
minotaur|0.36756|3|3|
WisdomOfTheCrowd|0.36809|4||
GoRoys|0.37004|5|4|
Crowbar|0.37062|6|5|
HenryTheGreenEngine|0.37093|7|6|
RandomShrubbery|0.37183|8|7|
PickleRickSanchez|0.37192|9|8|
BenHarvey|0.37206|10||
Optibrebs|0.37412|11|9|
UtaniGranHur|0.37529|12|10|
WheeloRatings|0.37581|13|11|
GoSwans2024|0.37582|14|12|
ThrowingDarts|0.3763|15||
ConspiracyAgainstHeeney|0.37697|16|13|
GoTheBloodsV66|0.37971|17|14|
chicken|0.3804|18|15|
EyeNoBall|0.38079|19|16|
InsufficientIntent|0.38101|20|17|
KickADropPunt|0.38268|21|18|
FeelingDustyRegression|0.38363|22||
FeelingDustyMultiClass|0.38494|23||
GoodGrief|0.38553|24|19|
Pudds|0.38558|25|20|
craigslist|0.38651|26|21|
willingly|0.38753|27|22|
TrackMyBrownlow|0.38871|28|23|
ChatGptDidNotHelp|0.3904|29|24|
TheLoser|0.3915|30|25|
FoxyWeighted|0.39199|31|26|
DrinkCard|0.39311|32|27|
BlakesModel|0.39426|33|28|
SturdyBrownlowPredictor|0.39563|34|29|
MidfieldersMedal|0.40051|35|30|
CoachesVotes|0.402|36||
charlieChooser|0.40963|37|31|
Nightingale|0.41426|38|32|
watpTV|0.4206|39|33|
Wade|0.42968|40|34|
BurntToast|0.43111|41|35|
PEBrownlow|0.44863|42|36|
BlueAndYellow|0.46218|43|37|
blahboy|0.46377|44|38|
cregh|0.51075|45|39|
CorebridgeAnalytics|0.56966|46|40|



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



