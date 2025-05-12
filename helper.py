import math
# any imports needed


def getPreviousSeasons(activeSeason: int, numOfPreviousSeasons: int) -> list:
  """Returns a list of strings representing the seasons specified before the given active season.
  For example, passing in (17, 3) would return [e6a1, e5a3, e5a2]

  Parameters
  ----------
  activeSeason : int
    This represents the 'current' season, aka the season you want to start searching
    for previous seasons non-inclusive of the entered value

  numOfPreviousSeasons : int
    This value represents the number of seasons you want to go back
  
  Return
  ------
    Returns a list with the string value of the numOfPreviousSeasons previous seasons
  """
  seasons = ["e1a1", "e1a2", "e1a3", "e2a1", "e2a2", "e2a3", 
           "e3a1", "e3a2", "e3a3", "e4a1", "e4a2", "e4a3", 
           "e5a1", "e5a2", "e5a3", "e6a1", "e6a2", "e6a3", 
           "e7a1", "e7a2", "e7a3", "e8a1", "e8a2", "e8a3", 
           "e9a1", "e9a2", "e9a3", "e10a1", "e10a2", "e10a3"]
  
  listOfSeasons = []
  activeSeason -= 2  # subtract 1 to start counting previous seasons and another to account for 0 index
  for x in range(numOfPreviousSeasons):
    if activeSeason < 0:
      break
    listOfSeasons.append(seasons[activeSeason])
    activeSeason -= 1
  return listOfSeasons


def getPlayersFromMatch(match_data: dict) -> list[str]:
  """Returns a list of players from a match

  Parameters
  ----------
  match_data (dict):
    The match data JSON response from the Match API call

  Return
  ------
  A list of every player's name from the match sorted by team in the form of playerName#playerTag
  
  """
  players = []
  red_players = match_data["players"]["red"]
  blue_players = match_data["players"]["blue"]
  for player in red_players:
    players.append(player["name"] + "#" + player["tag"])
  for player in blue_players:
    players.append(player["name"] + "#" + player["tag"])
  return players


def isTraded(player_stats: list[dict], attacker: str, time_of_death: int) -> bool:
  """Determines whether a player was traded a.k.a. if their attacker was killed within
     5 seconds of killing the player.
  
  Parameters
  ----------
  player_stats (list[dict]):
    The list of all the player's stats for a given round obtained from the response
    from the Match API call
  
  attacker (str):
    The name of the player who is to be killed to confirm a valid trade.

  time_of_death (int):
    The time in the match at which the player was killed. A valid trade means the attacker
    was also killed with 5 seconds (5000ms) of the time of death.

  Return
  ------
  True if the player was successfully traded.
  False if the player was unsuccessfully traded.
  
  """
  for player in player_stats:
    for kill in player["kill_events"]:
      if kill["victim_display_name"] == attacker:
        if kill["kill_time_in_round"] < time_of_death + 5000:
          return True
        else:
          return False  # Attacker was not killed within 5 seconds
  return False  # Attacker was never killed


