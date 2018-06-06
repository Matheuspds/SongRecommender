import numpy as np 
import pandas as pd
from pandas.io.json import json_normalize
import json
import os

result = os.listdir('../result/')
result_cosine = os.listdir('../result_cosine/')
test_arr = os.listdir('../test_def/')
train_arr = os.listdir('../training/')

#Lets only the tracks (removes artist and album) in the playlist
def trackerize(pl):
    new_p = {}
    new_p["tracks"] = []
    new_p["num_tracks"] = pl["num_tracks"]
    new_p["pid"] = pl["pid"]
    for track in pl["tracks"]:
        tr = {}
        tr["track_uri"] = track["track_uri"]
        tr["track_name"] = track["track_name"]
        new_p["tracks"].append(tr)
    return new_p

#Select the best candidates with similarity superior to 0.2
def findBestCands(pid):
    with open('../result/'+str(pid)+".json") as p:
        cands = json.load(p)
    res = []
    for c in cands:
        if (c["jac"] > 0.2):
            res.append(c)
    return res

def findBestCandsCosine(pid):
    with open('../result_cosine/'+str(pid)+".json") as p:
        cands = json.load(p)
    res = []
    for c in cands:
        if (c["cos"] > 0.2):
            res.append(c)
    return res


#Access the playlist with best similiarity and returns its tracks 
def findPl(cands):
    for f in train_arr:
        s = f.replace('mpd.slice.','')
        s = s.replace('.json', '')
        a,b = s.split('-')
        tracks = []
        if int(cands) > int(a) and int(cands) < int(b):
            with open('../training/'+f) as pl:
                pl_data = json.load(pl)
            for p in pl_data["playlists"]:
                p = trackerize(p)
                if p["pid"] == cands:
                    tracks = p["tracks"]
                    return tracks
        else:
            next

#Fills the incomplete Playlist with the data of the best candidates
def complete(tracks, pl, path):
    new_p = trackerize(pl)
    for i in tracks:
        if len(new_p["tracks"]) < pl["num_tracks"]:
            if i not in new_p["tracks"]:
                new_p["tracks"].append(i)
    new_p["added"] = len(new_p["tracks"])-len(pl["tracks"])
    if len(new_p["tracks"]) == pl["num_tracks"]: 
        with open("../"+path+"/"+str(new_p["pid"])+".json", "w") as result:
            json.dump(new_p, result)


#Executes the algorithm of recommendation
for f in test_arr:  
    with open('../test_def/'+f) as pl:
        pl_data = json.load(pl)
    cands = []
    for p in pl_data["playlists"]:
        aux = findBestCands(p["pid"])
        if aux:
            for a in aux: 
                if a["jac"] > 0.2:
                    tracks = findPl(a["cand"])
                    complete(tracks, p, "complete")
                
for f in test_arr:  
    with open('../test_def/'+f) as pl:
        pl_data = json.load(pl)
    cands = []
    for p in pl_data["playlists"]:
        aux = findBestCandsCosine(p["pid"])
        if aux:
            for a in aux: 
                if a["cos"] > 0.2:
                    tracks = findPl(a["cand"])
                    complete(tracks, p, "complete_cosine")
                