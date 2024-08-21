from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd

def get_player_stats():
    """
    Retrieve the game stats for a player based on their full name.

    Returns:
        pd.DataFrame: A DataFrame containing the player's game stats for the season.
    """
    # Retrieve a list of all active players
    active_player_list = pd.DataFrame(players.get_active_players())

    # Input the player's name
    player_name = input("Player Full Name (Ex. 'Kevin Durant'): ")

    # Convert player name to title case
    player_name = player_name.title()
    
    # Retrieve the player's ID
    chosen_player_id = active_player_list.loc[active_player_list['full_name'] == player_name, 'id'].values[0]
    
    # Grab player games for the season
    player_stats = pd.DataFrame(playergamelog.PlayerGameLog(player_id=chosen_player_id).get_data_frames()[0])
    
    return player_stats

def get_player_id(player_stats):
    """
    Retieve the player's ID
    """
    chosen_player_id = player_stats
    player_id = chosen_player_id["Player_ID"][0]
    return player_id

def get_similar_players_stats(similar_player_ids):
    """
    Retrieve game stats for a list of similar players.

    Args:
        similar_player_ids (list of int): List of player IDs representing similar players.

    Returns:
        pd.DataFrame: A DataFrame containing the combined game stats for all similar players.
    """
    sim_player_df = pd.DataFrame()

    # Retrieve a list of all active players
    active_player_list = pd.DataFrame(players.get_active_players())

    # Loop over each player ID in the similar players list
    for sim_player_id in similar_player_ids:
        # Check if the player is in the active players list
        if sim_player_id in active_player_list['id'].values:
            # Grab player games for the season
            player_stats = pd.DataFrame(playergamelog.PlayerGameLog(player_id=sim_player_id).get_data_frames()[0])
            # Append the stats to the DataFrame
            sim_player_df = pd.concat([sim_player_df, player_stats], ignore_index=True)

    return sim_player_df