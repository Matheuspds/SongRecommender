import numpy as np 
import pandas as pd
from pandas.io.json import json_normalize
import json
import os


training_arr = os.listdir('./training/')
iterator = 0
for js in training_arr:
    frames = []
    with open('./training/'+js) as f:
        d = json.load(f)
    iterator += 1
    print iterator
    df = json_normalize(d["playlists"], record_path="tracks", meta=["pid", "num_tracks"])
    frames.append(df)
    if iterator == 1:
        break
train_data = pd.concat(frames)

train = train_data[train_data.columns[7:9]]

print train["track_uri"].tolist()


#df_list = [pd.read_table(file) for file in training_arr]

#big_df = pd.concat(df_list)