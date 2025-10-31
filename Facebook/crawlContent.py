# import pandas as pd

# def crawlContent(num_sheet):
#     spreadsheet_id = "1pDS-IWI--FWVgOYuMBqsbbANGTvGkmHIBWdFgFvR-hU"
#     url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={num_sheet}"

#     try:
#         df = pd.read_csv(url, on_bad_lines='skip', quotechar='"')
#     except Exception as e:
#         print("Error:", e)

#     df = df.drop(columns="instruction")
#     df.to_csv("data/content/contentFull.csv", index=False)

