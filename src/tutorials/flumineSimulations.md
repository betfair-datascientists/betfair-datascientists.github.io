# Simulating Past Betfair Markets

It seems to be a common experience of designing and backtesting a model using a csv dataset, only to find that the behaviour of the model in production doesn't match the backtesting.
There could be instances of not being matched despite being at the front of the queue or just some weird unexplainable behaviour in the markets.

Thankfully Flumine, the python wrapper for the Betfair API, natively has a simulation mode that can be used to playback the historic data files and simulate placing bets in the market.
We have run through how to process a small set of markets in simulation model in our [How To Automate Series](../How_to_Automate_5.md) tutorials.
So powerful is the simulation mode however, that it deserves its own standalone tutorial!

## Limitations

The historic data files and their use in simulation mode have some limitations compared to using the live API.

 - Market Catalogue is not included in the historic stream files, so things like Runner Metadata cannot be accessed from the stream files
 - Cross matching (Virtual Bets) is also not included in the historic stream files, though for racing this should have limited impact
 - Live markets react to changes in volume on the exchange, so there will be no data on how any simulated bets would have affected other players in the market. This is salient if you wanted to test a strategy utilising large bet sizes or on high odds selections or using a trading model

This tutorial will utilise the PRO level files only, and has not been tested on the BASIC or ADVANCED level files. Australian and New Zealand customers can reach out to us at [data@betfair.com.au](mailto:data@betfair.com.au) to gain access to the PRO data files

## Tutorial Outline

In this tutorial, we will:

 - Create a list of market ids from publicly available CSV files
 - Unzip the .tar files and decompress the stream files only for the markets we're interested in
 - Run the simulation on our racing win markets (Code will be provided for Harness, Greyhounds and Thoroughbred Simulations)
 - Process the output of listClearedOrders to understand where we might find an angle

The important thing that we'll test here is entering the market at different points in time relative to the scheduled race time to determine if we can find better prices (both back and lay) depending on how far out from the off we decide to enter the market!