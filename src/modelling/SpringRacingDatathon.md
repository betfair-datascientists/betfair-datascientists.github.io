# **Betfair’s 2023 Spring Racing Data Modelling Competition**

![png](../img/SPRING-RACING-MODELLING-DATATHON.png)

## Registrations

Registrations have now closed

## The Competition

Do you think you have what it takes to model Victorian thoroughbred racing this Spring? Betfair is giving you the chance to show off your data modelling skills with a prize pool of $50,000! 

The 2023 Spring Racing Data Modelling Competition will see Competition Entrants provided with a bespoke set of Punting Form historic thoroughbred data. 

The goal from there is to use the provided data (or any other data) to build your own model, to predict the winning probability of each selection, on nominated race days and meetings (see below) starting on Saturday 28 October 2023 and concluding on Saturday 18 November 2023. 

With $50,000 in prizes up for grabs, we’re challenging you to use your modelling skills to your advantage, be that by building your first predictive racing model, improving on an existing design or have a go at something different by adapting your data skills from other fields. 

**Time to get modelling!**

Progressive updates will be posted here after the conclusion of each race day and in the Betfair Quants Discord Server.

For an invite to the discord server, please fill out the form [here](https://forms.office.com/r/ZG9ea1xQj1 )

Please direct all questions and submissions to [datathon@betfair.com.au](mailto:datathon@betfair.com.au).

### The Specifics

The Terms and Conditions for the 2023 Spring Racing Data Modelling Competition can be viewed [here](../assets/SPDMC_2023_TCs.pdf)

### Prizes

$50,000 in prizes are up for grabs!
See the list below for the prizes each placing at the end of the Competition will receive:

| Place | Prize |
| --- | --- |
| 1 | $25,000.00 |
| 2 | $10,000.00 |
| 3 | $5000.00 |
| 4 | $2000.00 |
| 5 | $2000.00 |

| Other Prize Winners | Prize |
| --- | --- |
| Lowest Weekly Score Week 1 | $1000.00 |
| Lowest Weekly Score Week 2 | $1000.00 |
| Lowest Weekly Score Week 3 | $1000.00 |
| Lowest Weekly Score Week 4 | $1000.00 |
| Best New Modeller | $2000.00 |
| Total Prize Pool | $50,000.00 | 

(for further information see the Terms and Conditions) 

Prize winners will be announced following the final day of racing, and all prizes will be distributed after the conclusion of the final day of racing. 

### Competition Rules

The 2023 Spring Racing Data Modelling Competition will see Competition Entrants provided with a bespoke set of historic form data in partnership with Punting Form 

The goal from there is to use the provided data (or any other data) to **build your own model to predict the probability of a horse winning a given race on the nominated race day.**

**The nominated race days and meetings are:**

 - Saturday October 28th, 2023 – Mooney Valley – ALL races; 
 - Saturday November 4th, 2023 – Flemington – ALL races;
 - Saturday November 11th, 2023 – Flemington – ALL races; and 
 - Saturday November 18th, 2023 – Caulfield – ALL races. 

How you go about building the model is entirely up to you – do you want to build an Elo model, a regression-based model, a Machine Learning algorithm or something entirely different? Get as innovative with it as you want! 

Your set of predictions will be due before 10:59am AEDT on the nominated race day. All submissions must be emailed to [datathon@betfair.com.au](mailto:datathon@betfair.com.au).

See the Terms and Conditions for full Competition rules.

### Submissions & Judging

The Datathon will be judged using the log loss method where the log loss score is calculated using the difference between the predicted probability and the actual outcome. The scoring calculation will involve finding the SUM of the log loss across all runners in each race and then finding the AVERAGE log loss of each race. The entrant with the lowest average log loss across all races over the nominated race days will be victorious.

![png](../img/LogLoss.PNG)

One submission file template will be available to Competition Entrants on www.betfair.com.au/hub/datathon along with the updated data set by 11:59am on the day prior to the nominated race day. Submissions must follow the template set out in the submission file template provided and must be submitted in a csv format. 

For each race, **each Competition Entrant is required to predict the probability of a horse winning the race.** This prediction will then be used against the actual outcome to calculate the model’s score. The sum of the probabilities for every race must equal 1 – being the number accepted winners. 

Please name submission file using the following formatting: 

‘Spring_Racing_Data_Modelling_Competition_2023_Submission_Form_{Model_Name}.csv’; 

To submit your model entry, please send it through to [datathon@betfair.com.au](mailto:datathon@betfair.com.au)

### Code Check

To be eligible for prize money, each Competition Entrant must provide proof that the code used to create their submission is unique and not similar to that of another Competition Entrant. 

The code requirements are:

 - Either 50% of the code or 1000 lines of code (whichever is smaller)
 - Feature engineering aspects may be redacted or altered at the discretion of the entrant
 - Submitted in a .txt file with the first submission of the competition. If not submitted with the first submission, entrants have until close of the submissions on the second nominated race day

## Submission File Template

The submission file template will be loaded here by 11:59am on the day prior to the nominated race day.

 - [example file Caulfield Cup 21/10/2023](../assets/example_submission_file_caulfield_20231021.csv)
 - [Week 1 Submission File 28/10/2023](../assets/Spring_Racing_Data_Modelling_Competition_2023_Submission_Form_Week_1_{Model_Name}.csv)
 - [Week 2 Submission File 04/11/2023](../assets/Spring_Racing_Data_Modelling_Competition_2023_Submission_Form_Week_2_{Model_Name}.csv)
 - [Week 3 Submission File 11/11/2023](../assets/Spring_Racing_Data_Modelling_Competition_2023_Submission_Form_Week_3_{Model_Name}.csv)

## Dataset updates

Dataset updates will be loaded to the dataset page (link included in your registration confirmation email) by 4:59pm AEDT each Friday prior to the nominated race day.

## Results

Leaderboards will be posted here weekly as well as in the Betfair Quants Discord server.

For an invite to the discord server, please fill out the form [here](https://forms.office.com/r/ZG9ea1xQj1 )

|model_name|Score|Rank|
|---------------------------------------|--------|---|
|BSP|2.66096460337926||
|ConcensusSCD2023|2.66951050471409|1|
|willingly|2.67722160568938|2|
|RonW|2.68229975475102|3|
|OnMyHighHorse|2.68280803908963|4|
|ShinyNewThings|2.68816129167671|5|
|Skunkworks|2.68911015592952|6|
|Naomi|2.6904205079147|7|
|melatonin|2.6904267648749|8|
|Doriemus|2.7021051650429|9|
|watptv|2.70263491092202|10|
|BetfairHubPredictionsModel|2.71115917909521||
|KeenAsABean|2.71154493592994|11|
|BelleEpoque|2.72091255406827|12|
|Elle-Macpherson|2.72152431356899|13|
|VinhoVerde|2.72180813102495|14|
|Sportpunter|2.72586732006104|15|
|boshea|2.7273904125382|16|
|nihaoshijie|2.7365928071291|17|
|sebnatann|2.73666475594045|18|
|Cfrance|2.73979945431609|19|
|Gee-Gee-Genius|2.74601807066849|20|
|tomsguesses|2.75694901969074|21|
|HorsesAreJustLargeDogsRight|2.7700174308785|22|
|Definitely-not-overfitted|2.77699459335531|23|
|Looney-mods|2.81043123518048|24|
|ANCR101|2.82807449905763|25|
|Chautauqua|2.83442213118863|26|
|SpicyPredictions|2.83680915707202|27|
|zazzage|2.85590625365442|28|
|exogen|2.86925363179541|29|
|Vertex|2.87337747221819|30|
|matouka|2.88112086422855|31|
|Craigs-List|2.92022818986619|32|
|grunet|2.93971836405406|33|
|reliable-lumberjack|2.96160638254584|34|
|DamienThirst|3.07518291633932|35|
|TheDartMethod|3.07934150782365|36|
|Moose-Ste|3.0844682159332|37|
|236john-KvKid|3.08658995059886|38|
|TopPunter|3.15814397059494|39|
|RandomShrubbery|3.1944403487785|40|
|High-Hat|3.22847155460683|41|
|RockSystems|3.26794471534217|42|
|bruno|3.278506507868|43|
|ReiningIn|3.31598451261996|44|
|Katana|4.10921461918075|45|
|HackerHandicapping|5.32808171654579|46|

