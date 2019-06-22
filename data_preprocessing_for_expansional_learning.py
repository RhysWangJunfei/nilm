import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split 

'''Sliding window function'''
def create_dataset(dataset, look_back=1):
    dataX = []
    for i in range(len(dataset)-look_back+1):
        a = dataset[i:(i+look_back)]
        dataX.append(a)
    return np.array(dataX)

base_dir='D://canada//uwo//project//dataset//'
WHE_data = pd.read_csv(base_dir+'Electricity_WHE.csv')
CDE_data = pd.read_csv(base_dir+'Electricity_CDE.csv')

WHE_data['new_time']=pd.to_datetime(WHE_data['unix_ts'],unit='s')

final_hourly=[]
window_size=24


for i in range (0,60):
    offset=str(i)+'T'
    WHE_new = WHE_data.shift(-i)['P']
    WHE_new = WHE_new[0:-i]
    WHE_time = WHE_data[0:-i]['new_time']
    whe_code = pd.concat([WHE_time, WHE_new], axis=1)
    WHE_hourly = whe_code.resample('H',on='new_time',how='sum',loffset=offset)['P']
    dataX = create_dataset(WHE_hourly.as_matrix(), window_size)
    final_hourly.append(dataX)

final_appY=[]
for i in range (0,60):
    CDE_hourly = CDE_data.loc[CDE_data['unix_ts']%3600==(i*60)]['P']
    app_Y = CDE_hourly[window_size-1:].values.reshape([CDE_hourly.shape[0]\
                                                      -window_size+1,1])
    final_appY.append(app_Y)
    
final_time=[]
for i in range (0,60):
    CDE_time = CDE_data.loc[CDE_data['unix_ts']%3600==(i*60)]['unix_ts']
    time_array = CDE_time[window_size-1:].values.reshape([CDE_time.shape[0]\
                                                  -window_size+1,1])
    final_time.append(time_array)

final_appY.remove(final_appY[0])
final_hourly.remove(final_hourly[0])

dataX = np.concatenate(final_hourly,axis=0)
app_Y = np.concatenate(final_appY,axis=0)
    
'''
import pickle
file_name='final_time'
file_obj = open(file_name,'wb')
pickle.dump(final_time,file_obj)
file_obj.close()
'''
