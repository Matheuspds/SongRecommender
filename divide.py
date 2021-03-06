import json
import math
import os 
import random 

#Creates the training set
def createTraining(file_arr):  
    iterator = 0
    res = {}
    res["playlists"] = []
    for f in file_arr:
        iterator += 1
        with open('../data/mpd.v1/data/'+f) as pl:
            pl_data = json.load(pl)
        print "generating file " + f + " " + str(iterator)  
        res["playlists"] = random.sample(pl_data["playlists"], 700)
        with open("./training/"+f, "w") as training:
            json.dump(res, training)
    return 

#Creates the test set
def createTest(file_arr):
    iterator = 0
    res = {}
    res["playlists"] = []
    for f in file_arr:
        res["playlists"] = []
        iterator += 1
        with open('../data/mpd.v1/data/'+f) as pl:
            pl_data = json.load(pl)
        with open("./training/"+f) as training:
            pl_training = json.load(training)
        for pl in pl_data["playlists"]:
            if pl not in pl_training["playlists"]: 
                res["playlists"].append(pl)
        with open("./test/"+f, "w") as test:
            json.dump(res, test)
        print "generating file " + f + " " + str(iterator) 
    return

#Removes 30% os the musics in a playlist
def testDefinitive(file_array):
    iterator = 0
    res = {}
    res["playlists"] = []
    for f in file_array:
        res["playlists"] = []
        iterator += 1
        with open("../data/test/"+f) as playlists:
            pl_arr = json.load(playlists)
        for p in pl_arr["playlists"]: 
            max_remove = int(math.floor(float(30 * (len(p["tracks"]))) / 100))
            rang = len(p["tracks"]) - max_remove
            p["tracks"] = random.sample(p["tracks"], rang)
            res["playlists"].append(p)
        with open("../data/test_def/"+f, "w") as test:
            json.dump(res, test)
        print "generating file " + f + " " + str(iterator)
    return

#Compare the size of the test set with the one generated without 30% of the musics
def sizeChecker(file1, file2):
    for f in file1:
        with open("./test/"+f) as play:
            pl1_arr = json.load(play)
        with open("./test_def/"+f) as playlists:
            pl2_arr = json.load(playlists)
        for p1, p2 in zip(pl1_arr["playlists"], pl2_arr["playlists"]):
            if len(p2["tracks"]) > len(p1["tracks"]):
                print str(len(p1["tracks"])) + " " + str(len(p2["tracks"]))



test_arr = os.listdir('../data/test')
test_def_arr = os.listdir('../data/test_def')