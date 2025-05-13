from pathlib import Path

outputFileLocation = str(Path.home() / "Downloads")

def createCSVFile(data: list, fileName="output.csv", rounds=0):
  """Creates a csv file with the inputted data

  Parameters
  ----------
    data list(dict):
      A list containing the data to write to the file.
      The first item in the list is a list of strings representing the first row of the CSV file initializing the columns.
      Each subsequent item is a dictionary which should have values that match the first list.

    fileName (str):
      The name of the file to output
      DEFAULT is 'output.csv'
      NOTE: As of now the output location will always be the Downloads folder.

    rounds (int):
      The number of rounds in a match.
      This is used for outputting a Match file when a round-by-round data point is selected

  
  """
  output_file = outputFileLocation + f"\\{fileName}"
  with open(output_file, "w") as file:
    columns: list[str] = data.pop(0)
    round_by_round_options = []
    for column in columns[:]:
      if column.startswith("Round:"):
        round_by_round_options.append(column.split(":")[1])
        columns.remove(column)
    if round_by_round_options:
      for game_round in range(rounds):
        for round_option in round_by_round_options:
          columns.append(f"Round {game_round + 1} {round_option}")
          
    file.write(f"{','.join(columns)}\n")  # Writes first line which is column names
    for row_data in data:
      row = []
      for column_name in columns:
        row.append(row_data[column_name])
      file.write(f"{','.join(row)}\n")

    file.close()