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
|BSP|2.6867000670099||
|ConcensusSCD2023|2.72589321500844|1|
|melatonin|2.72870678333835|2|
|ShinyNewThings|2.74045964252941|3|
|watptv|2.74130628993672|4|
|Naomi|2.7446574700527|5|
|OnMyHighHorse|2.74767116243166|6|
|Elle-Macpherson|2.75246554210744|7|
|Sportpunter|2.75294951724324|8|
|willingly|2.76119922454775|9|
|RonW|2.77096778750752|10|
|BelleEpoque|2.77643743544209|11|
|boshea|2.77703264827639|12|
|nihaoshijie|2.77851741974697|13|
|HorsesAreJustLargeDogsRight|2.78573200252421|14|
|Gee-Gee-Genius|2.78995051430206|15|
|CarrotCruncher|2.79761863239879||
|sebnatann|2.79986585816796|16|
|Doriemus|2.80571680682154|17|
|VinhoVerde|2.80640795606154|18|
|Skunkworks|2.82409704675125|19|
|Looney-mods|2.83326609871804|20|
|Cfrance|2.83332292858508|21|
|tomsguesses|2.8385809540608|22|
|Craigs-List|2.85509826642013|23|
|SpicyPredictions|2.87541797902157|24|
|ANCR101|2.87864661844503|25|
|Definitely-not-overfitted|2.88956390797872|26|
|Chautauqua|2.90487892856798|27|
|LiverpoolCapper|2.92758899437985|28|
|TopPunter|2.93681282793188|29|
|zazzage|2.95689937566986|30|
|exogen|2.96183991769485|31|
|grunet|2.96422427723889|32|
|Vertex|2.98800942403936|33|
|reliable-lumberjack|2.99676131376172|34|
|TheDartMethod|3.04796221876107|35|
|DamienThirst|3.04903988600072|36|
|matouka|3.07538826127678|37|
|High-Hat|3.11103075513236|38|
|236john-KvKid|3.16289203573925|39|
|Moose-Ste|3.17925166962664|40|
|RockSystems|3.23671678174203|41|
|bruno|3.37528736608561|42|
|RandomShrubbery|3.4482752843776|43|
|Hoover|3.59507916459696|44|
|HackerHandicapping|3.68367771271078|45|
|ReiningIn|3.71913788855543|46|
|jdo|4.55189918624135|47|
|Katana|4.81745685400048|48|
