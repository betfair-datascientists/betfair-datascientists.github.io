# Betfair’s 2024 AFL Player Disposals Datathon

### Registration

Registrations are closed

## The Competition

Do you think you have what it takes to predict how many disposals a player will have in an AFL match?

Betfair is giving you the chance to show off your data modelling skills by building a predictive model for the rounds 17 - 20 of the 2024 AFL Season.

With $5,000 in prizes up for grabs, we’re challenging you to use your modelling skills to your advantage, be that by building your first predictive sports model, improving on an existing design or have a go at something different by adapting your data skills from other fields.

This year's AFL in-season datathon, over all 4 rounds in July, presents the perfect opportunity for keen sports and data enthusiasts to get involved. Put your skills to the test against the masses to compete for both prizes and ultimate glory!

Submissions close at at 5:00pm AEST on Fridays and 12:00pm AEST on Saturday & Sunday on each match day in rounds 17 - 20 (a total of 12 submissions)

Weekly leaderboard updates will be published here throughout the competition so be sure to check back to follow your model’s competition ranking.

Please direct all questions and submissions to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

## The Specifics

The Terms and Conditions for the 2024 AFL Player Disposals Datathon can be viewed [here](../assets/AFL_Disposals_2024_TCs.pdf)

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

The 2024 AFL Player Disposals Datathon will see entrants provided with a bespoke set of historic AFL data for all matches from the AFL 2016 season until the present day which will be updated on a weekly basis during the competition.
The goal from there is to use the provided data (or any other data) to build your own model to predict the disposal count of every player named in the squad of 26 for each team.

How you go about building the model is entirely up to you – do you want to build an Elo model, a regression-based model, a Machine Learning algorithm or something entirely different? Get as innovative with it as you want!

Your set of predictions will be due by 5:00pm AEST on Fridays and 12:00pm AEST on Saturday & Sunday on the day of each nominated match – all submissions must be emailed to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

See the Terms and Conditions for full competition rules.

### Historic Disposals Data

All entrants received a bulk historic data file upon registration. Data updates will be posted here throughout the competition.

- [Round 13 - Round 15 Data Update](../assets/data_update_R13-R15.csv)
- [Round 16 Data Update](../assets/data_update_R16.csv)
- [Round 17 Data Update](../assets/data_update_R17.csv)
- [Round 18 Data Update](../assets/data_update_R18.csv)

## Submission File Template

All submission file templates will be loaded here by 10:00am AEST on the Friday before the commencement of the round.

- [Example Submission File](../assets/exampleSubmissionFile.csv)
- [Week 1 Submission File](../assets/AFL_Disposals_Datathon_2024_Submission_Form_{Model_Name}_Week_1.csv)
- [Week 2 Submission File](../assets/AFL_Disposals_Datathon_2024_Submission_Form_{Model_Name}_Week_2.csv)
- [Week 3 Submission File](../assets/AFL_Disposals_Datathon_2024_Submission_Form_{Model_Name}_Week_3.csv)

### Submissions & Judging

The Datathon will be judged using the [root-mean-square-error](https://en.wikipedia.org/wiki/Root-mean-square_deviation) (RMSE) method. The winner will be the Competition Entrant with the lowest average RMSE per player over all matches that take place between Round 17 and Round 20; 36 in total.

One submission file template will be provided to Competition Entrants along with the data set upon registration. Submissions must follow the template set out in the submission file template provided and must be submitted in a csv format, not .numbers or .xlsx.

For each player named in the squad of 26 for each team in that round, each entrant is required to predict **the total number of disposals of each player in the match.** This prediction will then be used against the player's actual disposal count to calculate the model’s RMSE. Only players who actually take the field will be considered for scoring purposes. This means that players named as emergencies or as substitutes that do not take the field will be excluded from the scoring. 

Please name submission file using the following formatting:

- 	AFL_Disposals_Datathon_2024_Submission_Form_{Model_Name}_202407{day}.csv;

To submit your model entry, please send it through to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

## Leaderboard - Week 3

|modelName|RMSE|Rank|PrizeRank|
|-----------------------------------------|------|--|--|
|Plugger|4.9446|1|1|
|PassThePill|4.9577|2|2|
|crowbar|4.9829|3|3|
|GoTheBloods|5.0413|4|4|
|Gigi|5.0838|5|5|
|willingly|5.1218|6|6|
|Nightingale|5.1626|7|7|
|TheAintz|5.2004|8||
|TheBrew|5.2005|9|8|
|RandomShrubbery|5.225|10|9|
|CaptainsChoice|5.226|11|10|
|BAAALLLL|5.2307|12|11|
|cyggy|5.2469|13|12|
|WormBurner|5.2788|14||
|randint(5,30)|5.3192|15|13|
|blahboy|5.3847|16|14|
|watpTV|5.4543|17|15|
|Pudds|5.6756|18|16|
|DisposalDoctor|5.8211|19|17|


## FAQs

**Will I receive a confirmation email once I submit my entry?**

No

**If I notice an error with my submission, can I resubmit?**

Yes, only the last entry received before the submission deadline will be considered for scoring

**What happens if there is a very late squad change where a player not named in the squad of 26 takes the field?**

The player will be removed from the competition scoring for that match

**What happens if a player is named as substitute OR is injured in the match OR is substituted out of the match after taking the field?**

The prediction for that player will stand

**What happens if a player is named as an emergency or as a substitute and does not take the field at any point?**

The player will be removed from the competition scoring for that match






