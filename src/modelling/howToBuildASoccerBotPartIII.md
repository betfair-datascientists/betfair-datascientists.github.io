# How To Build A Betfair Soccer Bot Part 3

This is a continuation of the tutorial - [How To Build A Betfair Soccer Bot Part 2](../modelling/howToBuildASoccerBotPartII.md)

**"I've done my simulations, now how I use it to bet with?"**

The previous tutorial describes how to run simulations on historical stream files using what I call a "shotgun" approach; where we bet on everything (both backing and laying) and then analyse the simulation results to determine a profitable angle.

To do this, we'll need to group selections together so as not to overfit. For market like Over/Under 1.5 Goals, the selection names are always the same and so this is straightforward but for any market where the team name is in the selection id, we'd want to group the selections together using a different characteristic related to each selection. In racing, this might be by grouping together runners by barrier groups, whereas in sports this is usually by utilising the home/away status of each team.

So the next code block will process our simulation results and initiate a selection grouping column where we can apply changes depending on the home/away status of the team and the market type. Once we've grouped together our markets we'll create some cha