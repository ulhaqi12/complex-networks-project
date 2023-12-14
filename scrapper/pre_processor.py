import json
from tqdm import tqdm
import pandas as pd

json_file_path = "data.json"

actor1 = []
actor2 = []

# Load the JSON data from the file
with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

for i in tqdm(range(len(data))):
    for j in range(i+1, len(data)):
        if data[i]['actor_name'] != data[j]['actor_name']:
            for movie in data[i]['movies']:
                if movie in data[j]['movies']:
                    actor1.append(data[i]['actor_name'])
                    actor2.append(data[j]['actor_name'])
                    break

df = pd.DataFrame()
df['actor1'] = actor1
df['actor2'] = actor2

df.to_csv('actor_edges.csv', index=False)

actor_df = pd.DataFrame(data).drop(['movies'], axis=1)
actor_df.to_csv('actors.csv', index=False)
