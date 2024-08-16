import pandas as pd
import json
from collections import Counter

def new_player(Player_name, Team, Pos):
    return {
        "Full Name": Player_name,
        "Display": shorten_name(Player_name),
        "NFLid": None,
        "POS": Pos,
        "Current_Team": Team,
        "Teams_List": [],
        "Previous_Games": []
    }

def shorten_name(full_name):
    # Split the name into parts
    name_parts = full_name.split()
    
    if len(name_parts) < 2:
        return full_name  # Return the name as-is if it doesn't have at least two parts
    
    # Extract first name, last name, and suffix (if any)
    first_name = name_parts[0]
    last_name = name_parts[-2] if len(name_parts) > 2 else name_parts[-1]
    suffix = name_parts[-1] if len(name_parts) > 2 and name_parts[-1] in ["Jr.", "Sr.", "II", "III", "IV"] else None
    
    # Shorten the first name to its initial
    first_initial = first_name[0]
    
    # Construct the shortened name
    shortened_name = f"{first_initial}.{last_name}"
    
    return shortened_name

#read depthcharts
df = pd.read_csv("../DepthCharts/OFFdepthchart.csv")
print(df)

g = open('game_info.json')
games = json.load(g)

#open output json
with open('player_info.json', 'w') as f:
    f.write('[')
    first_entry = True
    player_dic = {}
#assign players accordingly
    for _, row in df.iterrows():
        team = row['Team']
        pos = row['Pos']
        for i in range(1,6):
            player = row.get(f'Player {i}')
            if pd.notna(player):  # Only process if player name is not NaN
                print(f"Team: {team}, Position: {pos}, Player {i}: {player}")
                player_dic = new_player(player, team, pos)

        #parse games json to see former teams
                for game in games:
                    if any(player["Name"] == player_dic["Display"] for player in game["Players1"]):
                        player_dic["Teams_List"].append(game["Team1"])
                    if any(player["Name"] == player_dic["Display"] for player in game["Players2"]):
                        player_dic["Teams_List"].append(game["Team2"])

                player_dic["Teams_List"] = list(set(player_dic["Teams_List"]))
                if not first_entry:
                    f.write(',\n')  # Write comma before every entry except the first one
                json.dump(player_dic, f, indent=4)
                first_entry = False
    f.write(']')

h = open('player_info2.json')
players = json.load(h)
#Print duplicate display names
# Extract display names
display_names = [player["Display"] for player in players]

# Count occurrences of each display name
name_counts = Counter(display_names)

# Find duplicates
duplicates = [name for name, count in name_counts.items() if count > 1]

print("Duplicate Display Names:", duplicates)

#did some manual entry

#Get nfl ids by checking play names
# for player1 in players:
#     if player.get("NFLid") is None:
#         for game in games:
#             if (player["Name"] == player_dic["Display"] for player in game["Players1"]):
#                 player1["Id"] = player["NFLid"]

# Create a dictionary to map display names to NFLids
display_to_nflid = {}
for player in players:
    display_name = player['Display']
    nflid = player['NFLid']
    display_to_nflid[display_name] = nflid

def update_nflid(display_name, id):
    for player in players:
        if player['Display'] == display_name:
            if player['NFLid'] is None:
                player['NFLid'] = id
            return
        
#loop to add ids
for game in games:
    for team in ['Players1', 'Players2']:
        if team in game:
            for player in game[team]:
                display_name = player['Name']
                id = player['Id']
                update_nflid(display_name, id)

#loop to add games
nflid_to_player_index = {player['NFLid']: i for i, player in enumerate(players) if player['NFLid']}
def update_player_data(display_name, id, game_id):
    for i, player in enumerate(players):
        if player['Display'] == display_name:
            if player['NFLid'] is None:
                player['NFLid'] = id
                nflid_to_player_index[id] = i
            
            if id in nflid_to_player_index:
                player_index = nflid_to_player_index[id]
                if game_id not in players[player_index]['Previous_Games']:
                    players[player_index]['Previous_Games'].append(game_id)
            return
        
for game in games:
    game_id = game['game_id']
    for team in ['Players1', 'Players2']:
        if team in game:
            for player in game[team]:
                display_name = player['Name']
                id = player['Id']
                update_player_data(display_name, id, game_id)

with open('player_info_main.json','w') as j:
    json.dump(players, j, indent=4)