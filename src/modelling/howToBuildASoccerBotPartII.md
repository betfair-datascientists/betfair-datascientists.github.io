# How To Build A Betfair Soccer Bot Part 2

This is a continuation of the tutorial - [How To Build A Betfair Soccer Bot Part 1](../modelling/howToBuildASoccerBotPartI.md)

**"I've trained a model, but how can I use it to bet with?"**

This is an example of what we predicted in the previous tutorial

```
{date_home':'2022-08-13',
'match_id':'221827',
'name_home':'Arsenal',
'name_away':'Leicester',
'goalsScored_home':'4',
'goalsScored_away':'2',
'halfTimeGoalsScored_home':'2',
'halfTimeGoalsScored_away':'0',
'home_0_x_away_0':'0.0615',
'home_0_x_away_1':'0.0573',
'home_0_x_away_2':'0.0256',
'home_0_x_away_3':'0.0092',
'home_0_x_away_4':'0.0016',
'home_0_x_away_5':'0.0004',
'home_0_x_away_6':'0.0003',
'home_0_x_away_7':'0',
'home_1_x_away_0':'0.1152',
'home_1_x_away_1':'0.1074',
'home_1_x_away_2':'0.0479',
'home_1_x_away_3':'0.0172',
'home_1_x_away_4':'0.003',
'home_1_x_away_5':'0.0008',
'home_1_x_away_6':'0.0006',
'home_1_x_away_7':'0',
'home_2_x_away_0':'0.1132',
'home_2_x_away_1':'0.1054',
'home_2_x_away_2':'0.0471',
'home_2_x_away_3':'0.0169',
'home_2_x_away_4':'0.0029',
'home_2_x_away_5':'0.0008',
'home_2_x_away_6':'0.0006',
'home_2_x_away_7':'0',
'home_3_x_away_0':'0.0545',
'home_3_x_away_1':'0.0508',
'home_3_x_away_2':'0.0227',
'home_3_x_away_3':'0.0081',
'home_3_x_away_4':'0.0014',
'home_3_x_away_5':'0.0004',
'home_3_x_away_6':'0.0003',
'home_3_x_away_7':'0',
'home_4_x_away_0':'0.0388',
'home_4_x_away_1':'0.0362',
'home_4_x_away_2':'0.0161',
'home_4_x_away_3':'0.0058',
'home_4_x_away_4':'0.001',
'home_4_x_away_5':'0.0003',
'home_4_x_away_6':'0.0002',
'home_4_x_away_7':'0',
'home_5_x_away_0':'0.0083',
'home_5_x_away_1':'0.0077',
'home_5_x_away_2':'0.0034',
'home_5_x_away_3':'0.0012',
'home_5_x_away_4':'0.0002',
'home_5_x_away_5':'0.0001',
'home_5_x_away_6':'0',
'home_5_x_away_7':'0',
'home_6_x_away_0':'0.0024',
'home_6_x_away_1':'0.0022',
'home_6_x_away_2':'0.001',
'home_6_x_away_3':'0.0004',
'home_6_x_away_4':'0.0001',
'home_6_x_away_5':'0',
'home_6_x_away_6':'0',
'home_6_x_away_7':'0',
'home_7_x_away_0':'0.0004',
'home_7_x_away_1':'0.0004',
'home_7_x_away_2':'0.0002',
'home_7_x_away_3':'0.0001',
'home_7_x_away_4':'0',
'home_7_x_away_5':'0',
'home_7_x_away_6':'0',
'home_7_x_away_7':'0',
'home_0_ht_x_away_0_ht':'0.311',
'home_0_ht_x_away_1_ht':'0.115',
'home_0_ht_x_away_2_ht':'0.0213',
'home_0_ht_x_away_3_ht':'0.0115',
'home_0_ht_x_away_4_ht':'0.0002',
'home_0_ht_x_away_5_ht':'0',
'home_1_ht_x_away_0_ht':'0.2309',
'home_1_ht_x_away_1_ht':'0.0854',
'home_1_ht_x_away_2_ht':'0.0158',
'home_1_ht_x_away_3_ht':'0.0085',
'home_1_ht_x_away_4_ht':'0.0002',
'home_1_ht_x_away_5_ht':'0',
'home_2_ht_x_away_0_ht':'0.1158',
'home_2_ht_x_away_1_ht':'0.0428',
'home_2_ht_x_away_2_ht':'0.0079',
'home_2_ht_x_away_3_ht':'0.0043',
'home_2_ht_x_away_4_ht':'0.0001',
'home_2_ht_x_away_5_ht':'0',
'home_3_ht_x_away_0_ht':'0.0174',
'home_3_ht_x_away_1_ht':'0.0064',
'home_3_ht_x_away_2_ht':'0.0012',
'home_3_ht_x_away_3_ht':'0.0006',
'home_3_ht_x_away_4_ht':'0',
'home_3_ht_x_away_5_ht':'0',
'home_4_ht_x_away_0_ht':'0.0023',
'home_4_ht_x_away_1_ht':'0.0009',
'home_4_ht_x_away_2_ht':'0.0002',
'home_4_ht_x_away_3_ht':'0.0001',
'home_4_ht_x_away_4_ht':'0',
'home_4_ht_x_away_5_ht':'0',
'home_5_ht_x_away_0_ht':'0.0001',
'home_5_ht_x_away_1_ht':'0',
'home_5_ht_x_away_2_ht':'0',
'home_5_ht_x_away_3_ht':'0',
'home_5_ht_x_away_4_ht':'0',
'home_5_ht_x_away_5_ht':'0',
}
```

While we might directly be able to use these values for Correct Score markets, they're overall not that useful for other markets. We could certainly manually figure them out for upcoming matches but to run a back test on two seasons worth of data, we certainly don't want to be doing this manually for 748 matches. So let's run through how we turn this into something more useful!

## Creating Rated Prices

Now that we've trained our model and calculated the probability for each unique scoreline possible for both full-time and half-time outcomes, we'll need to do some additional processing to be able to use these probabilities to bet into the Betfair markets. The next code block will take our model outputs and create rated prices for a selection of markets from the exchange. 

This isn't an exhaustive list but it gives an idea of the type of calculation required to transition between modelling and betting.

---

The next block of code assumes that all required modules have already been imported

