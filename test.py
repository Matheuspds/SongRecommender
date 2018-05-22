import numpy as np 
import pandas as pd
from pandas.io.json import json_normalize
import json
import os


training_arr = os.listdir('../data/training/')
iterator = 0
for js in training_arr:
    print iterator
    frames = []
    with open('../data/training/'+js) as f:
        d = json.load(f)
    iterator += 1
    df = json_normalize(d["playlists"], record_path="tracks", meta=["pid", "num_tracks"])
    frames.append(df)
train_data = pd.concat(frames)
train = train_data[["track_uri","pid"]]
train = train.groupby("pid")["track_uri"].apply(list)

test_arr = os.listdir('../data/test_def/')
iterator = 0
for js in training_arr:
    print iterator
    frames = []
    with open('../data/test_def/'+js) as f:
        d = json.load(f)
    iterator += 1
    df = json_normalize(d["playlists"], record_path="tracks", meta=["pid", "num_tracks"])
    frames.append(df)
test_data = pd.concat(frames)
test = test_data[["track_uri","pid"]]
test = test.groupby("pid")["track_uri"].apply(list)