import os
from dotenv import load_dotenv, dotenv_values
import requests
import json

from ApiEndpoints import getMMRData

load_dotenv()

list_of_names = [
  "CU ClownZ#7647",
  "CU Boomcycle#9999",
  "CU Bapo#Quaan",
  "MissSquirrel#EEPY",
  "Yum58#6857",
  "ReTap#1shot",
  "USA Supermnot#Coach",
  "CU Golden#llama",
  "CU Sly#reapr",
  "CU Jumble#reese",
]

API_KEY = os.getenv("API_KEY")
region = "na"

with open("./output.csv", "w") as f:
  f.write("IGN,RiotID,Tag,puuid,current rank,highest rank,elo\n")
  for x in list_of_names:
    tokenized = x.split("#")
    name = tokenized[0]
    tag = tokenized[1]
    # response = requests.get(
    #   f"https://api.henrikdev.xyz/valorant/v2/mmr/{region}/{name}/{tag}",
    #   headers={"Authorization":API_KEY, "Accept":"*/*"},
    # )
    try:
      data = getMMRData(region, name, tag)
      currentData = data["current_data"]

      IGN = f"{name}#{tag}"
      puuid = data["puuid"]
      currentRank = currentData["currenttierpatched"]
      highestRank = data["highest_rank"]["patched_tier"]
      elo = currentData["elo"]
      f.write(f"{IGN},{name},{tag},{puuid},{currentRank},{highestRank},{elo}\n")
    except requests.exceptions.HTTPError as error:
      print(error)
      f.write(f"{IGN},ERROR\n")