```py title="Define our markets"

df=pd.read_csv('ensemble_model_results.csv')

'''
The below code will calculate probabilities for each individual market and selection for most markets related to goals scored/conceded
The new column name takes the format that matches the exchange 'marketName_selectionName'
'''

# Both Teams To Score
df['Both Teams To Score?_Yes'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i > 0 and j > 0]].sum(axis=1)
df['Both Teams To Score?_No'] = 1 - df['Both Teams To Score?_Yes']

# Match Odds
df['Match Odds_Home'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i > j]].sum(axis=1)
df['Match Odds_The Draw'] = df[[f'home_{i}_x_away_{i}' for i in full_time_indices]].sum(axis=1)
df['Match Odds_Away'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i < j]].sum(axis=1)

# Draw No Bet - This is equivalent to match odds normalised after removal of the Draw probability (In the event of a draw, the market is voided)
df['Draw No Bet_Home'] = df['Match Odds_Home'] / (1 - df['Match Odds_The Draw'])
df['Draw No Bet_Away'] = df['Match Odds_Away'] / (1 - df['Match Odds_The Draw'])

# Double Chance - This is a 2 winner market and has a market percentage of 200%
df['Double Chance_Home Or Away'] = df['Match Odds_Home'] + df['Match Odds_Away']
df['Double Chance_Home Or Draw'] = df['Match Odds_Home'] + df['Match Odds_The Draw']
df['Double Chance_Draw Or Away'] = df['Match Odds_The Draw'] + df['Match Odds_Away']

# Match Odds & Both Teams to Score
df['Match Odds And Both Teams To Score_Home/Yes'] = df['Match Odds_Home'] * df['Both Teams To Score?_Yes']
df['Match Odds And Both Teams To Score_Home/No'] = df['Match Odds_Home'] * df['Both Teams To Score?_No']
df['Match Odds And Both Teams To Score_Draw/Yes'] = df['Match Odds_The Draw'] * df['Both Teams To Score?_Yes']
df['Match Odds And Both Teams To Score_Draw/No'] = df['Match Odds_The Draw'] * df['Both Teams To Score?_No']
df['Match Odds And Both Teams To Score_Away/Yes'] = df['Match Odds_Away'] * df['Both Teams To Score?_Yes']
df['Match Odds And Both Teams To Score_Away/No'] = df['Match Odds_Away'] * df['Both Teams To Score?_No']

# Correct Score
df['Correct Score_0 - 0'] = df['home_0_x_away_0']
df['Correct Score_0 - 1'] = df['home_0_x_away_1']
df['Correct Score_0 - 2'] = df['home_0_x_away_2']
df['Correct Score_0 - 3'] = df['home_0_x_away_3']
df['Correct Score_1 - 0'] = df['home_1_x_away_0']
df['Correct Score_1 - 1'] = df['home_1_x_away_1']
df['Correct Score_1 - 2'] = df['home_1_x_away_2']
df['Correct Score_1 - 3'] = df['home_1_x_away_3']
df['Correct Score_2 - 0'] = df['home_2_x_away_0']
df['Correct Score_2 - 1'] = df['home_2_x_away_1']
df['Correct Score_2 - 2'] = df['home_2_x_away_2']
df['Correct Score_2 - 3'] = df['home_2_x_away_3']
df['Correct Score_3 - 0'] = df['home_3_x_away_0']
df['Correct Score_3 - 1'] = df['home_3_x_away_1'] 
df['Correct Score_3 - 2'] = df['home_3_x_away_2']
df['Correct Score_3 - 3'] = df['home_3_x_away_3']
df['Correct Score_Any Other Home Win'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i > 3 and i > j]].sum(axis=1)
df['Correct Score_Any Other Draw'] = df[[f'home_{i}_x_away_{i}' for i in full_time_indices if i > 3]].sum(axis=1)
df['Correct Score_Any Other Away Win'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if j > 3 and j > i]].sum(axis=1)

# Over/Under 5.5 Goals
df['Over/Under 5.5 Goals_Over 5.5 Goals'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if (i + j) > 5.5]].sum(axis=1)
df['Over/Under 5.5 Goals_Under 5.5 Goals'] = 1 - df['Over/Under 5.5 Goals_Over 5.5 Goals']

# Over/Under 4.5 Goals
df['Over/Under 4.5 Goals_Over 4.5 Goals'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if (i + j) > 4.5]].sum(axis=1)
df['Over/Under 4.5 Goals_Under 4.5 Goals'] = 1 - df['Over/Under 4.5 Goals_Over 4.5 Goals']

# Over/Under 3.5 Goals
df['Over/Under 3.5 Goals_Over 3.5 Goals'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if (i + j) > 3.5]].sum(axis=1)
df['Over/Under 3.5 Goals_Under 3.5 Goals'] = 1 - df['Over/Under 3.5 Goals_Over 3.5 Goals']

# Over/Under 2.5 Goals
df['Over/Under 2.5 Goals_Over 2.5 Goals'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if (i + j) > 2.5]].sum(axis=1)
df['Over/Under 2.5 Goals_Under 2.5 Goals'] = 1 - df['Over/Under 2.5 Goals_Over 2.5 Goals']

# Over/Under 1.5 Goals
df['Over/Under 1.5 Goals_Over 1.5 Goals'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if (i + j) > 1.5]].sum(axis=1)
df['Over/Under 1.5 Goals_Under 1.5 Goals'] = 1 - df['Over/Under 1.5 Goals_Over 1.5 Goals']

# Over/Under 0.5 Goals
df['Over/Under 0.5 Goals_Under 0.5 Goals'] = df['home_0_x_away_0']
df['Over/Under 0.5 Goals_Over 0.5 Goals'] = 1 - df['home_0_x_away_0']

# Home Over/Under 0.5 Goals
df['Home Over/Under 0.5 Goals_Over 0.5 Goals'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i > 0.5]].sum(axis=1)
df['Home Over/Under 0.5 Goals_Under 0.5 Goals'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i < 0.5]].sum(axis=1)

# Home Over/Under 1.5 Goals
df['Home Over/Under 1.5 Goals_Over 1.5 Goals'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i > 1.5]].sum(axis=1)
df['Home Over/Under 1.5 Goals_Under 1.5 Goals'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i < 1.5]].sum(axis=1)

# Home Over/Under 2.5 Goals
df['Home Over/Under 2.5 Goals_Over 2.5 Goals'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i > 2.5]].sum(axis=1)
df['Home Over/Under 2.5 Goals_Under 2.5 Goals'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i < 2.5]].sum(axis=1)

# Away Over/Under 0.5 Goals
df['Away Over/Under 0.5 Goals_Over 0.5 Goals'] = df[[f'home_{i}_x_away_{j}' for j in full_time_indices for i in full_time_indices if j > 0.5]].sum(axis=1)
df['Away Over/Under 0.5 Goals_Under 0.5 Goals'] = df[[f'home_{i}_x_away_{j}' for j in full_time_indices for i in full_time_indices if j < 0.5]].sum(axis=1)

# Away Over/Under 1.5 Goals
df['Away Over/Under 1.5 Goals_Over 1.5 Goals'] = df[[f'home_{i}_x_away_{j}' for j in full_time_indices for i in full_time_indices if j > 1.5]].sum(axis=1)
df['Away Over/Under 1.5 Goals_Under 1.5 Goals'] = df[[f'home_{i}_x_away_{j}' for j in full_time_indices for i in full_time_indices if j < 1.5]].sum(axis=1)

# Away Over/Under 2.5 Goals
df['Away Over/Under 2.5 Goals_Over 2.5 Goals'] = df[[f'home_{i}_x_away_{j}' for j in full_time_indices for i in full_time_indices if j > 2.5]].sum(axis=1)
df['Away Over/Under 2.5 Goals_Under 2.5 Goals'] = df[[f'home_{i}_x_away_{j}' for j in full_time_indices for i in full_time_indices if j < 2.5]].sum(axis=1)

# Match Odds & O/U 2.5 Goals
df['Match Odds And Over/Under 2.5 Goals_Home/Over 2.5 Goals'] = df['Match Odds_Home'] * df['Over/Under 2.5 Goals_Over 2.5 Goals']
df['Match Odds And Over/Under 2.5 Goals_Home/Under 2.5 Goals'] = df['Match Odds_Home'] * df['Over/Under 2.5 Goals_Under 2.5 Goals']
df['Match Odds And Over/Under 2.5 Goals_Draw/Over 2.5 Goals'] = df['Match Odds_The Draw'] * df['Over/Under 2.5 Goals_Over 2.5 Goals']
df['Match Odds And Over/Under 2.5 Goals_Draw/Under 2.5 Goals'] = df['Match Odds_The Draw'] * df['Over/Under 2.5 Goals_Under 2.5 Goals']
df['Match Odds And Over/Under 2.5 Goals_Away/Over 2.5 Goals'] = df['Match Odds_Away'] * df['Over/Under 2.5 Goals_Over 2.5 Goals']
df['Match Odds And Over/Under 2.5 Goals_Away/Under 2.5 Goals'] = df['Match Odds_Away'] * df['Over/Under 2.5 Goals_Under 2.5 Goals']

# Match Odds & O/U 3.5 Goals
df['Match Odds And Over/Under 3.5 Goals_Home/Over 3.5 Goals'] = df['Match Odds_Home'] * df['Over/Under 3.5 Goals_Over 3.5 Goals']
df['Match Odds And Over/Under 3.5 Goals_Home/Under 3.5 Goals'] = df['Match Odds_Home'] * df['Over/Under 3.5 Goals_Under 3.5 Goals']
df['Match Odds And Over/Under 3.5 Goals_Draw/Over 3.5 Goals'] = df['Match Odds_The Draw'] * df['Over/Under 3.5 Goals_Over 3.5 Goals']
df['Match Odds And Over/Under 3.5 Goals_Draw/Under 3.5 Goals'] = df['Match Odds_The Draw'] * df['Over/Under 3.5 Goals_Under 3.5 Goals']
df['Match Odds And Over/Under 3.5 Goals_Away/Over 3.5 Goals'] = df['Match Odds_Away'] * df['Over/Under 3.5 Goals_Over 3.5 Goals']
df['Match Odds And Over/Under 3.5 Goals_Away/Under 3.5 Goals'] = df['Match Odds_Away'] * df['Over/Under 3.5 Goals_Under 3.5 Goals']

# Home Win To Nil
df['Home Win To Nil_Yes'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i > j and j == 0]].sum(axis=1)
df['Home Win To Nil_No'] = 1 - df['Home Win To Nil_Yes']

# Away Win To Nil
df['Away Win To Nil_Yes'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if j > i and i == 0]].sum(axis=1)
df['Away Win To Nil_No'] = 1 - df['Away Win To Nil_Yes']

# Home +1
df['Home +1_Home +1'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i > j - 1]].sum(axis=1)
df['Home +1_Draw'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i == j - 1]].sum(axis=1)
df['Home +1_Away -1'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i < j - 1]].sum(axis=1)

# Away +1
df['Away +1_Away +1'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if j > i - 1]].sum(axis=1)
df['Away +1_Draw'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if j == i - 1]].sum(axis=1)
df['Away +1_Home -1'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if j < i - 1]].sum(axis=1)

# Home +2
df['Home +2_Home +2'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i > j - 2]].sum(axis=1)
df['Home +2_Draw'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i == j - 2]].sum(axis=1)
df['Home +2_Away -2'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i < j - 2]].sum(axis=1)

# Away +2
df['Away +2_Away +2'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if j > i - 2]].sum(axis=1)
df['Away +2_Draw'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if j == i - 2]].sum(axis=1)
df['Away +2_Home -2'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if j < i - 2]].sum(axis=1)

# Home +3
df['Home +3_Home +3'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i > j - 3]].sum(axis=1)
df['Home +3_Draw'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i == j - 3]].sum(axis=1)
df['Home +3_Away -3'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if i < j - 3]].sum(axis=1)

# Away +3
df['Away +3_Away +3'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if j > i - 3]].sum(axis=1)
df['Away +3_Draw'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if j == i - 3]].sum(axis=1)
df['Away +3_Home -3'] = df[[f'home_{i}_x_away_{j}' for i in full_time_indices for j in full_time_indices if j < i - 3]].sum(axis=1)

# Half Time Result
df['Half Time_Home'] = df[[f'home_{i}_ht_x_away_{j}_ht' for i in half_time_indices for j in half_time_indices if i > j]].sum(axis=1)
df['Half Time_The Draw'] = df[[f'home_{i}_ht_x_away_{i}_ht' for i in half_time_indices]].sum(axis=1)
df['Half Time_Away'] = df[[f'home_{i}_ht_x_away_{j}_ht' for i in half_time_indices for j in half_time_indices if i < j]].sum(axis=1)

# Half Time / Full Time
df['Half Time/Full Time_Home/Home'] = df['Match Odds_Home'] * df['Half Time_Home']
df['Half Time/Full Time_Home/Draw'] = df['Match Odds_The Draw'] * df['Half Time_Home']
df['Half Time/Full Time_Home/Away'] = df['Match Odds_Away'] * df['Half Time_Home']
df['Half Time/Full Time_Draw/Home'] = df['Match Odds_Home'] * df['Half Time_The Draw']
df['Half Time/Full Time_Draw/Draw'] = df['Match Odds_The Draw'] * df['Half Time_The Draw']
df['Half Time/Full Time_Draw/Away'] = df['Match Odds_Away'] * df['Half Time_The Draw']
df['Half Time/Full Time_Away/Home'] = df['Match Odds_Home'] * df['Half Time_Away']
df['Half Time/Full Time_Away/Draw'] = df['Match Odds_The Draw'] * df['Half Time_Away']
df['Half Time/Full Time_Away/Away'] = df['Match Odds_Away'] * df['Half Time_Away']

# First Half Over/Under 2.5 Goals
df['First Half Goals 2.5_Over 2.5 Goals'] = df[[f'home_{i}_ht_x_away_{j}_ht' for i in half_time_indices for j in half_time_indices if (i + j) > 2.5]].sum(axis=1)
df['First Half Goals 2.5_Under 2.5 Goals'] = 1 - df['First Half Goals 2.5_Over 2.5 Goals']

# First Half Over/Under 1.5 Goals
df['First Half Goals 1.5_Over 1.5 Goals'] = df[[f'home_{i}_ht_x_away_{j}_ht' for i in half_time_indices for j in half_time_indices if (i + j) > 1.5]].sum(axis=1)
df['First Half Goals 1.5_Under 1.5 Goals'] = 1 - df['First Half Goals 1.5_Over 1.5 Goals']

# First Half Over/Under 0.5 Goals
df['First Half Goals 0.5_Under 0.5 Goals'] = df['home_0_ht_x_away_0_ht']
df['First Half Goals 0.5_Over 0.5 Goals'] = 1 - df['home_0_ht_x_away_0_ht']

# Half Time Score
df['Half Time Score_0 - 0'] = df['home_0_ht_x_away_0_ht']
df['Half Time Score_0 - 1'] = df['home_0_ht_x_away_1_ht']
df['Half Time Score_0 - 2'] = df['home_0_ht_x_away_2_ht']
df['Half Time Score_1 - 0'] = df['home_1_ht_x_away_0_ht']
df['Half Time Score_1 - 1'] = df['home_1_ht_x_away_1_ht']
df['Half Time Score_1 - 2'] = df['home_1_ht_x_away_2_ht']
df['Half Time Score_2 - 0'] = df['home_2_ht_x_away_0_ht']
df['Half Time Score_2 - 1'] = df['home_2_ht_x_away_1_ht']
df['Half Time Score_2 - 2'] = df['home_2_ht_x_away_2_ht']
df['Half Time Score_Any Unquoted'] = df[[f'home_{i}_ht_x_away_{j}_ht' for i in half_time_indices for j in half_time_indices if i > 2 or j > 2]].sum(axis=1)

# Reshape the dataframe to keep only required columns for our simulations
df = df.drop(columns=new_column_names)
df = df.drop(columns=['match_id','goalsScored_home','goalsScored_away','halfTimeGoalsScored_home','halfTimeGoalsScored_away'])
df = df.rename(columns={'date_home':'event_date'})
df.insert(3,'fixture',df['name_home'].fillna('').astype(str) + ' v ' + df['name_away'].fillna('').astype(str))

# Create a rated price for each column, and ensuring that each rating is in the range valid for the exchange (1.01-1000)
for col in df.columns:
    if col not in ['event_date','name_home','name_away','fixture']:
        # Avoid division by zero by replacing zeroes with 0.001 before taking the reciprocal
        df[col] = 1 / df[col].replace(0, 0.001)
        df[col] = df[col].round(2) # Round to 2 decimal places
        df[col] = df[col].clip(lower=1.01, upper=1000) # Restrict rated prices to exchange min/max prices

'''
The below code block is to transform the dataframe from one row per match to having one row per market/selection

Pre-Transformation Shape: 144 columns x 727 rows
Post-Transformation Shape: 5 columns x 92,202 rows
'''
# Initialize an empty list to store the sub-DataFrames
sub_dfs = []

# Get the list of columns excluding the first four
columns = df.columns[4:]

# Loop through each column
for col in columns:
    # Create a sub-DataFrame with the first four columns and the current column
    sub_df = df.iloc[:, :4].copy()
    sub_df['rated_price'] = df[col]
    # Extract market_name and runner_name from the column name
    market_name, runner_name = col.split('_', 1)
    sub_df['market_name'] = market_name
    sub_df['runner_name'] = runner_name

    # Define a function to replace 'Home' and 'Away' only if 'Any Other' is not in the string
    def replace_names(value, home_name, away_name):
        if 'Any Other' not in value and ' Or ' not in value:
            value = value.replace('Home', home_name).replace('Away', away_name)
        return value
    
    sub_df['market_name'] = sub_df.apply(lambda row: replace_names(row['market_name'], row['name_home'], row['name_away']), axis=1)
    sub_df['runner_name'] = sub_df.apply(lambda row: replace_names(row['runner_name'], row['name_home'], row['name_away']), axis=1)
    
    # Add the sub-DataFrame to the list
    sub_dfs.append(sub_df)

# Concatenate all sub-DataFrames
final_df = pd.concat(sub_dfs, ignore_index=True)
final_df = final_df[['event_date','fixture','market_name','runner_name','rated_price']]

# Write our predictions to a csv file for our simulations
final_df.to_csv('ensemble_model_results_processed.csv',index=False)

```
Following this we've applied the models to our test set (on which we'll run our simulations) and then generated rated prices for a (non-exhaustive) list of popular markets present on English Premier League matches. 

