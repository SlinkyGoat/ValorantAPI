import os
from dotenv import load_dotenv, dotenv_values
import requests
import json
from pathlib import Path

from ApiEndpoints import (
  APIError,
  getAccountData,
  getMatchData,
  getMMRData
)
from helper import *
from CSVFileController import *

load_dotenv()

# temp array for testing
list_of_names = [
  "CU ClownZ#7647",
  "CU Boomcycle#9999",
  "Yum58#6857",
  "ReTap#1shot",
  "USA Supermnot#Coach",
  "CU Golden#llama",
]

# Global Variables
API_KEY = os.getenv("API_KEY")
downloads_path = str(Path.home() / "Downloads")
region = "na"
current_season = 'e10a2'
current_season_int = 29
data = {}
row: list[str] = []


# NOTE: almost all lines in each method are exactly the same. If project grows
#       consider creating another method that contains the repeated code to 
#       follow DRY coding conventions


def createAccountFile(selected_options: list, users: list[str]):
  """Creates file with the returned Accounts data

  Parameters
  ----------
    selected_options (list):
      All possible options for user to choose from to be written to the outputted file.
      Options include: IGN, RiotID, Tag, puuid, Account Level.
    
    users (list[str]):
      A list of the user's IGNs to grab data from the API and write to file.
  """

  data_points = {
    "IGN": lambda data: f"{data["name"]}#{data["tag"]}",
    "RiotID": lambda data: f"{data["name"]}",
    "Tag": lambda data: f"{data["tag"]}",
    "puuid": lambda data: f"{data["puuid"]}",
    "Account Level": lambda data: f"{str(data["account_level"])}"
  }
  with open(downloads_path + "\\AccountOutput.csv", "w") as file:
    file.write(f"{','.join(selected_options)}\n")  # Writes first line of csv files, ex. IGN,Username,Tag,puuid,Current Rank,Highest Rank
    for user in users:
      tokenized_name = user.split("#")
      try:
        data = getAccountData(tokenized_name[0], tokenized_name[1])
      except APIError as error:
        print(f"ERROR: {error}")
        file.write(f"{user},ERROR: {error.status_code} - MESSAGE: {error.message} - DETAILS: {error.details}\n")
      row = []
      for option in selected_options:
        row.append(data_points[option](data))
      file.write(f"{','.join(row)}\n")

  file.close()


def createMatchFile(selected_options: list, match_id: str):
  """Creates file with the returned Accounts data

  Parameters
  ----------
    selected_options (list):
      All possible options for user to choose from to be written to the outputted file.
      Options include: IGN, RiotID, Tag, Team Name, Agent, Score Total, Score Per Round, Total Kills, Total Deaths,
        Total Assists, KD Rate, Total Points, Total Defuses, KAST, Headshot %, First Kills, First Deaths, First Kill/Death Ratio
      Round-by-round datapoints always start with the 'Round:' prefix. These options include:
        Kills, Deaths, Assists, Traded, Team Kills, Plant, Defuse, Score, Loadout Value, Weapon, Armor
    
    users (list[str]):
      A list of the user's IGNs to grab data from the API and write to file.
  """
  # TODO figure out how to add team name to output
  # TODO debug, not printing anything after first line, print to console to see what is being put into parsed data if anything
  try:
    data = getMatchData(match_id)
  except APIError as error:
    print(f"ERROR: {error}")
  parsed_data: list = parseMatchData(data)
  parsed_data.insert(0, selected_options)
  createCSVFile(parsed_data, "MatchOutput.csv", rounds=data["metadata"]["rounds_played"])


def createMMRFile(selected_options: list, users: list[str]):
  """Creates file with the returned MMR data

  Parameters
  ----------
    selected_options (list):
      All possible options for user to choose from to be written to the outputted file.
    
    users (list[str]):
      A list of the user's IGNs to grab data from the API and write to file.
      Options include: IGN, RiotID, Tag, puuid, Current Rank, Elo, Highest Rank, Previous Ranks
  """

  data_points = {
    "IGN": lambda data: f"{data["name"]}#{data["tag"]}",
    "RiotID": lambda data: f"{data["name"]}",
    "Tag": lambda data: f"{data["tag"]}",
    "puuid": lambda data: f"{data["puuid"]}",
    "Current Rank": lambda data: f"{data["current_data"]["currenttierpatched"]}",
    "Elo": lambda data: f"{data["current_data"]["elo"]}",
    "Highest Rank": lambda data: f"{data["highest_rank"]["patched_tier"]}",
    "Previous Ranks": lambda data: f"{data["by_season"][previous_seasons[0]]["final_rank_patched"]},{data["by_season"][previous_seasons[1]]["final_rank_patched"]},{data["by_season"][previous_seasons[2]]["final_rank_patched"]}",  # TODO return all 3 previous season ranks separated by commas
  }
  with open(downloads_path + "\\MMROutput.csv", "w") as file:
    if "Previous Ranks" in selected_options:
      temp = selected_options.copy()
      previous_seasons = getPreviousSeasons(current_season_int, 3)
      temp[temp.index("Previous Ranks")] = ','.join(previous_seasons)  # shows the previous 3 season ranks
      file.write(f"{','.join(temp)}\n")
    else:
      file.write(f"{','.join(selected_options)}\n")
    for user in users:
      tokenized_name = user.split("#")
      try:
        data = getMMRData(region, tokenized_name[0], tokenized_name[1])
      except APIError as error:
        print(f"ERROR: {error}")
        file.write(f"{user},ERROR: {error.status_code} - MESSAGE: {error.message} - DETAILS: {error.details}\n")
      row = []
      for option in selected_options:
        row.append(data_points[option](data))
      file.write(f"{','.join(row)}\n")
  file.close()


myOptions = ["IGN", "RiotID", "Tag", "Agent", "Score Total", "Score Per Round", "Total Kills", "Total Deaths", "Total Assists", "KD Rate", "Total Plants", "Total Defuses", "KAST", "Headshot %", "First Kills", "First Deaths", "First Kill/Death Ratio", "Round:Kills", "Round:Deaths", "Round:Assists", "Round:Traded", "Round:Team Kills", "Round:Plant", "Round:Defuse", "Round:Score", "Round:Loadout Value", "Round:Weapon", "Round:Armor"]
createMatchFile(myOptions, "6e639e2a-fa38-4c94-9df6-5a2ff9feb372")
      
