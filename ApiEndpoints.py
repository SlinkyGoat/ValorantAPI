import os
from dotenv import load_dotenv, dotenv_values
import requests
from requests.models import Response

load_dotenv()

API_KEY = os.getenv("API_KEY")


def raiseHTTPError(response: Response, valuesCalled=""):
  data: dict = response.json()
  errorString = f"""Error: {response.status_code}
    Message: {data["errors"][0]["message"]}
    Details: {data["errors"][0]["details"]}"""
  if valuesCalled != "":
    errorString += f"\n\tAPI Called: {valuesCalled}"
  raise requests.exceptions.HTTPError(errorString)


def getAccountData(name: str, tag: str) -> dict:
  """Calls the Account API Endpoint and returns a dict with account details

  Parameters
  ----------
  name : str
    The player's username excluding the # symbol or the tag thereafter

  tag : str
    The player's tag that comes after username#

  Raises
  ------
    requests.exceptions.HTTPError
      If response did not have a 200 status. Includes the status, message, and details
      as well as the method call with its parameters
  
  """
  response = requests.get(
    f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}",
    headers={"Authorization":API_KEY, "Accept":"*/*"},
  )
  if response.status_code != 200:
    raiseHTTPError(response, f"getAccountData({name}, {tag})")

  return response.json()["data"]


def getMMRData(region: str, name: str, tag: str) -> dict:
  """Gets a more detailed response for all MMR data
  
  Parameters
  ----------
  region : str
    region the player is from
    possible values :
      eu (Europe)
      na (North America)
      latam (Latin America)
      br (Brazil)
      ap (Asia Pacific)
      kr (South Korea)

  name : str
    The player's username excluding the # symbol or the tag thereafter

  tag : str
    The player's tag that comes after username#

  Raises
  ------
    requests.exceptions.HTTPError
      If response did not have a 200 status. Includes the status, message, and details
      as well as the method call with its parameters
  
  """
  response = requests.get(
    f"https://api.henrikdev.xyz/valorant/v2/mmr/{region}/{name}/{tag}",
    headers={"Authorization":API_KEY,"Accept":"*/*"},
  )
  if response.status_code != 200:
    raiseHTTPError(response, f"getMMRData({region}, {name}, {tag})")
  return response.json()["data"]