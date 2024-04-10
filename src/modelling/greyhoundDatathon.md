# Betfair’s 2024 Greyhound Racing Datathon

## Registrations

Register [here](https://forms.office.com/r/23gT5gNvXL)

Once you have registered, you will receive the dataset and submission template by email within 2 business days.

Registrations close **4:59PM AEST Monday May 6th 2024**

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

One submission file template will be available to Competition Entrants on www.betfair.com.au/hub/datathon by 11:59am on the nominated race day. Submissions must follow the template set out in the submission file template provided and must be submitted in a csv format. 

For each race, **each Competition Entrant is required to predict the probability of a dog winning the race.** This prediction will then be used against the actual outcome to calculate the model’s score. The sum of the probabilities for every race must equal 1 – being the number of accepted winners. 

## Submission File Template

The submission file template will be loaded here by 11:59am on the nominated race day.

 - [example file  10/04/2024](../assets/examples_submission_file_20240410.csv)

Please name submission file using the following formatting: 

‘Greyhound_Racing_Dathon_2024_Submission_Form_{Model_Name}.csv’; 

To submit your model entry, please send it through to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

## Results

Leaderboards will be posted here daily as well as in the Betfair Quants Discord server.

For an invite to the discord server, please fill out the form [here](https://forms.office.com/r/ZG9ea1xQj1 )

## Registrations
 
Register [here](https://forms.office.com/r/23gT5gNvXL)

Once you have registered, you will receive the dataset and submission template by email within 2 business days.