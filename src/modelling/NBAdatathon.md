# Betfair’s 2024 NBA Datathon

![NBA Datathon Banner](../img/NBA_DATATHON_BANNER.png)

## Registration

Registrations are closed

---

## The Competition

Think you’ve got what it takes to predict NBA scorelines? Now’s your chance to showcase your data modeling skills in Betfair’s 2024 NBA Datathon!

With **$5,000 in prizes** on offer, this is your opportunity to create a predictive model for the 2024-2025 NBA Season. Whether you're a seasoned pro or new to sports modeling, we encourage you to get creative—adapt your skills from other fields, improve an existing model, or start fresh!

This year’s Datathon features **103 matches** from the 2024-2025 NBA Regular Season, and we challenge you to test your skills against others for both **prizes** and **ultimate bragging rights**.

- Leaderboard updates will be posted here throughout the competition, so check back often.
- Join the conversation in the Quants Discord server (#datathon channel), where you can discuss models with fellow participants.
- Don't forget to complete the [registration form](https://forms.office.com/r/ZG9ea1xQj1) to join the Discord Server.

For questions and submissions, contact [datathon@betfair.com.au](mailto:datathon@betfair.com.au).

---

## The Specifics

Review the full Terms and Conditions for the 2024 NBA Datathon [here](../assets/NBA_Datathon_2024_TCs.pdf).

### Prizes

**$5,000 in prizes** are up for grabs! Here's the breakdown of the prize pool:

| Place | Prize     |
|-------|-----------|
| 1     | $2,500.00 |
| 2     | $1,000.00 |
| 3     | $500.00   |
| 4     | $250.00   |
| 5     | $250.00   |
| 6     | $100.00   |
| 7     | $100.00   |
| 8     | $100.00   | 
| 9     | $100.00   | 
| 10    | $100.00   |
| **Total Prize Pool** | **$5,000.00** |

Winners will be announced at the end of the competition, with prizes distributed shortly afterward.

### Competition Rules

Entrants will receive a bespoke set of historical NBA player data for all matches from the 2019-2020 season to the present. Your goal is to build a model to predict:

- **Home Team Handicap**
- **Total Match Points Scored by Both Teams**

How you build your model is entirely up to you—whether it's an Elo model, regression, Machine Learning, or something else, the creativity is in your hands.

Submit your predictions by these deadlines:

- **10:59pm AEDT** for matches starting **before 10:00am AEDT** the following day.
- **8:59am AEDT** for matches starting **at or after 10:00am AEDT**.

See the full Terms and Conditions for more competition rules.

---

### Submission Process

Submissions will be evaluated based on the [Mean Absolute Error (MAE)](https://en.wikipedia.org/wiki/Mean_absolute_error). The entrant with the lowest average MAE per match will be declared the winner.

| Step | Info |
|------|------|
| 1    | After registration, each entrant will receive a bespoke link to their submission file hosted in Microsoft Excel Online. |
| 2    | Enter both predictions (handicap and total points) into the submission file before each match deadline. |
| 3    | The cells for each match will be locked after the submission deadline. |
| 4    | After completion of the match, team scores will be entered by Betfair and your MAE will be calculated automatically|

**Missed submissions before tip-off?**

 - Email your predictions to [datathon@betfair.com.au](mailto:datathon@betfair.com.au).

**Missed submissions after tip-off?**

 - You’ll be assigned the median MAE of all other entrants for that match.

---

### Judging

 - The MAE for both the Home Handicap & Total Points predictions will be added together.
 - Entrants will be ranked in ascending order on their average MAE per match

---

### Historic Data

The dataset for the competition:

- [Player Dataset 2019-10-22 to 2024-10-30](../assets/NBA_Dataset-2019-2024.zip)
- [Player Dataset 2024-10-31 to 2024-11-20](../assets/nba_player_data_update_20241031-20241120.csv)

The data has been collected using the [nba_api package](https://github.com/swar/nba_api). Daily updates will be posted here throughout the competition.

### Data Download Code

```py
import pandas as pd
from pandas import json_normalize
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from tqdm import tqdm
import numpy as np

nba_teams = teams.get_teams()
teams = [team for team in nba_teams]
id_list = [item['id'] for item in teams]

league_dataframe = pd.DataFrame()

for team_id in id_list:
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
    games = gamefinder.get_data_frames()[0]
    league_dataframe = pd.concat([league_dataframe,games])

league_dataframe['GAME_DATE'] = pd.to_datetime(league_dataframe['GAME_DATE'])
unique_game_ids = league_dataframe.loc[league_dataframe['GAME_DATE'] >= '2019-10-01', 'GAME_ID'].unique().astype(str).tolist()

# List of required columns
required_columns = [
    'gameId', 'gameTimeLocal', 'gameTimeUTC', 'duration', 'gameCode',
    'gameStatusText', 'gameStatus', 'regulationPeriods', 'period',
    'arenaId', 'arenaName', 'arenaCity', 'arenaState', 'arenaCountry',
    'arenaTimezone', 'teamId', 'teamName', 'teamCity', 'teamTricode',
    'score', 'teamStatus', 'status', 'order', 'personId', 'jerseyNum',
    'position', 'starter', 'oncourt', 'played', 'name', 'nameI',
    'firstName', 'familyName', 'statistics.assists', 'statistics.blocks',
    'statistics.blocksReceived', 'statistics.fieldGoalsAttempted',
    'statistics.fieldGoalsMade', 'statistics.fieldGoalsPercentage',
    'statistics.foulsOffensive', 'statistics.foulsDrawn',
    'statistics.foulsPersonal', 'statistics.foulsTechnical',
    'statistics.freeThrowsAttempted', 'statistics.freeThrowsMade',
    'statistics.freeThrowsPercentage', 'statistics.minus',
    'statistics.minutes', 'statistics.minutesCalculated', 'statistics.plus',
    'statistics.plusMinusPoints', 'statistics.points',
    'statistics.pointsFastBreak', 'statistics.pointsInThePaint',
    'statistics.pointsSecondChance', 'statistics.reboundsDefensive',
    'statistics.reboundsOffensive', 'statistics.reboundsTotal',
    'statistics.steals', 'statistics.threePointersAttempted',
    'statistics.threePointersMade', 'statistics.threePointersPercentage',
    'statistics.turnovers', 'statistics.twoPointersAttempted',
    'statistics.twoPointersMade', 'statistics.twoPointersPercentage',
    'notPlayingReason', 'notPlayingDescription'
]

for matchup in tqdm(unique_game_ids, desc="Processing Matchups", unit="matchup"):
    try:
        box = boxscore.BoxScore(matchup)
        box_dict = box.get_dict()

        arena_df = json_normalize(box_dict['game']['arena'])
        away_team_df = json_normalize(box_dict['game']['awayTeam'])
        away_team_df = away_team_df[['teamId','teamName','teamCity','teamTricode','score','players']]
        away_team_df['teamStatus'] = 'AWAY'
        away_team_exploded = away_team_df.explode('players').reset_index(drop=True)
        players_df = pd.json_normalize(away_team_exploded['players'])
        away_team_df_flattened = pd.concat([away_team_exploded.drop(columns=['players']).reset_index(drop=True), players_df.reset_index(drop=True)], axis=1)

        home_team_df = json_normalize(box_dict['game']['homeTeam'])
        home_team_df = home_team_df[['teamId','teamName','teamCity','teamTricode','score','players']]
        home_team_df['teamStatus'] = 'HOME'
        home_team_exploded = home_team_df.explode('players').reset_index(drop=True)
        players_df = pd.json_normalize(home_team_exploded['players'])
        home_team_df_flattened = pd.concat([home_team_exploded.drop(columns=['players']).reset_index(drop=True), players_df.reset_index(drop=True)], axis=1)

        game_details_df = json_normalize({k: v for k, v in box_dict['game'].items() if not isinstance(v, dict)})
        for column in ['gameId', 'gameTimeLocal', 'gameTimeUTC', 'duration', 'gameCode', 'gameStatusText', 'gameStatus', 'regulationPeriods', 'period']:
            if column not in game_details_df.columns:
                game_details_df[column] = pd.Series([pd.NA] * len(game_details_df))

        game_information = pd.concat([game_details_df, arena_df], axis=1)
        team_info = pd.concat([away_team_df_flattened, home_team_df_flattened], axis=0)

        game_information['key'] = 1
        team_info['key'] = 1
        merged_df = pd.merge(game_information, team_info, on='key')
        merged_df = merged_df.drop(columns=['key'])

        # Add missing columns with NaN values
        for column in required_columns:
            if column not in merged_df.columns:
                merged_df[column] = np.nan

        # Reorder the DataFrame to ensure all required columns are included
        merged_df = merged_df[required_columns]

        merged_df.to_csv('nba_player_data.csv', index=False, mode='a', header=False)
    
    except Exception:
        continue

```

## Leaderboard

Check back later for leaderboard updates.

---

## FAQs

### Can I edit my submission if I notice an error?

- Yes, submissions can be edited until the cells are locked.
- If changes are needed after the deadline but before tip-off, email [datathon@betfair.com.au](mailto:datathon@betfair.com.au).

### What are the guidelines for the home handicap prediction?

- The Home Handicap can be an integer or float, positive or negative.
- If the home team is expected to win, submit a negative handicap (and vice versa).
- For reference, the highest winning margin since 1983 has been 73 points.

### What are the guidelines for the total points prediction?

- Total Points can be an integer or float, but it must be a positive number.
- Historically, the lowest score since 1983 was 108 points, and the highest was 370 points.

### What if I want to use a Machine Learning model?

- The algorithm choice doesn’t matter from a competition perspective. However, you should use a regression model, not a classification model.

### What happens if I miss a match?

- You’ll be assigned the median MAE from other entrants for that match.

### Who is the home team and who is the away team?

- In NBA match names, the format is “**Away Team @ Home Team**”, where the away team plays at the home team’s venue.

### How do I know which players will be playing in a match?

 - In the dataset, each team has their entire playing list listed for each match, with any players out with injury having a status of "INACTIVE"
 - Information on day-to-day injuries can be found on the [ESPN website](https://www.espn.com.au/nba/injuries)

---