Player markets are not modelled here due to the nature of the dataset but this method could be applied to Cards, Corners and Shots as these fields are all present in our training data. 

There are a subset of markets which are only loaded in-play if required (e.g. Over/Under 10.5 Goals) which have been excluded. Markets like Over/Under 8.5 Goals exist but usually contain very little liquidity unless the goal count approaches that value (i.e. scores are unusually high and most volume will come in-play).

Now our model outputs for Arsenal v Leicester look like:

| event_date | fixture             | market_name                         | runner_name               | rated_price |
| ---------- | ------------------- | ----------------------------------- | ------------------------- | ----------- |
| 13/08/2022 | Arsenal v Leicester | Both Teams To Score?                | Yes                       | 1.96        |
| 13/08/2022 | Arsenal v Leicester | Both Teams To Score?                | No                        | 2.05        |
| 13/08/2022 | Arsenal v Leicester | Match Odds                          | Arsenal                   | 1.7         |
| 13/08/2022 | Arsenal v Leicester | Match Odds                          | The Draw                  | 4.44        |
| 13/08/2022 | Arsenal v Leicester | Match Odds                          | Leicester                 | 5.32        |
| 13/08/2022 | Arsenal v Leicester | Draw No Bet                         | Arsenal                   | 1.32        |
| 13/08/2022 | Arsenal v Leicester | Draw No Bet                         | Leicester                 | 4.12        |
| 13/08/2022 | Arsenal v Leicester | Double Chance                       | Home Or Away              | 1.29        |
| 13/08/2022 | Arsenal v Leicester | Double Chance                       | Home Or Draw              | 1.23        |
| 13/08/2022 | Arsenal v Leicester | Double Chance                       | Draw Or Away              | 2.42        |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Both Teams To Score  | Arsenal/Yes               | 3.33        |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Both Teams To Score  | Arsenal/No                | 3.49        |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Both Teams To Score  | Draw/Yes                  | 8.69        |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Both Teams To Score  | Draw/No                   | 9.08        |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Both Teams To Score  | Leicester/Yes             | 10.41       |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Both Teams To Score  | Leicester/No              | 10.88       |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 0 - 0                     | 16.25       |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 0 - 1                     | 17.44       |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 0 - 2                     | 39.08       |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 0 - 3                     | 108.73      |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 1 - 0                     | 8.68        |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 1 - 1                     | 9.31        |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 1 - 2                     | 20.87       |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 1 - 3                     | 58.06       |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 2 - 0                     | 8.84        |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 2 - 1                     | 9.48        |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 2 - 2                     | 21.25       |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 2 - 3                     | 59.13       |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 3 - 0                     | 18.34       |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 3 - 1                     | 19.69       |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 3 - 2                     | 44.11       |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | 3 - 3                     | 122.74      |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | Any Other Home Win        | 8           |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | Any Other Draw            | 928.52      |
| 13/08/2022 | Arsenal v Leicester | Correct Score                       | Any Other Away Win        | 72.27       |
| 13/08/2022 | Arsenal v Leicester | Over/Under 5.5 Goals                | Over 5.5 Goals            | 16.73       |
| 13/08/2022 | Arsenal v Leicester | Over/Under 5.5 Goals                | Under 5.5 Goals           | 1.06        |
| 13/08/2022 | Arsenal v Leicester | Over/Under 4.5 Goals                | Over 4.5 Goals            | 6.79        |
| 13/08/2022 | Arsenal v Leicester | Over/Under 4.5 Goals                | Under 4.5 Goals           | 1.17        |
| 13/08/2022 | Arsenal v Leicester | Over/Under 3.5 Goals                | Over 3.5 Goals            | 3.3         |
| 13/08/2022 | Arsenal v Leicester | Over/Under 3.5 Goals                | Under 3.5 Goals           | 1.43        |
| 13/08/2022 | Arsenal v Leicester | Over/Under 2.5 Goals                | Over 2.5 Goals            | 1.92        |
| 13/08/2022 | Arsenal v Leicester | Over/Under 2.5 Goals                | Under 2.5 Goals           | 2.08        |
| 13/08/2022 | Arsenal v Leicester | Over/Under 1.5 Goals                | Over 1.5 Goals            | 1.31        |
| 13/08/2022 | Arsenal v Leicester | Over/Under 1.5 Goals                | Under 1.5 Goals           | 4.27        |
| 13/08/2022 | Arsenal v Leicester | Over/Under 0.5 Goals                | Under 0.5 Goals           | 16.25       |
| 13/08/2022 | Arsenal v Leicester | Over/Under 0.5 Goals                | Over 0.5 Goals            | 1.07        |
| 13/08/2022 | Arsenal v Leicester | Arsenal Over/Under 0.5 Goals        | Over 0.5 Goals            | 1.18        |
| 13/08/2022 | Arsenal v Leicester | Arsenal Over/Under 0.5 Goals        | Under 0.5 Goals           | 6.41        |
| 13/08/2022 | Arsenal v Leicester | Arsenal Over/Under 1.5 Goals        | Over 1.5 Goals            | 1.81        |
| 13/08/2022 | Arsenal v Leicester | Arsenal Over/Under 1.5 Goals        | Under 1.5 Goals           | 2.23        |
| 13/08/2022 | Arsenal v Leicester | Arsenal Over/Under 2.5 Goals        | Over 2.5 Goals            | 3.78        |
| 13/08/2022 | Arsenal v Leicester | Arsenal Over/Under 2.5 Goals        | Under 2.5 Goals           | 1.36        |
| 13/08/2022 | Arsenal v Leicester | Leicester Over/Under 0.5 Goals      | Over 0.5 Goals            | 1.65        |
| 13/08/2022 | Arsenal v Leicester | Leicester Over/Under 0.5 Goals      | Under 0.5 Goals           | 2.54        |
| 13/08/2022 | Arsenal v Leicester | Leicester Over/Under 1.5 Goals      | Over 1.5 Goals            | 4.2         |
| 13/08/2022 | Arsenal v Leicester | Leicester Over/Under 1.5 Goals      | Under 1.5 Goals           | 1.31        |
| 13/08/2022 | Arsenal v Leicester | Leicester Over/Under 2.5 Goals      | Over 2.5 Goals            | 13.48       |
| 13/08/2022 | Arsenal v Leicester | Leicester Over/Under 2.5 Goals      | Under 2.5 Goals           | 1.08        |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Over/Under 2.5 Goals | Arsenal/Over 2.5 Goals    | 3.28        |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Over/Under 2.5 Goals | Arsenal/Under 2.5 Goals   | 3.55        |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Over/Under 2.5 Goals | Draw/Over 2.5 Goals       | 8.54        |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Over/Under 2.5 Goals | Draw/Under 2.5 Goals      | 9.25        |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Over/Under 2.5 Goals | Leicester/Over 2.5 Goals  | 10.23       |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Over/Under 2.5 Goals | Leicester/Under 2.5 Goals | 11.07       |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Over/Under 3.5 Goals | Arsenal/Over 3.5 Goals    | 5.63        |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Over/Under 3.5 Goals | Arsenal/Under 3.5 Goals   | 2.44        |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Over/Under 3.5 Goals | Draw/Over 3.5 Goals       | 14.67       |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Over/Under 3.5 Goals | Draw/Under 3.5 Goals      | 6.37        |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Over/Under 3.5 Goals | Leicester/Over 3.5 Goals  | 17.57       |
| 13/08/2022 | Arsenal v Leicester | Match Odds And Over/Under 3.5 Goals | Leicester/Under 3.5 Goals | 7.63        |
| 13/08/2022 | Arsenal v Leicester | Arsenal Win To Nil                  | Yes                       | 3           |
| 13/08/2022 | Arsenal v Leicester | Arsenal Win To Nil                  | No                        | 1.5         |
| 13/08/2022 | Arsenal v Leicester | Leicester Win To Nil                | Yes                       | 10.58       |
| 13/08/2022 | Arsenal v Leicester | Leicester Win To Nil                | No                        | 1.1         |
| 13/08/2022 | Arsenal v Leicester | Arsenal +1                          | Arsenal +1                | 1.23        |
| 13/08/2022 | Arsenal v Leicester | Arsenal +1                          | Draw                      | 8.07        |
| 13/08/2022 | Arsenal v Leicester | Arsenal +1                          | Leicester -1              | 15.6        |
| 13/08/2022 | Arsenal v Leicester | Leicester +1                        | Leicester +1              | 2.42        |
| 13/08/2022 | Arsenal v Leicester | Leicester +1                        | Draw                      | 4.01        |
| 13/08/2022 | Arsenal v Leicester | Leicester +1                        | Arsenal -1                | 2.96        |
| 13/08/2022 | Arsenal v Leicester | Arsenal +2                          | Arsenal +2                | 1.07        |
| 13/08/2022 | Arsenal v Leicester | Arsenal +2                          | Draw                      | 21.58       |
| 13/08/2022 | Arsenal v Leicester | Arsenal +2                          | Leicester -2              | 56.26       |
| 13/08/2022 | Arsenal v Leicester | Leicester +2                        | Leicester +2              | 1.51        |
| 13/08/2022 | Arsenal v Leicester | Leicester +2                        | Draw                      | 5.51        |
| 13/08/2022 | Arsenal v Leicester | Leicester +2                        | Arsenal -2                | 6.41        |
| 13/08/2022 | Arsenal v Leicester | Arsenal +3                          | Arsenal +3                | 1.02        |
| 13/08/2022 | Arsenal v Leicester | Arsenal +3                          | Draw                      | 75.29       |
| 13/08/2022 | Arsenal v Leicester | Arsenal +3                          | Leicester -3              | 222.5       |
| 13/08/2022 | Arsenal v Leicester | Leicester +3                        | Leicester +3              | 1.18        |
| 13/08/2022 | Arsenal v Leicester | Leicester +3                        | Draw                      | 10.58       |
| 13/08/2022 | Arsenal v Leicester | Leicester +3                        | Arsenal -3                | 16.25       |
| 13/08/2022 | Arsenal v Leicester | Half Time                           | Arsenal                   | 2.39        |
| 13/08/2022 | Arsenal v Leicester | Half Time                           | The Draw                  | 2.47        |
| 13/08/2022 | Arsenal v Leicester | Half Time                           | Leicester                 | 5.65        |
| 13/08/2022 | Arsenal v Leicester | Half Time/Full Time                 | Arsenal/Arsenal           | 4.08        |
| 13/08/2022 | Arsenal v Leicester | Half Time/Full Time                 | Arsenal/Draw              | 10.62       |
| 13/08/2022 | Arsenal v Leicester | Half Time/Full Time                 | Arsenal/Leicester         | 12.72       |
| 13/08/2022 | Arsenal v Leicester | Half Time/Full Time                 | Draw/Arsenal              | 4.21        |
| 13/08/2022 | Arsenal v Leicester | Half Time/Full Time                 | Draw/Draw                 | 10.97       |
| 13/08/2022 | Arsenal v Leicester | Half Time/Full Time                 | Draw/Leicester            | 13.13       |
| 13/08/2022 | Arsenal v Leicester | Half Time/Full Time                 | Leicester/Arsenal         | 9.63        |
| 13/08/2022 | Arsenal v Leicester | Half Time/Full Time                 | Leicester/Draw            | 25.1        |
| 13/08/2022 | Arsenal v Leicester | Half Time/Full Time                 | Leicester/Leicester       | 30.07       |
| 13/08/2022 | Arsenal v Leicester | First Half Goals 2.5                | Over 2.5 Goals            | 8.29        |
| 13/08/2022 | Arsenal v Leicester | First Half Goals 2.5                | Under 2.5 Goals           | 1.14        |
| 13/08/2022 | Arsenal v Leicester | First Half Goals 1.5                | Over 1.5 Goals            | 2.91        |
| 13/08/2022 | Arsenal v Leicester | First Half Goals 1.5                | Under 1.5 Goals           | 1.52        |
| 13/08/2022 | Arsenal v Leicester | First Half Goals 0.5                | Under 0.5 Goals           | 3.22        |
| 13/08/2022 | Arsenal v Leicester | First Half Goals 0.5                | Over 0.5 Goals            | 1.45        |
| 13/08/2022 | Arsenal v Leicester | Half Time Score                     | 0 - 0                     | 3.22        |
| 13/08/2022 | Arsenal v Leicester | Half Time Score                     | 0 - 1                     | 8.7         |
| 13/08/2022 | Arsenal v Leicester | Half Time Score                     | 0 - 2                     | 46.97       |
| 13/08/2022 | Arsenal v Leicester | Half Time Score                     | 1 - 0                     | 4.33        |
| 13/08/2022 | Arsenal v Leicester | Half Time Score                     | 1 - 1                     | 11.72       |
| 13/08/2022 | Arsenal v Leicester | Half Time Score                     | 1 - 2                     | 63.26       |
| 13/08/2022 | Arsenal v Leicester | Half Time Score                     | 2 - 0                     | 8.63        |
| 13/08/2022 | Arsenal v Leicester | Half Time Score                     | 2 - 1                     | 23.36       |
| 13/08/2022 | Arsenal v Leicester | Half Time Score                     | 2 - 2                     | 126.13      |
| 13/08/2022 | Arsenal v Leicester | Half Time Score                     | Any Unquoted              | 18.5        |

