import numpy as np 
import pandas as pd
from pandas.io.json import json_normalize
import json
import os
from sklearn.metrics.pairwise import cosine_similarity

training_arr = os.listdir('../training')

iterator_tr = 0
frames_tr = []
for js in training_arr:
    print "file "+str(iterator_tr)
        
    with open('../training/'+js) as f:
        d = json.load(f)
    iterator_tr += 1
    df = json_normalize(d["playlists"], record_path="tracks", meta=["pid", "num_tracks"])
    frames_tr.append(df)
    train_data = pd.concat(frames_tr)
     
train = train_data[["track_uri","pid"]]
train = train.groupby("pid")["track_uri"].apply(list)

print train