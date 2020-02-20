
![Automating a ratings based strategy with Bet Angel](./img/Elo.jpg)

--- 
## - What is Elo?

 The Elo rating system was orginally created by Hungarian born physics professor Arpad Elo who was a chess master and competed within the United States Chess Federation (USCF) and developed the system as an alternative to other rating systems that were considered to be inaccurate. Rather than rating a players performance by their overall wins and losses like previous systems, the Elo rating system works by assigning each player or team an Elo rating. When a team or player beats another, the winning side gains a portion of the losing sides points. This difference between Elo ratings between competitors is then used to create a probability for a particular outcome.

 The Elo rating system has become so popular since its inception, it is widely used today behind the scenes for a range of applications such as dating websites to determince compatibility between matches and even video game tournaments to ensure players of a similar skill level are matched together.        




## - How does Elo work?

For the purpose of this explanation, we'll be using Elo in the context of rating AFL teams. Each team begins with an Elo rating of 1500 and will gain or lose a portion of their Elo from / to the opposite team depending if they win or lose a game. For example, if team A has 1500 Elo and they beat team B - who also started with a 1500 Elo, then a certain portion of Elo (usually 30) is deducted from the loser and awarded to the winner. In this scenario, Team A will have an Elo rating of 1530 and Team B will be left with 1470. What makes Elo great for betting in sports is that it can be converted to a probability which in turn can be converted into odds used to place bets.  

---

## - The Algorithm

Each team will have their own Elo rating which will be determined based on their historical performance. If a team has never played a game, then they will begin with an Elo rating of 1500. The following formula is used to calculate the probability of a win for each team: 

![Automating a ratings based strategy with Bet Angel](./img/EloFormula1.jpg)

A crucial consideration of any Elo rating system is the implementation of what is known as the K-factor. This determines the "sensitivity" how much of an impact a win or a loss has on a teams Elo rating. A good K-factor is generally around 32 but this can be adjusted to suit. 

Once the match has been concluded, each teams Elo is then updated to reflect any changes to their Elo rating, taking into account the full sequence of wins and loses up to the most recent match played. For this, the below formula is used:

![Automating a ratings based strategy with Bet Angel](./img/EloFormula2.jpg)

Where **elo_i (t+1)** is the updated Elo, **elo_i (t)** was their Elo before the match, **K** is the K-factor mentioned before (which we determined to be 32), **outcome** is an indicator of the match outcome (1 if it was won by team A, 0 if a loss), and **Pwin** was the pre-match probability of winning for team A, as given by the previous formula.

If two teams play their first match, both with Elo of 1500, **Pwin** is equal to 0.5 so, for a K-factor of 32, the winning team would gain 16 points and the losing team would lose 16 points. In their next match, the teams start with Elo ratings of 1,516 and 1,484 respectively, and by updating their rating for all matches played, their current Elo rating can be calculated.

---

## - Taking Elo to the next level

If you're interested in learning more about Elo and implementing a dynamic K-factor instead of a static one for greater accuracy, check out the article we've created in the Betfair Hub which applies [Elo in the context of modelling tennis](https://www.betfair.com.au/hub/tennis-elo-modelling/). Doing so can bring greater accuracy, especially when applied to the AFL season as the K-factor can be set to change depending on the importance of a particular match such as finals and early / late season games. 

---

!!! info "Resources"
    - Learn more about the origins of Elo by visiting the [Elo Wikipedia page](https://en.wikipedia.org/wiki/Elo_rating_system#History)
    - Take a look at the [Elo Tennis model article on the Betfair Hub](https://www.betfair.com.au/hub/tennis-elo-modelling/)
    - Here's another good resource to help gain a better understanding of how Elo works and is applied: [The Math behind Elo](https://blog.mackie.io/the-elo-algorithm)
    
---

## Disclaimer

Note that whilst automated strategies are fun and rewarding to create, we can't promise that your betting strategy will be profitable, and we make no representations in relation to the information on this page. If you're implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred.  Under no circumstances will Betfair be liable for any loss or damage you suffer.