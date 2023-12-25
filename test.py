import csv
import pandas as pd

df = pd.read_csv('static/data/club-data.csv')

for index, row in df.iterrows():
    real_path = row['id']
    fields = ['img_path', 'social_name']
    data = [['bi-google', "aryavrat.mishra@rocklinusd.org"]]
    with open(f"static/data/{real_path}/{real_path}-socials.csv",
              'w',newline='') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow(fields)
        csvwriter.writerows(data)