## Flumine Simulation

Our next step is to take our results and run simulations on the Betfair Historical Stream Files. These files have a cost associated with them (Australia and New Zealand customers should reach out to us at automation@betfair.com.au to discuss options). We'll use Flumine and its simulation mode to run these tests as these tend to be accurate, and will also help us to test out our string matching against the exchange markets, as this is key to being able to place live bets. 

It's important to note that the historic files do not contain cross-matching volume (also called virtual bets) or information from the market catalogue. So just be aware that live behaviour may not necessarily reflect the simulations. Runner information is contained within market_book.market_definition.runners so runner names will be available in the files.

### Unzipping The Files

Flumine requires the tar files to be unzipped to run the simulations so we'll iterate over the tar files to extract only the markets we need before commencing the simulation.

We'll quickly process our tar files using our super fast **Rust**-driven tutorial: [JSON to CSV Revisted](https://betfair-datascientists.github.io/tutorials/jsonToCsvRevisited/)

By doing so we've created a csv file where we can easily pick out the markets we want to use. (You can skip this step and use the flumine process of check_market_book to filter out unwanted markets)

 - [EPL Market CSV File](../modelling/assets/EPL_Markets.csv)

!!! info "Market Ids"
    Market ids in the stream files are denoted by "1.XXXXXXXXX", however in the provided csv file we have removed the "1.".
    
    In excel we do this using the formula: (marketId - 1) * 1000000000

    We do this because excel likes to truncate trailing zeros on negative numbers. The python line is provided below

