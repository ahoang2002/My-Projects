import requests

api_key = ""
ARAM_games = []
CLASSIC_games = []

summoner_name = input('Enter your Summoner Name:')

summoner_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name
summoner_api_url = summoner_url + '?api_key=' + api_key
resp_summoner = requests.get(summoner_api_url)
player_info = resp_summoner.json()
puuid = player_info['puuid']

match_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=0&count=20"
match_api_url = match_url + '&api_key=' + api_key
resp_matches = requests.get(match_api_url)
matches = resp_matches.json()

for i in range(len(matches)):
    match_info_url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + matches[i]
    match_info_api_url = match_info_url + '?api_key=' + api_key
    resp_match_info = requests.get(match_info_api_url)
    match_data = resp_match_info.json()
    if (match_data['info']['gameMode'] == 'ARAM'):
        ARAM_games.append(matches[i])
    elif (match_data['info']['gameMode'] == 'CLASSIC'):
        CLASSIC_games.append(matches[i])
    else:
        pass
for i in range(len(CLASSIC_games)):
    game_url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + CLASSIC_games[i]
    game_api_url = game_url + '?api_key=' + api_key
    game_resp = requests.get(game_api_url)
    game = game_resp.json()
    j = 0
    while (game['info']['participants'][j]['puuid'] != puuid):
        j += 1
    role = game['info']['participants'][j]['teamPosition']
    champ = game['info']['participants'][j]['championName']
    print(champ)
    print(game['info']['participants'][j]['assists'])
    allIn_ping = match_data['info']['participants'][j]['allInPings']
    assist_ping = match_data['info']['participants'][j]['assistMePings']
    bait_ping = match_data['info']['participants'][j]['baitPings']
    basic_ping = match_data['info']['participants'][j]['basicPings']
    back_ping = match_data['info']['participants'][j]['getBackPings']
    hold_ping = match_data['info']['participants'][j]['holdPings']
    needVision_ping = match_data['info']['participants'][j]['needVisionPings']
    omw_ping = match_data['info']['participants'][j]['onMyWayPings']
    push_ping = match_data['info']['participants'][j]['pushPings']
    visionCleared_ping = match_data['info']['participants'][j]['visionClearedPings']
    danger_ping = match_data['info']['participants'][j]['dangerPings']
    enemyVision_ping = match_data['info']['participants'][j]['enemyVisionPings']
    missing_ping = match_data['info']['participants'][j]['enemyMissingPings']
    visionCleared_ping = match_data['info']['participants'][j]['visionClearedPings']
    command_ping = match_data['info']['participants'][j]['commandPings']




