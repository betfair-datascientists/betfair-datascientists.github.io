# Betfair API tutorials in R

Betfair's API can be easily traversed in R. It allows you to retrieve market information, create/cancel bets and manage your account. Here's a collection of easy to follow API tutorials in R:

- [Accessing the API using R](/api/apiRtutorial/#accessing-the-api-using-r)
- [Get Worldcup Odds](/api/apiRtutorial/#get-world-cup-odds-tutorial)
- [AFL Odds PulleR Tutorial](/api/apiRtutorial/#afl-odds-puller-tutorial)

---
## Accessing the API using R

### Set up R

- [What is R?](https://www.r-project.org/about.html)
- [Download and install R](https://cran.ms.unimelb.edu.au/) – get the language set up on your computer
- [Download and install RStudio](https://www.rstudio.com/) – you’ll need a program to develop in, and this one is custom-designed to work with R

---
### Required Packages

Two R packages are required:

``` r
library(tidyverse)
library(abettor)
```

The [abettor package can be downloaded here](https://github.com/phillc73/abettor). For an in-depth understanding of the package, have a read of the documentation. Instructions are also provided in the sample code.

---
### Login to Betfair

To login to Betfair, replace the following dummy username, password and app key with your own.

``` r
abettor::loginBF(username = "betfair_username",
                 password = "betfair_password",
                 applicationKey = "betfair_app_key")
```

If you don't have a live app key for the API yet [take a look at this page](../../api/apiappkey).

---
### Finding Event IDs

In order to find data for specific markets, you will first need to know the event ID. This is easily achieved with the [abettor package](https://github.com/phillc73/abettor). 

To find the event IDs of events in the next 60 days:

``` r
abettor::listEventTypes(toDate = (format(Sys.time() + 86400 * 60, "%Y-%m-%dT%TZ")))
```

This will return a DataFrame of the following structure:

``` r
eventType.id	eventType.name	marketCount
1	Soccer	1193
2	Tennis	2184
7522	Basketball	1
4	Cricket	37
7	Horse Racing	509
61420	Australian Rules	31
4339	Greyhound Racing	527
```

---
### Finding Competition IDs

Once you have the event ID, the next logical step is to find the competition IDs for the event you want to get data for. For example, if you want to find the competition IDs for Australian Rules, you would use the following

``` r
abettor::listCompetitions(
  eventTypeIds = 61420,  ## AFL is eventTypeId 61420,
  toDate = (format(Sys.time() + 86400 * 180, "%Y-%m-%dT%TZ")) ## Look ahead until the next 180 days
)
```

This will return the following structured DataFrame:

``` r
competition.id	competition.name	marketCount	competitionRegion
11516633	Brownlow Medal 2018	3	AUS
11897406	AFL	78	AUS
```

---
### Finding Specific Markets

The next logical step is to find the market that you are interested in. Furthering our example above, if you want the Match Odds for all Australian Rules games over the next 60 days, simply use the Competition ID from above in the following.

``` r
abettor::listMarketCatalogue(
  eventTypeIds = 61420,
  marketTypeCodes = "MATCH_ODDS", ## Restrict our search to Match Odds only, not other markets for the same match
  competitionIds = 11897406,
  toDate = (format(Sys.time() + 86400 * 60, "%Y-%m-%dT%TZ"))
```

This returns a large DataFrame object with each market, participants and associated odds.

---
## Get World Cup Odds Tutorial

This tutorial walks you through the process of retrieving exchange odds for all the matches from the 2018 FIFA World Cup 2018. This can be modified for other sports and uses.

You can run this script in R.

``` r
###################################################
### FIFA World Cup Datathon
### Betfair API Tutorial
###
### This script allows you to access the Betfair
### API and retrive exchange odds for all the 
### matches from the upcoming FIFA World Cup 2018
###################################################

###################################################
### Setup
###################################################

## Loading required packages
library(tidyverse) ## package for general data manipulation - https://www.tidyverse.org/
library(abettor) ## wrapper package for the Betfair API - https://github.com/phillc73/abettor

## Enter your Betfair API Credentials below
betfair_username <- ""
betfair_password <- ""
betfair_app_key <- ""

## Login to Betfair - should return "SUCCESS:" on successful login
betfair_login <- abettor::loginBF(username = betfair_username,
                                  password = betfair_password,
                                  applicationKey = betfair_app_key)

###################################################
## Retrieving all soccer competitions for 
## which markets are currently alive
## on the Betfair Exchange
###################################################

all_soccer_markets <- abettor::listCompetitions(
  eventTypeIds = 1,  ## Soccer is eventTypeId 1,
  toDate = (format(Sys.time() + 86400 * 60, "%Y-%m-%dT%TZ")) ## Look ahead until the next 60 days
  )
###################################################
## Retrieving the competition id
## for the 2018 World Cup 
###################################################

world_cup_competition_id <- all_soccer_markets %>%
  dplyr::pull(competition) %>% ## Extracting the variable competition which is a nested data frame
  dplyr::filter(name == "2018 FIFA World Cup") %>% ## Filtering for the competition we need
  dplyr::pull(id) ## Extracting the id for the competition we need

###################################################
## Obtaining all markets that are currently 
## alive on the Betfair Exchange that belong to
## Competition ID that is mapped to the World Cup 
###################################################

all_world_cup_markets <- abettor::listMarketCatalogue(
  eventTypeIds = 1, ## Soccer is eventTypeId 1
  marketTypeCodes = "MATCH_ODDS", ## Restrict our search to Match Odds only, not other markets for the same match
  competitionIds = world_cup_competition_id, ## Restrict our search to World Cup matches only
  toDate = (format(Sys.time() + 86400 * 60, "%Y-%m-%dT%TZ")) ## Look ahead until the next 60 days
)

###################################################
## Obtaining the current odds on the Betfair
## Exchange for all the markets that were 
## obtained in the previous step (World Cup Matches)
###################################################

## Creating a vector/array of all market ids
all_world_cup_markets_market_ids <- all_world_cup_markets %>%
  pull(marketId)

## This function takes in a single market id and returns 
## the current live odds on the Betfair Exchange for that market
fetch_odds <- function(market_id) {
  
  ## Retrieving market odds for a single market
  odds <- abettor::listMarketBook(marketIds = market_id, ##Runs listMarketBook for given market_id
                                  priceData = "EX_BEST_OFFERS" ##Fetching the top 3 odds, EX_ALL_OFFERS fetches the entire depth of prices
                                  ) %>%
    pull(runners) %>% ## Extracting the runners field which has details of odds
    as.data.frame() %>% ## Converting to data frame from list
    select(lastPriceTraded) %>% ## Extracting team and last matched odds
    mutate(market_id = market_id) %>% ## Padding market id to the data to make it unique to this match
    bind_cols(data.frame(outcome = c("o_1","o_2","o_3"))) %>% ## Creating outcome order to maintain consistency
    spread(outcome, lastPriceTraded) %>% ## Reshaping data to make it 1 row per match
    rename(team_1_odds = o_1,
           team_2_odds = o_2,
           draw_odds = o_3) %>% ##Renaming columns such that all matches can be combined into one data frame
    select(market_id, team_1_odds, draw_odds, team_2_odds) ## Ordering columns in the right order
  
  return(odds)
}

## The code below maps (or loops) each market id in the vector we created
## above through the fetch_odds function and retrives the market odds 
## into a single data frame
world_cup_market_odds <- map_df(.x = all_world_cup_markets_market_ids, ##Iterate over market ids
                                .f = fetch_odds ## through function fetch_odds
                                ) %>%
  bind_cols(all_world_cup_markets %>% ## Merge with event names to identify which match odds it is
              pull(event) %>%
              select(name)) %>% 
  mutate(team_1 = gsub(" v .*","",name), ## Extracting team 1 from match name
         team_2 = gsub(".* v ", "", name)) %>% ## Extracing team 2 from match name
  select(team_1, team_2, team_1_odds, draw_odds, team_2_odds) ## Extracting columns that we need

## Writing output to csv file
write_csv(world_cup_market_odds, "world_cup_market_odds.csv")
```

---
## AFL Odds PulleR Tutorial

This tutorial walks you through the process of retrieving exchange odds for the the next round of Australian Rules.

You can run this script in R.

``` r
###################################################
### AFL Model
### Betfair API Odds GrabbR
###
### This script allows you to access the Betfair
### API and retrive exchange odds for all the 
### matches for the upcoming round of AFL games
###################################################

## Loading required packages
library(tidyverse) ## package for general data manipulation - https://www.tidyverse.org/
library(abettor) ## wrapper package for the Betfair API - https://github.com/phillc73/abettor

## Login to Betfair - should return "SUCCESS:" on successful login
betfair_login <- abettor::loginBF(username = 'your_username',
                                  password = 'your_password',
                                  applicationKey = "your_betfair_app_key")

###################################################
## Retrieving all AFL competitions for 
## which markets are currently alive
## on the Betfair Exchange
###################################################

all_afl_markets <- abettor::listCompetitions(
  eventTypeIds = 61420,  ## AFL is eventTypeId 61420,
  toDate = (format(Sys.time() + 86400 * 180, "%Y-%m-%dT%TZ")) ## Look ahead until the next 180 days
)
###################################################
## Retrieving the competition id
## for the regular AFL season
###################################################

afl_competition_id <- all_afl_markets %>%
  dplyr::pull(competition) %>% ## Extracting the variable competition which is a nested data frame
  dplyr::filter(name == "AFL") %>% ## Filtering for the competition we need
  dplyr::pull(id) ## Extracting the id for the competition we need

###################################################
## Obtaining all markets that are currently 
## alive on the Betfair Exchange that belong to
## Competition ID that is mapped to the AFL
###################################################

all_afl_markets <- abettor::listMarketCatalogue(
  eventTypeIds = 61420, ## AFL is eventTypeId 61420
  marketTypeCodes = "MATCH_ODDS", ## Restrict our search to Match Odds only, not other markets for the same match
  competitionIds = afl_competition_id, ## Restrict our search to AFL Matches Only
  toDate = (format(Sys.time() + 86400 * 60, "%Y-%m-%dT%TZ")) ## Look ahead until the next 60 days
)

###################################################
## Obtaining the current odds on the Betfair
## Exchange for all the markets that were 
## obtained in the previous step
###################################################

## Creating a vector/array of all market ids
all_afl_markets_market_ids <- all_afl_markets %>%
  pull(marketId)

## This function takes in a single market id and returns 
## the current live odds on the Betfair Exchange for that market
fetch_odds <- function(market_id) {
  
  ## Retrieving market odds for a single market
  odds <- abettor::listMarketBook(marketIds = market_id, ##Runs listMarketBook for given market_id
                                  priceData = "EX_BEST_OFFERS" ##Fetching the top 3 odds, EX_ALL_OFFERS fetches the entire depth of prices
  ) %>%
    pull(runners) %>% ## Extracting the runners field which has details of odds
    as.data.frame() %>% ## Converting to data frame from list
    select(lastPriceTraded) %>% ## Extracting team and last matched odds
    mutate(market_id = market_id) %>% ## Padding market id to the data to make it unique to this match
    bind_cols(data.frame(outcome = c("o_1","o_2"))) %>% ## Creating outcome order to maintain consistency
    spread(outcome, lastPriceTraded) %>% ## Reshaping data to make it 1 row per match
    rename(team_1_odds = o_1,
           team_2_odds = o_2) %>% ##Renaming columns such that all matches can be combined into one data frame
    select(market_id, team_1_odds, team_2_odds) ## Ordering columns in the right order
  
  return(odds)
}

## The code below maps (or loops) each market id in the vector we created
## above through the fetch_odds function and retrives the market odds 
## into a single data frame
afl_market_odds <- map_df(.x = all_afl_markets_market_ids, ##Iterate over market ids
                                .f = fetch_odds ## through function fetch_odds
) %>%
  bind_cols(all_afl_markets %>% ## Merge with event names to identify which match odds it is
              pull(event) %>%
              select(name)) %>% 
  mutate(team_1 = gsub(" v .*","",name), ## Extracting team 1 from match name
         team_2 = gsub(".* v ", "", name)) %>% ## Extracing team 2 from match name
  select(team_1, team_2, team_1_odds, team_2_odds) ## Extracting columns that we need

## Writing output to csv file
write_csv(afl_market_odds, "weekly_afl_odds.csv")
```