```py title="Remove '1.' from market_id in Python"

df['market_id'] = df['market_id'].apply(lambda x: str(x).ljust(9, '0')[:9])

```

```py title="Unzip Historic Stream Files"

import os
import glob
import shutil
import tarfile
import bz2
import pandas as pd

'''
Here we will specify the folder where we are storing our stream files and where we want to extract the files to
The code will check if the output folder exists, and will create one if it does not.
It will then check the folder and delete any files in the folder that are not tar or csv files
This deletion is to clear any previously extracted stream files and will be much faster than manually deleting them
'''

# Specify the directory where your stream files are stored and where you want to extract the files
source_folder = 'DIRECTORY OF DOWNLOADED FILES'
output_folder = 'DIRECTORY TO OUTPUT DECOMPRESSED STREAM FILES'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Get a list of all files in the directory
files = glob.glob(os.path.join(output_folder, '*'))

# Loop through the files and delete if they are not tar/csv files
for file in files:
    if not file.endswith('.tar') and not file.endswith('.csv'):
        try:
            os.remove(file)
            print(f'Deleted: {file}')
        except Exception as e:
            print(f'Error deleting {file}: {e}')

'''
The following section will iterate over all files in your folder, so the options to optimize are:

    - Move the files you don't want to process to another folder
    - Copy the files you do want to process to a new folder
    - Use string matching to remove unwanted files from the tar_files list
    - Manually specify each file by typing out a list
'''

# Iterate over all .tar files in the source folder
tar_files = glob.glob(os.path.join(source_folder, '*.tar'))

def retrieve_betfair_markets():
    markets = pd.read_csv('C:/Users/motykam/Downloads/EPL_Markets.csv',dtype={'MARKET_ID' : str})

    markets = markets['MARKET_ID'].tolist()

    return markets

markets = retrieve_betfair_markets()

'''
The next code block here will iterate over each stream file and check if the market_id is in the list of our win market ids
Only the win markets will be extracted to the folder.
'''

for tar_path in tar_files:

    with tarfile.open(tar_path, 'r') as tar:
        # Iterate over each file in the tar archive
        for member in tar.getmembers():
            if member.name.endswith('.bz2'):
                # Extract the .bz2 file to a temporary location
                extracted_bz2_path = os.path.join(output_folder, os.path.basename(member.name))

                # Determine the final output path by removing the .bz2 extension
                final_output_path = extracted_bz2_path[:-4]
                market_id = extracted_bz2_path[-13:-4]
                
                if market_id in markets:

                    try:
                        with tar.extractfile(member) as extracted_file, open(extracted_bz2_path, 'wb') as temp_bz2_file:
                            shutil.copyfileobj(extracted_file, temp_bz2_file)

                        # Extract the .bz2 file to the final destination
                        with bz2.BZ2File(extracted_bz2_path, 'rb') as bz2_file, open(final_output_path, 'wb') as output_file:
                            shutil.copyfileobj(bz2_file, output_file)
                    
                        # Remove the temporary .bz2 file
                        os.remove(extracted_bz2_path)
                        
                        print(f'Extracted {member.name} to {final_output_path}')
                    except OSError:
                        pass

```

