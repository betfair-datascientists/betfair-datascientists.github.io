# Betfair’s 2024 Greyhound Racing Datathon

## Registrations

Registrations have closed.

## The Competition

Do you think you have what it takes to predict the outcome of a greyhound race?

Betfair is giving you the chance to show off your data modelling skills by building a predictive model for a set of Victorian greyhound race meetings.

With $5,000 in prizes up for grabs, we’re challenging you to use your modelling skills to your advantage, be that by building your first predictive racing model, improving on an existing design or have a go at something different by adapting your data skills from other fields.

Submissions will be daily for the duration of the competition and will be due 60 minutes before the first race of the day.

**Time to get modelling!**

Progressive updates will be posted here after the conclusion of each race day and in the Betfair Quants Discord Server.

For an invite to the discord server, please fill out the form [here](https://forms.office.com/r/ZG9ea1xQj1 )

Please direct all questions and submissions to [datathon@betfair.com.au](mailto:datathon@betfair.com.au).

## The specifics

The Terms and Conditions for the 2024 Greyhound Racing Datathon can be viewed [here](../assets/Greyhound_2024_TCs.pdf)

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


### Competition Rules

The 2024 Greyhound Racing Datathon will see Competition Entrants provided with a set of historical pricing data pertaining to Victorian Greyhound Racing. Additional data can be found [here](https://betfair-datascientists.github.io/data/dataListing/)

The goal from there is to use the provided data (or any other data) to **build your own model to predict the probability of a dog winning a given race on the nominated race day.**

**The nominated race days and meetings are:**

 - Monday May 13th, 2024 – Traralgon, Warrnambool & Sandown Park – ALL races; and
 - Tuesday May 14th, 2024 – Horsham, Geelong & Warragul – ALL races; and
 - Wednesday May 15th, 2024 – Bendigo, Ballarat & The Meadows – ALL races; and 
 - Thursday May 16th, 2024 – Warragul, Warrnambool & Sandown Park – ALL races; and  
 - Friday May 17th, 2024 – Bendigo, Geelong & Traralgon – ALL races; and
 - Saturday May 18th, 2024 – Warragul & The Meadows – ALL races; and 
 - Sunday May 19th, 2024 – Ballarat & Sale – ALL races. 

How you go about building the model is entirely up to you – do you want to build an Elo model, a regression-based model, a Machine Learning algorithm or something entirely different? Get as innovative with it as you want! 

Your set of predictions will be due 60 minutes prior to the first race on the nominated race day. All submissions must be emailed to [datathon@betfair.com.au](mailto:datathon@betfair.com.au).

See the Terms and Conditions for full Competition rules.

### Submissions & Judging

The Datathon will be judged using the log loss method where the log loss score is calculated using the difference between the predicted probability and the actual outcome. The scoring calculation will involve finding the SUM of the log loss across all runners in each race and then finding the AVERAGE log loss of each race. The entrant with the lowest average log loss across all races over the nominated race days will be victorious.

![png](../img/LogLoss.PNG)

One submission file template will be available to Competition Entrants on this page by 11:59am on the nominated race day. Submissions must follow the template set out in the submission file template provided and must be submitted in a csv format. 

For each race, **each Competition Entrant is required to predict the probability of a dog winning the race.** This prediction will then be used against the actual outcome to calculate the model’s score. The sum of the probabilities for every race must equal 1 – being the number of accepted winners. 

## Submission File Template

The submission file template will be loaded here by 11:59am on the nominated race day.

Please name submission file using the following formatting: 
 - ‘Greyhound_Racing_Datathon_2024_Submission_Form_{Model_Name}.csv’; 

 - Day 1 - [submission file - 13/05/2024](../assets/Greyhound_Racing_Datathon_2024_Submission_Form_{Model_Name}_20240513.csv)
 - Day 2 - [submission file - 14/05/2024](../assets/Greyhound_Racing_Datathon_2024_Submission_Form_{Model_Name}_20240514.csv)
 - Day 3 - [submission file - 15/05/2024](../assets/Greyhound_Racing_Datathon_2024_Submission_Form_{Model_Name}_20240515.csv)
 - Day 4 - [submission file - 16/05/2024](../assets/Greyhound_Racing_Datathon_2024_Submission_Form_{Model_Name}_20240516.csv)
 - Day 5 - [submission file - 17/05/2024](../assets/Greyhound_Racing_Datathon_2024_Submission_Form_{Model_Name}_20240517.csv)
 - Day 6 - [submission file - 18/05/2024](../assets/Greyhound_Racing_Datathon_2024_Submission_Form_{Model_Name}_20240518.csv)
 - Day 7 - [submission file - 19/05/2024](../assets/Greyhound_Racing_Datathon_2024_Submission_Form_{Model_Name}_20240519.csv)

### Historic Form Data

All entrants received a bulk historic data file upon registration

 - [Form Data Update](../assets/Form_dataset_20240411-20240512.csv)
 - [Pricing Data Update](../assets/Pricing_dataset_20240401-20240512.csv)

To submit your model entry, please send it through to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

### Leaderboard - After Day 6

|Model|Log Loss|Rank|PrizeRank|
|-----------------------------|---------|----|----|
|BSP|2.3762|1||
|selling-full-rune-200k|2.3961|2|1|
|Mach7|2.4231|3|2|
|RapidRacer|2.4247|4|3|
|willingly|2.4448|5|4|
|InLimbo|2.4451|6|5|
|TinHare|2.4453|7|6|
|FirstDayFudge|2.4545|8|7|
|YaLikeDags|2.4551|9|8|
|RIPPED|2.4593|10|9|
|Analytique|2.4743|11|10|
|Cortina|2.4807|12|11|
|blahboy|2.4964|13|12|
|NormalChannels|2.5055|14|13|
|WeDontTalkAboutBruno|2.5088|15|14|
|EbbingFlowing|2.5164|16|15|
|WisdomOfTheCrowd|2.5212|17||
|Nightingale|2.5312|18|16|
|RandomShrubbery|2.544|19|17|
|ScrapingTheDulux|2.581|20|18|
|Iggy|2.5881|21||
|PlusEvOnly|2.5961|22|19|
|CanGetThirsty|2.6106|23|20|
|BiggyModel|2.6206|24||
|Greys-V1|2.6257|25|21|
|Vertex|2.6351|26|22|
|Mutt-Maestro|2.6391|27|23|
|GradientGlider|2.7056|28||
|DreamWeaver|2.7138|29||
|LightningBolter|2.7178|30||
|Purrfection|2.7249|31||
|LogisticalLegend|2.7285|32||
|LeafyDecisions|2.737|33||
|XtremeRollers|2.7506|34||
|BelowAverage|2.766|35|24|
|crowbar|2.8126|36|25|
|HarbourBoostinator|2.8174|37||
|FashionModel|2.8955|38|26|
|Flash-Reality|2.9224|39|27|
|Katana|2.9298|40|28|


The following models are ineligible for prize money:

 - BSP (This is the actual Betfair Starting Price)
 - Iggy (This is the Betfair Hub Greyhound Predictions Model)
 - Wisdom of the Crowd (This is the average of all submitted models)
 - All other models with no value in the prize rank column


## FAQs

**Will I receive a confirmation email once I submit my entry?**
No

**If I notice an error with my submission, can I resubmit?**
Yes, only the last entry received before the submission deadline will be considered for scoring

**How is the log loss calculated for a runner assigned a probability of exactly zero or exactly one?**
A placeholder value of 0.000001 or 0.999999 (respectively) will be assigned in place of these values

**What happens if the race is a dead heat?**
The race will be removed from the competition scoring

**What happens if there is a scratching after the submission deadline?**
All probabilities for remaining runners will be renormalised so the field is equal to 1

**What happens if there is a scratching before the submission deadline?**
The runner may be removed from the submission or assigned a null or 0 probability. If a probability is entered, this probability will be removed and remaining probabilities will be renormalised as per the above

## Results

Leaderboards will be posted here daily as well as in the Betfair Quants Discord server.

For an invite to the discord server, please fill out the form [here](https://forms.office.com/r/ZG9ea1xQj1 )

