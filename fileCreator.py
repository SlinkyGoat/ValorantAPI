import os
from dotenv import load_dotenv, dotenv_values
import requests

from ApiEndpoints import getMMRData
from helper import *

load_dotenv()

list_of_names = [
  "CU ClownZ#7647",
  "CU Boomcycle#9999",
  "Yum58#6857",
  "ReTap#1shot",
  "USA Supermnot#Coach",
  "CU Golden#llama",
]

API_KEY = os.getenv("API_KEY")
region = "na"
currentSeason = 'e10a2'

with open("./output.csv", "w") as f:
  previousSeasonsToRecord = getPreviousSeasons(29, 3)
  f.write("IGN,RiotID,Tag,puuid,current rank,highest rank,elo")
  for season in previousSeasonsToRecord:
    f.write(f",{season}")
  f.write("\n")
  for x in list_of_names:
    tokenized = x.split("#")
    name = tokenized[0]
    tag = tokenized[1]
    try:
      data = getMMRData(region, name, tag)
      currentData = data["current_data"]
      seasonData = data["by_season"]

      IGN = f"{name}#{tag}"
      puuid = data["puuid"]
      currentRank = currentData["currenttierpatched"]
      highestRank = data["highest_rank"]["patched_tier"]
      elo = currentData["elo"]
      f.write(f"{IGN},{name},{tag},{puuid},{currentRank},{highestRank},{elo}")
      for season in previousSeasonsToRecord:
        f.write(f",{seasonData[season]["final_rank_patched"]}")
      f.write("\n")
    except requests.exceptions.HTTPError as error:
      print(error)
      f.write(f"{IGN},ERROR\n")
      
      
