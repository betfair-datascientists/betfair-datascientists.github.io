# Greyhound Modelling in Python using the Topaz API
Building a greyhound racing model using Python and Machine Learning

This tutorial is a refreshed version of our previous tutorials utilising the new version of the FastTrack API (now called Topaz). 
Topaz is a product provided to Betfair Australia & New Zealand customers by Greyhound Racing Victoria (GRV). 

If you would like your own Topaz API key, please contact us [here](mailto:data@betfair.com.au). 
Access can only be provided to Betfair Australia or New Zealand customers with active accounts

---
## Overview
This tutorial will walk you through the different steps required to generate Greyhound racing winning probabilities

1. Download historic greyhound data from Topaz API
1. Cleanse and normalise the data
1. Generate features using raw data
1. Build and train classification models
1. Evaluate models' performances
1. Evaluate feature importance

---
## Requirements
- Coding environment which supports Jupyter Notebooks (e.g. Visual Studio Code)
- Betfair API Key. If you don't have one please follow the steps outlined on the [The Automation Hub](https://betfair-datascientists.github.io/api/apiappkey/)
- Topaz API Key. If you would like to be considered for a Topaz key, please email [data@betfair.com.au](mailto:data@betfair.com.au) (Australian/New Zealand customers only).
- Python Topaz API wrapper. To install this package using pip, type 'pip install topaz_api' into your terminal

---
## Historic Data
To get started on building our own Topaz model, first we need to download the historic data from the Topaz API. The API has rate limits in place and so for the purposes of a bulk download of historic data, we will need to implement some way of handling these rate limits in order for us to download the data with a high degree of completeness. After all, the maxim 'Garbage In, Garbage Out' in regards to modelling holds true. If you don't feed your model good, complete data, then you won't have much success.

In the code block below, there are multiple instances of retries and programmed sleep functions to allow the rate limits to reset. We are also requesting the races for each state in blocks of 7 days.

NOTE: For state / date-range combinations where there are genuinely no races that occurred, the function will continuously error until it reaches the maximum specified retries before continuing to the next block. This may occur during the pandemic shutdown period in 2020 or the NSW Greyhound racing ban in 2017 or for time periods with the 'NT' jurisdiction where greyhound meetings may be up to 14 days apart.