### Running the Simulation

Now that we've unzipped the files, we'll need to run the simulations on the files.

**Just a word of warning**: This is not a fast process to run over two years of EPL data. It took my machine with 4 CPUs about 24 hours to pass over this data.
The further out from the match start you're looking to place bets, the longer the process will take, as well if you leave bets inplay (using persistence_type="PERSIST") this will also take longer.

The advice here is to use the check_market_book function to not process markets that you're not interested in (e.g. OVER/UNDER_8.5_GOALS, SHOTS_ON_TARGET).

There's a code snippet included after the simulation code that enables you to delete markets that you've already processed so the entire process doesn't need to be restarted if it crashes or needs to be paused.

```py title="Import modules and set-up logging"

# Import libraries
import os
import time
import logging
import csv
import pandas as pd
from pythonjsonlogger import jsonlogger
from flumine import FlumineSimulation, BaseStrategy, clients
from flumine.order.trade import Trade
from flumine.order.order import LimitOrder
from flumine.order.ordertype import OrderTypes
from flumine.markets.market import Market
from flumine.controls.loggingcontrols import LoggingControl
from betfairlightweight.resources import MarketBook
from pythonjsonlogger import jsonlogger
from concurrent import futures 
from flumine.utils import price_ticks_away
from collections import OrderedDict
from tqdm import tqdm

# Create custom logger
logger = logging.getLogger()

# Remove existing handlers to avoid duplicates
logger.handlers = []

# Set up JSON formatter for the log file
log_handler = logging.FileHandler(destination+'process_logs.log')
custom_format = "%(asctime)s %(levelname)s %(message)s"
formatter = jsonlogger.JsonFormatter(custom_format)
formatter.converter = time.gmtime  # Optional: Use UTC/GMT time for logs
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

# Ensure logs are only written to the file
logger.propagate = False

# Specify the folder where the unzipped stream files are stored
source_folder = output_folder # We defined this earlier

```

