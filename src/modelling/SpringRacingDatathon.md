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

[example file Caulfield Cup 21/10/2023](../assets/example_submission_file_caulfield_20231021.csv)

[Week 1 Submission File 28/10/2023](../assets/Spring_Racing_Data_Modelling_Competition_2023_Submission_Form_Week_1_{Model_Name}.csv)

## Dataset updates

Dataset updates will be loaded to the dataset page (link included in your registration confirmation email) by 4:59pm AEDT each Friday prior to the nominated race day.

## Results

Leaderboards will be posted here weekly as well as in the Betfair Quants Discord server.

For an invite to the discord server, please fill out the form [here](https://forms.office.com/r/ZG9ea1xQj1 )

|model_name|Score|Rank|
|---------------------------------------|--------|---|
|boshea|2.20202849510987|1|
|BSP|2.20891466779169||
|ConcensusSCD2023|2.21307684826519|2|
|KeenAsABean|2.21622755460686|3|
|HackerHandicapping|2.22364020024497|4|
|Doriemus|2.24635161726742|5|
|watptv|2.24925354290461|6|
|nihaoshijie|2.25746067690203|7|
|Naomi|2.26565540362391|8|
|OnMyHighHorse|2.26954206499015|9|
|BelleEpoque|2.27324889338786|10|
|ReiningIn|2.29952778612028|11|
|willingly|2.30431610798469|12|
|RonW|2.31236201496025|13|
|Elle-Macpherson|2.3184539131686|14|
|ShinyNewThings|2.33757548466816|15|
|Betfair Hub Prediction Model|2.33757797014824||
|sebnatann|2.34073315618566|16|
|HorsesAreJustLargeDogsRight|2.34946779155738|17|
|melatonin|2.35527718919005|18|
|VinhoVerde|2.35861417154038|19|
|Skunkworks|2.37759112811249|20|
|Cfrance|2.39875458466462|21|
|TopPunter|2.43356493147934|22|
|Sportpunter|2.44482245488384|23|
|Gee-Gee-Genius|2.46502045935803|24|
|ANCR101|2.47707920040049|25|
|exogen|2.48353629466958|26|
|tomsguesses|2.52673040663449|27|
|Craigs-List|2.53395668854249|28|
|Looney-mods|2.54908111488899|29|
|Definitely-not-overfitted|2.57252515436117|30|
|SpicyPredictions|2.63180738701456|31|
|LiverpoolCapper|2.63793097619283|32|
|grunet|2.65231719662243|33|
|Chautauqua|2.69046045740994|34|
|Vertex|2.72518628858603|35|
|Katana|2.76074553956356|36|
|DamienThirst|2.76372425679997|37|
|High-Hat|2.81746160468562|38|
|TheDartMethod|2.84888316402265|39|
|RandomShrubbery|2.87986243547551|40|
|zazzage|2.89189087364781|41|
|reliable-lumberjack|2.902634496701|42|
|236john-KvKid|2.94970857112953|43|
|bruno|3.12192235135728|44|
|Moose-Ste|3.12559876677284|45|
|RockSystems|3.20850498210682|46|
|Hoover|3.97901948405137|47|
|jdo|4.98054503383353|48|
|LOUMMv1|6.52456477885587|49|