```py title="Downloading Historic Data"
import pandas as pd
from tqdm import tqdm
import time
from datetime import datetime, timedelta
from topaz import TopazAPI
from sklearn.preprocessing import MinMaxScaler 
import numpy as np
import requests
import os

api_key = '' #Insert your API key 
topaz_api = TopazAPI(api_key)

# Your existing function to generate date range
def generate_date_range(start_date, end_date):
    start_date = start_date
    end_date = end_date

    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return date_list

# Example usage:
start_date = datetime(2024,2,19)
end_date = (datetime.today() - timedelta(days=1))

# Generate the date range
date_range = generate_date_range(start_date, end_date)

# Iterate over 7-day blocks
for i in range(0, len(date_range), 10):
    start_block_date = date_range[i]
    print(start_block_date)
    end_block_date = date_range[min(i + 9, len(date_range) - 1)]  # Ensure the end date is within the range

    codes = ['NT','VIC','NSW','SA','WA','QLD','TAS','NZ']
    for code in codes:
        all_races = []
        print(code)
        retries = 10  # Number of retries
        while retries > 0:
            try:
                races = topaz_api.get_races(from_date=start_block_date, to_date=end_block_date, owning_authority_code=code)
                all_races.append(races)
                break  # Break out of the loop if successful
            except requests.HTTPError as http_err:
                if http_err.response.status_code == 429:
                    retries -= 1
                    if retries > 0:
                        print(f"Rate limited. Retrying in 121 seconds...")
                        time.sleep(121)
                    else:
                        print("Max retries reached. Moving to the next block.")
                else:
                    print(f"Error fetching races for {code}: {http_err.response.status_code}")
                    retries -= 1
                    if retries > 0:
                        print(f"Retrying in 30 seconds...")
                        time.sleep(30)
                    else:
                        print("Max retries reached. Moving to the next block.")

        try:
            all_races_df = pd.concat([all_races], ignore_index=True)
        except ValueError:
            continue

        # Extract unique race IDs
        race_ids = list(all_races_df['raceId'].unique())

        for race_id in tqdm(race_ids, desc="Processing races", unit="race"):
            result_retries = 10
            
            while result_retries > 0:
                # Use tqdm to create a progress bar
                # Get race run data
                try:
                    race_run = topaz_api.get_race_runs(race_id=race_id)
                    race_result_json = topaz_api.get_race_result(race_id=race_id)
                    file_path = code + '_DATA.csv'
                    file_exists = os.path.isfile(file_path)
                    header_param = not file_exists
                    
                    race_result = pd.DataFrame.from_dict([race_result_json])
                    split_times_df = pd.DataFrame(race_result['splitTimes'].tolist(),index=race_result.index)
                    
                    splits_dict = split_times_df.T.stack().to_frame()
                    splits_dict.reset_index(drop=True, inplace= True)
                    splits_normalised = pd.json_normalize(splits_dict[0])
                    
                    if len(splits_normalised) == 0:
                        race_run.to_csv(code + '_DATA.csv', mode='a', header=header_param, index=False)
                        break

                    first_split = splits_normalised[splits_normalised['splitTimeMarker'] == 1]
                    first_split = first_split[['runId','position','time']]
                    first_split = first_split.rename(columns={'position':'firstSplitPosition','time':'firstSplitTime'})
                    second_split = splits_normalised[splits_normalised['splitTimeMarker'] == 2]
                    second_split = second_split[['runId','position','time']]
                    second_split = second_split.rename(columns={'position':'secondSplitPosition','time':'secondSplitTime'})

                    split_times = splits_normalised[['runId']]
                    split_times = pd.merge(split_times,first_split,how='left',on=['runId'])
                    split_times = pd.merge(split_times,second_split,how='left',on=['runId'])

                    race_run = pd.merge(race_run,split_times,how='left',on=['runId'])
                    race_run.drop_duplicates(inplace=True)
                    race_run.to_csv(code + '_DATA.csv', mode='a', header=header_param, index=False)
                    break
                except requests.HTTPError as http_err:
                    if http_err.response.status_code == 404:
                        file_path = code + '_DATA.csv'
                        file_exists = os.path.isfile(file_path)
                        header_param = not file_exists
                        race_run.to_csv(code + '_DATA.csv', mode='a', header=header_param, index=False)
                        break
                except Exception as e:
                    print(race_id)
                    result_retries -= 1
                    if result_retries > 0:
                        time.sleep(15)
                    else:
                        time.sleep(120)
```

---

The Topaz race results endpoint requires the passing of a jurisdiction ID as a parameter to pull the results. Simply passing a date range will return no data. This is why we have looped over all jurisdictions in 7 day blocks.

Bulk downloading the historical data in this way may take a while depending on how many years of data you are requesting. Bruno, the author of one of our previous greyhound modelling tutorials, uses 6 years worth of data for his backtesting. This however is computationally expensive to process in a machine learning model, so we suggest 2-3 years for those just starting out. 

NOTE: In the above code we have exported each state separately to its own csv file. This will keep each file under a million rows ensuring that you can manually inspect the data by opening the file in Excel. This is not required (we will pull in each file to our model before we begin to process the data)

## Cleaning the data

Let's pull all of our state files and get cleaning on this data!

