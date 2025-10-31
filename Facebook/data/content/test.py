import pandas as pd

curl = "https://docs.google.com/spreadsheets/d/1dAzxOmTbrrekYvk9HqIVBq7A1c61k4kaGOm42w3kGlM/edit?gid=1583500962#gid=1583500962"

df = pd.read_csv(curl)
print(df)