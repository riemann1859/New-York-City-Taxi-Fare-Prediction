# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 21:30:22 2019

@author: YUNUS
"""
import numpy as np
from shapely.geometry import Point
from geographic_data import zipcodes

# if necessary, we appeal to geopy package to obtain state, county, zipcode information

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")

possible_states=[ "New York", "New Jersey" ,  "Connecticut", "Pennsylvania","Massachusetts",  "Maryland", "Delaware", "Vermont", "Rhode Island" ,"Maine", "New Hampshire" ]

threshold=0.01
state_=""
county=""



def zipcode_county_state(p):
    
    #transform lat and lon values into a tuple of zipcode, county, state if the point belongs to NYC

    for i in range(zipcodes['New York City'].shape[0]): 
        if zipcodes['New York City'].iloc[i,5].contains(Point(p[0],p[1])):
            return zipcodes['New York City'].iloc[i,0], zipcodes['New York City'].iloc[i,3], 'New York'
    
        
    #we now check whether the unknown locations belong to the remaining part of new york state, out of NYC, or not?

    result=zipcodes['New York'].loc[zipcodes['New York'].contains(Point(p[0],p[1])),['ZCTA','countyname']]
    if result.shape[0]==1:
        return result['ZCTA'].values[0],result['countyname'].values[0], 'New York'
    

    
    # check out of New York State


    for state in possible_states[1:]:
        result=zipcodes[state].loc[zipcodes[state].contains(Point(p[0],p[1])),['ZCTA','countyname']]
        if result.shape[0]==1:
            return result['ZCTA'].values[0],result['countyname'].values[0], state

            
   
    #last hope: calculate the distance between  the remaining unknown location and all counties in all possible states
    #if minimum of these distances is really small, lower than the threshold, choose the state and the county giving minimum
    
    
    for state in ['New York City']+possible_states:
        
        distance_series=zipcodes[state].distance(Point(p[0],p[1]))
        minimum_distance=distance_series.min()
        index_giving_minimum=distance_series.idxmin()
        
        if minimum_distance<=threshold:
            if state=='New York City':
                return zipcodes[state].loc[index_giving_minimum,"ZCTA"], zipcodes[state].loc[index_giving_minimum,"countyname"], "New York"
            else:
                return zipcodes[state].loc[index_giving_minimum,"ZCTA"], zipcodes[state].loc[index_giving_minimum,"countyname"], state
     
    #last hope: use geopy package 
    try:
        location = geolocator.reverse("{x},{y}".format(x=p[1],y=p[0]))
        return location.raw['address']['postcode'].split('-')[0].strip(), location.raw['address']['county'].replace('County',"").strip(), location.raw['address']['state']
    except:
        return 'Unknown','Unknown','Unknown'


# find distance in km between two locations


def distance(coordinates):
    a = 0.5 - np.cos((coordinates[3] - coordinates[1]) * np.pi/180)/2 + np.cos(coordinates[1]* np.pi/180) * np.cos(coordinates[3] * np.pi/180)* (1 - np.cos((coordinates[2] - coordinates[0]) * np.pi/180)) / 2
    return 12742 * np.arcsin(np.sqrt(a)) 
           