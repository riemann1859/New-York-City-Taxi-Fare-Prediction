# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 01:58:34 2019

@author: YUNUS
"""
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from preparing_data import preparing_data

#divide the whole training into 50 parts randomly

np.random.seed(22)
x=np.arange(1,54273574)
np.random.shuffle(x)
parts=np.split(x[:50000000],25)

#our strategy is that to avoid memory problems, instead of taking a training sample
#of size 5000000, take a sample of size 1000000 and establish a random forest model on this 
#sample and predict the test data, repeat this process 5 times, finally average the 
#resulting 5 prediction sets 





# the followings are data types in the original training data

types = {'fare_amount': 'float32',
         'pickup_longitude': 'float32',
         'pickup_latitude': 'float32',
         'dropoff_longitude': 'float32',
         'dropoff_latitude': 'float32',
         'passenger_count': 'uint8'}
    

    

for i in range(10):
    start_time = time.time()
    print(start_time)
    rows_chosen=list(parts[i])
    rows_chosen.append(0)
    rows_chosen.sort()
    
    #54273574 is the total number of row in the modified training data
    
    rows_skipped=list(set(list(range(0,54273574)))-set(rows_chosen))
    rows_skipped.sort()
    df=pd.read_csv('D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/modified_taxi_data2.csv', header=0, skiprows=rows_skipped, dtype=types)

    
    #delete rows when  fare_amount<=0 or >200
    df.drop(df[(df.fare_amount<=0)|(df.fare_amount>200)].index,axis=0, inplace=True)
    df=preparing_data(df)
    X=df.drop('fare_amount', axis=1)
    y=df['fare_amount']
    if i==0:
        rfr=RandomForestRegressor(warm_start=True, n_estimators=20, max_features=int(X.shape[1]/3))
        rfr.fit(X,y)
    else:
        rfr.set_params(n_estimators=20*(i+1), max_features=int(X.shape[1]/3))
        rfr.fit(X,y)
    print("--- %s seconds ---" % (time.time() - start_time))
 
    
#We finally prepare test_data and predict it and then prepare the submission file
 

df_test=pd.read_csv('D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/modified_taxi_test_data2.csv', header=0,  dtype=types)
d={}
d['key']=df_test.key
new_df_test=preparing_data(df_test)
y_pred=rfr.predict(new_df_test)

d['fare_amount']=np.round(y_pred,2)


pred_submission=pd.DataFrame(d, columns=['key','fare_amount'])
add_pred='D:/datasets/kaggle/New York City Taxi Fare Prediction/pred18.csv'
pred_submission.to_csv(add_pred, index=False)
print("finish_time:",time.time())

#4 tane 3.11(estimatorların toplam sayısı 200)

#10 tane 3.09536 (estimatorların toplam sayısı 200)

#5 tane (estimator)
