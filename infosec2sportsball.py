import pandas as pd
import os
import time
from datetime import datetime, timedelta

def is_updated_recently(file_path):
    if not os.path.exists(file_path):
        return False

    last_modified = os.path.getmtime(file_path)
    one_week_ago = time.time() - 7 * 24 * 60 * 60
    return last_modified >= one_week_ago

def is_nearby(city1, city2):
    if not isinstance(city1, str) or not isinstance(city2, str):
        return False

    return city1.lower() == city2.lower()

def main():
    # Prompt the user for a start and end date and sport
    start_date_input = input("Enter a start date (YYYY-MM-DD): ")
    end_date_input = input("Enter an end date (YYYY-MM-DD): ")
    sport = input("Choose a sport: B (Baseball), F (Football), or H (Hockey): ")

    if sport.lower() not in ["b", "f", "h"]:
        print("Invalid sport. Please choose B (Baseball), F (Football), or H (Hockey).")
        return

    if sport.lower() != "b":
        print("Other sports coming soon. Visit https://github.com/GuillaumeRoss/infosec2sportsball to file a PR")
        return

    # Convert the input dates to datetime objects
    start_date = datetime.strptime(start_date_input, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_input, '%Y-%m-%d')

    # Ask the user for the number of days around the start date of a conference
    days_input = input("How many days around the start date of a conference should I look for? (default: 3, range: 1-5): ")
    if days_input == "":
        days_around = 3
    elif days_input.isdigit() and 1 <= int(days_input) <= 5:
        days_around = int(days_input)
    else:
        print("Invalid input. Please enter a number between 1 and 5.")
        return

    if not is_updated_recently("all_home_games.csv"):
        print("Updating schedule files")
        os.system("python3 mlbscrape.py")

    if not is_updated_recently("security_conferences.csv"):
        print("Updating schedule files")
        os.system("python3 infosecfetch.py")

    security_conferences = pd.read_csv('security_conferences.csv')
    all_home_games = pd.read_csv('all_home_games.csv')

    results = set()

    for _, conf in security_conferences.iterrows():
        conf_date = datetime.strptime(conf['Start Date'], '%Y-%m-%d')
        conf_city = conf['City']

        if conf_date < start_date or conf_date > end_date:
            continue

        for _, game in all_home_games.iterrows():
            game_date = datetime.strptime(game['Date'], '%Y-%m-%d')
            game_city = game['City']

            if game_date < start_date or game_date > end_date:
                continue

            if abs((conf_date - game_date).days) <= days_around and is_nearby(conf_city, game_city):
                results.add((conf['Conference Name'], conf['Start Date'], conf_city, game['Date'], game_city, game['Home team name'], game['Away team name']))

    for result in results:
        conf_name, conf_date, conf_city, game_date, game_city, home_team, away_team = result
        print(f"Conference '{conf_name}' on {conf_date} in {conf_city} is within {days_around} days of a baseball game on {game_date} in {game_city} between {home_team} and {away_team}.")


if __name__ == "__main__":
    main()
