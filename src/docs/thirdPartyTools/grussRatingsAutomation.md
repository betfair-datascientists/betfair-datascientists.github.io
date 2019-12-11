# Gruss Betting Assistant: Ratings automation
---
## Automating a greyhound ratings strategy using Gruss

Using ratings from reputable sources can be a great way to increase your wagering IQ. In this tutorial, we'll be following a similar process to the ratings automation tutorial for Bet Angel, but here we'll be using the ratings for greyhounds, created by the data science team at Betfair and incorporate them into our automation in Gruss. 

Gruss Betting Assistant has a spreadsheet functionality that lets you place bets using your own variables and information from the live market, which is what we've used here to automate these ratings. There are so many different ways to use this part Gruss and we're very open to any thoughts about more effective ways of implementing this sort of strategy. You're welcome to reach out to us on automation@betfair.com.au with your feedback and opinions. 

--- 
## - The plan

We're using the [Greyhound Ratings Model](https://www.betfair.com.au/hub/tools/models/greyhound-ratings-model/) put together by some of our Data Scientists. This model creates ratings for Victorian and Queensland greyhound races daily and is freely available on the Hub. It's pretty good at predicting winners, so we're going to place back bets on the dogs with shorter ratings where the market price is better than the model's rating. Gruss Betting Assistant's Excel triggered betting feature has the capacity to let you create spreadsheets with pretty complicated rules that can be applied to multiple markets, which is what we've used for the automation here. 

Here we'll step through how we went about getting Gruss to place bets using [these ratings](https://www.betfair.com.au/hub/tools/models/greyhound-ratings-model/). Once it's set up the goal is to be able to upload a new set of ratings, choose your races, set the program running and be able to walk away. Obviously, you can use your own ratings and change the rules according to what your strategy is.

![Automating a ratings based strategy with Gruss](./img/GrussHubGreyRatings.png)