```py title="Cleaning The Data"
codes = ['NT','VIC','NSW','SA','WA','QLD','TAS']

TopazData = pd.DataFrame()

for code in codes:
    StateData = pd.read_csv(code+'_DATA.csv',low_memory=False)
    StateData['state']=code
    TopazData = pd.concat([TopazData,StateData])

# Discard the columns which either have leakage or aren't that useful

TopazData = TopazData[['state',    
                    'track',
                    'distance',
                    'raceId',
                    'meetingDate',
                    'raceTypeCode',
                    'runId',
                    'dogId',
                    'dogName',
                    'weightInKg',
                    'gradedTo',
                    'rating',
                    'raceNumber',
                    'boxNumber',
                    'rugNumber',
                    'sex',
                    'trainerId',
                    'trainerState',
                    'damId',
                    'damName',
                    'sireId',
                    'sireName',
                    'dateWhelped',
                    'last5',
                    'pir',
                    'place',
                    'prizeMoney',
                    'resultTime',
                    'resultMargin']]

# Dropping all rows with no place - meaning the dog was scratched/reserve not used or the meeting is in the future or was abandoned
TopazData = TopazData.dropna(subset=['place'], how='all')    

# Dropping duplicate rows
TopazData.drop_duplicates(inplace=True)

# If you want to reset the index after dropping duplicates
TopazData.reset_index(drop=True, inplace=True)

# Let's correct the track names to align with Betfair names (Not all tracks in Topaz are on the exchange due to being closed or not hosting TAB-meetings)
# We're not using the NZ tracks in this tutorial, however they are included below for completeness
# The "Straight" tracks at Murray Bridge and Richmond are not differentiated on Betfair but we can treat these later.

TrackDict = {
    'Auckland (NZ)':'Manukau',
    'Christchurch (NZ)':'Addington',
    'Dport @ HOB':'Hobart',
    'Dport @ LCN':'Launceston',
    'Meadows (MEP)':'The Meadows',
    'Otago (NZ)':'Forbury Park',
    'Palmerston Nth (NZ)':'Manawatu',
    'Sandown (SAP)':'Sandown Park',
    'Southland (NZ)':'Ascot Park',
    'Tokoroa (NZ)':'Tokoroa',
    'Waikato (NZ)':'Cambridge',
    'Wanganui (NZ)':'Hatrick',
    'Taranaki (NZ)':'Taranaki',
    'Ashburton (NZ)':'Ashburton',
    'Richmond (RIS)':'Richmond Straight',
    'Murray Bridge (MBR)':'Murray Bridge',
    'Murray Bridge (MBS)':'Murray Bridge Straight'
}

TopazData['track'] = TopazData['track'].replace(TrackDict)

TopazData['meetingDate'] = pd.to_datetime(TopazData['meetingDate'])
TopazData['dateWhelped'] = pd.to_datetime(TopazData['dateWhelped'])

TopazData['dogName']=TopazData['dogName'].str.replace("'","")
TopazData['sireName']=TopazData['sireName'].str.replace("'","")
TopazData['damName']=TopazData['damName'].str.replace("'","")

TopazData['last5'] = TopazData['last5'].astype(str)

# Function to extract numbers from the 'last5' column
def extract_numbers(row):
    try:
        numbers = list(map(int, row.split('-')))
        # If there are fewer than 5 numbers, pad with zeros
        numbers += [10] * (5 - len(numbers))
        return numbers
    except ValueError:
        # Handle the case where the string cannot be split into integers
        return [10, 10, 10, 10, 10]

# Apply the function to create new columns for each position
TopazData[['positionLastRace', 'positionSecondLastRace', 'positionThirdLastRace',
    'positionFourthLastRace', 'positionFifthLastRace']] = TopazData['last5'].apply(extract_numbers).apply(pd.Series)


#Let's utilise our position columns to generate some win percentages
TopazData['lastFiveWinPercentage'] = ((TopazData[['positionLastRace', 'positionSecondLastRace', 'positionThirdLastRace','positionFourthLastRace', 'positionFifthLastRace']] == 1).sum(axis=1)) / ((TopazData[['positionLastRace', 'positionSecondLastRace', 'positionThirdLastRace','positionFourthLastRace', 'positionFifthLastRace']] != 10).sum(axis=1))
TopazData['lastFiveWinPercentage'].fillna(0,inplace=True)
TopazData['lastFivePlacePercentage'] = ((TopazData[['positionLastRace', 'positionSecondLastRace', 'positionThirdLastRace','positionFourthLastRace', 'positionFifthLastRace']] <= 3).sum(axis=1)) / ((TopazData[['positionLastRace', 'positionSecondLastRace', 'positionThirdLastRace','positionFourthLastRace', 'positionFifthLastRace']] != 10).sum(axis=1))
TopazData['lastFivePlacePercentage'].fillna(0,inplace=True)
TopazData.replace([np.inf, -np.inf], 0, inplace=True)

# Convert the 'pir' column to string
TopazData['pir'] = TopazData['pir'].fillna(0)
TopazData['pir'] = TopazData['pir'].astype(int).astype(str)

# Extract the second last letter and create a new column '2ndLastPIR'
TopazData['2ndLastPIR'] = TopazData['pir'].apply(lambda x: x[-2] if len(x) >= 2 else None)
TopazData['2ndLastPIR'].fillna(TopazData['place'],inplace=True)
TopazData['2ndLastPIR'] = TopazData['2ndLastPIR'].astype(int)

# Create a feature that calculates places gained/conceded in the home straight
TopazData['finishingPlaceMovement'] = TopazData['2ndLastPIR'] - TopazData['place']

TopazData['weightInKgScaled'] = TopazData.groupby('raceId')['weightInKg'].transform(lambda x: scaler.fit_transform(x.values.reshape(-1, 1)).flatten())

#Scale values as required
TopazData['prizemoneyLog'] = np.log10(TopazData['prizeMoney'] + 1)
TopazData['placeLog'] = np.log10(TopazData['place'] + 1)
TopazData['marginLog'] = np.log10(TopazData['resultMargin'] + 1)

# Calculate median winner time per track/distance
win_results = TopazData[TopazData['place'] == 1]

grouped_data = win_results.groupby(['track', 'distance', 'meetingDate'])['resultTime'].median().reset_index()

median_win_time = pd.DataFrame(grouped_data.groupby(['track', 'distance']).apply(lambda x: x.sort_values('meetingDate').set_index('meetingDate')['resultTime'].shift(1).rolling('365D', min_periods=1).median())).reset_index()
median_win_time.rename(columns={"resultTime": "runTimeMedian"},inplace=True)

median_win_time['speedIndex'] = (median_win_time['runTimeMedian'] / median_win_time['distance'])
median_win_time['speedIndex'] = MinMaxScaler().fit_transform(median_win_time[['speedIndex']])

# Merge with median winner time
TopazData = TopazData.merge(median_win_time, how='left', on=['track', 'distance','meetingDate'])

# Normalise time comparison
TopazData['runTimeNorm'] = (TopazData['runTimeMedian'] / TopazData['resultTime']).clip(0.9, 1.1)
TopazData['runTimeNorm'] = MinMaxScaler().fit_transform(TopazData[['runTimeNorm']])

# Sort the DataFrame by 'RaceId' and 'Box'
TopazData = TopazData.sort_values(by=['raceId', 'boxNumber'])

# Check if there is an entry equal to boxNumber + 1
TopazData['hasEntryBoxNumberPlus1'] = (TopazData.groupby('raceId')['boxNumber'].shift(1) == TopazData['boxNumber'] + 1) | (TopazData['boxNumber'] == 8)
TopazData['hasEntryBoxNumberMinus1'] = (TopazData.groupby('raceId')['boxNumber'].shift(-1) == TopazData['boxNumber'] - 1)
# Convert boolean values to 1
TopazData['hasEntryBoxNumberPlus1'] = TopazData['hasEntryBoxNumberPlus1'].astype(int)
TopazData['hasEntryBoxNumberMinus1'] = TopazData['hasEntryBoxNumberMinus1'].astype(int)
# Display the resulting DataFrame which shows adjacent Vacant Boxes
# Box 1 is treated as having a vacant box to the left always as we are looking how much space the dog has to move.
TopazData['adjacentVacantBoxes'] = 2 - TopazData['hasEntryBoxNumberPlus1'] - TopazData['hasEntryBoxNumberMinus1']
# Calculate 'hasAtLeast1VacantBox'
TopazData['hasAtLeast1VacantBox'] = (TopazData['adjacentVacantBoxes'] > 0).astype(int)

TopazData['win'] = TopazData['place'].apply(lambda x: 1 if x == 1 else 0)

grouped_data = TopazData.groupby(['track', 'distance', 'boxNumber', 'hasAtLeast1VacantBox', 'meetingDate'])['win'].mean().reset_index()
grouped_data.set_index('meetingDate', inplace=True)

# Apply rolling mean calculation to the aggregated data
box_win_percent = grouped_data.groupby(['track', 'distance', 'boxNumber', 'hasAtLeast1VacantBox']).apply(lambda x: x.sort_values('meetingDate')['win'].shift(1).rolling('365D', min_periods=1).mean()).reset_index()

# Reset index and rename columns
box_win_percent.columns = ['track', 'distance', 'boxNumber', 'hasAtLeast1VacantBox', 'meetingDate', 'rolling_box_win_percentage']

# Add to dog results dataframe
TopazData = TopazData.merge(box_win_percent, on=['track', 'distance', 'meetingDate','boxNumber','hasAtLeast1VacantBox'], how='left')
```

