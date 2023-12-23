import csv

club_id = "Bird-Club"
real_path = f"static/data/{club_id}"
Func = open(f"templates/{club_id}.html", "w")
all_data = []
with open(f"{real_path}/{club_id}.csv", 'r') as file:
    csvreader = csv.reader(file, delimiter=',')
    for row in csvreader:
        all_data.append(row)
club_basic_data = all_data[1:][0]
print(club_basic_data)