# How does a Data Scientist model the Brownlow?

This article has been written by Liam from [Crow Data Science](https://www.crowdatascience.com/) for the [Betfair 2024 AFL Brownlow Medal Datathon](../modelling/BrownlowMedal2024Datathon.md).
You can chat with Liam in the [Betfair Quants Discord Server](https://forms.office.com/r/ZG9ea1xQj1) or on Twitter/X (@crow_data_sigh)

---

## Intro

The Brownlow Medal is the AFL’s most prestigious individual award. The pinnacle of achievement in Australian Rules Football, awarded to the ‘Best and Fairest’ of a home and away season. 

Each game, the umpires award a total of 6 votes to the players they judge to be best afield:

 - 3 votes to the best player
 - 2 votes to the 2nd best player
 - 1 vote to the 3rd best player
 
In 2024, each game featured at most 46 players (23 from each team), with only 3 of those players able to receive votes.

Just as the game has evolved in terms of game style and tactics over the last century, so has the way umpires adjudicate worthy Brownlow vote recipients. 

**How have umpires changed the way they vote? What are the metrics most predictive of votes?**

## Disposals

A disposal is the basic currency of footy stats, the first statistic that pundits and fans alike point to as a source of how well a player performed. Rudimentary sure, but a stat with a lot of historical data. 

**Do umpires hold the same view, more disposals means better player? Have there been any noticeable trends in voting patterns?**

In 2023, the average player polling a vote had 25.5 disposals, while players polling no votes averaged 15.1 disposals per game.

![png](../img/avgDisposalsBrownlowVotes.png)

There does seem to be an increase in the amount of disposals needed to poll votes, but this seems to be in line with the general increase in average disposals per player. 

We can visualise this as a percentage increase on the AFL average for that season.

![png](../img/percentageDiffDisposalsBrownlowVotes.png)

The period between 1995 to 2005 saw high disposal players take the lion's share of the votes, similar to the modern era from 2010 and peaking in 2022. Players polling 3 votes in 2021 achieved an average of 30.18 disposals while the average per player was 15.88 disposals, an increase of 90% on the AFL average, the peak difference seen with available data.

Players that generate these types of high disposal games are overwhelmingly midfielders, which leads to accusation that the Brownlow medal has “become” a midfielders award. I’d argue that it’s almost always been a midfielders award. The more you possess and dispose of the ball, the more times the umpires sees you which can lead to more votes being awarded.

**How does the distribution of disposals for the 2023 season look?**

![png](../img/distDisposalsBrownlowVotes.png)

The spread of votes across disposal counts is quite wide. Quite a few cases where players with less than 20 disposals recorded votes. Of the 373 players to claim 30+ disposals in a game, only 50% of players polled any votes in 2023. Players with 40+ disposals polled votes 76% of the time, of which 69% polled 3 votes in 2023.

## AFL Player Ratings

Disposals are quite a simple metric so let’s look at one of the more advanced metrics, AFL PR. This metric takes into account actions undertaken by players and what that action resulted in. Players get points for completing high equity plays, such as intercepting the ball in a dangerous position or turning a contested ball into a possession for a teammate. Players generally average 9 AFL PR points per game, with elite players generating 20 or more points in a game. 

**How well does this metric inform Brownlow Votes?**

![png](../img/distPlayerRatingBrownlowVotes.png)

AFL PR does a good job at separating the non-polling from the polling players better than disposals. While disposals are a good measure of how much a player is around the ball, the stat doesn’t capture how well the player used the ball. In 2023, of the 1335 players to have better than 15 PR points, 28% of them received a vote. Players with more than 20 PR points polled votes 48% of the time, of which 21% polled 3 votes. Players with 26 PR points were nearly odds on to poll 3 votes at 48% of the time (13% 2 votes, 16% 1 vote, 20% 0 votes).

**Have umpires changed the way they adjudicate players?**

We can look at the average rating points per voting outcome over time. Data is available from 2012 onwards.

![png](../img/avgPlayerRatingBrownlowVotes.png)

There doesn’t seem to be a noticeable trend when either looking at a basic stat like disposals or an advanced stat like Player Ratings. It is comforting to see a clear distinction between 3, 2 and 1 votes which implies that field umpires do understand which players have been best on ground (to at least some degree) and that it’s not just a random sample of top players.

## AFL Fantasy and SuperCoach Points

The metrics of AFL Fantasy (AF) and SuperCoach (SC) are probably the most used statistics used to evaluate a player's performance. AF is a linear combination of 9 match statistics, each assigned a value which is then summed to give a player their final score. SC is similar to the previously mentioned AFL player ratings, using a basic equity model on actions in game. SC also uses a match scaling method, ensuring that an equal number of points are assigned every game. 

**How well do these metrics inform Brownlow Votes?**

![png](../img/supercoachBrownlowVotes.png)

SC and AF provide some good separation, 50+ AF and 50+ SC are good cutoffs that capture most of the polling. However, it’s still difficult to accurately separate out the polling votes. Just looking at the polling players and layering the dot points over each other, the following graph shows the difficulty at teasing the groups apart.

![png](../img/superCoachFantasyPoints.png)

Looking back at the previous density plots, this isn’t a problem exclusive to AF and SC. While the means in each group of votes may be higher, there is significant overlap in the distributions of the target variables, like disposals and Player Ratings.

## Coaches Votes

The Brownlow is an opinionated vote, and what better feature to analyse than more opinions! At the conclusion of each game, the coaches of each team name their top 5 players, with the best on ground getting 5 votes and fifth best getting 1 vote. The votes are then combined from the 2 opposing coaches, the highest possible votes for a player being 10. Let’s see how well Coaches Votes (CV) inform Brownlow Votes.

![png](../img/avgCoachesVotesBrownlowVotes.png)

CV gives us the biggest separation we’ve seen among the statistics we’ve seen today. Coaches and umpires do seem to be aligned on the “best on ground” decision; players receiving 10CV polled 3 votes 67% of the time over the last decade (933 players).

The following table displays this correlation.

![png](../img/convertingCoachesVotes.png)

Coaches Votes are by far the best indicator of Brownlow Votes. 10 Vote players imply that both coaches thought this player was best on ground and it seems that the umpires also tend to agree.

## Interactions

Interactions are a fundamental part of modelling, a way to effectively combine features to better predict outcomes. If you’re using a linear model, you’ll need to specify which features you want to interact, while an ML technique like XGBoost will handle this for you with the right hyperparameters set. Another option is to create your features as a combination of features, commonly called **“feature engineering”.**

Let’s look at the interaction between the 2 most important features, Coaches Votes and Fantasy Points.

![png](../img/groupingCoachesVotesFantasyPoints.png)

The interaction between AF and CV reveals quite a lot about how votes can be distributed. Players with low Coaches Votes can poll votes with high enough Fantasy score, implying that the amount of actions a player is involved in can influence umpires. On the contrary, a high Coaches Votes tally and middling Fantasy score can result in being awarded Votes. These two features are just one example of an interaction that works well due to the metrics being somewhat uncorrelated. One is an in-game counting metric, the other is an opinion and this juxtaposition works great when combined.

This is just one example of an interaction, no doubt there's many more that yield similar and varied insights.

## Notes and Additional Features

For those unfamiliar with Aussie Rules Football, the 2020 season featured shortened game lengths, with each quarter being played for 16 minutes. You can either exclude the 2020 season or scale up certain metrics by 25% returning the quarter lengths to the standard 20 minutes.

Since votes are awarded on a per game basis, it makes sense to scale numerical features per game. If 10 players all have over 30 disposals, how does the umpire (or model) pick out a potential winner (other than using other statistics)? Scaling so that the metric centres on 0 with a standard deviation of 1 can help the model find significant differences from the mean, as outlined in the first graph. Players with 75% more than the average are more likely to poll votes, and it makes sense to exploit these facts.

Other features I’d recommend investigating include:

 - Goals. Players with 5+ goals poll 3 votes 38% of the time, rises to 84% with 7+ goals.
 - Margin, team score and opponent score. The winning team polls 7% more than losing teams.
 - Contested Possessions. Players with 20+ Cont Poss poll votes 68% of the time.
 - Kicks. Players with 25+ kicks poll votes 60% of the time.

I’ve built my Brownlow medal model using 80+ features trained on an XGBoost classification model. 

After training on 2012 to 2023 data, these are the top 7 most important features according to my Brownlow Medal model:

    1.	Coaches Votes
    2.	Fantasy Points
    3.	SuperCoach Points
    4.	Disposals
    5.	Rating Points
    6.	Goals
    7.	Margin

## Final Thoughts

The Brownlow Medal presents a very tough modelling problem, and for those participating in the Betfair Datathon, I wish you the best of luck! 

You can follow my predictions and insights as @crow_data_sigh on twitter, and in the #Datathon channel in the [Betfair Quants Discord Server](https://forms.office.com/r/ZG9ea1xQj1).

---

### Disclaimer (Betfair Team)

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.
