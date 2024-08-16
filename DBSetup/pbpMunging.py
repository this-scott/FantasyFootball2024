import pandas as pd
import json

def shorten_abbr(full_name):
    # Split the name into parts based on the dot
    name_parts = full_name.split('.')
    
    if len(name_parts) != 2:
        return full_name  # Return the name as-is if it doesn't have exactly one dot
    
    # Extract first name initial and last name
    first_name = name_parts[0]
    last_name = name_parts[1]
    
    # Shorten the first name to its initial
    first_initial = first_name[0]
    
    # Construct the shortened name
    shortened_name = f"{first_initial}.{last_name}"
    
    return shortened_name

plays_path = "play_by_play_2023.csv"

columns = ['game_id','season_type','week','posteam','defteam','play_type','yards_gained','air_yards','yards_after_catch','td_player_name','touchdown','pass_touchdown','rush_touchdown','two_point_attempt','fumble','complete_pass','passer_player_id','passer_player_name','passing_yards','receiver_player_id','receiver_player_name','receiving_yards','rusher_player_id','rusher_player_name','rushing_yards','two_point_conv_result']

df = pd.read_csv(plays_path, usecols=columns)
df = df[df['play_type'].isin(['run','pass'])]

df.reset_index(drop=True, inplace=True)
df.to_csv("shaved_pbp.csv")
print(df.head(100))

with open('play_info.json', 'w') as f:
    f.write('[')  # Start of the JSON array
    first_entry = True  # Flag to handle commas between JSON objects

    for index, row in df.iterrows():
        play_info = {
            'play_id' : index,
            'game_id' : row['game_id'],
            'week' : row['week'],
            'offense' : row['posteam'],
            'defense' : row['defteam'],
            'play_type' : row['play_type'],
            'touchdown' : True if row['touchdown'] == 1.0 else False,
            'extra_point' : True if row['two_point_conv_result'] is not None and row['two_point_conv_result'] == 'success' else False
        }
        einfo = {}
        if row['play_type']=='pass':
            einfo['NFLid_passer'] = row['passer_player_id']
            einfo['passer'] = shorten_abbr(row['passer_player_name'])
            if pd.notna(row['receiver_player_name']):
                einfo['NFLid_receiver'] = row['receiver_player_id']
                einfo['receiver'] = shorten_abbr(row['receiver_player_name'] )
            if row['complete_pass'] == 1.0:
                einfo['pass_complete'] = True
                einfo['passing_yards'] = row['passing_yards']
                einfo['receiving_yards'] = row['receiving_yards']
            else: einfo['pass_complete'] = False
        else:
            einfo['NFLid_rusher'] = row['rusher_player_id']
            einfo['rusher'] = shorten_abbr(row['rusher_player_name'])
            einfo['rushing_yards'] = row['rushing_yards']

        play_info['info'] = einfo

        if not first_entry:
            f.write(',\n')  # Write comma before every entry except the first one
        json.dump(play_info, f, indent=4)
        first_entry = False

    f.write(']') 