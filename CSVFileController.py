from pathlib import Path

outputFileLocation = str(Path.home() / "Downloads")

def createCSVFile(data: list, fileName="output.csv"):
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
  
  """
  output_file = outputFileLocation + f"\\{fileName}"
  with open(output_file, "w") as file:
    columns = data.pop(0)
    file.write(f"{','.join(columns)}\n")  # Writes first line which is column names
    for row_data in data:
      row = []
      for column_name in columns:
        row.append(row_data[column_name])
      file.write(f"{','.join(row)}\n")
      
    file.close()