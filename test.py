# import csv
# import os
# import requests
# from pathlib import Path
# from datetime import datetime,timezone
#
# all_data = []
# with open(f"static/data/club-data.csv", 'r') as file:
#     csvreader = csv.reader(file, delimiter=',')
#     header = next(csvreader)
#     for row in csvreader:
#         all_data.append(row)
# clubs_by_category = {}
# for club in all_data:
#     category = club[3]
#     if category not in clubs_by_category:
#         clubs_by_category[category] = []
#     clubs_by_category[category].append({
#         'name': club[0],
#         'image': club[1],
#         'description': club[2],
#         'joined_date': club[4],
#         'club_id': club[5]
#     })
# print(clubs_by_category)


import pandas as pd
import os

# Read the main club data CSV
club_data_df = pd.read_csv("club-data.csv")

# Define the function to process each file
def process_file(file_path):
    # Read the leadership CSV file
    leadership_df = pd.read_csv(file_path)

    # Add a new column "icon_color" with default value "bg-info"
    leadership_df['icon_color'] = 'bg-info'

    # Save the modified CSV
    leadership_df.to_csv(file_path, index=False)

# Iterate through directories and files
directory = "static/data/"
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith("-leadership.csv"):
            file_path = os.path.join(root, file)
            process_file(file_path)

print("All files processed successfully.")
