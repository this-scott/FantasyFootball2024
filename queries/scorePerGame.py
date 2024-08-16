import json
import matplotlib.pyplot as plt

#load jsons
f = open("player_info.json")
players = json.load(f)
g = open('game_info.json')
games = json.load(g)

# Function to get player_id for a given player name
def get_player_id(player_name):
    for player in players:
        if player['Full Name'] == player_name:
            return player['NFLid']
    return None  # Return None if player is not found

def get_player_games(player_name):
    for player in players:
        if player['Full Name'] == player_name:
            return player["Previous_Games"]
    return None

def get_player_scores(player_name):
    id = get_player_id(player_name)
    scores = []
    pgames = get_player_games(player_name)
    #print(pgames)
    for game in games:
        if game["game_id"] in pgames:
            players = game["Players1"]+game["Players2"]
            for player in players:
                if player["Id"] == id:
                    scores.append(player["Fantasy_Score"])
    return scores

def get_avg(list):
    total = 0
    for i in range(0, len(list)):
        total = total + list[i]
    return total/len(list)

def get_targets_completions(player_name):
    id = get_player_id(player_name)
    targets = []
    completions = []
    pgames = get_player_games(player_name)
    for game in games:
        if game["game_id"] in pgames:
            players = game["Players1"]+game["Players2"]
            for player in players:
                if player["Id"] == id:
                    targets.append(player["Receiving"]["Targets"])
                    completions.append(player["Receiving"]["Completed"])
    return[targets, completions]

def plot_list(list):
    plt.plot(range(len(list)), list)
    plt.xlabel("week")
    plt.ylabel("Scores")
    plt.axhline(y=get_avg(list), color = 'orange', linestyle='--')
    plt.title("Scores: Avg:" + str(get_avg(list)))
    plt.show()

def plot_2_lists(list,list2):
    plt.plot(range(len(list)), list,label='Line1')
    plt.plot(range(len(list2)), list2, label='Line2')
    plt.axhline(y=get_avg(list), color = 'orange', linestyle='--')
    plt.axhline(y=get_avg(list2), color = 'red', linestyle='--')
    plt.xlabel("week")
    plt.ylabel("Scores")
    plt.title("Scores: Avg1:" + str(get_avg(list)) + "Avg2:" + str(get_avg(list2)))
    plt.legend()
    plt.show()

#desired player
player1 = "Zay Flowers"
player2 = "CeeDee Lamb"
plot_list(get_player_scores(player1))
#plot_2_lists(get_targets_completions(player1)[0],get_targets_completions(player1)[1])
#plot_2_lists(get_player_scores(player1),get_player_scores(player2))
