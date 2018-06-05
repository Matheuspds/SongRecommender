from sklearn.metrics import precision_score
from math import sqrt
import json
import os

result = os.listdir('../result/')

test_arr = os.listdir('../test/')
train_arr = os.listdir('../training/')
complete_arr = os.listdir('../complete/')

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

def getPlOriginal(pid):
    for f in test_arr:
        s = f.replace('mpd.slice.','')
        s = s.replace('.json', '')
        a,b = s.split('-')
        if int(pid) >= int(a) and int(pid) <= int(b):
            with open('../test/'+f) as pl:
                pl_data = json.load(pl)
            for p in pl_data["playlists"]:
                if p["pid"] == int(pid):
                    return p    
        else:
            next

def getPlRecommended(pid):
    with open('../complete/'+str(pid)+".json") as pl:
        pl_data = json.load(pl)
    return pl_data

pid = 1259
p_original = trackerize(getPlOriginal(pid))
p_recommend = getPlRecommended(pid)
cont = 0

def unify(p):
    tracks = []
    for i in p["tracks"]:
        tracks.append(i["track_uri"])
    return tracks

for i in complete_arr:
    i = i.replace('.json', '')
    p_original = trackerize(getPlOriginal(i))
    p_recommend = getPlRecommended(i) 
    error = 0
    for track in p_original["tracks"]:
        if track not in p_recommend["tracks"]:
            error += 1 
    #r = precision_score(unify(p_original), unify(p_recommend), average='macro')
    print p_original["pid"] , "adicionei", p_recommend["added"],  "acertei", p_recommend["added"] - error
    #print r 



