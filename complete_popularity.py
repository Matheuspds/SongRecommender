import numpy as np 
import pandas as pd
from pandas.io.json import json_normalize
import json
import os

df = pd.read_json('../ranking/ranking.json')

df = df.sort_values(by='frequency', ascending=False)

test_arr = os.listdir('../test_def/')


# for f in test_arr:
#     with open('../test_def/'+f) as r:
#         pl = json.load(r)
#     for p in pl["playlists"]:
#         for row in df.iterrows():
#             track = row[1]["track_uri"] 
#             add = 1
#             for tr in p["tracks"]:
#                 if track == tr["track_uri"]
