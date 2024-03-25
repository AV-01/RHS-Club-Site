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