Here we've cleaned our dataset as much as we can. Next it's on to the feature creation!

## Create the features

```py title="Creating Basic Features"

# resultMargin has the same value for 1st and 2nd placed dogs, but should be 0 for the 1st placed dog.
TopazData.loc[TopazData['place'] == 1, ['resultMargin']] = 0

TopazData['dogAge'] = (TopazData['meetingDate'] - TopazData['dateWhelped']).dt.days
scaler = MinMaxScaler()
TopazData['dogAgeScaled'] = TopazData.groupby('raceId')['dogAge'].transform(lambda x: scaler.fit_transform(x.values.reshape(-1, 1)).flatten())


```
Now we've created some basic features, it's time to create our big group of features where we iterate over different subsets, variables and time points to generate a large number of different features

```py title="Creating Bulk Features"
import itertools

dataset = TopazData.copy()
dataset['meetingDate'] = pd.to_datetime(dataset['meetingDate'])

# Calculate values for dog, trainer, dam and sire
subsets = ['dog', 'trainer', 'dam', 'sire']

# Use rolling window of 28, 91 and 365 days
rolling_windows = ['28D','91D', '365D']

# Features to use for rolling windows calculation
features = ['runTimeNorm', 'placeLog', 'prizemoneyLog', 'marginLog','finishingPlaceMovement']

# Aggregation functions to apply
aggregates = ['min', 'max', 'mean', 'median', 'std']

# Keep track of generated feature names
feature_cols = []

for i in subsets:
    # Generate rolling window features
    idnumber = i + 'Id'

    subset_dataframe = dataset[['meetingDate',idnumber] + features]
    average_df = pd.DataFrame()

    for feature in features:
        # Group by 'damId' and 'meetingDate' and calculate the average of the current feature
        feature_average_df = subset_dataframe.groupby([idnumber, 'meetingDate'])[feature].mean().reset_index()
        # Rename the feature column to indicate it's the average of that feature
        feature_average_df.rename(columns={feature: f'{feature}{i}DayAverage'}, inplace=True)
    
        # If average_df is empty, assign the feature_average_df to it
        if average_df.empty:
            average_df = feature_average_df
        else:
            # Otherwise, merge feature_average_df with average_df
            average_df = pd.merge(average_df, feature_average_df, on=[idnumber, 'meetingDate'])

        # Assuming df is your DataFrame
    column_names = average_df.columns.tolist()
    # Columns to exclude
    columns_to_exclude = [idnumber,'meetingDate']
    # Exclude specified columns from the list
    column_names_filtered = [col for col in column_names if col not in columns_to_exclude]

    average_df.drop_duplicates(inplace=True)
    average_df['meetingDate'] = pd.to_datetime(average_df['meetingDate'])
    average_df = average_df.set_index([idnumber, 'meetingDate']).sort_index() 

    for rolling_window in rolling_windows:
        print(f'Processing {i} rolling window {rolling_window} days')

        rolling_result = (
            average_df
            .reset_index(level=0)
            .groupby(idnumber)[column_names_filtered]
            .rolling(rolling_window)  # Use timedelta for rolling window
            .agg(aggregates)
            .groupby(level=0)
            .shift(1)
        )

        # Generate list of rolling window feature names (eg: RunTime_norm_min_365D)
        agg_features_cols = [f'{i}_{f}_{a}_{rolling_window}' for f, a in itertools.product(features, aggregates)]
        # Add features to dataset
        average_df[agg_features_cols] = rolling_result
        # Keep track of generated feature names
        feature_cols.extend(agg_features_cols)
        average_df.fillna(0, inplace=True)
    
    average_df.reset_index(inplace=True)
    dataset = pd.merge(dataset,average_df,on=[idnumber, 'meetingDate'])

# Only keep data 12 months after the start date of your dataset since we've used a 365D rolling timeframe for some features
feature_cols = np.unique(feature_cols).tolist()
dataset = dataset[dataset['meetingDate'] >= '2021-01-01']
dataset = dataset[[
                'meetingDate',
                'state',
                'track',
                'distance',
                'raceId',
                'raceTypeCode',
                'raceNumber',
                'boxNumber',
                'rugNumber',
                'runId',
                'dogId',
                'dogName',
                'weightInKg',
                'sex',
                'trainerId',
                'trainerState',
                'damId',
                'damName',
                'sireId',
                'sireName',
                'win',
                'dogAgeScaled',
                'lastFiveWinPercentage',
                'lastFivePlacePercentage',
                'weightInKgScaled',
                'rolling_box_win_percentage']
                 + feature_cols
                ]

feature_cols.extend(['dogAgeScaled',
                'lastFiveWinPercentage',
                'lastFivePlacePercentage',
                'weightInKgScaled',
                'rolling_box_win_percentage'])

#The below line will output your dataframe to a csv but may be too large to open in Excel.
#dataset.to_csv('testing.csv',index=False)

```

