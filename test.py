import csv
import os
import requests

with open(f"static/data/club-data.csv", 'r', newline='') as source2:
    csvreader = csv.reader(source2)
    header = next(csvreader)
    for row in csvreader:
        club_id = row[5]
        with open(f"static/data/{club_id}/{club_id}.csv", 'r', newline='') as source, open(f"static/data/{club_id}/{club_id}-results.csv", 'w', newline='') as result:
            csvreader = csv.reader(source)
            csvwriter = csv.writer(result)
            header = next(csvreader)
            header.append("username")
            header.append("password")
            csvwriter.writerow(header)
            for row in csvreader:
                row.append(club_id)
                r = requests.get(url = "https://passwordinator.onrender.com/?num=true&char=true&caps=true&len=10")
                data = r.json()
                row.append(data['data'])
                csvwriter.writerow(row)
        os.remove(f"static/data/{club_id}/{club_id}.csv")
        os.rename(f"static/data/{club_id}/{club_id}-results.csv",f"static/data/{club_id}/{club_id}.csv")
