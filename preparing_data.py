# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 23:46:08 2019

@author: YUNUS
"""

from geographic_functions import zipcode_county_state, distance
from geographic_data import public_facilities
from shapely.geometry import Point
import pandas as pd

state_categories=['Massachusetts', 'Connecticut', 'Pennsylvania', 'New York', 'New Jersey']

county_categories=['Union','Hudson', 'Nassau', 'Passaic','Rockland','Fairfield','Mercer',
                   'Suffolk','Pike', 'Bergen', 'Middlesex', 'New York', 'Somerset',
                   'Ulster', 'Kings', 'Orange', 'Monmouth', 'Northampton', 'Morris',
                   'Westchester','Hunterdon','New Haven','Monroe','Queens',
                   'Dutchess','Sussex','Bronx','Essex','Ocean','Richmond']

zipcode_categories=['10019', '10022', '10003', '10016', '10001', '10011', '10036', '10023',
                    '10017', '10014', '10021', '10065', '10010', '10024', '10012', '10128', 
                    '10028', '10013', '10018', '10025', '10009', '10002', '10075', '11371',
                    '11430', '10119', '10029','11211', '10007', '11201', '10038', '10027',
                    '10004', '10005', '10280', '11101', '10282', '10020', '10035', '10026',
                    '10006','11217', '11215', '11222', '10170', '11106', '10069', '10031', 
                    '11231', '11377', '10165', '11238', '10168', '11102', '10032', '10152',
                    '11103', '11206', '11205', '11104', '10199', '10174', '10153', '11216',
                    '10171', '10172', '10103', '11105','10110', '10033', '11375', '10154',
                    '10167', '11372', '11373', '10112', '10030', '10173', '11221', '10111',
                    '10037', '07114', '11369','11218', '11237', '11225', '10044', '10034', 
                    '11209', '10177', '11368', '10169', '10162', '10040', '11226', '11370',
                    '11109', '10451', '11374', '11385', '10039', '11378', '11232','10278',
                    '06483','10279', '10463', '07030', '11354', '11213', '11435', '11230',
                    '11220', '10454', '11233', '10452', '11367', '11434', '07302', '11436',
                    '11432', '11355', '10462']
                    
def preparing_data(df):
    # input is pandas dataframe
    
    #remove the column named key
    df.drop(labels='key', axis=1, inplace=True)
    #delete rows with suspicous passanger_count
    df.drop(df[(df.passenger_count>6) |(df.passenger_count==0)].index,axis=0, inplace=True)
    
    
    #from lat and lon values to state, county, zipcode values
    df['departure-zipcode'],df['departure-county'],df['departure-state']=zip(*df[['pickup_longitude', 'pickup_latitude']].apply(zipcode_county_state, axis=1))
    df['destination-zipcode'],df['destination-county'],df['destination-state']=zip(*df[['dropoff_longitude', 'dropoff_latitude']].apply(zipcode_county_state, axis=1))
    
    df['to-jfk-airport']=df[['dropoff_longitude',"dropoff_latitude"]].apply(lambda p:public_facilities.iloc[4,4].distance(Point(p[0],p[1]))<0.001,axis=1)
    df['from-jfk-airport']=df[['pickup_longitude',"pickup_latitude"]].apply(lambda p:public_facilities.iloc[4,4].distance(Point(p[0],p[1]))<0.001,axis=1)

    df['to-LaGuardia-airport']=df[['dropoff_longitude',"dropoff_latitude"]].apply(lambda p:public_facilities.iloc[3,4].distance(Point(p[0],p[1]))<0.001,axis=1)
    df['from-LaGuardia-airport']=df[['pickup_longitude',"pickup_latitude"]].apply(lambda p:public_facilities.iloc[3,4].distance(Point(p[0],p[1]))<0.001,axis=1)

    #convert these geographic properties into categoric variables
    df['departure-state']=df['departure-state'].astype('category')
    df['departure-county']=df['departure-county'].astype('category')
    df['departure-zipcode']=df['departure-zipcode'].astype('category')
    df['destination-state']=df['destination-state'].astype('category')
    df['destination-county']=df['destination-county'].astype('category')
    df['destination-zipcode']=df['destination-zipcode'].astype('category')
    df['to-jfk-airport']=df['to-jfk-airport'].astype('category')
    df['from-jfk-airport']=df['from-jfk-airport'].astype('category')
    df['to-LaGuardia-airport']=df['to-LaGuardia-airport'].astype('category')
    df['from-LaGuardia-airport']=df['from-LaGuardia-airport'].astype('category')
    
    #we need to fix the categories in the columns 'departure-state', 'departure-county', 
    #'departure-zipcode', 'destination-state','destination-county','destination-zipcode'
    # for different dataframes by this way we fix the number of features and their name
    # after converting these columns into dummy variables. This is required in random forest application
    
    df['departure-state'].cat.set_categories(state_categories,inplace=True)
    df['departure-county'].cat.set_categories(county_categories,inplace=True)
    df['departure-zipcode'].cat.set_categories(zipcode_categories,inplace=True)

    df['destination-state'].cat.set_categories(state_categories,inplace=True)
    df['destination-county'].cat.set_categories(county_categories,inplace=True)
    df['destination-zipcode'].cat.set_categories(zipcode_categories,inplace=True)
    
    # convert to datetime object

    df.pickup_datetime=pd.to_datetime(df.pickup_datetime)
    
    #create some new features 
    df['year']=df.pickup_datetime.apply(lambda x:x.year)
    df['month']=df.pickup_datetime.apply(lambda x:x.month)
    df['day']=df.pickup_datetime.apply(lambda x:x.day)
    df['hour']=df.pickup_datetime.apply(lambda x:x.hour)
    df['dayofweek']=df.pickup_datetime.apply(lambda x:x.dayofweek)

    df.drop(labels='pickup_datetime', axis=1, inplace=True)
    
    #convert these new  features into categoric variables
    df.year=df.year.astype('category')
    df.month=df.month.astype('category')
    df.day=df.day.astype('category')
    df.hour=df.hour.astype('category')
    df.dayofweek=df.dayofweek.astype('category')
    
    # taxi ride with zero km

    df['loop']=0
    df.loc[(df.pickup_latitude==df.dropoff_latitude)&(df.pickup_longitude==df.dropoff_longitude),'loop']=1

    df.passenger_count=df.passenger_count.astype('category')
    df.loop=df.loop.astype('category')
    
    # add  distance in km between departure and destination points as a new feature
    df['distance_km'] = df[['pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude']].apply(distance,axis=1)

    #delete rows with distance_km>150
    
    df.drop(df[df['distance_km']>150].index, axis=0, inplace=True)


    #create three new categories: in-state, in-county, in-zipcode
    #in-region: rides from one region to the same region

    df['in-state']=df[['departure-state','destination-state']].apply(lambda x:1 if x[0]==x[1] else 0, axis=1)
    df['in-county']=df[['departure-county','destination-county']].apply(lambda x:1 if x[0]==x[1] else 0, axis=1)
    df['in-zipcode']=df[['departure-zipcode','destination-zipcode']].apply(lambda x:1 if x[0]==x[1] else 0, axis=1)

    df['in-state']=df['in-state'].astype('category')
    df['in-county']=df['in-county'].astype('category')
    df['in-zipcode']=df['in-zipcode'].astype('category')

    #classify rides according to  distance_km: short, medium, long

    df['short/long-distance']='short'
    df.loc[(df['distance_km']>1) & (df['distance_km']<=15), 'short/long-distance']='medium'
    df.loc[df['distance_km']>15, 'short/long-distance']='long'

    df['short/long-distance']=df['short/long-distance'].astype('category')
    
    #the last step: convert categories into dummy variables
    
    if 'fare_amount' in df.columns:
        return pd.get_dummies(df.drop('fare_amount',axis=1), sparse=True), df['fare_amount']
    else:
        return pd.get_dummies(df, sparse=True)