!!! info "Resources"
    - Ratings: [Betfair Data Scientists' Greyhound Ratings Model](https://www.betfair.com.au/hub/tools/models/greyhound-ratings-model/)
    - Rules: [here's the spreadsheet](./assets/Gruss_RatingsAutomation.xlsx) We set up with our rules included, but you'll obviously need to tweak it to suit your strategy and the format of your ratings 
    - Tool: [Gruss Betting Assistant](http://www.gruss-software.co.uk/betfair-products/betfair-betting-assistant)

---
### - Set up 

Make sure you've downloaded and installed [Gruss Betting Assistant](http://www.gruss-software.co.uk/betfair-products/betfair-betting-assistant), and signed in.

![Automating a rating strategy with Gruss](./img/GrussRatingsUI.png)

---
### - Downloading & formatting ratings

Here we're using the [Betfair's Data Scientists' greyhound ratings model](https://www.betfair.com.au/hub/tools/models/greyhound-ratings-model/) for greyhound racing but alternatively you can follow the same process using the [Betfair's Data Scientists' thoroughbred Ratings Model](https://www.betfair.com.au/hub/horse-racing-tips/#today) which is also available on the hub. When there are ratings made available, you will have the options to download them as a CSV or JSON file. For this tutorial, we'll go ahead and download the ratings as a CSV file. 

![Automating a ratings based strategy with Gruss](./img/GrussHubRatings.png)

Once we've downloaded the ratings, we'll go ahead and open up the files in Excel and copy the contents (Excluding the column headers) from cell A2, across all applicable columns which in this example is column N. Make sure to copy all rows that has data in them. 

![Automating a ratings based strategy with Gruss](./img/GrussRatingsCSVData.png)

Copy the ratings data over to the [customised Gruss template Excel sheet](./assets/Gruss_RatingsAutomation.xlsx) 'RATINGS' worksheet, being sure that cell A2 is selected when pasting the data. In the Excel template that we've provided, we've coloured the cells green where the data should be populated.

![Automating a ratings based strategy with Gruss](./img/GrussRatingsWorksheet.png)

---

### - Writing your rules

As with any automated strategy, one of the most important steps is deciding what logical approach you want to take and writing rules that suit. 

We're using a [customised version of the default Gruss template Excel sheet](./assets/Gruss_RatingsAutomation.xlsx) to implement our strategy, so it can make betting decisions based on my ratings. Excel is an excellent tool, but it can take an investment of time to be able to use it effectively. There are lots of posts on the [Gruss Forum on the topic](http://www.gruss-software.co.uk/forum/viewforum.php?f=8) if you want to explore it more yourself.

This is how we used Excel to implement our set of rules. 


### - Trigger to place bet

In short, we want to back runners when:

- The available to back price is greater than the rating for that runner, then we will back the runner
- The available to back price is less than the rating for that runner, then we will lay the runner
- Back market percentage is less than a certain value that we choose
- The scheduled event start time is less than a certain number of seconds that we choose
- The event isn't in play 

### - Using cell references to simplify formulas

Throughout this tutorial, we'll be referencing certain cells with custom names that will make it easier to understand and follow the formulas as we progress. This is an especially effective method to
keep on top of more complex strategies that require long formaulas to implement.
 
!!! info "Cell names used in this tutorial"

     - **Ratings** refers to the entire Column J in the 'RATINGS' worksheet

     - **RunnerName** refers to the entire column L in the 'RATINGS' worksheet

     - **Overround** refers to cell Y in the 'MARKET'worksheet, where the overrounds for the current market are calculated. 

     - **UserOverround** refers to cell C5 in the 'SETTINGS' worksheet which allows you to change a single value that will automatically update the formulas for all runners

     - **TimeTillJump** refers to cell C9 in the 'SETTINGS' worksheet

     - **UserTimeTillJump** refers to cell C4 in the 'SETTINGS' worksheet which allows you to change a single value that will automatically update the formulas for all runners

     - **InPlay** refers to cell E2 in the 'MARKET' worksheet. Gruss will populate a 'Not In Play' status leading up to the jump

     - **BACKLAY** refers to cell C6 in the 'SETTINGS' worksheet which allows you to easily switch between Back and Lay bet typers via a drop-down box and will automatically update the formulas for all runners

     - **MARKETSTATUS** refers to F2 in the 'MARKET' worksheet




**This is our trigger for the 'MARKET' worksheet**

``` excel tab="Multi line"
=IF(
    AND(
        OR(
             AND(BACKLAY="BACK",(F5>(INDEX(Ratings,MATCH(A5,RunnerName,0))))),
             AND(BACKLAY="LAY",(F5<(INDEX(Ratings,MATCH(A5,RunnerName,0)))))),
        Overround<UserOverround,
        TimeTillJump<UserTimeTillJump,
        InPlay="Not In Play",
        MarketStatus<>"Suspended"),
        BACKLAY,
    ""
)
```

``` excel tab="Single line"
=IF(AND(OR(AND(BACKLAY="BACK",(F5>(INDEX(Ratings,MATCH(A5,RunnerName,0))))),AND(BACKLAY="LAY",(F5<(INDEX(Ratings,MATCH(A5,RunnerName,0)))))),Overround<UserOverround,TimeTillJump<UserTimeTillJump,InPlay="Not In Play",MarketStatus<>"Suspended"),BACKLAY,"")
```

Stepping through each step:

- **Checking market odds based on back or lay bet type:** Here we're checking which bet type we've chosen from the dropdown box in the 'SETTINGS' worksheet (cell D6). If a BACK bet has been selected, the best available back bet must greater than our ratings that have been defined for that particular runner in the 'RATINGS' worksheet. On the flip side, if a LAY bet has been selected, then the best available back bet must be less than our ratings.


``` excel hl_lines="4 5"
=IF(
    AND(
        OR(
             AND(BACKLAY="BACK",(F5>(INDEX(Ratings,MATCH(A5,RunnerName,0))))),
             AND(BACKLAY="LAY",(F5<(INDEX(Ratings,MATCH(A5,RunnerName,0)))))),
        Overround<UserOverround,
        TimeTillJump<UserTimeTillJump,
        InPlay="Not In Play",
        MarketStatus<>"Suspended"),
        BACKLAY,
    ""
)
```


- **Back market percentage (Overround) is less than what we define (UserOverround):** Here we're making a calculation for each runner (100 / best back price) and then calculating the sum of all of the runners together to give us the back market percentage. As the closer the BMP is to 100%, the fairer the market is, we use this to ensure that we only place bets when the market is less than what we define in the 'RATINGS' worksheet. [Additional information relating to over-rounds can be found on the Hub.](https://www.betfair.com.au/hub/understanding-over-round/)


``` excel hl_lines="6"
=IF(
    AND(
        OR(
             AND(BACKLAY="BACK",(F5>(INDEX(Ratings,MATCH(A5,RunnerName,0))))),
             AND(BACKLAY="LAY",(F5<(INDEX(Ratings,MATCH(A5,RunnerName,0)))))),
        Overround<UserOverround,
        TimeTillJump<UserTimeTillJump,
        InPlay="Not In Play",
        MarketStatus<>"Suspended"),
        BACKLAY,
    ""
)
```


- **Time until the jump is less than what we define:** Check whether the seconds left on the countdown timer are less than what we define in cell C4 in the 'SETTINGS' worksheet. This one's a bit complicated, as the time is actually returned as a percentage of a 24-hour day, which you need to convert into positive or negative seconds. [You can read about the formula here](https://www.betangel.com/forum/viewtopic.php?t=7657) or just keep it simple by referencing the value in cell E2 of the 'SETTINGS' worksheet (named 'TimeTillJump1'), where we've already done the calculations for you. 


``` excel hl_lines="7"
=IF(
    AND(
        OR(
             AND(BACKLAY="BACK",(F5>(INDEX(Ratings,MATCH(A5,RunnerName,0))))),
             AND(BACKLAY="LAY",(F5<(INDEX(Ratings,MATCH(A5,RunnerName,0)))))),
        Overround<UserOverround,
        TimeTillJump<UserTimeTillJump,
        InPlay="Not In Play",
        MarketStatus<>"Suspended"),
        BACKLAY,
    ""
)
```

- **Not in play:** checking whether the event has gone in play - as odds change so much in the run we only want to use this strategy pre-play. If cell E2 in the 'MARKET' worksheet has a 'Not In Play' flag, it's safe to place bets. 


``` excel hl_lines="8"
=IF(
    AND(
        OR(
             AND(BACKLAY="BACK",(F5>(INDEX(Ratings,MATCH(A5,RunnerName,0))))),
             AND(BACKLAY="LAY",(F5<(INDEX(Ratings,MATCH(A5,RunnerName,0)))))),
        Overround<UserOverround,
        TimeTillJump<UserTimeTillJump,
        InPlay="Not In Play",
        MarketStatus<>"Suspended"),
        BACKLAY,
    ""
)
```


- **Market Status** checking whether the event has been suspended - if there is any flag other than 'Suspended' in cell F2 of the 'MARKET' worksheet, it's safe to place bets.

``` excel hl_lines="9"
=IF(
    AND(
        OR(
             AND(BACKLAY="BACK",(F5>(INDEX(Ratings,MATCH(A5,RunnerName,0))))),
             AND(BACKLAY="LAY",(F5<(INDEX(Ratings,MATCH(A5,RunnerName,0)))))),
        Overround<UserOverround,
        TimeTillJump<UserTimeTillJump,
        InPlay="Not In Play",
        MarketStatus<>"Suspended"),
        BACKLAY,
    ""
)
```


- **Result:** if the statement above is true, the formula returns either a "BACK" or "LAY" depending on what has been selected from the 'SETTINGS' worksheet, at which point the bet will trigger, otherwise the cell will remain blank and no bet will be placed.

``` excel hl_lines="10"
=IF(
    AND(
        OR(
             AND(BACKLAY="BACK",(F5>(INDEX(Ratings,MATCH(A5,RunnerName,0))))),
             AND(BACKLAY="LAY",(F5<(INDEX(Ratings,MATCH(A5,RunnerName,0)))))),
        Overround<UserOverround,
        TimeTillJump<UserTimeTillJump,
        InPlay="Not In Play",
        MarketStatus<>"Suspended"),
        BACKLAY,
    ""
)
```

!!! info "Excel functions"

    - [IF statement:](https://support.office.com/en-us/article/if-function-69aed7c9-4e8a-4755-a9bc-aa8bbff73be2) IF(if this is true, do this, else do this)
    - [AND statement:](https://support.office.com/en-us/article/and-function-5f19b2e8-e1df-4408-897a-ce285a19e9d9) AND(this is true, and so is this, and so is this) - returns true or false
    - [And Or statement:](https://support.office.com/en-us/article/use-and-and-or-to-test-a-combination-of-conditions-e1ed88d7-1de3-4422-ae41-45291a69f9e1) checks that the statement meets more than one condition. If this OR that, then do the following. 
    - [Absolute references:](https://support.office.com/en-us/article/switch-between-relative-absolute-and-mixed-references-dfec08cd-ae65-4f56-839e-5f0d8d0baca9) if you're copy/pasting formulas it's important that you make links absolute when you don't want the cell being referenced to change relative to the new cell the formula is being pasted into. You do this by putting a $ in front of the parts of the reference you don't want to 'move'.  

---
### - Preparing the spreadsheet

You need to copy/paste these three formulas into the relevant cell on each runner - we did a few extra rows than the number of runners in the markets we were looking at, just in case the fields are bigger in future events. Excel is clever enough to automatically update the relative links in the formulas, so you should be able to copy/paste the same formula into each cell as long as you've got your [relative and absolute references straight](https://support.office.com/en-us/article/switch-between-relative-absolute-and-mixed-references-dfec08cd-ae65-4f56-839e-5f0d8d0baca9). 

- **Trigger bet rule:** this is the bet trigger Excel formula we created earlier, and it needs to go in column Q (Q5 for the first runner) in the 'MARKET' worksheet.

``` excel tab="Multi line"
=IF(
    AND(
        OR(
             AND(BACKLAY="BACK",(F5>(INDEX(Ratings,MATCH(A5,RunnerName,0))))),
             AND(BACKLAY="LAY",(F5<(INDEX(Ratings,MATCH(A5,RunnerName,0)))))),
        Overround<UserOverround,
        TimeTillJump<UserTimeTillJump,
        InPlay="Not In Play",
        MarketStatus<>"Suspended"),
        BACKLAY,
    ""
)
```

``` excel tab="Single line"
=IF(AND(OR(AND(BACKLAY="BACK",(F5>(INDEX(Ratings,MATCH(A5,RunnerName,0))))),AND(BACKLAY="LAY",(F5<(INDEX(Ratings,MATCH(A5,RunnerName,0)))))),Overround<UserOverround,TimeTillJump<UserTimeTillJump,InPlay="Not In Play",MarketStatus<>"Suspended"),BACKLAY,"")
```

![Automating a ratings based strategy with Gruss](./img/GrussRatingsExcel1.PNG)

- **Odds:** initially we were using the runner's rating as the price, but we got a bet placement error for some of the selections - eventually we realised that the odds the bet's being placed at need to be [valid Betfair 'ticks'](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/placeOrders#placeOrders-BetfairPriceIncrements). For simplicity's sake we're now just using the currently available back odds (cell F5 for the first runner). This goes in column R (R5 for the first runner). Another option would be to create a look up table that rounded your rating to the nearest ['tick' price](https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/placeOrders#placeOrders-BetfairPriceIncrements) - if you do this, please do [send us](mailto:automation@betfair.com.au) through your formula and we'll add it to this tutorial. 

```=IF(F5=0,"",F5)```

![Automating a ratings based strategy with Gruss](./img/GrussRatingsExcel2.PNG)

**Stake:** It's completely up to you what staking approach you want to take. We've kept it simple and are just using a 'to win / to lose' strategy. Each bet aims to win whatever value has been entered in the 'SETTINGS' worksheet on that runner at the current odds if the bet type has been set to BACK. If the bet type has been changed to LAY, then the stake becomes the liability - again, easily changed in the 'SETTINGS' worksheet. We've got some [good resources on the Hub](https://www.betfair.com.au/hub/better-betting/betting-principles/basic-principles/staking-plans-and-strategies/) that look at different staking approaches - these might be useful in helping you decide which strategy you want to use. 

```=IF(A5="","",IF(BACKLAY="BACK", stake/(F5-1),stake*(H5/(H5-1))-stake)
```

![Automating a ratings based strategy with Gruss](./img/GrussRatingsExcel3.PNG)

---
### - Selecting markets

Gruss makes it really easy to select markets in bulk. You could go through an add each market you have in your ratings individually, but it's much easier to just use the quick Pick functionality to add all Australian racing win markets. This is safe, because bets will only fire when they link up with a runner in your 'RATINGS' sheet. 

![Automating a ratings based strategy with Gruss](./img/GrussRatingsMarkets.png)

You also need to make sure you set it up so that the program will automatically move on to the next market, when the previous one jumps.

![Automating a ratings based strategy with Gruss](./img/GrussRatingsMarkets2.png)

---
### - Linking the spreadsheet

This is a little tricky the first time, but easy once you know how. Make sure you have the [Excel sheet](./assets/Gruss_RatingsAutomation.xlsx) saved to your local computer - when we tried using a file we had saved in OneDrive it simply didn't work. Open the Excel sheet, then click on Excel/Log current prices. 

![Automating a ratings based strategy with Gruss](./img/GrussRatingsLinkingExcel.png)

It will autofill the workbook and sheet names. You'll then need to make sure you tick:

- Enable triggered betting
- Clear Bet refs on auto select market
- Quick pick reload triggers select first market

Then click OK and the sheet with be linked with the program. 

![Automating a ratings based strategy with Gruss](./img/GrussRatingsLinkingExcel2.PNG)

---
## And you're set!

Once you've set your spreadsheet set up and you're comfortable using Gruss Betting Assistant it should only take a number of seconds to load your markets and ratings up and set your strategy running for the day. Just make sure you have all of the app settings correctly selected before you leave the bot to run, as some of them reset by default when you turn the program off.

!!! info "Note:" 
    you will need to leave your computer up and running for the duration of the chosen markets, as the program needs the computer to be 'awake' to be able to run.
    
---
## Areas for improvement

There are parts of this approach that we're still trying to get to work to our liking, and we'll update this article as we find better solutions. If you have any suggestions for improvements please reach out to automation@betfair.com.au - we'd love to hear your thoughts. 

For example, the spreadsheet only binds with one market at a time, so if one market gets delayed and runs overtime the program won't be able to move on to the next market - we missed some races because of this. 

---
## What next? 

We're working through some of the popular automation tools and creating articles like this one to help you learn how to use them to implement different styles of strategies. If you have any thoughts or feedback on this article or other programs you'd like to see us explore please reach out to automation@betfair.com.au 

---
## Disclaimer

Note that whilst automated strategies are fun and rewarding to create, we can't promise that your betting strategy will be profitable, and we make no representations in relation to the information on this page. If you're implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred.  Under no circumstances will Betfair be liable for any loss or damage you suffer.