import numpy as np 
import pandas as pd
from pandas.io.json import json_normalize
import json
import os

result = os.listdir('../result/')

test_arr = os.listdir('../test_def/')
train_arr = os.listdir('../training/')

#acha o pid da melhor candidata
def findBestCands(pid):
    #acessa o arquivo
    with open('../result/'+str(pid)+".json") as p:
        cands = json.load(p)
    #busca a playlist
    res = []
    for c in cands:
        if (c["jac"] > 0.2):
            res.append(c)
    return res

#acessa a melhor candidata e retorna todas as tracks dela     
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
                if p["pid"] == cands:
                    tracks = p["tracks"]
                    return tracks
        else:
            next

iterator = 0
for f in test_arr:  
    with open('../test_def/'+f) as pl:
        pl_data = json.load(pl)
    cands = []
    for p in pl_data["playlists"]:
        iterator += 1
        #agora eu tenho o pid da playlist e preciso procurar as candidatas
        aux = findBestCands(p["pid"])
        if aux:
            for a in aux: 
                if a["jac"] > 0.2:
                    print a
                    findPl(a["cand"])
                    #crio uma funcao aqui que recebe as tracks e uma playlist
                    #retorna a playlist completa e escreve num arquivo

                
    

        
