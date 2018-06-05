import json
import os

result = os.listdir('../result/')
test_arr = os.listdir('../test/')
train_arr = os.listdir('../training/')
complete_arr = os.listdir('../complete/')
complete_cos_arr = os.listdir('../complete_cosine/')

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

#Gets the complete playlist with the original tracks
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

#Gets the playlist completed by the algorithm
def getPlRecommended(pid):
    with open('../complete/'+str(pid)+".json") as pl:
        pl_data = json.load(pl)
    return pl_data

def getPlRecommendedCos(pid):
    with open('../complete_cosine/'+str(pid)+".json") as pl:
        pl_data = json.load(pl)
    return pl_data

#Executes evaluation
withheld_tracks = 0
relevant_recommended_tracks = 0
for i in complete_arr:
    i = i.replace('.json', '')
    p_original = trackerize(getPlOriginal(i))
    p_recommend = getPlRecommended(i) 
    error = 0
    for track in p_original["tracks"]:
        if track not in p_recommend["tracks"]:
            error += 1 
    withheld_tracks += p_recommend["added"]
    relevant_recommended_tracks += (p_recommend["added"] - error)
    print p_original["pid"] , "adicionei", p_recommend["added"],  "acertei", p_recommend["added"] - error
r_precision = relevant_recommended_tracks / float(withheld_tracks)

print "R Precision Jaccard is ", r_precision

withheld_tracks = 0
relevant_recommended_tracks = 0
for i in complete_cos_arr:
    i = i.replace('.json', '')
    p_original = trackerize(getPlOriginal(i))
    p_recommend = getPlRecommendedCos(i) 
    error = 0
    for track in p_original["tracks"]:
        if track not in p_recommend["tracks"]:
            error += 1 
    withheld_tracks += p_recommend["added"]
    relevant_recommended_tracks += (p_recommend["added"] - error)
    print p_original["pid"] , "adicionei", p_recommend["added"],  "acertei", p_recommend["added"] - error
r_precision = relevant_recommended_tracks / float(withheld_tracks)

print "R Precision Cosine is ", r_precision



