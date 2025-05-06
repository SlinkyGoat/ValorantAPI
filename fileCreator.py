import os
from dotenv import load_dotenv, dotenv_values
import requests
from pathlib import Path

from ApiEndpoints import (
  APIError,
  getAccountData,
  getMatchData,
  getMMRData
)
from helper import *

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
data = {}
row: list[str] = []

def createAccountFile(selected_options: list, users: list[str]):
  data_points = {
    "IGN": lambda data: f"{data["name"]}#{data["tag"]}",
    "RiotID": lambda data: f"{data["name"]}",
    "Tag": lambda data: f"{data["tag"]}",
    "puuid": lambda data: f"{data["puuid"]}",
    "Account Level": lambda data: f"{str(data["account_level"])}"
  }
  with open(downloads_path + "\\output.csv", "w") as file:
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


def createMatchFile(selected_options: list, users: list[str]):
  pass


def createMMRFile(selected_options: list, user: list[str]):
  pass

# with open(downloads_path, "w") as file:
#   previousSeasonsToRecord = getPreviousSeasons(29, 3)
#   file.write("IGN,RiotID,Tag,puuid,current rank,highest rank,elo")
#   for season in previousSeasonsToRecord:
#     file.write(f",{season}")
#   file.write("\n")
#   for x in list_of_names:
#     tokenized = x.split("#")
#     name = tokenized[0]
#     tag = tokenized[1]
#     try:
#       data = getMMRData(region, name, tag)
#       currentData = data["current_data"]
#       seasonData = data["by_season"]

#       IGN = f"{name}#{tag}"
#       puuid = data["puuid"]
#       currentRank = currentData["currenttierpatched"]
#       highestRank = data["highest_rank"]["patched_tier"]
#       elo = currentData["elo"]
#       file.write(f"{IGN},{name},{tag},{puuid},{currentRank},{highestRank},{elo}")
#       for season in previousSeasonsToRecord:
#         file.write(f",{seasonData[season]["final_rank_patched"]}")
#       file.write("\n")
#     except requests.exceptions.HTTPError as error:
#       print(error)
#       file.write(f"{IGN},ERROR\n")
      
