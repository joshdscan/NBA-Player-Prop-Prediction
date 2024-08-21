import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import boxscoreadvancedv3
from nba_api.stats.endpoints import leaguegamefinder
import numpy as np

def get_games_since_2018():
    # Get NBA teams
    nba_teams = pd.DataFrame(teams.get_teams())
    nba_teams['id'] = pd.to_numeric(nba_teams['id'])

    # Initialize a list to hold the games per team
    games_per_team = []

    # Loop through each team and find games since 2018
    for team in nba_teams['id']:
        gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team)
        games = gamefinder.get_data_frames()[0]
        games = games[games['SEASON_ID'].str[-4:].astype(int) >= 2018]
        games_per_team.append(games)

    return games_per_team