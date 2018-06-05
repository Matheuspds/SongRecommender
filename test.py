import numpy as np 
import pandas as pd
from pandas.io.json import json_normalize
import json
import os

def pushArr(arr, obj):
    if len(arr) < 4:
        arr.append(obj)
        return evaluate
    else:
        for i in arr:
            if i["jac"] < obj["jac"]:
                i = obj
                break
        return evaluate

def jaccard(a, b):
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

training_arr = os.listdir('../training/')
iterator_tr = 0

test_arr = os.listdir('../test_def/')
iterator_tes = 0
frames = []
for js in test_arr:
    print iterator_tes
    
    with open('../test_def/'+js) as f:
        d = json.load(f)
    iterator_tes += 1
    df = json_normalize(d["playlists"], record_path="tracks", meta=["pid", "num_tracks"])
    frames.append(df)
    test_data = pd.concat(frames)

test = test_data[["track_uri","pid"]]
test = test.groupby("pid", as_index=True)["track_uri"].apply(list)

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

for k, p in test.iteritems():
    evaluate = []
    for k2, p2 in train.iteritems():
        obj = {}
        el1 = set(p)
        el2 = set(p2)
        obj["jac"] = jaccard(el1, el2)
        if obj["jac"] > 0.0:
            obj["pid"] = k
            obj["cand"] = k2
            evaluate = pushArr(evaluate, obj)
    with open("../result/"+str(k)+".json", "w") as result:
        json.dump(evaluate, result)