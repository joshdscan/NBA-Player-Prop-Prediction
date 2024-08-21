from nba_api.stats.static import players
from nba_api.stats.endpoints import playerindex
from nba_api.stats.endpoints import boxscoreadvancedv2

import pandas as pd

def get_active_players_data():
    """
    Retrieves and returns a DataFrame containing active NBA players' data.

    Returns:
        pd.DataFrame: DataFrame containing active NBA players' data.
    """
    active_player_list = playerindex.PlayerIndex()
    player_data = pd.DataFrame(active_player_list.get_data_frames()[0])
    
    columns_to_drop = [
        'PLAYER_SLUG', 'TEAM_ID', 'TEAM_SLUG', 'IS_DEFUNCT', 'TEAM_CITY',
        'TEAM_NAME', 'TEAM_ABBREVIATION', 'JERSEY_NUMBER', 'COUNTRY',
        'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER', 'ROSTER_STATUS',
        'FROM_YEAR', 'TO_YEAR', 'COLLEGE', 'STATS_TIMEFRAME', 'POSITION',
        'HEIGHT', 'WEIGHT'
    ]
    
    player_data = player_data.drop(columns=columns_to_drop)
    
    return player_data

def filter_similar_players(dataframe, player_id, percentage):
    """
    Filters players in the DataFrame who have similar stats (PTS, REB, AST) to the specified player.

    Args:
        dataframe (pd.DataFrame): DataFrame containing players' stats.
        player_id (int): The player ID to compare others against.
        percentage (float): The percentage range to consider for similarity.

    Returns:
        pd.DataFrame: Filtered DataFrame of similar players.
    """
    # Extract the specific player's data
    player_data = dataframe.loc[dataframe['PERSON_ID'] == player_id].iloc[0]
    
    # Filter players within the specified percentage range for PTS, REB, and AST
    filtered_data = dataframe[
        (dataframe['PTS'].between(player_data['PTS'] * (1 - percentage / 100), player_data['PTS'] * (1 + percentage / 100))) &
        (dataframe['REB'].between(player_data['REB'] * (1 - percentage / 100), player_data['REB'] * (1 + percentage / 100))) &
        (dataframe['AST'].between(player_data['AST'] * (1 - percentage / 100), player_data['AST'] * (1 + percentage / 100)))
    ]
    
    return filtered_data

def get_filtered_players_id(filtered_data):
    similar_players = filtered_data["PERSON_ID"].tolist()  # Using filtered_data instead of similar_players
    return similar_players 