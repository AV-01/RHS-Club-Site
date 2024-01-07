import csv
import os
import requests
from pathlib import Path

def test():
    club_id = "Bird-Club"
    real_path = f"static/data/{club_id}"
    all_data = []
    with open(f"{real_path}/{club_id}.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            all_data.append(row)
    club_basic_data = all_data[1]
    print(club_basic_data)
    category = club_basic_data[1]
    club_name = club_basic_data[0]
    meeting_date = club_basic_data[5]
    desc = Path(f'{real_path}/{club_id}-desc.txt').read_text()
    all_data = []
    with open(f'{real_path}/{club_id}-socials.csv') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        for row in csvreader:
            all_data.append(row)
    socials_list = all_data[1:]
    all_data = []
    with open(f'{real_path}/{club_id}-leadership.csv') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        for row in csvreader:
            all_data.append(row)
    leaders_list = all_data[1:]
    print(leaders_list)


test()