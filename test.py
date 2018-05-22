import numpy as np 
import pandas as pd
from pandas.io.json import json_normalize
import json
import os


training_arr = os.listdir('../training/')
iterator = 0
for js in training_arr:
    frames = []
    with open('../training/'+js) as f:
        d = json.load(f)
    iterator += 1
    df = json_normalize(d["playlists"], record_path="tracks", meta=["pid", "num_tracks"])
    frames.append(df)
    if iterator == 1:
        break
train_data = pd.concat(frames)

train = train_data[train_data.columns[7:9]]

users = (train.groupby('pid')
            .apply(lambda x: x['track_uri'].tolist())
            .reset_index())
#print users 

dva1 = pd.DataFrame(users[0].tolist(),)

#print dva1.head()

users = users.drop(0, axis=1)

data_final = pd.concat([users, dva1], axis=1)

num_columns = len(data_final.columns)

cols = range(0, num_columns-1)

#df2[cols] = df2[cols].replace({'0':np.nan, 0:np.nan})

data_final[cols] = data_final[cols].replace({None: 0})

print data_final

#df_list = [pd.read_table(file) for file in training_arr]

#big_df = pd.concat(df_list)da