Now that we've created our features, lets feed them into our Machine Learning Algorithm to generate some probabilities!

## Training

```py title="Training the model"

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression

# Gradient Boosting Machines libraries
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

# Common models parameters
verbose       = 0
learning_rate = 0.1
n_estimators  = 500

# Train different types of models
models = {
    'GradientBoostingClassifier': GradientBoostingClassifier(verbose=verbose, learning_rate=learning_rate, n_estimators=n_estimators, max_depth=8, max_features=8),
    'RandomForestClassifier':     RandomForestClassifier(verbose=verbose, n_estimators=n_estimators, max_depth=20, max_features=8, min_samples_leaf=5,min_samples_split=10),
    'LGBMClassifier':             LGBMClassifier(learning_rate=learning_rate, n_estimators=n_estimators, force_col_wise=True,num_leaves=80,verbose=-1),
    'XGBClassifier':              XGBClassifier(verbosity=verbose, learning_rate=learning_rate, n_estimators=n_estimators, max_depth = 8, subsample = 1.0, objective='binary:logistic'),
    'CatBoostClassifier':         CatBoostClassifier(verbose=verbose, learning_rate=learning_rate, n_estimators=n_estimators, depth=8, l2_leaf_reg=10),
    'KNeighborsClassifier':       KNeighborsClassifier(n_neighbors=15,weights='distance',p=2),
    'DecisionTreeClassifier':     DecisionTreeClassifier(max_depth=20,min_samples_split=10,min_samples_leaf=5,max_features=8),
    'MLPClassifier':              MLPClassifier(hidden_layer_sizes=100,activation='relu',solver='adam', alpha=0.0001),
    'AdaBoostClassifier':         AdaBoostClassifier(n_estimators=n_estimators,learning_rate=learning_rate,algorithm='SAMME'),
    'GuassianNB':                 GaussianNB(),
    'QuadDiscriminantAnalysis':   QuadraticDiscriminantAnalysis(),
    'LogisticsRegression':        LogisticRegression(verbose=0, solver='liblinear',max_iter=5000000, C=10,penalty='l2')
}

import pickle
from sklearn.metrics import log_loss
import time

dataset.fillna(0,inplace=True)

# Split the data into train and test data
train_data = dataset[dataset['meetingDate'] < '2023-01-01'].reset_index(drop=True)
test_data = dataset[dataset['meetingDate'] >= '2023-01-01'].reset_index(drop=True)

train_x, train_y = train_data[feature_cols], train_data['win']
test_x, test_y = test_data[feature_cols], test_data['win']

for key, model in models.items():
    print(f'Fitting model {key}')
    start_time = time.time()  # Record start time
    model.fit(train_x, train_y)
    end_time = time.time()  # Record end time
    print(f"Training time for {key}: {end_time - start_time} seconds")
    # Calculate log loss
    train_preds = model.predict_proba(train_x)
    train_loss = log_loss(train_y, train_preds)
    print(f"Log loss for {key} on train data: {train_loss}")


# Calculate probabilities for each model on the test dataset
probs_columns = ['StartPrice_probability']

for key, model in models.items():
    probs_column_key = f'prob_{key}'
    # Calculate runner win probability
    dog_win_probs = model.predict_proba(test_x)[:, 1]
    test_data[probs_column_key] = dog_win_probs
    # Normalise probabilities
    test_data[probs_column_key] = test_data.groupby('raceId', group_keys=False)[f'prob_{key}'].apply(
        lambda x: x / sum(x))
    predicted_winners = test_data.groupby('raceId', group_keys=False)[f'prob_{key}'].apply(lambda x: x == max(x))
    probs_columns.append(probs_column_key)
    # Dump the pickle
    with open(key + '_.pickle.dat', 'wb') as f:
        pickle.dump(model, f)

test_data.to_csv('testing_set_predictions.csv', index=False)

```

