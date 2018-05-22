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


""" def makeRank(train_arr, test_arr):
    res = {}
    interator = 0
    for f in test_arr:
        with open('../data/test_def/'+f) as pl:
            test_data = json.load(pl)
        print "calculating file " + f + " " + str(interator)
        for p_test in test_data["playlists"]:
            iterator = 0
            evaluate = []
           
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
        interator += 1 """

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
training_data = []
for f2 in training_arr:
    with open('../data/training/'+f2) as pl2:
        training_data.append(json.load(pl2))
test_arr = os.listdir('../data/test_def/')

#makeRank(training_arr, test_arr)

print training_data






# #print searchBest(pl_u, file_arr)

# def cosine_similarity(vec1,vec2):
#     sum11, sum12, sum22 = 0, 0, 0
#     for i in range(len(vec1)):
#         x = vec1[i]; y = vec2[i]
#         sum11 += x*x
#         sum22 += y*y
#         sum12 += x*y
#     return sum12/math.sqrt(sum11*sum22)

# def cos_sim(pl1, pl2, cat):
#     vec1 = []
#     vec2 = []
#     valid = 0
#     for p1 in pl1[cat]: 
#         vec1.append(1)
#     for p1 in pl1[cat]:
#         if p1 in pl2[cat]:
#             vec2.append(1)
#         else:
#             vec2.append(0)
#     for v in vec2:
#         if v == 1:
#             valid = 1
#     if valid:
#         return cosine_similarity(vec1, vec2)
#     else: 
#         return 0




