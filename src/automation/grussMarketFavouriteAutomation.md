# Gruss Betting Assistant: Market favourite automation

---
## Automating a market favourite strategy using Gruss Betting Assistant

Here we explore how to implement an automated strategy to place [Betfair Starting Price (BSP)](https://www.betfair.com.au/hub/education/betfair-basics/betfair-starting-price-bsp/) bets on the top two runners in the market. This lets you choose your selections based on market sentiment close to the jump, and not worry about current market price by using BSP to place your bets. You could equally use effectively the same approach if you wanted to lay the favourite(s) instead of backing them.

Building on our [previous articles](../grussRatingsAutomation/), we're using the spreadsheet functionality available in Gruss Betting Assistant to implement this strategy. If you haven't already we'd recommend going back and having a read of [this article](../grussRatingsAutomation/), as the concepts here do build on what we covered previously. As we've said before, there are so many different ways to use this part of Gruss and we're very open to any thoughts about more effective ways of implementing this sort of strategy. You're welcome to reach out to us at automation@betfair.com.au with your feedback and opinions. 

--- 
## - The plan

Given that we're simply choosing our selections based on the market we don't need any ratings for this strategy. The plan is to look at the market a couple of minutes before the scheduled jump and place BSP bets based on its formation. 

Our approach here, and how we've set up the accompanying spreadsheet, backs the top two runners in the market two minutes out from the scheduled start time using the Betfair Starting Price. 

!!! info "Resources"
    - Rules: [here's the spreadsheet](./assets/Gruss_MarketFavAutomation.xlsx) we set up with our macros and rules included, but you'll obviously need to tweak it to suit your strategy and approach
    - Tool: [Gruss Betting Assistant](https://www.gruss-software.co.uk/)

---
### - Set up 

Make sure you've downloaded and installed Gruss, and signed in.

![Automating a market favourite strategy with Gruss](./img/GrussRatingsUI.png)

---
### - Writing your rules

As with any automated strategy, one of the most important steps is deciding what logical approach you want to take and writing rules that suit. 

We're using a [customised version of the default Gruss template Excel sheet](./assets/Gruss_MarketFavAutomation.xlsx) to implement our strategy, so it can make betting decisions based on the favourites being shown in the market. Excel is an excellent tool, but it can take an investment of time to be able to use it effectively. 

This is how we used Excel to implement our set of rules. 


### - Trigger to place bet

In short, we want to back runners when:

- the selection's available to back price (Column F) is either the lowest or second lowest in the market - the top two market favourites with the ability to easily change this
- the scheduled event start time is less and greater than what we specify
- Back market percentage is less than a certain value that we choose
- the event isn't in play 

### - Using cell references to simplify formulas

Throughout this tutorial, we'll be referencing certain cells with custom names that will make it easier to understand and follow the formulas as we progress. This is an especially effective method to
keep on top of more complex strategies that require long formaulas to implement.
 
!!! info "Cell names used in this tutorial"

    - **Fav** refers to cell C5 in the 'SETTINGS' worksheet

    - **Overrounds1, Overrounds2 and Overrounds3** refers to cell Y4 in the 'MARKET', 'MARKET 2' and 'MARKET 3' worksheets repectively, where the overrounds are calculated. Each worksheet needs to contain their own formula calculations as they will each be working off different markets

    - **UserOverround** refers to cell C4 in the 'SETTINGS' worksheet which allows you to change a single value that will automatically update the formulas for all runners

    - **TimeTillJump1, TimeTillJump2 and TimeTillJump3** refers to cell C9, C10 and C11 in the 'SETTINGS' worksheet respectively. Just like the overrounds, each worksheet needs their own TimeTillJump calculation - one for each market

    - **MinTime** refers to cell C3 in the 'SETTINGS' worksheet which allows you to change a single value that will automatically update the formulas for all runners

    - **MaxTime** refers to cell E3 in the 'SETTINGS' worksheet which allows you to change a single value that will automatically update the formulas for all runners

    - **InPlay1, InPlay2, InPlay3** refers to cell E2 in the 'MARKET', 'MARKET 2' and 'MARKET 3' worksheets respectively. Gruss will populate a status in these worksheet cells such as "Not in Play" for each market

    - **MarketStatus1, MarketStatus2, MarketStatus3** refers to cell F2 in the 'MARKET', 'MARKET 2' and 'MARKET 3' worksheets respectively. Gruss will populate a status in these worksheet cells such as "Suspended" for each market


**This is our trigger on Excel formula:**

``` excel tab="Multi line"
=IF(
    AND(
        (COUNT($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50)
        -RANK(F5,($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50))+1) < Fav+1,
        TimeTillJump1 < MaxTime,
        TimeTillJump1 > MinTime,
        Overrounds1<UserOverrounds,
        InPlay1="Not In Play",
        MarketStatus1<>"Suspended"),
    "BACK-SP",
    "")
```

``` excel tab="Single line"
=IF(
    AND(
        (COUNT($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50)-RANK(F5,($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50))+1) < Fav+1,TimeTillJump1 < MaxTime,TimeTillJump1 > MinTime,Overrounds1<UserOverrounds,InPlay1="Not In Play",MarketStatus1<>"Suspended"),"BACK-SP","")

```

Stepping through each step:

- **Finding the top two selections in the market:** check each runner to see if they're one of the two market favourites - We're doing this by going through the best available to back (column F) price for each runner, ranking them in order (which sorts them from highest to lowest - which is the opposite of what we want) then subtracting that rank number from the total number of selections available to inverse the order. Finally, we plus one to the resulting rank - if we didn't do this then you'd have a rank order that started at 0, not 1, and we thought that would just confuse matters!

Once it's established what each selection's rank is, we then check if that rank is less than three, and if it is we know that the runner in question is one of the top two in the market, based on the current available to back prices.

``` excel hl_lines="3 4"
=IF(
    AND(
        (COUNT($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50)
        -RANK(F5,($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50))+1) < Fav+1,
        TimeTillJump1 < MaxTime,
        TimeTillJump1 > MinTime,
        Overrounds1<UserOverrounds,
        InPlay1="Not In Play",
        MarketStatus1<>"Suspended"),
    "BACK-SP",
    "")
```

- **TimeTillJump1 < MaxTime and > MinTime:** check whether the seconds left on the countdown are smaller than what is defined in cell C3 and greater than cell E3 in the 'SETTINGS' worksheet (named 'MinTime' and 'MaxTime' respectively). This one's a bit complicated, as the time is actually returned as a percentage of a 24 hour day, which you need to convert into positive or negative seconds. We'll keep it simple by referencing the value in cell C9 (named 'TimeTillJump1') in the 'SETTINGS' worksheet, where we've already done the calculations for you.

``` excel hl_lines="5 6"
=IF(
    AND(
        (COUNT($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50)
        -RANK(F5,($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50))+1) < Fav+1,
        TimeTillJump1 < MaxTime,
        TimeTillJump1 > MinTime,
        Overrounds1<UserOverrounds,
        InPlay1="Not In Play",
        MarketStatus1<>"Suspended"),
    "BACK-SP",
    "")
```

- **Overrounds1 < UserOverrounds:** checking whether the market overrounds are less than the specific value that is specified in cell C4 of the 'SETTINGS' worksheet

``` excel hl_lines="7"
=IF(
    AND(
        (COUNT($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50)
        -RANK(F5,($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50))+1) < Fav+1,
        TimeTillJump1 < MaxTime,
        TimeTillJump1 > MinTime,
        Overrounds1<UserOverrounds,
        InPlay1="Not In Play",
        MarketStatus1<>"Suspended"),
    "BACK-SP",
    "")
```

- **InPlay1:** checking whether the event has gone in play, as this is purely a pre-play strategy, though you could certainly take a similar approach to in-play markets. InPlay refers to E2 in the 'MARKET' worksheet, if this cell displays "Not In Play" as a value, it's safe to place bets. 

``` excel hl_lines="8"
=IF(
    AND(
        (COUNT($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50)
        -RANK(F5,($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50))+1) < Fav+1,
        TimeTillJump1 < MaxTime,
        TimeTillJump1 > MinTime,
        Overrounds1<UserOverrounds,
        InPlay1="Not In Play",
        MarketStatus1<>"Suspended"),
    "BACK-SP",
    "")
```

- **MarketStatus1:** checks whether the event is suspended, by checking if Gruss has populated cell F2 in the "MARKET" worksheet with "Suspended". If the cell has any other value, it's safe to place bets. 

``` excel hl_lines="9"
=IF(
    AND(
        (COUNT($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50)
        -RANK(F5,($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50))+1) < Fav+1,
        TimeTillJump1 < MaxTime,
        TimeTillJump1 > MinTime,
        Overrounds1<UserOverrounds,
        InPlay1="Not In Play",
        MarketStatus1<>"Suspended"),
    "BACK-SP",
    "")
```

- **Result:** if the statement above is true, the formula returns 'BACK-SP', at which point the bet will trigger, taking BSP. If any of the previous conditions are not met, then no bet will be placed and the cell will remin blank. 

``` excel hl_lines="10 11"
=IF(
    AND(
        (COUNT($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50)
        -RANK(F5,($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50))+1) < Fav+1,
        TimeTillJump1 < MaxTime,
        TimeTillJump1 > MinTime,
        Overrounds1<UserOverrounds,
        InPlay1="Not In Play",
        MarketStatus1<>"Suspended"),
    "BACK-SP",
    "")
```

!!! info "updating the trigger for 'MARKET 2' and 'MARKET 3' worksheets"

     You will need to ensure that the reference names for Overrounds, TimeTillJump and InPlay are changed so that they are referencing the cells that are applicable for those specific worksheets. Forgetting to do this can lead to the automation working off information from the wrong market.  


- **Trigger for 'MARKET 2' worksheet:** Note that Overrounds has been changed to Overrounds2, TimeTillJump1 to TimeTillJump2 and InPlay1 to InPlay2

``` excel hl_lines="5 6 7 8 9"
=IF(
    AND(
        (COUNT($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50)
        -RANK(F5,($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50))+1) < Fav+1,
        TimeTillJump2 < MaxTime,
        TimeTillJump2 > MinTime,
        Overrounds2<UserOverrounds,
        InPlay2="Not In Play",
        MarketStatus2<>"Suspended"),
    "BACK-SP",
    "")
```

- **Trigger for 'MARKET 3' worksheet:** Note that Overrounds has been changed to Overrounds3, TimeTillJump1 to TimeTillJump3 and InPlay1 to InPlay3

``` excel hl_lines="5 6 7 8 9"
=IF(
    AND(
        (COUNT($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50)
        -RANK(F5,($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50))+1) < Fav+1,
        TimeTillJump3 < MaxTime,
        TimeTillJump3 > MinTime,
        Overrounds3<UserOverrounds,
        InPlay3="Not In Play",
        MarketStatus3<>"Suspended"),
    "BACK-SP",
    "")
```     

!!! info "Excel functions"

    - [IF function:](https://support.office.com/en-us/article/if-function-69aed7c9-4e8a-4755-a9bc-aa8bbff73be2) IF(if this is true, do this, else do this)
    - [AND function:](https://support.office.com/en-us/article/and-function-5f19b2e8-e1df-4408-897a-ce285a19e9d9) AND(this is true, and so is this, and so is this) - returns true or false
    - [COUNT function:](https://support.office.com/en-us/article/count-function-a59cd7fc-b623-4d93-87a4-d23bf411294c) returns number of cells in the range you pass in tha contain a number
    - [RANK function:](https://support.office.com/en-us/article/rank-function-6a2fc49d-1831-4a03-9d8c-c279cf99f723) returns the rank of a number in a list of numbers, with the smallest number returning the highest rank.
    - [Absolute references:](https://support.office.com/en-us/article/switch-between-relative-absolute-and-mixed-references-dfec08cd-ae65-4f56-839e-5f0d8d0baca9) if you're copy/pasting formulas it's important that you make links absolute when you don't want the cell being referenced to change relative to the new cell the formula is being pasted into. You do this by putting a $ in front of the parts of the reference you don't want to 'move'. 

---
### - Preparing the spreadsheet

You need to copy/paste this formula into the relevant cells for each of the runners. Excel is clever enough to automatically update the relative links in the formulas, so you should be able to copy/paste the same formula into each cell as long as you've got your [relative and absolute references straight](https://support.office.com/en-us/article/switch-between-relative-absolute-and-mixed-references-dfec08cd-ae65-4f56-839e-5f0d8d0baca9). 

- **Trigger bet rule:** this is the bet trigger Excel formula we created earlier, and it needs to go in column Q (Q5 for the first runner).

``` excel tab="Multi line"
=IF(
    AND(
        (COUNT($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50)
        -RANK(F5,($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50))+1) < Fav+1,
        TimeTillJump1 < MaxTime,
        TimeTillJump1 > MinTime,
        Overrounds1<UserOverrounds,
        InPlay1="Not In Play",
        MarketStatus1<>"Suspended"),
    "BACK-SP",
    "")
```

``` excel tab="Single line"
=IF(AND((COUNT($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50)-RANK(F5,($F$5,$F$6,$F$7,$F$8,$F$9,$F$10,$F$11,$F$12,$F$13,$F$14,$F$15,$F$16,$F$17,$F$18,$F$19,$F$20,$F$21,$F$22,$F$23,$F$24,$F$25,$F$26,$F$27,$F$28,$F$29,$F$30,$F$31,$F$32,$F$33,$F$34,$F$35,$F$36,$F$37,$F$38,$F$39,$F$40,$F$41,$F$42,$F$43,$F$44,$F$45,$F$46,$F$47,$F$48,$F$49,$F$50))+1) < Fav+1,TimeTillJump1 < MaxTime,TimeTillJump1 > MinTime,Overrounds1<UserOverrounds,InPlay1="Not In Play",MarketStatus1<>"Suspended"),"BACK-SP","")
```

![Automating a market favourite strategy with Gruss](./img/GrussMarketFav1.png)

- **Odds:** as we said we're putting the bet up initially at odds of 1000, so this is a simple one. 

!!! info "Note:" 
    The IF statement in both the odds and stake cells is purely to keep our document clean of clutter when there are no runners in column A. A similar effect to IFERROR, if Gruss hasn't populated cell A5 with a runner name, then dont populate this cell at all.

```=IF(A5="","","1000")```

![Automating a market favourite strategy with Gruss](./img/GrussMarketFav2.png)

- **Stake:** it's completely up to you what staking approach you want to take. We're keeping it simple and using flat stake here, so will just place $10 on each runner. This goes in column S (S5 for the first runner). We've got some [good resources on the Hub](https://www.betfair.com.au/hub/education/racing-strategy/staking-and-money-management/) that look at different staking approaches - these might be useful in helping you decide which strategy you want to use. 

```=IF(A5="","",stake)```

![Automating a market favourite strategy with Gruss](./img/GrussMarketFav3.png)

---
### - You know the drill

The process is effectively the same from here on as for our previously automated strategy, but we've included it here just in case you want a refresher or are new to Gruss.

---
### - Selecting markets

Gruss makes it really easy to select markets in bulk. You could go through an add each market individually, but it's much easier to just use the quick pick functionality to add all Australian racing win markets. 

![Automating a market favourite strategy with Gruss](./img/GrussRatingsMarkets.png)

You also need to make sure you set it up so that the program will automatically move on to the next market, when the previous one jumps.

![Automating a market favourite strategy with Gruss](./img/GrussRatingsMarkets2.png)

---
### - Linking the spreadsheet

This is a little tricky the first time, but easy once you know how. Make sure you have the [Excel sheet](./assets/Gruss_RatingsAutomation.xlsx) saved to your local computer - when we tried using a file we had saved in OneDrive it simply didn't work. Open the Excel sheet, then click on Excel/Log current prices. 

![Automating a market favourite strategy with Gruss](./img/GrussRatingsLinkingExcel.png)

It will autofill the workbook and sheet names. You'll then need to make sure you tick:

- Enable triggered betting
- Clear Bet refs on auto select market
- Quick pick reload triggers select first market

Then click OK and the sheet with be linked with the program. 

![Automating a market favourite strategy with Gruss](./img/GrussRatingsLinkingExcel2.PNG)

---
## And you're set!

Once you've set your spreadsheet set up and you're comfortable using Gruss Betting Assistant it should only take a number of seconds to load your markets and set your strategy running for the day. Just make sure you have all of the app settings correctly selected before you leave the bot to run, as some of them reset by default when you turn the program off.

!!! info "Note:" 
    you will need to leave your computer up and running for the duration of the chosen markets, as the program needs the computer to be 'awake' to be able to run.
    
---
## Areas for improvement

There are parts of this approach that we're still trying to get to work to our liking, and we'll update this article as we find better solutions. If you have any suggestions for improvements please reach out to automation@betfair.com.au - we'd love to hear your thoughts. 

For example, the spreadsheet only binds with one market at a time, so if one market gets delayed and runs overtime the program won't be able to move on to the next market - we missed some races because of this. 

---
## What next? 

We're working through some of the popular automation tools and creating articles like this one to help you learn how to use them to implement different styles of strategies. If you have any thoughts or feedback on this article or other programs you'd like to see us explore please reach out to automation@betfair.com.au - this article has already been updated with extra learnings including variable percentages and new macros.

---
## Disclaimer

Note that whilst automated strategies are fun and rewarding to create, we can't promise that your betting strategy will be profitable, and we make no representations in relation to the information on this page. If you're implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred.  Under no circumstances will Betfair be liable for any loss or damage you suffer.