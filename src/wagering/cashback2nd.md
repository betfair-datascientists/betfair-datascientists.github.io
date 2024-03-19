# Cashback 2nd - New Markets

In February 2024, Betfair Australia launched a new product on Australian Greyhound and Thoroughbred racing markets called 'Cashback 2nd' with a market type of 'MONEY_BACK_2ND'
In these markets the runner who finishes in second place will have all bets voided before the market is settled (this includes lay bets)

How could you go about calculating a fair price for a runner in this market? Well, lets discuss how you can do that just by the using the price available for the runner in the regular 'WIN' market.
This approach uses the data found [here](https://betfair-datascientists.github.io/data/dataListing/) as an example

## The Code

``` py title="Loading the data"

import pandas as pd

# Read the data
cashbacksecond = pd.read_csv('ANZ_Greyhounds_2024_02.csv')

# Select relevant columns
cashbacksecond = cashbacksecond[['LOCAL_MEETING_DATE','TRACK','STATE_CODE','RACE_NO','WIN_MARKET_ID','SELECTION_ID','TAB_NUMBER','SELECTION_NAME','BEST_AVAIL_BACK_AT_SCHEDULED_OFF']]

# Calculate IMPLIED_WIN_PERCENTAGE
cashbacksecond['IMPLIED_WIN_PERCENTAGE'] = 1/cashbacksecond['BEST_AVAIL_BACK_AT_SCHEDULED_OFF']

# Calculate BMP (Back Market Percentage) (i.e. Overround)
cashbacksecond['BMP'] = cashbacksecond.groupby('WIN_MARKET_ID')['IMPLIED_WIN_PERCENTAGE'].transform('sum')

# Calculate SCALED_WIN_PROBABILITY
cashbacksecond['SCALED_WIN_PROBABILITY'] = cashbacksecond['IMPLIED_WIN_PERCENTAGE']/cashbacksecond['BMP']

```
Here we've calculated our efficient win price based on the best available price at the scheduled off by removing the effect of the overround.

``` py title="Assign the win probability of all other runners in the race"

# Get unique tab numbers
unique_tab_numbers = cashbacksecond['TAB_NUMBER'].unique()

# Create sub-dataframes for each unique tab_number
sub_dataframes = []
for tab_number in unique_tab_numbers:
    # Filter the main DataFrame based on 'TAB_NUMBER' == X
    sub_df = cashbacksecond[cashbacksecond['TAB_NUMBER'] == tab_number][['WIN_MARKET_ID', 'SCALED_WIN_PROBABILITY']]
    # Rename the 'IMPLIED_WIN_PERCENTAGE' column to 'IMPLIED_WIN_PERCENTAGE_{X}'
    sub_df = sub_df.rename(columns={'SCALED_WIN_PROBABILITY': f'SCALED_WIN_PROBABILITY_{tab_number}'})
    # Append the sub-dataframe to the list
    sub_dataframes.append(sub_df)

# Merge sub-dataframes back to the main dataframe
for sub_df in sub_dataframes:
    cashbacksecond = pd.merge(cashbacksecond, sub_df, on=['WIN_MARKET_ID'], how='left')

cashbacksecond = cashbacksecond.fillna(0)
cashbacksecond = cashbacksecond.drop_duplicates()

```

Now to assign the proper cashback price we need to subtract the percentage of the market that represents the runner that will be voided and then renormalise the probabilities for the remaining outcomes

``` py title="Calculate probability of winning given that a certain dog comes 2nd"

# Calculate probability of winning given that a certain dog comes 2nd
for tab_number in unique_tab_numbers:
    # Calculate the denominator (1 - Probability_Second_{X})
    # This is the line where we remove the cashback2nd runner from our market
    denominator = 1 - cashbacksecond[f'SCALED_WIN_PROBABILITY_{tab_number}']
    # Create the new column Prob_Win_With_2nd_Dog_Being_{X}
    cashbacksecond[f'Prob_Win_With_2nd_Dog_Being_{tab_number}'] = cashbacksecond['SCALED_WIN_PROBABILITY'] / denominator
    # If Probability_Second_{tab_number} is 0, set Prob_Win_With_2nd_Dog_Being_{tab_number} to 0
    cashbacksecond.loc[cashbacksecond[f'SCALED_WIN_PROBABILITY_{tab_number}'] == 0, f'Prob_Win_With_2nd_Dog_Being_{tab_number}'] = 0
    # If 'TAB_NUMBER' equals tab_number, set Prob_Win_With_2nd_Dog_Being_{tab_number} to 0
    cashbacksecond.loc[cashbacksecond['TAB_NUMBER'] == tab_number, f'Prob_Win_With_2nd_Dog_Being_{tab_number}'] = 0

```

Finally lets assign the sum the probabilities across all outcomes, renormalise and assign the cashback prices. 
It is expected that the efficient market overround will be over 100% to deal with the runner being voided. This is normal for back markets but not usually for lay markets.

If you wanted to calculate a price where you wanted to include an edge for yourself, you would multiply the column 'CASHBACK_WIN_PERCENTAGE' by a number greater than 1 for lay bets and less than 1 for back bets.
This implies that should those bets get matched, you have positive expected value on these bets.

``` py title="Calculate and assign the cashback prices"

# Select the relevant columns
prob_columns = [f'Prob_Win_With_2nd_Dog_Being_{tab_number}' for tab_number in unique_tab_numbers]
# Sum the selected columns row-wise
total_probability = cashbacksecond[prob_columns].sum(axis=1)
# Count the number of non-zero entries in the selected columns
non_zero_count = (cashbacksecond[prob_columns] != 0).sum(axis=1)
# Divide the total probability by the count of non-zero entries to get the average
cashback_percentage = total_probability / non_zero_count
# Assign the calculated average to the 'CASHBACK_WIN_PERCENTAGE' column
cashbacksecond['CASHBACK_WIN_PERCENTAGE'] = cashback_percentage
# Assign the cashback price
cashbacksecond['CASHBACK_PRICE'] = 1 / cashbacksecond['CASHBACK_WIN_PERCENTAGE']
# Remove unnecessary columns
cashbacksecond=cashbacksecond[['LOCAL_MEETING_DATE','TRACK','STATE_CODE','RACE_NO','WIN_MARKET_ID','SELECTION_ID','TAB_NUMBER','SELECTION_NAME','BEST_AVAIL_BACK_AT_SCHEDULED_OFF','CASHBACK_PRICE']]
# Print the first few rows of the dataframe
print(cashbacksecond.head)
# Export to csv
cashbacksecond.to_csv('Cashback2nd_Probabilities.csv',index=False)

```

LOCAL_MEETING_DATE | TRACK | RACE_NO | WIN_MARKET_ID | SELECTION_ID | TAB_NUMBER | SELECTION_NAME |  WIN_PRICE |  CASHBACK_PRICE
----------|-------------|---|-----------|----------|---|-----------------|---------|-------
1/02/2024 | Albion Park | 1 | 224245223 | 62990490 | 2 | Cleopatra Hayze |  $2.22  |  $2.07
1/02/2024 | Albion Park | 1 | 224245223 | 65520447 | 3 | Bounding Over |  $6.40  |  $5.54
1/02/2024 | Albion Park | 1 | 224245223 | 65328340 | 1 | Whistle Away |  $7.80  |  $6.72
1/02/2024 | Albion Park | 1 | 224245223 | 65520448 | 4 | Gone On Green |  $9.80  |  $8.41
1/02/2024 | Albion Park | 1 | 224245223 | 65520449 | 8 | Serrai |  $10.00  |  $8.58
1/02/2024 | Albion Park | 1 | 224245223 | 64876290 | 7 | Snowy Waugh |  $18.00  |  $15.34
1/02/2024 | Albion Park | 1 | 224245223 | 54266223 | 6 | Pocket Say Itch |  $50.00  |  $42.42
1/02/2024 | Albion Park | 1 | 224245223 | 59147471 | 5 | City Steamer |  $170.00  |  $143.99

## Conclusion

This approach can also be used to calculate place market probabilities (though be aware that the complexity will be much higher for a 3rd or 4th place market than just a 2nd place market) as well as exotics like quinellas and exactas.
Here we've just used a win market price to calculate a price for the cashback 2nd market, but this approach can easily be applied to a model's rated place like the Betfair Hub Thoroughbred and Greyhound predictions models!

If you have any questions or want to learn more, [join the Discord server](https://forms.office.com/r/ZG9ea1xQj1) or Australian/New Zealand customers can email us at automation@betfair.com.au. 

We're also endeavouring to provide a simple excel tool for this purpose so watch this space!