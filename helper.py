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