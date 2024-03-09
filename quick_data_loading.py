import pandas as pd
import os

df = pd.read_csv('static/data/club-data.csv')

for index, row in df.iterrows():
    fields = ['name', 'category', 'img', 'time-update', 'id', 'meeting']
    data = [[
        row['name'], row['category'], row['img'], row['time-update'], row['id'],
        "Whenever I feel like it"
    ]]
    real_path = row['id']
    try:
        os.mkdir(f"static/data/{real_path}")
    except:
        w = True
    with open(f"static/data/{real_path}/{real_path}.csv", 'w',newline='', encoding='utf-8') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow(fields)
        csvwriter.writerows(data)
    default_desc = """
  <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
    dolore magna aliqua. Volutpat maecenas volutpat blandit aliquam etiam erat. Id semper risus in hendrerit
    gravida rutrum quisque non tellus. Magna etiam tempor orci eu. Eget gravida cum sociis natoque penatibus et
    magnis dis. Cursus eget nunc scelerisque viverra mauris in aliquam sem. Montes nascetur ridiculus mus mauris
    vitae ultricies leo. Diam sollicitudin tempor id eu nisl nunc mi. Morbi tincidunt ornare massa eget egestas.
    Magna etiam tempor orci eu lobortis elementum nibh tellus molestie. Urna nec tincidunt praesent semper
    feugiat nibh sed pulvinar proin.</p>
  <p>
    Nulla porttitor massa id neque aliquam vestibulum morbi blandit cursus. Sit amet consectetur adipiscing elit
    pellentesque habitant morbi tristique senectus. Tincidunt tortor aliquam nulla facilisi cras fermentum odio
    eu feugiat. Semper viverra nam libero justo laoreet sit amet cursus. In ante metus dictum at. Bibendum ut
    tristique et egestas quis ipsum suspendisse ultrices. Malesuada bibendum arcu vitae elementum. Porta non
    pulvinar neque laoreet suspendisse interdum consectetur. Rhoncus dolor purus non enim praesent elementum
    facilisis leo. Pellentesque adipiscing commodo elit at imperdiet dui accumsan sit amet. At in tellus integer
    feugiat scelerisque varius morbi enim. Tristique senectus et netus et malesuada fames ac turpis. Turpis
    massa sed elementum tempus egestas sed sed. Malesuada fames ac turpis egestas integer eget aliquet. Viverra
    orci sagittis eu volutpat odio facilisis mauris sit. Duis ut diam quam nulla porttitor massa. Feugiat in
    fermentum posuere urna nec tincidunt. Cum sociis natoque penatibus et magnis dis parturient montes nascetur.
    Commodo odio aenean sed adipiscing diam donec. Viverra nam libero justo laoreet sit.
  </p>
  """
    with open(f"static/data/{real_path}/{real_path}-desc.txt", "w") as text_file:
        text_file.write(default_desc)
    fields = ['img_path', 'social_name']
    data = [['/static/icons/email.webp', "aryavrat.mishra@rocklinusd.org"]]
    with open(f"static/data/{real_path}/{real_path}-socials.csv",
              'w',newline='', encoding='utf-8') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow(fields)
        csvwriter.writerows(data)

    fields = ['name', 'role', 'initials']
    data = [['Aryavrat Mishra', 'Dictator', 'AM']]
    with open(f"static/data/{real_path}/{real_path}-leadership.csv",'w',newline='', encoding='utf-8') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow(fields)
        csvwriter.writerows(data)