```py title="define custom functions"

'''
This code file is designed to iterate over the folder with the previously unzipped stream files
and place simulated bets on selections at 10 minutes before kick-off

We will speed this process up using multi-threading
'''


# Function to split our list into chunks
def split_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

# Function to process the runner_book to gather each selection_id
def process_runner_books(runner_books):
    selection_ids = [runner_book.selection_id for runner_book in runner_books]

    df = pd.DataFrame({
        'selection_id': selection_ids,
    })
    return df.set_index('selection_id')

# Function to process the runner catalogue to gather all selection names
def process_runner_catalogue(market_book: MarketBook):

    runners_df = process_runner_books(market_book.runners)

    for runner in market_book.runners:
        runner_name = next((rd.name for rd in market_book.market_definition.runners if rd.selection_id == runner.selection_id), None)
        # rstrip() removes any trailing white spaces
        runners_df.loc[runner.selection_id, 'runner_name'] = runner_name.rstrip().title()

    return runners_df

```

```py title="Define Flumine Class & Logging Control"

# Defining our flumine class
class SoccerSimulation(BaseStrategy):

    '''
    The __init__ function defines what the strategy should do when it first fires
    We define our external dataframe where we have loaded our rated prices
    It is essential that we tie the dataframe to the class using a self definition
    We also define an empty list to use later
    '''
    def __init__(self, soccer_df, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processed_selection_ids = []
        self.soccer_df = soccer_df

    def check_market_book(self, market: Market, market_book: MarketBook) -> bool:
        ''' 
        process_market_book only executed if this returns True.
        if True is not returned then the framework will skip to the next market
        '''
        # This check skips markets for the ring-fenced Italian and Spanish exchanges
        if market_book.market_definition.regulators != ["MR_INT"]:
            return False
        # Skip markets with unwanted market types
        if market_book.market_definition.market_type in ['OVER_UNDER_85']
            return False
        if market_book.status != "CLOSED" and market_book.inplay == False:
            return True

    def process_market_book(self, market: Market, market_book: MarketBook) -> None:
 
        # Create a dataframe with all the selection_ids and runner_names from the market
        runners_df = process_runner_catalogue(market_book)
        # Define the event name as the fixture name e.g. Aston Villa v Chelsea
        runners_df['fixture'] = market_book.market_definition.event_name
        # Define the market name and ensure each word is capitalised
        runners_df['market_name'] = market_book.market_definition.name.title()
        # Extract market_type
        runners_df['market_type'] = market_book.market_definition.market_type
        # Extract the date from the market_time
        runners_df['event_date'] = market_book.market_definition.market_time.date()
        # Ensure the event_date is datetime format
        runners_df['event_date'] = pd.to_datetime(runners_df['event_date'])
        # Preserve the index as a column before merging
        runners_df['selection_id'] = runners_df.index
        # Merge the market info with our ratings dataframe
        market_df = pd.merge(runners_df,self.soccer_df, how='left', on=['event_date', 'fixture', 'market_name', 'runner_name'])
        # Set the index as the selection_id for order placement
        market_df.set_index('selection_id',inplace=True)

        if round(market.seconds_to_start, 0) <= 600 and round(market.seconds_to_start, 0) > 30:

            # Loop over each runner in the market
            for runner in market_book.runners:
                # Check runner isn't scratched and that first layer of back/lay prices exists
                if runner.status == "ACTIVE" and len(runner.ex.available_to_back) > 0 and len(runner.ex.available_to_lay) > 0:
                    runner_name = market_df.loc[runner.selection_id, 'runner_name']
                    event_name = market_df.loc[runner.selection_id, 'fixture']
                    market_type = market_df.loc[runner.selection_id, 'market_type']
                    market_name = market_df.loc[runner.selection_id, 'market_name']
                    rated_price = float(market_df.loc[runner.selection_id, 'rated_price'] or 0)

                    if runner.selection_id not in self.processed_selection_ids:
                        # Create our ordered dictionary to store our order notes
                        notes = OrderedDict()
                        # Write our order notes - adding these notes is time-consuming but is helpful for troubleshooting string matching issues
                        notes["fixture"] = "fixture:" + str(event_name)
                        notes["market_type"] = "market_type:" + str(market_type)
                        notes["market"] = "market:" + str(market_name)
                        notes["runner_name"] = "selection:" + str(runner_name).replace(' - ','&')
                        notes["rated_price"] = "rated_price:" + str(rated_price)

                        trade = Trade(
                            market_id=market_book.market_id,
                            selection_id=runner.selection_id,
                            handicap=runner.handicap,
                            notes=notes,
                            strategy=self,
                        )
                        order = trade.create_order(
                            side="BACK",
                            order_type=LimitOrder(
                                price=price_ticks_away(runner.ex.available_to_back[0]['price'],-1),
                                size=round(100 / rated_price, 2),
                                persistence_type="LAPSE"
                            )
                        )
                        market.place_order(order)
                        # Add the selection to the list to ensure that we don't bet on it again.
                        self.processed_selection_ids.append(runner.selection_id)
        
        # cancel unmatched bets 30 seconds before the scheduled off
        if round(market.seconds_to_start, 0) <= 30:
            market.cancel_order(market_id=market_book.market_id)

# Fields we want to log in our simulations
FIELDNAMES = [
    "bet_id",
    "strategy_name",
    "market_id",
    "selection_id",
    "trade_id",
    "date_time_placed",
    "price",
    "price_matched",
    "size",
    "size_matched",
    "profit",
    "side",
    "elapsed_seconds_executable",
    "order_status",
    "market_note",
    "trade_notes",
    "order_notes",
]

# Class to define logging class and output results to csv files
class BacktestLoggingControl(LoggingControl):
    NAME = "BACKTEST_LOGGING_CONTROL"

    def __init__(self, model, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)
        self._setup()

    def _setup(self):
        if os.path.exists(destination + f"soccer_simulation_{self.model}.csv"):
            logging.info("Results file exists")
        else:
            with open(destination + f"soccer_simulation_{self.model}.csv", "w") as m:
                csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                csv_writer.writeheader()

    def _process_cleared_orders_meta(self, event):
        orders = event.event
        with open(destination+f"soccer_simulation_{self.model}.csv", "a") as m:
            for order in orders:
                if order.order_type.ORDER_TYPE == OrderTypes.LIMIT:
                    size = order.order_type.size
                else:
                    size = order.order_type.liability
                if order.order_type.ORDER_TYPE == OrderTypes.MARKET_ON_CLOSE:
                    price = None
                else:
                    price = order.order_type.price
                try:
                    order_data = {
                        "bet_id": order.bet_id,
                        "strategy_name": order.trade.strategy,
                        "market_id": order.market_id,
                        "selection_id": order.selection_id,
                        "trade_id": order.trade.id,
                        "date_time_placed": order.responses.date_time_placed,
                        "price": price,
                        "price_matched": order.average_price_matched,
                        "size": size,
                        "size_matched": order.size_matched,
                        "profit": order.simulated.profit,
                        "side": order.side,
                        "elapsed_seconds_executable": order.elapsed_seconds_executable,
                        "order_status": order.status.value,
                        "market_note": order.trade.market_notes,
                        "trade_notes": order.trade.notes_str,
                        "order_notes": order.notes_str,
                    }
                    csv_writer = csv.DictWriter(m, delimiter=",", fieldnames=FIELDNAMES)
                    csv_writer.writerow(order_data)
                except Exception as e:
                    logger.error(
                        "_process_cleared_orders_meta: %s" % e,
                        extra={"order": order, "error": e},
                    )

        logger.info("Orders updated", extra={"order_count": len(orders)})

```