def parseMatchData(match_data: dict) -> dict:
  """Returns a dictionary of players with all their data formatted for easy access

  Parameters
  ----------
  match_data (dict):
    The match data JSON response from the Match API call

  Return
  ------
  A list containing dictionaries with all the specified data points for the Match file creation which includes:
  IGN, RiotID, Tag, Team Name, Agent, Score Total, Score Per Round, Total Kills, Total Deaths, Total Assists, 
  KD Rate, Total Plants, Total Defuses, KAST, Headshot %, First Kills, First Deaths, First Kill/Death Ratio
  
  """
  parsed_data: dict = {}
  players: list[dict] = match_data["players"]["all_players"]
  round_data: list = match_data["rounds"]
  for player in players:
    player_entry = {}
    player_entry["IGN"] = f"{player["name"]}#{player["tag"]}"
    player_entry["RiotID"] = player["name"]
    player_entry["Tag"] = player["tag"]
    player_entry["Team Name"] = ""  # TODO figure out how to get team name
    player_entry["Agent"] = player["character"]
    player_entry["Score Total"] = str(player["stats"]["score"])
    player_entry["Score Per Round"] = str(player["stats"]["score"] / match_data["metadata"]["rounds_played"])  # avg score per round
    player_entry["Total Kills"] = str(player["stats"]["kills"])
    player_entry["Total Deaths"] = str(player["stats"]["deaths"])
    player_entry["Total Assists"] = str(player["stats"]["assists"])
    player_entry["KD Rate"] = str(round(player["stats"]["kills"] / player["stats"]["deaths"], 2))
    player_entry["Total Plants"] = "0"
    player_entry["Total Defuses"] = "0"
    player_entry["KAST"] = "0" # TODO
    total_hits = player["stats"]["bodyshots"] + player["stats"]["headshots"] + player["stats"]["legshots"]
    player_entry["Headshot %"] = str(round((player["stats"]["headshots"] / total_hits) * 100, 2)) + "%"
    player_entry["First Kills"] = "0"
    player_entry["First Deaths"] = "0"
    player_entry["First Kill/Death Ratio"] = "0"
    # Add round by round column names, data is entered later
    # NO DATA string used for debugging in case value is not filled in
    number_of_rounds = match_data["metadata"]["rounds_played"]
    for round_number in range(number_of_rounds):
      player_entry[f"Round {round_number + 1} Kills"] = "0"
      player_entry[f"Round {round_number + 1} Deaths"] = "0"
      player_entry[f"Round {round_number + 1} Assists"] = "0"
      player_entry[f"Round {round_number + 1} Traded"] = "No"
      player_entry[f"Round {round_number + 1} Team Kills"] = "0"
      player_entry[f"Round {round_number + 1} Plant"] = "No"
      player_entry[f"Round {round_number + 1} Defuse"] = "No"
      player_entry[f"Round {round_number + 1} Score"] = "0"
      player_entry[f"Round {round_number + 1} Loadout Value"] = "NO DATA"
      player_entry[f"Round {round_number + 1} Weapon"] = "NO DATA"
      player_entry[f"Round {round_number + 1} Armor"] = "NO DATA"
    # Add player's data to parsed_data
    parsed_data[player_entry["IGN"]] = player_entry
  
  # Set Total Plants/Defuses and calculate KAST
  KAST: dict = {}
  # initialize KAST values to 0
  # after every round loop if a player's value in KAST is > -1 parsed_data will increase KAST by 1
  # then KAST will be reset to all 0s. Once rounds loop is finished it will divide parsed_data KAST
  # by the number of rounds to get the final KAST value
  for player in parsed_data:
    KAST[player] = 0
  
  counter = 0
  for game_round in match_data["rounds"]:
    # adjusts the plants/defuses
    if game_round["bomb_planted"]:
      planted_by_player_name = game_round["plant_events"]["planted_by"]["display_name"]
      parsed_data[planted_by_player_name]["Total Plants"] = str(
        int(parsed_data[planted_by_player_name]["Total Plants"]) + 1) # Add 1 to planter's Total Plants value
      parsed_data[planted_by_player_name][f"Round {counter + 1} Plant"] = "Yes"
    if game_round["bomb_defused"]:
      defused_by_player_name = game_round["defuse_events"]["defused_by"]["display_name"]
      parsed_data[defused_by_player_name]["Total Defuses"] = str(
        int(parsed_data[defused_by_player_name]["Total Defuses"]) + 1) # Add 1 to defuser's Total Defuses value
      parsed_data[defused_by_player_name][f"Round {counter + 1} Defuse"] = "Yes"
    
    for player_stat in game_round["player_stats"]:
      player_name = player_stat["player_display_name"]
      if player_stat["kills"] > 0:
        KAST[player_stat["player_display_name"]] += 1
        for kill_event in player_stat["kill_events"]:
          for assistant in kill_event["assistants"]:
            KAST[assistant["assistant_display_name"]] += 1
          KAST[kill_event["victim_display_name"]] -= 1 # Subtract 1 from player's KAST if they died (-1 means they did nothing that round)
          parsed_data[kill_event["victim_display_name"]][f"Round {counter + 1} Deaths"] = "1"
          if isTraded(game_round["player_stats"], kill_event["killer_display_name"], kill_event["kill_time_in_round"]):
            KAST[kill_event["victim_display_name"]] += 1
            parsed_data[player_stat["player_display_name"]][f"Round {counter + 1} Traded"] = "Yes"
      # round by round data
      parsed_data[player_name][f"Round {counter + 1} Kills"] = player_stat["kills"]
      parsed_data[player_name][f"Round {counter + 1} Score"] = player_stat["score"]
      parsed_data[player_name][f"Round {counter + 1} Loadout Value"] = player_stat["economy"]["loadout_value"]
      parsed_data[player_name][f"Round {counter + 1} Weapon"] = player_stat["economy"]["weapon"]["name"]
      parsed_data[player_name][f"Round {counter + 1} Armor"] = player_stat["economy"]["armor"]["name"]
    for player in KAST:
      if KAST[player] >= 0:
        parsed_data[player]["KAST"] = str(int(parsed_data[player]["KAST"]) + 1)
      KAST[player] = 0
    counter += 1
  for player in parsed_data:
    parsed_data[player]["KAST"] = str(math.floor((int(parsed_data[player]["KAST"]) / int(match_data["metadata"]["rounds_played"])) * 100))


  # Set First Kills, First Deaths, and First Kill/Death Ratio
  kills: list = match_data["kills"]
  kills_round = 0
  for recorded_kill in kills:
    if recorded_kill["round"] == kills_round:  # Finds first kill in a match as they are sorted in order by time of kill
      kills_round += 1
      parsed_data[recorded_kill["killer_display_name"]]["First Kills"] = str(
        int(parsed_data[recorded_kill["killer_display_name"]]["First Kills"]) + 1)  # Add 1 to killer's First Kills value
      parsed_data[recorded_kill["victim_display_name"]]["First Deaths"] = str(
        int(parsed_data[recorded_kill["victim_display_name"]]["First Deaths"]) + 1) # Add 1 the victim's First Deaths value
  for player in parsed_data:
    first_kills = int(parsed_data[player]["First Kills"])
    first_deaths = int(parsed_data[player]["First Deaths"])
    if first_deaths == 0:
      first_deaths = 1  # set to 1 to prevent divide by 0 error
    parsed_data[player]["First Kill/Death Ratio"] = str(round(first_kills / first_deaths, 1))

  # Add round by round data
  round_number = 1
  for game_round in round_data:
    # Kills
    # deaths
    # assists
    # team kill
    # score
    # loadout value
    # weapon
    # armor
    
    round_number += 1
  
  data: list = []
  for player in parsed_data:
    data.append(parsed_data[player])
  return data