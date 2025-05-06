import os
from dotenv import load_dotenv, dotenv_values
import requests
from requests.models import Response

load_dotenv()

API_KEY = os.getenv("API_KEY")


class APIError(Exception):
  """Custom Exception for API errors

  Parameters:
    status_code (int): The HTTP status code of the error.
    message (str): The error message returned by the API.
    details (str): Additional details about the error.
    api_called (str): The API endpoint or method that was called (optional).
  
  """
  def __init__(self, status_code: int, message: str, details: str, api_called: str = "unkown"):
    self.status_code  = status_code
    self.message = message
    self.details = details
    self.api_called = api_called
    super().__init__(f"APIError {status_code}: {message} - {details}. Called from {api_called}")


def raiseAPIError(response: Response, valuesCalled=""):
  data: dict = response.json()
  status_code = response.status_code
  message = data["errors"][0]["message"]
  details = data["errors"][0]["details"]
  raise APIError(status_code, message, details, valuesCalled)


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
    APIError
      If response did not have a 200 status. Includes the status, message, and details
      as well as the method call with its parameters
  
  """
  response = requests.get(
    f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}",
    headers={"Authorization":API_KEY, "Accept":"*/*"},
  )
  if response.status_code != 200:
    raiseAPIError(response, f"getAccountData({name}, {tag})")

  return response.json()["data"]


def getMatchData(matchid: str) -> dict:
  """Gets data from a single match

  Parameters
  ----------
  matchid : str
    the unique identifier for the match whose data is to be pulled

  Raises
  ------
    APIError
      If response did not have a 200 status. Includes the status, message, and details
      as well as the method call with its parameters
  """

  response = requests.get(
    f"https://api.henrikdev.xyz/valorant/v2/match/{matchid}",
    headers={"Authorization":API_KEY,"Accept":"*/*"},
  )
  if response.status_code != 200:
    raiseAPIError(response, f"getMatchData({matchid})")
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
    APIError
      If response did not have a 200 status. Includes the status, message, and details
      as well as the method call with its parameters
  
  """
  response = requests.get(
    f"https://api.henrikdev.xyz/valorant/v2/mmr/{region}/{name}/{tag}",
    headers={"Authorization":API_KEY,"Accept":"*/*"},
  )
  if response.status_code != 200:
    raiseAPIError(response, f"getMMRData({region}, {name}, {tag})")
  return response.json()["data"]