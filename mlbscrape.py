import pandas as pd
import requests
from io import StringIO

# Dictionary of team names and their corresponding team IDs
team_ids = {
    'Arizona Diamondbacks': 109,
    'Atlanta Braves': 144,
    'Baltimore Orioles': 110,
    'Boston Red Sox': 111,
    'Chicago Cubs': 112,
    'Chicago White Sox': 145,
    'Cincinnati Reds': 113,
    'Cleveland Indians': 114,
    'Colorado Rockies': 115,
    'Detroit Tigers': 116,
    'Houston Astros': 117,
    'Kansas City Royals': 118,
    'Los Angeles Angels': 108,
    'Los Angeles Dodgers': 119,
    'Miami Marlins': 146,
    'Milwaukee Brewers': 158,
    'Minnesota Twins': 142,
    'New York Mets': 121,
    'New York Yankees': 147,
    'Oakland Athletics': 133,
    'Philadelphia Phillies': 143,
    'Pittsburgh Pirates': 134,
    'San Diego Padres': 135,
    'San Francisco Giants': 137,
    'Seattle Mariners': 136,
    'St. Louis Cardinals': 138,
    'Tampa Bay Rays': 139,
    'Texas Rangers': 140,
    'Toronto Blue Jays': 141,
    'Washington Nationals': 120
}

# Initialize an empty list to store the extracted data
games = []

# Loop through each team's ID and download their schedule
for team, team_id in team_ids.items():
    csv_url = f"https://www.ticketing-client.com/ticketing-client/csv/GameTicketPromotionPrice.tiksrv?team_id={team_id}&home_team_id={team_id}&display_in=singlegame&ticket_category=Tickets&site_section=Default&sub_category=Default&leave_empty_games=true&event_type=T&year=2023&begin_date=20230201"
    response = requests.get(csv_url)
    response.raise_for_status()
    csv_content = StringIO(response.text)
    df = pd.read_csv(csv_content)

    # Extract Home and Away team names
    df["Home team name"] = df["SUBJECT"].str.extract(r'at (.+)$')
    df["Away team name"] = df["SUBJECT"].str.extract(r'^(.+) at')

    # Extract City
    df["City"] = df["LOCATION"].str.extract(r'- (.+)$')

    # Convert 'START DATE' to YYYY-MM-DD format and rename the column to "Date"
    df["Date"] = pd.to_datetime(df["START DATE"], format="%m/%d/%y").dt.strftime("%Y-%m-%d")
    df = df.rename(columns={"Date (YYYY-MM-DD)": "Date"})

    # Select only the desired columns and append to the list of games
    games.append(df[["Home team name", "Away team name", "City", "Date"]])

# Concatenate all dataframes in the games list
result = pd.concat(games, ignore_index=True)

# Write the result to a CSV file
result.to_csv('all_home_games.csv', index=False)

print(result)
