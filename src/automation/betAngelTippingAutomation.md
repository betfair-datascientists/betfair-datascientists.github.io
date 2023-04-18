# Bet Angel Pro: Tipping automation

---
## Automating a (non-ratings based) tipping strategy using Bet Angel Pro

We all love getting some good racing tips, but who has time to sit and place bets all day? Wouldn't it be easier if you could take those tips and get a program to automatically place the bets on your behalf? 

This is what we're going to explore here - we'll be using Bet Angel Pro to place bets automatically based on a set of tips. This is our first-time using Bet Angel for this approach and we are very open to any thoughts about more effective ways of implementing this sort of strategy. You're welcome to reach out to us at automation@betfair.com.au with your feedback and opinions. 

--- 
## - The plan

We have a set of tips that we've taken from our DataScientists' Racing Prediction Model, but this approach should work for any set of tips you may have. Our goal is to create an automated process which will let us choose our tips for the day, then walk away and the program do the leg work. 

Here we'll step through how we went about getting Bet Angel Pro to place bets on the favourite runner identified by [Betfair's Data Scientists](https://www.betfair.com.au/hub/racing/horse-racing/predictions-model/). There are no ratings associated with these tips, so we're happy to take [Betfair's Starting Price](https://www.betfair.com.au/hub/education/betfair-basics/betfair-starting-price-bsp/) instead of a price for these bets. 

![Automating a tipping strategy with Bet Angel](./img/BetAngeltipHub.png)

If you want to follow along and try this approach yourself you'll need to download [Bet Angel Pro](https://www.betangel.com/bet-angel-professional/) and sign up for either a subscription or at least a test period. They have a [14 day free trial](https://www.betangel.com/trial/) that's valuable for establishing whether this tool will do what you want it to for your specific strategy. 

!!! info "Resources"
    - Tips: [Betfair Data Scientists' Racing Prediction Model](https://www.betfair.com.au/hub/racing/horse-racing/predictions-model/)
    - Rules: [here's the spreadsheet](./assets/BetAngel_Tipping.xls), we used to automate our tips but you may need to tweak it a bit to suit your own tips. 
    - Tool: [Bet Angel Pro](https://www.betangel.com/bet-angel-professional/)

--- 
### - Set up

First up we need to make sure we've downloaded and installed Bet Angel Pro, and signed in.

Once you open the program up click on the 'G' Guardian icon and open the Guardian functionality up. 

![Automating a tipping strategy with Bet Angel](./img/BetAngeltipPro.png)

---

### -  Writing your rules

As with any automated strategy, one of the most important steps is deciding what logical approach you want to take and writing rules that suit. 

We're using an [customised Bet Angel template Excel sheet](./assets/BetAngel_Tipping.xls) to implement our strategy, so it can make betting decisions based on our tips and automate on multiple markets. Excel is an excellent tool, but it can take an investment of time to be able to use it effectively. 

This is how we used Excel to implement our set of rules. 

### - Trigger to place bet

In short, we want to back or lay runners when:

- The runners name has been specified in our tipping list
- Back market percentage is less than a certain value that we choose
- The scheduled event start time is less than a certain number of seconds that we choose
- The event isn't in play 

### - Using cell references to simplify formulas

Throughout this tutorial, we'll be referencing certain cells with custom names that will make it easier to understand and follow the formulas as we progress. This is an especially effective method to
keep on top of more complex strategies that require long formaulas to implement.
 
!!! info "Cell names used in this tutorial"

     - **RunnerName** refers to the entire column A in the 'TIP' worksheet

     - **Overrounds1, Overrounds2 and Overrounds3** refers to cell AF8 in the 'BET ANGEL', 'BET ANGEL 2' and 'BET ANGEL 3' worksheets repectively, where the overrounds are calculated. Each worksheet needs to contain their own formula calculations as they will each be working off different markets. 

     - **UserOverround** refers to cell H5 in the 'SETTINGS' worksheet which allows you to change a single value that will automatically update the formulas for all runners

     - **TimeTillJump1, TimeTillJump2 and TimeTillJump3** refers to cell E9, E13 and E17 in the 'SETTINGS' worksheet respectively. Just like the overrounds, each worksheet needs their own TimeTillJump calculation - one for each market. 

     - **UserTimeTillJump** refers to cell H2 in the 'SETTINGS' worksheet which allows you to change a single value that will automatically update the formulas for all runners

     - **InPlay1, InPlay2, InPlay3** refers to cell G1 in the 'BET ANGEL', 'BET ANGEL 2' and 'BET ANGEL 3' worksheets respectively. Bet Angel will populate a status in these worksheet cells such as "In Play" or "Suspended" for each market

     - **BackStake** refers to cell H3 in the 'SETTINGS' worksheet and like the name suggests, will be the stake for any back bets that are triggered

     - **LayStake** refers to cell H4 in the 'SETTINGS' worksheet and will be the stake for any lay bets that are triggered

     - **BetType** is the entire B column in the 'TIP' worksheet. Depending on your tip for each runner, you can choose whether you want a back or lay bet to be triggered for that runner


**This is our trigger for the 'BET ANGEL' worksheet:**

``` excel tab="Multi line"
=IF(
   AND(
      COUNTIF(RunnerName,B9)>0,
      TimeTillJump1<UserTimeTillJump,
      Overrounds1<UserOverround,
      ISBLANK(InPlay1)),
      INDEX(TIP!A:B,MATCH(B9,RunnerName,0),2),
    ""
)
```

``` excel tab="Single line"
=IF(AND(COUNTIF(RunnerName,B9)>0,TimeTillJump1<UserTimeTillJump,Overrounds1<UserOverround,ISBLANK(InPlay1)),INDEX(TIP!A:B,MATCH(B9,RunnerName,0),2),"")
```

Stepping through each step:

- **Checking whether the runner is to have a bet placed:** Here the trigger is checking the list of runners in the 'TIPS' worksheet so it can decide whether we want a bet to be placed or not. If the name does appear in our list, then it returns a TRUE flag and continues with the next trigger condition. If the name is not in the list, then no bet will be placed. 

``` excel hl_lines="3"
=IF(
   AND(
      COUNTIF(RunnerName,B9)>0,
      TimeTillJump1<UserTimeTillJump,
      Overrounds1<UserOverround,
      ISBLANK(InPlay1)),
      INDEX(TIP!A:B,MATCH(B9,RunnerName,0),2),
    ""
)
```

- **Time until the jump is less than what we define:** Check whether the seconds left on the countdown timer are less than what we define in cell H2 in the 'SETTINGS' worksheet. This one's a bit complicated, as the time is actually returned as a percentage of a 24-hour day, which you need to convert into positive or negative seconds. [You can read about the formula here](https://www.betangel.com/forum/viewtopic.php?t=7657) or just keep it simple by referencing the value in cell E9 of the 'SETTINGS' worksheet (named 'TimeTillJump1'), where we've already done the calculations for you. 

``` excel hl_lines="4"
=IF(
   AND(
      COUNTIF(RunnerName,B9)>0,
      TimeTillJump1<UserTimeTillJump,
      Overrounds1<UserOverround,
      ISBLANK(InPlay1)),
      INDEX(TIP!A:B,MATCH(B9,RunnerName,0),2),
    ""
)
```

!!! info "Calculating the time until the jump for multiple markets at the same time"

    One thing to be aware of here is that because we're wanting to follow up to three markets in our excel workbook, we need to have three instances of the time conversion formula - One for each possible market that we may want to link into our Excel file. These formulas are located in the 'SETTINGS' worksheet on columns C, D and E.
    
    In the 'BET ANGEL' worksheet, the formulas will be written ```TimeTillJump1<UserTimeTillJump,``` while in the 'BET ANGEL 2' and 'BET ANGEL 3' worksheets it will be written ```TimeTillJump2<UserTimeTillJump,``` and ```TimeTillJump3<UserTimeTillJump,``` respectively. This will mean that every 'BET ANGEL' worksheet will display and track the correct time till jump for their own applicable market.  


- **Back market percentage (Overrounds1) is less than what we define (UserOverround):** Here we're making a calculation for each runner (100 / best back price) and then calculating the sum of all of the runners together to give us the back market percentage. As the closer the BMP is to 100%, the fairer the market is, we use this to ensure that we only place bets when the market is less than what we define in the 'SETTINGS' worksheet. [Additional information relating to over-rounds can be found here.](https://caanberry.com/understanding-the-over-round-in-betting-markets/)

``` excel hl_lines="5"
=IF(
   AND(
      COUNTIF(RunnerName,B9)>0,
      TimeTillJump1<UserTimeTillJump,
      Overrounds1<UserOverround,
      ISBLANK(InPlay1)),
      INDEX(TIP!A:B,MATCH(B9,RunnerName,0),2),
    ""
)
```

- **Not in play:** checking whether the event has gone in play - as odds change so much in the run we only want to use this strategy pre-play. If this cell is blank it means it's not displaying the 'in-play' flag, so it's safe to place bets. 

``` excel hl_lines="6"
=IF(
   AND(
      COUNTIF(RunnerName,B9)>0,
      TimeTillJump1<UserTimeTillJump,
      Overrounds1<UserOverround,
      ISBLANK(InPlay1)),
      INDEX(TIP!A:B,MATCH(B9,RunnerName,0),2),
    ""
)
```

- **Result:** if the statement above is true, check whether BACK or LAY has been selected in column B of the 'TIPS' worksheet for that runner. Whatever has been specified, trigger that bet type. 

``` excel hl_lines="7"
=IF(
   AND(
      COUNTIF(RunnerName,B9)>0,
      TimeTillJump1<UserTimeTillJump,
      Overrounds1<UserOverround,
      ISBLANK(InPlay1)),
      INDEX(TIP!A:B,MATCH(B9,RunnerName,0),2),
    ""
)
```

!!! info "updating the trigger for 'BET ANGEL 2' and 'Bet ANGEL 3' worksheets"

     You will need to ensure that the reference names for Overrounds, TimeTillJump and InPlay are changed so that they are referencing the cells that are applicable for those specific worksheets. Forgetting to do this can lead to the automation working off information from the wrong market.  

- **Trigger for 'BET ANGEL 2' worksheet:** Note that Overrounds has been changed to Overrounds2, TimeTillJump1 to TimeTillJump2 and InPlay1 to InPlay2

``` excel hl_lines="7"
=IF(
   AND(
      COUNTIF(RunnerName,B9)>0,
      TimeTillJump2<UserTimeTillJump,
      Overrounds2<UserOverround,
      ISBLANK(InPlay2)),
      INDEX(TIP!A:B,MATCH(B9,RunnerName,0),2),
    ""
)
```

- **Trigger for 'BET ANGEL 3' worksheet:** Note that Overrounds has been changed to Overrounds3, TimeTillJump1 to TimeTillJump3 and InPlay1 to InPlay3

``` excel hl_lines="7"
=IF(
   AND(
      COUNTIF(RunnerName,B9)>0,
      TimeTillJump3<UserTimeTillJump,
      Overrounds3<UserOverround,
      ISBLANK(InPlay3)),
      INDEX(TIP!A:B,MATCH(B9,RunnerName,0),2),
    ""
)
```

!!! info "Excel functions"

    - [IF function:](https://support.office.com/en-us/article/if-function-69aed7c9-4e8a-4755-a9bc-aa8bbff73be2) IF(if this is true, do this, else do this)
    - [AND function:](https://support.office.com/en-us/article/and-function-5f19b2e8-e1df-4408-897a-ce285a19e9d9) AND(this is true, and so is this, and so is this) - returns true or false
    - [COUNTIF function:]
    - [Absolute references:](https://support.office.com/en-us/article/switch-between-relative-absolute-and-mixed-references-dfec08cd-ae65-4f56-839e-5f0d8d0baca9) if you're copy/pasting formulas it's important that you make links absolute when you don't want the cell being referenced to change relative to the new cell the formula is being pasted into. You do this by putting a $ in front of the parts of the reference you don't want to 'move'. 


### - Preparing the spreadsheet

You need to copy/paste this formula into the relevant cell on each green row - we copied ours into all of the coloured cells in the sheet, just in case the fields are bigger in future events such as the Melbourne Cup. Excel is clever enough to automatically update the relative links in the formulas, so you should be able to copy/paste the same formula into each cell as long as you've got your [relative and absolute references straight](https://support.office.com/en-us/article/switch-between-relative-absolute-and-mixed-references-dfec08cd-ae65-4f56-839e-5f0d8d0baca9). 

- **Trigger bet rule:** this is the bet trigger Excel formula we created earlier, and it needs to go in column L (L9 for the first runner).

``` excel tab="Multi line"
=IF(
   AND(
      COUNTIF(RunnerName,B9)>0,
      TimeTillJump3<UserTimeTillJump,
      Overrounds3<UserOverround,
      ISBLANK(InPlay3)),
      INDEX(TIP!A:B,MATCH(B9,RunnerName,0),2),
    ""
)
```

``` excel tab="Single line"
=IF(AND(COUNTIF(RunnerName,B9)>0,TimeTillJump3<UserTimeTillJump,Overrounds3<UserOverround,ISBLANK(InPlay3)),INDEX(TIP!A:B,MATCH(B9,RunnerName,0),2),"")
```

![Automating your tipping with Bet Angel](./img/BetAngelTippingExcel1.png)

- **Odds:** Because we will be taking the BSP, we want to ensure that the initial bets that we place are not matched so that the "TAKE_SP_ALL" command can trigger for the global command. To do this, it checks the bet type for that particular runner. If it is Backing, then place odds at 1000 and if its going to be a lay bet, then set odds at 1.01

!!! info "Note:" 
    The IF statement in both the odds and stake cells is purely to keep our document clean of clutter when there are no runners in column B. A similar effect to IFERROR which we're also using, if Bet Angel hasn't populated cell B9 with a runner name, then dont populate this cell at all. 

```=IFERROR(IF(B9="","",IF(INDEX(TIP!A:B,MATCH(B9,RunnerName,0),2)="LAY",1.01,1000)),"")```

![Automating your tipping with Bet Angel](./img/BetAngelTippingExcel2.png)


- **Stake:** It's completely up to you what staking approach you want to take. We've kept it simple and are using seperate variables for a back bet and lay bet. These variables can be easily changed from the 'SETTINGS' tab. We've got some [good resources on the Hub](https://www.betfair.com.au/hub/education/racing-strategy/staking-and-money-management/) that look at different staking approaches - these might be useful in helping you decide which strategy you want to use. 

```=IFERROR(IF(B9="","",IF(INDEX(TIP!A:B,MATCH(B9,RunnerName,0),2)="BACK", BackStake,LayStake)),"")
```

![Automating your tipping with Bet Angel](./img/BetAngelTippingExcel3.png)


## - Connecting to Bet Angel

### Video walk through

We've put together a litte video walk through to help make this process easier. 

<iframe width="700" height="455" src="https://www.youtube.com/embed/xKfNEpyE3KE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### - Selecting markets

We used the markets menu in the 'Guardian' tool to navigate to Australian tracks that we have ratings for, then multi-selected all the win markets by holding down the control key and clicking on the different markets.

Once you've chosen the races you're interested in, click the 'add' button and you'll see them appear in the main body of the screen. 

Make sure you sort the races **by start time**, so Bet Angel will automatically move through them in the right order and allocate the next race to the spreadsheet once the previous one ends. 

You do this by clicking on the 'start time' column heading until the races are in time order (when the arrow is pointing up). Below is an example of doing this on Australian markets.

![Automating your tipping with Bet Angel](./img/BetAngelRatingsMarketTimes.png)

The Excel spreadsheet used in this tutorial is created in a way that allows it to link multiple markets at the same time. Take a look at the [Betfair automating simultaneous markets tutorial](/automation/betAngelSimultaneousMarkets/) on the hub which will step you through the process so you can take advantage of this feature. 


### - Linking the spreadsheet

Open the 'Excel' tab in 'Guardian', then use the browse functionality to choose the spreadsheet you've been working on. From there, click on 'open workbook', then make sure you have 'connect', 'auto-bind Bet Angel sheets and 'auto-clear Bet Angel bindings' all selected. You also need to make sure that the first race has the 'Bet Angel' tab selected in the 'Excel sheet' column - from there it will then automatically update this for each race as one finishes and the next one begins. 

![Automating your tipping with Bet Angel](./img/BetAngelRatingsSetUp.png)

---
## And you're set!

Once you've set your rules up and got comfortable using Bet Angel Pro it should only take  number of seconds to load the markets up and choose your selections for the day. 

!!! info "Note:" 
    You will need to leave your computer up and running for the duration of the chosen markets, as the program needs the computer to be 'awake' to be able to run.
    
---
## What next? 

We're working through some of the popular automation tools and creating articles like this one to help you learn how to use them to implement different styles of strategies. If you have any thoughts or feedback on this article or other programs you'd like to see us explore please reach out to us at automation@betfair.com.au 

---
## Disclaimer

Note that whilst automated strategies are fun and rewarding to create, we can't promise that your betting strategy will be profitable, and we make no representations in relation to the information on this page. If you're implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred.  Under no circumstances will Betfair be liable for any loss or damage you suffer.