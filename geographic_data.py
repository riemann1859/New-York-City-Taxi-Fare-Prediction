# data files for zipcodes ( from https://earthworks.stanford.edu/)

import geopandas as gpd

zipcodes={
                "New York City":gpd.read_file("D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/geographic_data/usa-zipcodes/newyork/nyu_2451_34509_modified.shp"),
                "New York"     :gpd.read_file("D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/geographic_data/usa-zipcodes/newyork/TG00NYZCTA_modified.shp"),
                "Connecticut"  :gpd.read_file("D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/geographic_data/usa-zipcodes/connecticut/TG00CTZCTA_modified.shp"),
                "New Jersey"   :gpd.read_file("D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/geographic_data/usa-zipcodes/newjersey/TG00NJZCTA_modified.shp"),
                "Delaware"     :gpd.read_file("D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/geographic_data/usa-zipcodes/delaware/TG00DEZCTA_modified.shp"),
                "Maine"        :gpd.read_file("D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/geographic_data/usa-zipcodes/maine/TG00MEZCTA_modified.shp"),
                "Massachusetts":gpd.read_file("D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/geographic_data/usa-zipcodes/massachusetts/TG00MAZCTA_modified.shp"),
                "New Hampshire":gpd.read_file("D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/geographic_data/usa-zipcodes/new-hampshire/TG00NHZCTA_modified.shp"),
                "Pennsylvania" :gpd.read_file("D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/geographic_data/usa-zipcodes/pennsylvania/TG00PAZCTA_modified.shp"),
                "Rhode Island" :gpd.read_file("D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/geographic_data/usa-zipcodes/Rhode-Island/TG00RIZCTA_modified.shp"),
                "Vermont"      :gpd.read_file("D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/geographic_data/usa-zipcodes/vermont/TG00VTZCTA_modified.shp"),
                "Maryland"     :gpd.read_file("D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/geographic_data/usa-zipcodes/maryland/TG00MDZCTA_modified.shp")
          }

#data containing polygon boundaries of JFK Intl and LaGuardia Intl airports

public_facilities=gpd.read_file("D:/Anaconda3/kaggle-competitions/newyork taxi fare prediction/geographic_data/NewYork_town_county_city_state/2010 New York City Large Public Facilities/nyu_2451_34492.shp")
    
#we use this data to determine whether a taxi ride is related to airports or not 

#all geodataframes here are modified, suited to our purposes, not in their original forms. But we skip these kind of works. 


