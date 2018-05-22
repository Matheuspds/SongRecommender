import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing, cross_validation
import pandas as pd
import json
from pandas.io.json import json_normalize
import hashlib
import math
import os 






def searchBest(pl_user, file_arr):
    res = {}
    res["tracks"] = {}
    res["tracks"]["cand"] = 0.0
    res["albums"] = {}
    res["albums"]["cand"] = 0.0
    res["artists"] = {}
    res["artists"]["cand"] = 0.0
    iterator = 0
    for f in file_arr:
        iterator += 1
        with open('../data/mpd.v1/data/'+f) as pl:
            pl_data = json.load(pl)
            print "calculating file " + f + " " + str(iterator)
        for p in pl_data["playlists"]:
            p_treat = treatPlay(p)
            if p_treat["pid"] == 2163:
                continue
            jac_tracks = jaccard_pls(p_treat, pl_user, "tracks")
            jac_albums = jaccard_pls(p_treat, pl_user, "albums")
            jac_artists = jaccard_pls(p_treat, pl_user, "artists")
            if  jac_tracks > res["tracks"]["cand"]:
                res["tracks"]["cand"] = float(jac_tracks)
                res["tracks"]["pid"] = p_treat["pid"]
                res["tracks"]["file"] = f
            if  jac_albums > res["albums"]["cand"]:
                res["albums"]["cand"] = float(jac_albums)
                res["albums"]["pid"] = p_treat["pid"]
                res["albums"]["file"] = f
            if  jac_artists > res["artists"]["cand"]:
                res["artists"]["cand"] = float(jac_artists)
                res["artists"]["pid"] = p_treat["pid"]
                res["artists"]["file"] = f
    return res

def treatPlay(pl):
    play = {}
    play["tracks"] = []
    play["albums"] = []
    play["artists"] = []
    play["pid"] = pl["pid"]
    play["num_tracks"] = pl["num_tracks"]
    play["name"] = pl["name"]
    for t in pl["tracks"]:
        obj = {}
        obj["track_name"] = t["track_name"]
        obj["track_uri"] = t["track_uri"]
        play["tracks"].append(obj)
        obj = {}
        obj["album_name"] = t["album_name"]
        obj["album_uri"] = t["album_uri"]
        play["albums"].append(obj) 
        obj = {}
        obj["artist_name"] = t["artist_name"]
        obj["artist_uri"] = t["artist_uri"]
        play["artists"].append(obj)
    return play


def jaccard_pls(pl1, pl2, cat):
    intersection = []
    for p1 in pl1[cat]:
        if p1 in pl2[cat]:
            intersection.append(p1)
    union = []
    for p1 in pl1[cat]:
        union.append(p1)
    for p2 in pl2[cat]:
        if p2 not in union:
            union.append(p2)
    return len(intersection)/float(len(union))


def makeRank(train_arr, test_arr):
    res = {}
    interator = 0
    for f in test_arr:
        with open('../data/test_def/'+f) as pl:
            test_data = json.load(pl)
        print "calculating file " + f + " " + str(interator)
        for p_test in test_data["playlists"]:
            iterator = 0
            evaluate = []
            for f2 in train_arr:
                with open('../data/training/'+f2) as pl2:
                    training_data = json.load(pl2)
                print "verifying file " + str(iterator) + " of 1000"
                iterator+=1
                for p_train in training_data["playlists"]:              
                    jacc = jaccard_pls(p_test, p_train, "tracks")
                    if jacc > 0.0 :   
                        res["origin_pid"] = p_test["pid"]
                        res["cand_pid"] = p_train["pid"]
                        res["similarity"] = jacc
                        evaluate = maxArray(evaluate, res)
                    res = {} 
            with open("../data/result/"+str(p_test["pid"])+".json", "w") as result:
                json.dump(evaluate, result)
        interator += 1

def maxArray(evaluate, res):
    if len(evaluate) <= 4:
        evaluate.append(res)
    else: 
        for i in range(5):
            if evaluate[i]["similarity"] < res["similarity"]:
                evaluate[i] = res
                break
    return evaluate

#file_arr = os.listdir('../data/mpd.v1/data/')
# with open('play.json') as f:
#     pls2 = json.load(f)
# with open('test.json') as f:
#     pls3 = json.load(f)
# pl_u = treatPlay(pls2["playlists"][0])
# pl_t = treatPlay(pls3["playlists"][0])

training_arr = os.listdir('../data/training/')
test_arr = os.listdir('../data/test_def/')

makeRank(training_arr, test_arr)






#print searchBest(pl_u, file_arr)

def cosine_similarity(vec1,vec2):
    sum11, sum12, sum22 = 0, 0, 0
    for i in range(len(vec1)):
        x = vec1[i]; y = vec2[i]
        sum11 += x*x
        sum22 += y*y
        sum12 += x*y
    return sum12/math.sqrt(sum11*sum22)

def cos_sim(pl1, pl2, cat):
    vec1 = []
    vec2 = []
    valid = 0
    for p1 in pl1[cat]: 
        vec1.append(1)
    for p1 in pl1[cat]:
        if p1 in pl2[cat]:
            vec2.append(1)
        else:
            vec2.append(0)
    for v in vec2:
        if v == 1:
            valid = 1
    if valid:
        return cosine_similarity(vec1, vec2)
    else: 
        return 0


def searchBestCos(pl_user, file_arr):
    res = {}
    res["tracks"] = {}
    res["tracks"]["cand"] = 0.0
    res["albums"] = {}
    res["albums"]["cand"] = 0.0
    res["artists"] = {}
    res["artists"]["cand"] = 0.0
    iterator = 0
    for f in file_arr:
        iterator += 1
        with open('../data/mpd.v1/data/'+f) as pl:
            pl_data = json.load(pl)
            print "calculating file " + f + " " + str(iterator)
        for p in pl_data["playlists"]:
            p_treat = treatPlay(p)
            if p_treat["pid"] == 2163:
                continue
            jac_tracks = cos_sim(p_treat, pl_user, "tracks")
            jac_albums = cos_sim(p_treat, pl_user, "albums")
            jac_artists = cos_sim(p_treat, pl_user, "artists")
            if  jac_tracks > res["tracks"]["cand"]:
                res["tracks"]["cand"] = float(jac_tracks)
                res["tracks"]["pid"] = p_treat["pid"]
                res["tracks"]["file"] = f
            if  jac_albums > res["albums"]["cand"]:
                res["albums"]["cand"] = float(jac_albums)
                res["albums"]["pid"] = p_treat["pid"]
                res["albums"]["file"] = f
            if  jac_artists > res["artists"]["cand"]:
                res["artists"]["cand"] = float(jac_artists)
                res["artists"]["pid"] = p_treat["pid"]
                res["artists"]["file"] = f
    return res

#searchBestCos(pl_u, file_arr)



