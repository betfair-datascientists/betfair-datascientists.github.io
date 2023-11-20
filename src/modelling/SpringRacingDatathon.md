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
 - [Week 4 Submission File 18/11/2023](../assets/Spring_Racing_Data_Modelling_Competition_2023_Submission_Form_Week_4_{Model_Name}.csv)

## Dataset updates

Dataset updates will be loaded to the dataset page (link included in your registration confirmation email) by 4:59pm AEDT each Friday prior to the nominated race day.

## Final Results

Leaderboards will be posted here weekly as well as in the Betfair Quants Discord server.

For an invite to the discord server, please fill out the form [here](https://forms.office.com/r/ZG9ea1xQj1 )

|model_name|Score|Rank|
|---------------------------------------|--------|---|
|BSP|2.77788996997805||
|OnMyHighHorse|2.7906939396213|1|
|willingly|2.79479411408101|2|
|ShinyNewThings|2.7997219805638|3|
|melatonin|2.82023873698256|4|
|Sportpunter|2.82209518025333|5|
|BetfairHubPredictionsModel|2.82722068224616||
|ConcensusSCD2023|2.82801203747167|6|
|nihaoshijie|2.82882380798673|7|
|Elle-Macpherson|2.82949035955336|8|
|watptv|2.83220716456428|9|
|Doriemus|2.83280544288701|10|
|sebnatann|2.84644233918721|11|
|VinhoVerde|2.85267147439722|12|
|Cfrance|2.85483856884689|13|
|tomsguesses|2.85871078349823|14|
|RonW|2.86289564706468|15|
|Gee-Gee-Genius|2.86323498280765|16|
|BelleEpoque|2.87046918602378|17|
|HorsesAreJustLargeDogsRight|2.88255972209085|18|
|ANCR101|2.908669415987|19|
|Naomi|2.92736405744928|20|
|Vertex|2.94735261875303|21|
|Craigs-List|2.97002109980415|22|
|exogen|2.99524266470316|23|
|SpicyPredictions|2.99738014682078|24|
|Chautauqua|3.02877922721002|25|
|matouka|3.04024295542127|26|
|reliable-lumberjack|3.04760653609704|27|
|DamienThirst|3.11828100020267|28|
|236john-KvKid|3.14292359860204|29|
|High-Hat|3.15224272966616|30|
|RandomShrubbery|3.17516493828797|31|
|Moose-Ste|3.21855177030658|32|
|KeenAsABean|3.24194972021672|33|
|TopPunter|3.24471673034183|34|
|TheDartMethod|3.26158155505263|35|
|bruno|3.26421531746475|36|
|ReiningIn|3.3335306628469|37|
|Skunkworks|3.46770257357916|38|
|RockSystems|3.58239827522267|39|
|Hoover|3.73795524949571|40|
|Definitely-not-overfitted|3.87507506226626|41|
|Katana|4.49222287728695|42|
|HackerHandicapping|7.11891434429891|43|

### Contestants who did not submit every week 

|model_name|Score|
|---------------------------------------|--------|
|FastandCoefficient|3.87494725084764|
|jdo|4.55189918624135|
|LiverpoolCapper|2.92758899437985|
|boshea|2.73075899282043|
|Looney-mods|2.81198074377767|
|zazzage|2.86275935836261|
|grunet|2.94138126530589|