Alright, now that we've trained the models, let's have a look at the log loss calculations for each model and the time taken to train each model

|Model|Training Time|Log Loss|
|--------------------------------|-------|-------|
|AdaBoostClassifier|6248|0.532|
|XGBClassifier|2599|0.278|
|RandomForestClassifier|1930|0.269|
|MLPClassifier|1513|0.376|
|GradientBoostingClassifier|1278|0.308|
|LogisticsRegression|492|0.378|
|CatBoostClassifier|200|0.355|
|LGBMClassifier|92|0.305|
|QuadDiscriminantAnalysis|29|3.641|
|DecisionTreeClassifier|6|0.278|
|GuassianNB|3|7.015|
|KNeighborsClassifier|1|0.00000935|

As we can see some models took a lot longer than others to train, with the longest being the AdaBoostClassifier taking close to 2 hours and KNeighbours Classifier at 1 second. 
The log loss values also differ significantly between models. We've only used one set of parameters for training each model. You could try using a GridSearch to find the best parameters for each model.

Another method of comparing the accuracy of a model is the Brier Score. Let's compare the Brier score for a couple of the highest performing models (i.e. with the lowest log loss) and graph the feature importance for one of the models.

Here's a great explanation of the differences between log loss and Brier score for machine learning models - [more info](https://www.dratings.com/log-loss-vs-brier-score/)

