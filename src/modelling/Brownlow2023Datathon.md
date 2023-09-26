# Betfair’s 2023 AFL Brownlow Medal Datathon

## Registrations

Register [here](https://forms.office.com/r/padSktAhB5)

Once you have registered, you will receive the dataset and submission template by email within 2 business days.

Registrations close **4:45PM AEST Friday September 22nd 2023**

## The Competition

Do you think you have what it takes to predict how the umpires will vote on the Brownlow medal?

Betfair is giving you the chance to show off your data modelling skills by building a predictive model for the 2023 Brownlow Medal count!

With $5,000 in prizes up for grabs, we’re challenging you to use your modelling skills to your advantage, be that by building your first predictive sports model, improving on an existing design or have a go at something different by adapting your data skills from other fields.

Submissions close at 2:59pm AEST Monday September 25th 2023!
**Time to get modelling!**

Round by Round updates will be posted in the Quants Discord server with the final results being posted here. 
For an invite to the discord server, please fill out the form [here](https://forms.office.com/r/ZG9ea1xQj1 )

Please direct all questions and submissions to [datathon@betfair.com.au](mailto:datathon@betfair.com.au).

## Previous AFL Modelling Meet-Up
![png](../img/AFL-Meet-Up.png)

Check out our Online Meet-Up with Stats Insider on modelling the AFL [here](https://www.youtube.com/watch?v=8Zq87d1AVyI&list=PLvw8KRdyfOY19ys_5lpSpcbjpy_PBoZEZ&index=21)
## The specifics

The Terms and Conditions for the 2023 Brownlow Medal Datathon Competition can be viewed [here](../assets/Brownlow_2023_TCs.pdf)

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

Prize winners will be announced at the end of the count and prizes will be distributed in the following days

### Final Results

Model|LogLoss|Rank|
|----------------------------------------|---------|---------|-------------|
Vertex|5.59971899693986|1|
Kathys-Lucky-Guesses|5.65064148455871|2|
ForTheTrees|5.78990422858799|3|
belleepoque|5.79400002454156|4|
ChromeBook|5.85635976392115|5|
FootyProphet|5.90339607366938|6|
LifesGood|5.96807894493434|7|
BLT|5.97007252475371|8|
MyLittlePony|6.04155148419435|9|
Bwownwow-modew-UwU|6.0417051646312|10|
RandomShrubbery|6.0833130481194|11|
Cindy|6.20046166558851|12|
Midfielders-Medal|6.22448844896409|13|
NotYourModelV2|6.23632064877733|14|
PabloEscobar|6.23860449303679|15|
Snoopy|6.28912469990177|16|
nzCharlieChooser|6.3362015352423|17|
random-number-generator|6.35297828843829|18|
NickyDwillwin|6.62981370403745|19|
LongRange|6.6834374158962|20|
Sportsmanifold-com|6.77706578552931|21|
BrownHighLow|7.31510324865778|22|
DCL|7.75006150745972|23|
VinhoVerde|7.87199859723157|24|
Corebridge-Analytics|8.52861655118625|25|
WATP|9.70207349246611|26|
DataWading|24.9278696539264|27|
craigs-list|31.4775455046783|28|
boylanc|33.2383077997184|29|
ReverseBanana|44.9988536000238|30|


### Competition Rules

The 2023 Brownlow Medal Datathon will see entrants provided with a bespoke set of historic AFL data from 2012 until the end of Round 24 2023.

The goal from there is to use the provided data (or any other data) to build your own model to **predict the probability of a player receiving at least 1 Brownlow vote** in every match for the 2023 season.

With 207 matches and 23 players per side, this is a whopping 9522 predictions!

How you go about building the model is entirely up to you – do you want to build an Elo model, a regression-based model, a Machine Learning algorithm or something entirely different? Get as innovative with it as you want!

Your set of predictions will be due before the 2:59pm AEST Monday September 25th 2023. All submissions must be emailed to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

See the Terms and Conditions for full competition rules. 

### Submissions & Judging

The Datathon will be judged using the log-loss method where the log-loss score is calculated using the difference between the predicted probability and the actual outcome. The scoring calculation will involve finding the SUM of the log-loss across all 46 players in one single match and then finding the AVERAGE log-loss of each match. The entrant with the lowest log-loss will be victorious.

One submission file template will be provided to Competition Entrants along with the data set upon registration. Submissions must follow the template set out in the submission file template provided and must be submitted in a csv format.

For each Home and Away Match, **each entrant is required to predict the probability of a player receiving at least 1 Brownlow vote.** This prediction will then be used against the actual outcome to calculate the model’s log-loss. The sum of the probabilities for every match must equal 3 – being the number of players in each match that will receive a Brownlow vote.

Please name submission file using the following formatting:

• Brownlow_Datathon_2023_Submission_Form_{Model_Name}.csv;

To submit your model entry, please send it through to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

## Results

Round-by-Round updates will be posted in our Discord server. Final results will be posted here.

## Registrations
 
Register [here](https://forms.office.com/r/padSktAhB5)

Once you have registered, you will receive the dataset and submission template by email within 2 business days.