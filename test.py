import csv

def call_python_function():
    leader_role = "King"
    leader_name = "Bob Jones"
    club_id = "Bird-Club"
    print(leader_role,leader_name)
    with open(f"static/data/{club_id}/{club_id}-leadership.csv", 'a',newline='', encoding='utf-8') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow([leader_name,leader_role,''.join([x[0].upper() for x in leader_name.split(' ')])])

call_python_function()