```py title="Run the simulation"


def run_process(chunk,soccer_df,model):  
    try:
        # Set Flumine to simulation mode
        client = clients.SimulatedClient(min_bet_validation=False)
        framework = FlumineSimulation(client=client)

        # Set parameters for our strategy
        strategy = SoccerSimulation(
            market_filter={
                "markets": chunk,  
                "listener_kwargs": {"inplay":False,"seconds_to_start": 660},  
            },
            soccer_df=soccer_df,
            max_order_exposure=1000,
            max_selection_exposure=1000,
            max_live_trade_count=2,
            max_trade_count=2,
        )
        # Run our strategy on the simulated market
        framework.add_strategy(strategy)
        framework.add_logging_control(BacktestLoggingControl(model))
        framework.run()
    except Exception as e:
        logger.error(f"Error in run_process: {e}")

def process_csv_file(model):

    df = pd.read_csv(destination+f'soccer_simulation_{model}.csv')

    # Process market_id column
    df['market_id'] = df['market_id'].astype(str).str.replace('1.', '', regex=False).str.ljust(9, '0')
    
    # Split trade_notes column into three new columns
    df[['fixture','market_type','market','selection',f'{model}_rated_price']] = df['trade_notes'].str.split(',', expand=True)
    
    # Remove column names from the strings in each row
    df['fixture'] = df['fixture'].str.replace('fixture:', '', regex=False)
    df['market_type'] = df['market_type'].str.replace('market_type:', '', regex=False)
    df['market'] = df['market'].str.replace('market:', '', regex=False)
    df['selection'] = df['selection'].str.replace('selection:', '', regex=False)
    df[f'{model}_rated_price'] = df[f'{model}_rated_price'].str.replace('rated_price:', '', regex=False).astype(float)
    df[f'{model}_implied_value'] = 1/df['price_matched'] - 1/df[f'{model}_rated_price']
    
    # Process date_time_placed column
    df['date_time_placed'] = pd.to_datetime(df['date_time_placed'], dayfirst=True,format='mixed')
    df['date_time_placed'] = df['date_time_placed'].dt.tz_localize('UTC', ambiguous=False).dt.tz_convert('Australia/Melbourne')

    # Select relevant columns
    columns_to_keep = ['date_time_placed', 'fixture', 'market_id','market_type','market', 'selection_id', 'selection', 'side', f'{model}_rated_price', f'{model}_implied_value', 'price_matched', 'size', 'size_matched', 'profit']
    df = df[columns_to_keep]
    
    df.to_csv(destination+f'soccer_simulation_{model}_processed.csv', index=False)

def process_model(model):

    # Read the model results CSV for the current model
    soccer_df = pd.read_csv(
        destination + f'{model}_model_results_processed.csv',
        parse_dates=['event_date'],
        dayfirst=False
    )
    logging.info(f"Processing model: {model}")

    data_folder = source_folder
    data_files = os.listdir(data_folder)
    data_files = [f'{data_folder}/{path}' for path in data_files]

    print(data_files)
    
    chunks = list(split_list(data_files, 1000))  # Splitting data into chunks of 1000 files
    
    # Iterate over each chunk
    for chunk_index, chunk in enumerate(tqdm(chunks, desc=f"Chunks Progress")):
        all_markets = chunk
        processes = 4  # Number of available CPUs
        markets_per_process = 8  # Number of markets each process should handle

        _process_jobs = []

        with futures.ProcessPoolExecutor(max_workers=processes) as p:
            # Here we use `markets_per_process` to split the chunk into smaller lists
            for m in split_list(all_markets, markets_per_process):
                _process_jobs.append(
                    p.submit(run_process, m, soccer_df, model)
                )
            for job in futures.as_completed(_process_jobs):
                job.result()

        logging.info(f"Completed processing chunk {chunk_index+1} for model {model}")
    
    # Once done, process final CSV
    process_csv_file(model)
    logging.info(f"Completed processing for model {model}")

process_model('ensemble')

```

```py title="Delete Processed Markets"

'''
If the market processing is stopped for any reason, use the below code to delete any markets that have
already been processed so you don't have to re-process them
'''

# Load the CSV file and extract unique values from the 'market_id' column
csv_file = destination+'soccer_simulation_ensemble.csv' 
df = pd.read_csv(csv_file,dtype={'market_id':'str'})
market_ids = df['market_id'].unique().tolist()
# Define the folder to iterate over
folder_path = 'FOLDER WHERE THE DECOMPRESSED STREAM FILES ARE STORED'

# Iterate over files in the folder
for filename in os.listdir(folder_path):
    # Check if the filename contains a market_id
    file_path = os.path.join(folder_path, filename)
    # If the filename (without extension) is in the market_ids list, print it
    if filename not in market_ids:
        print(f"{filename} has not been processed.")
    else:
        # If not, delete the file
        print(f"{filename} is in the list, deleting...")
        os.remove(file_path)

```

### Conclusion

In this tutorial we've taken our previously trained model, processed the model outputs into rated prices for the exchange markets, unzipped some historical files and run simulations using our rated prices!
In Part III we'll take our simulation output to decide what we can use to bet into future markets!

### Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.