```py title="Finding the Brier Score and finding feature importance"
from sklearn.metrics import brier_score_loss
import matplotlib.pyplot as plt

# Calculate Brier score for each model on the test data
brier_scores = {}
for key, model in models.items():
    prob_col_key = f'prob_{key}'
    brier_score = brier_score_loss(test_y, test_data[prob_col_key])
    brier_scores[key] = brier_score
    print(f"Brier score for {key}: {brier_score}")

# Plot feature importance for each model
for key, model in models.items():
    if hasattr(model, 'feature_importances_'):
        plt.figure(figsize=(10, 70))
        if hasattr(model, 'plot_importance'):
            model.plot_importance(ax=plt.gca(), importance_type='gain', title=f'Feature Importance - {key}')
        else:
            feature_importance = model.feature_importances_
            sorted_idx = np.argsort(feature_importance)
            plt.barh(train_x.columns[sorted_idx], feature_importance[sorted_idx])
            plt.xlabel("Feature Importance")
            plt.ylabel("Features")
            plt.title(f"Feature Importance - {key}")
        plt.show()
    else:
        print(f"No feature importance available for {key}")

```

```
Brier score for LGBMClassifier: 0.11015042860939694
Brier score for LogisticsRegression: 0.10978107663467736
```

![png](../img/featureImportanceLGBM.png)

## To be continued

The next step will be to do some backtesting on prior results to find a profitable betting angle

## Disclaimer

Note that whilst models and automated strategies are fun and rewarding to create, we can't promise that your model or betting strategy will be profitable, and we make no representations in relation to the code shared or information on this page. If you're using this code or implementing your own strategies, you do so entirely at your own risk and you are responsible for any winnings/losses incurred. Under no circumstances will Betfair be liable for any loss or damage you suffer.