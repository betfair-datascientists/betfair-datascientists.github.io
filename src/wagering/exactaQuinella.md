# Racing Exotics Markets

A common market type used by traditional bookmakers is the Exacta or Quinella where a punter will bet on the combination of runners coming in first and second place in a given race. In the case of the exacta, this is the first and second runner in order, whereas the quinella disregards the order. This is traditionally done utilising a tote pool instead of fixed odds, however Betfair offers these markets in a traditional format where punters can back and lay these combinations at fixed odds prices. 

How could you go about calculating a fair price for a runner in these markets? Well, lets discuss how you can do that just by the using the price available for the runner in the regular 'WIN' market.
This approach uses the data found [here](https://betfair-datascientists.github.io/data/dataListing/) as an example

## The Code

``` py title="Loading the data"

import pandas as pd

# Read the data
exacta_quinella = pd.read_csv('ANZ_Greyhounds_2024_02.csv')

# Select relevant columns
exacta_quinella = exacta_quinella[['LOCAL_MEETING_DATE','TRACK','STATE_CODE','RACE_NO','WIN_MARKET_ID','SELECTION_ID','TAB_NUMBER','SELECTION_NAME','BEST_AVAIL_BACK_AT_SCHEDULED_OFF']]

# Calculate IMPLIED_WIN_PERCENTAGE
exacta_quinella['IMPLIED_WIN_PERCENTAGE'] = 1/exacta_quinella['BEST_AVAIL_BACK_AT_SCHEDULED_OFF']

# Calculate BMP (Back Market Percentage) (i.e. Overround)
exacta_quinella['BMP'] = exacta_quinella.groupby('WIN_MARKET_ID')['IMPLIED_WIN_PERCENTAGE'].transform('sum')

# Calculate SCALED_WIN_PROBABILITY
exacta_quinella['SCALED_WIN_PROBABILITY'] = exacta_quinella['IMPLIED_WIN_PERCENTAGE']/exacta_quinella['BMP']

```
Here we've calculated our efficient win price based on the best available price at the scheduled off by removing the effect of the overround.

``` py title="Assign the win probability of all other runners in the race"

# Get unique values from the 'TAB_NUMBER' column
unique_tab_numbers = exacta_quinella['TAB_NUMBER'].unique()

# Create a list to store sub-dataframes
sub_dataframes = []

# Create sub-dataframes for each unique value of 'TAB_NUMBER'
for tab_number in unique_tab_numbers:
    # Filter the main DataFrame based on 'TAB_NUMBER' == X
    sub_df = exacta_quinella[exacta_quinella['TAB_NUMBER'] == tab_number][['WIN_MARKET_ID', 'SCALED_WIN_PROBABILITY']]
    
    # Rename the 'IMPLIED_WIN_PERCENTAGE' column to 'IMPLIED_WIN_PERCENTAGE_{X}'
    sub_df = sub_df.rename(columns={'SCALED_WIN_PROBABILITY': f'SCALED_WIN_PROBABILITY_{tab_number}'})
    
    # Append the sub-dataframe to the list
    sub_dataframes.append(sub_df)

# Merge sub-dataframes back to the main dataframe on 'WIN_MARKET_ID'
for sub_df in sub_dataframes:
    exacta_quinella = pd.merge(exacta_quinella, sub_df, on=['WIN_MARKET_ID'], how='left')

# Now exacta_quinella DataFrame contains the new columns with the 'IMPLIED_WIN_PERCENTAGE_{X}' for each TAB_NUMBER
exacta_quinella = exacta_quinella.fillna(0)
exacta_quinella = exacta_quinella.drop_duplicates()

```
Now lets calculate the probability of each runner finishing second to every other runner.

``` py title="Calculate probability of winning given that a certain dog comes 2nd"

# Calculate probability of winning given that a certain dog comes 2nd
for tab_number in unique_tab_numbers:
    # Calculate the denominator (1 - IMPLIED_WIN_PERCENTAGE_{X})
    denominator = 1 - exacta_quinella[f'SCALED_WIN_PROBABILITY_{tab_number}']
    
    # Calculate the 'Probability_Second_Given_{X}_Wins' column, handling the case where 'IMPLIED_WIN_PERCENTAGE_{X}' is 0
    exacta_quinella[f'Probability_Second_Given_{tab_number}_Wins'] = exacta_quinella['SCALED_WIN_PROBABILITY'] / denominator
    exacta_quinella.loc[exacta_quinella[f'SCALED_WIN_PROBABILITY_{tab_number}'] == 0, f'Probability_Second_Given_{tab_number}_Wins'] = 0

    # If 'TAB_NUMBER' equals tab_number, set Prob_Win_With_2nd_Dog_Being_{tab_number} to 0
    exacta_quinella.loc[exacta_quinella['TAB_NUMBER'] == tab_number, f'Probability_Second_Given_{tab_number}_Wins'] = 0

```

Now lets create two dataframes containing each runner finishing in first and second positions

``` py title="Setting up for creating the exotic combinations"

# Define the columns to include in the new DataFrame
columns_to_include = ['WIN_MARKET_ID','TAB_NUMBER']

# Add the scaled win probability and probability second columns for each tab_number
for tab_number in unique_tab_numbers:
    columns_to_include.extend([f'Probability_Second_Given_{tab_number}_Wins'])

# Create the new DataFrame 'exacta' by selecting the specified columns from 'greyhounds'
exacta_second = exacta_quinella[columns_to_include].copy()
exacta_second.rename(columns={'TAB_NUMBER': 'exacta_second'}, inplace=True)

columns_to_include = ['WIN_MARKET_ID','TAB_NUMBER','SCALED_WIN_PROBABILITY']

# Create the new DataFrame 'exacta' by selecting the specified columns from 'greyhounds'
exacta_first = exacta_quinella[columns_to_include].copy()
exacta_first = exacta_first.drop_duplicates()

exacta_first.rename(columns={'TAB_NUMBER': 'exacta_first'}, inplace=True)
# Now 'exacta_seconds' DataFrame contains the required columns
exacta_first.head

```

Next up is to assign every other runner to finish second to one runner with the runner's win probability in the exacta first table and to assign every other runner to beat to one runner with the runner's probability to finish second given that the other runner has won in the exacta second table. We'll then merge the tables at the end.

```py title="Assigning probability of first and second given first outcome probabilities to every outcome"
exacta_first_list = []
exacta_second_list = []

# Step 1: Iterate over unique tab_numbers in exacta_first
for tab_number in exacta_first['exacta_first'].unique():
    # Step 2: Create a sub-dataframe from exacta_first
    sub_exacta_first = exacta_first[exacta_first['exacta_first'] == tab_number].copy()
    sub_exacta_first = exacta_first[['WIN_MARKET_ID', 'exacta_first', 'SCALED_WIN_PROBABILITY']].copy()
    sub_exacta_first['exacta_second'] = tab_number
    # Append sub-dataframe to the list
    exacta_first_list.append(sub_exacta_first)

exacta_first_combined = pd.DataFrame()
# Concatenate all sub-dataframes into one dataframe called 'exacta_first_combined'
for i in exacta_first_list:
    exacta_first_combined = pd.concat([exacta_first_combined,i], ignore_index=True)

exacta_first_combined = exacta_first_combined.reset_index(drop=True)
exacta_first_combined = exacta_first_combined[exacta_first_combined['SCALED_WIN_PROBABILITY'] != 0]
exacta_first_combined = exacta_first_combined.dropna(subset=['SCALED_WIN_PROBABILITY'])

exacta_second_combined = pd.DataFrame()

# Step 3: Iterate over unique tab_numbers in exacta_second
for tab_number_2 in exacta_second['exacta_second'].unique():
    # Step 4: Create a sub-dataframe from exacta_second
    sub_exacta_second = exacta_second[exacta_second['exacta_second'] != tab_number_2].copy()
    sub_exacta_second = sub_exacta_second[['WIN_MARKET_ID', 'exacta_second', f'Probability_Second_Given_{tab_number_2}_Wins']].copy()
    sub_exacta_second.rename(columns={f'Probability_Second_Given_{tab_number_2}_Wins': 'Probability_Second_Given_Wins'}, inplace=True)
    sub_exacta_second['exacta_first'] = tab_number_2
    # Append sub-dataframe to the list
    exacta_second_list.append(sub_exacta_second)
    
for i in exacta_second_list:
    # Concatenate all sub-dataframes into one dataframe called 'exacta_second_combined'
    exacta_second_combined = pd.concat([exacta_second_combined,i], ignore_index=True)

exacta_second_combined = exacta_second_combined.reset_index(drop=True)
exacta_second_combined = exacta_second_combined[exacta_second_combined['Probability_Second_Given_Wins'] != 0]
exacta_second_combined = exacta_second_combined.dropna(subset=['Probability_Second_Given_Wins'])

exacta_combinations = pd.merge(exacta_first_combined, exacta_second_combined, how='left', on=['WIN_MARKET_ID','exacta_first','exacta_second'])

```

Finally we'll calculate the exacta probability by multiplying these two probabilites together. The quinella probability is found by simply adding the probability of the exacta combination with reverse selections.

E.g. Quinella Prob (1-2) = Exacta Prob (1-2) + Exacta Prob (2-1)

```py title="What are the odds?"
# Create a new column for exacta combinations
exacta_combinations['exacta_combination'] = exacta_combinations['exacta_first'].astype(str) + ' | ' + exacta_combinations['exacta_second'].astype(str)

# Create a column for exacta odds
exacta_combinations['exacta_probability'] = exacta_combinations['SCALED_WIN_PROBABILITY'] * exacta_combinations['Probability_Second_Given_Wins']
# Assuming exacta_combinations is your DataFrame containing the combinations
exacta_combinations = exacta_combinations[exacta_combinations['exacta_first'] != exacta_combinations['exacta_second']]
exacta_combinations = exacta_combinations.dropna(subset=['exacta_probability'])

# Create a copy of the DataFrame with columns 'WIN_MARKET_ID', 'exacta_second', 'exacta_first', 'exacta_odds'
exacta_combinations_reverse = exacta_combinations[['WIN_MARKET_ID', 'exacta_second', 'exacta_first', 'exacta_probability']].copy()
exacta_combinations_reverse.rename(columns={'exacta_probability':'reverse_exacta','exacta_first':'exacta_first_reverse','exacta_second':'exacta_second_reverse'},inplace=True)

# Merge the reverse dataframe together with the original dataframe to find the exacta probability for the reverse combination
exacta_combinations=pd.merge(exacta_combinations,exacta_combinations_reverse,how='left',left_on = ['WIN_MARKET_ID', 'exacta_first', 'exacta_second'],right_on = ['WIN_MARKET_ID', 'exacta_second_reverse', 'exacta_first_reverse'])
exacta_combinations['exacta_odds'] = 1/exacta_combinations['exacta_probability']

# Calculating quinella_odds by summing the exacta_odds for each combination
exacta_combinations['quinella_probability'] = exacta_combinations['exacta_probability']+exacta_combinations['reverse_exacta']
exacta_combinations['quinella_odds'] = 1/exacta_combinations['quinella_probability']

# Discard extra columns
exacta_combinations=exacta_combinations[['WIN_MARKET_ID','exacta_first','exacta_second','exacta_combination','exacta_probability','exacta_odds','quinella_probability','quinella_odds']]

# Display the result
print(exacta_combinations)
exacta_combinations.to_csv('exacta_combinations.csv',index=False)
```

## Conclusion

This approach can also be used to calculate place market probabilities by simply finding the average probability of the runner finishing second (though be aware that the complexity will be much higher for a 3rd or 4th place market than just a 2nd place market).
Here we've just used a win market price to calculate a price for the exacta and quinella markets, but this approach can easily be applied to a model's rated place like the Betfair Hub Thoroughbred and Greyhound predictions models!

If you have any questions or want to learn more, [join the Discord server](https://forms.office.com/r/ZG9ea1xQj1) or Australian/New Zealand customers can email us at automation@betfair.com.au. 

We've also done this in a simple excel sheet to use for a single race - [Download Excel](../assets/RacingCalculatorTool.xlsx)