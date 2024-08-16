import json
def new_player(Player_name, Player_id):
    return {
        "Name": Player_name,
        "Id": Player_id,
        "Rushing": {
            "attempts": 0,
            "yards": 0,
            "touchdowns": 0,
            "extra_points": 0
        },
        "Passing": {
            "Attempted": 0,
            "Completed": 0,
            "yards": 0,
            "touchdowns": 0,
            "extra_points": 0
        },
        "Receiving": {
            "Targets": 0,
            "Completed": 0,
            "yards": 0,
            "touchdowns": 0,
            "extra_points": 0
        },
        "Fantasy_Score": 0
    }


def increment_stat(team, player_id, stat, amount, category):
    # Identify the player's list based on the team
    players_list = game_dic['Players'+str(team)]  # Update this line if team is Team2
    
    # Find the player by ID
    for player in players_list:
        if player["Id"] == player_id:
            if category in player:
                if category == "Rushing":
                    player[category][stat] += amount
                elif category == "Passing":
                    player[category][stat] += amount
                elif category == "Receiving":
                    player[category][stat] += amount
                else:
                    raise ValueError("Invalid category")
            else:
                raise ValueError("Invalid category")
            break
    else:
        print("Player ID not found.")

def set_fscore(team, player_id):
    # Identify the player's list based on the team
    players_list = game_dic['Players'+str(team)]  # Update this line if team is Team2
    #print(players_list)
    # Find the player by ID
    for player in players_list:
        if player["Id"] == player_id:
            player["Fantasy_Score"] = (player["Rushing"]["yards"]*.1)+(player["Receiving"]["yards"]*.1)+(player["Passing"]["yards"]*.04)+(player["Receiving"]["Completed"]*1)+(player["Rushing"]["touchdowns"]*6)+(player["Receiving"]["touchdowns"]*6)+(player["Passing"]["touchdowns"]*4)+(player["Rushing"]["extra_points"]*2)+(player["Receiving"]["extra_points"]*2)+(player["Passing"]["extra_points"]*2)
        # else:
        #     print("Player ID " +str(player_id)+" not found.")

#gameplan

#read_json
#should I be using a full loader: no, am I anyway? yes
g = open('play_info.json')
plays = json.load(g)

with open('game_info.json', 'w') as f:
    f.write('[')
    first_entry = True
    game_id = None
    game_dic = {}
#loop each item in plays
    for play in plays:

#check pointed at game
#if new: write old to file and create a dictionary for the pointed at game
#if old: add to dictionary
        if play['game_id'] != game_id:
            #print(str(game_dic) + '\n')
            #write to file
            if game_dic:
                if not first_entry:
                    f.write(',\n')  # Write comma before every entry except the first one
                json.dump(game_dic, f, indent=4)
                first_entry = False

            #create new game_dic
            game_id = play['game_id']
            game_dic['game_id'] = game_id
            game_dic['week'] = play['week']
            game_dic['Team1'] = play['offense']
            game_dic['Team2'] = play['defense']
            game_dic['Players1'] = []
            game_dic['Players2'] = []
#Check players involved
        #get team1 team 2
        if play['offense'] == game_dic['Team1']:
            team = 1
        else:
            team = 2
        #if new player create summary item
        if play['play_type']=='run':
            if play['info']["NFLid_rusher"] not in [player["Id"] for player in game_dic['Players'+str(team)]]:
                game_dic['Players'+str(team)].append(new_player(play['info']['rusher'],play['info']['NFLid_rusher']))
        else:
            if play['info']["NFLid_passer"] not in [player["Id"] for player in game_dic['Players'+str(team)]]:
                game_dic['Players'+str(team)].append(new_player(play['info']['passer'],play['info']['NFLid_passer']))
            if play['info'].get("NFLid_receiver") and play['info']["NFLid_receiver"] not in [player["Id"] for player in game_dic['Players'+str(team)]]:
                game_dic['Players'+str(team)].append(new_player(play['info']['receiver'],play['info']['NFLid_receiver']))
    
#add to summary items
        if play['play_type']=='run':
            increment_stat(team,play['info']["NFLid_rusher"],"attempts",1,"Rushing")
            increment_stat(team,play['info']["NFLid_rusher"],"yards",play['info']["rushing_yards"],"Rushing")
            if play['touchdown']==True:
                increment_stat(team,play['info']["NFLid_rusher"],"touchdowns",1,"Rushing")
            if play['extra_point']==True:
                increment_stat(team,play['info']["NFLid_rusher"],"extra_points",1,"Rushing")
            set_fscore(team,play['info']["NFLid_rusher"])
        else:
            increment_stat(team,play['info']["NFLid_passer"],"Attempted",1,"Passing")
            if play['info'].get("NFLid_receiver"):
                increment_stat(team,play['info']["NFLid_receiver"],"Targets",1,"Receiving")
            if play['info']['pass_complete']:
                increment_stat(team,play['info']["NFLid_passer"],"yards",play['info']["passing_yards"],"Passing")
                increment_stat(team,play['info']["NFLid_passer"],"Completed",1,"Passing")
                increment_stat(team,play['info']["NFLid_receiver"],"yards",play['info']["receiving_yards"],"Receiving")
                increment_stat(team,play['info']["NFLid_receiver"],"Completed",1,"Receiving")
            if play['touchdown']:
                increment_stat(team,play['info']["NFLid_passer"],"touchdowns",1,"Passing")
                if play['info'].get("NFLid_receiver"):
                    increment_stat(team,play['info']["NFLid_receiver"],"touchdowns",1,"Receiving")
            if play['extra_point']:
                increment_stat(team,play['info']["NFLid_passer"],"extra_points",1,"Passing")
                if play['info'].get("NFLid_receiver"):
                    increment_stat(team,play['info']["NFLid_receiver"],"extra_points",1,"Receiving")
            set_fscore(team,play['info']["NFLid_passer"])
            if play['info'].get("NFLid_receiver"):
                set_fscore(team,play['info']["NFLid_receiver"])
#close file
    f.write(']') 