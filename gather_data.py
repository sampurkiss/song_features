# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:05:13 2019

@author: Sam Purkiss
"""
import os
os.chdir('C:/Users/sam purkiss/Documents/Code/Music/')

import pandas as pd
from charts_analyzer import get_music_features


##########################
#Define variables
filter_date = pd.Timestamp('1998-01-01')

############################
#Load data
billboard_charts = pd.read_csv('Hot Stuff.csv')

##########################
#Filter Data
billboard_charts_2000_on = billboard_charts.loc[billboard_charts['WeekID']>filter_date].copy()


############################
#Clean data
#convert dates to datetime 
billboard_charts.iloc[0]
billboard_charts.loc[:,'WeekID'] = pd.to_datetime(billboard_charts.loc[:,'WeekID'])
#fix names: dict(name in database:new name)
fix_names = {'\'N Sync': 'nsync',
             '+44':'\\+44',
             '98 degrees':'\\98 degrees'             
             }
for key, value in fix_names.items():
    #Change the old name to new name as identified in fix_names dict
    billboard_charts_2000_on.loc[billboard_charts_2000_on['Performer'] ==key,'Performer'] = value
 

##########################
#Create features database
    
#Create unique list of artists and songs
unique_list = (billboard_charts_2000_on[['Performer','Song','Weeks on Chart']]
                .groupby(['Performer','Song'])
                .max().reset_index())    

#use this loop to work through the billboard database
song_details = pd.DataFrame()
failures=1
for i in range(0, len(unique_list)):    
    #Get song and cleaned artist name to use in spotify query
    artist = unique_list.loc[i,'Performer']
    song = unique_list.loc[i,'Song']
    if (i+1)%1000 ==0:
        print('--------------------------------------')
        print("Now on %d out of %d" %(i+1, len(unique_list)))
        print('--------------------------------------')
        song_details.to_csv('song_details')
    song_features = get_music_features(artist, song)
    if song_features.empty:
        print("there have been %d failures so far" %(failures))
        failures+=1
    else:
        song_details = song_details.append(song_features)

song_details.to_csv('song_details')

song_details = song_details.reset_index().drop(columns =['index'])

#billboard_charts_2000_on.loc[:,'Performer'] = billboard_charts_2000_on.loc[:,'Performer'].str.lower()
billboard_charts_2000_on.loc[:,'year'] = billboard_charts_2000_on['WeekID'].map(lambda x: x.year)
#billboard_charts_2000_on.groupby(by = ['Song', 'Performer']).max()
billboard_charts_2000_on = billboard_charts_2000_on.merge(song_details, how='left', on =['Song','Performer'])
billboard_charts_2000_on = billboard_charts_2000_on.dropna()


billboard_charts_2000_on.to_csv('song_details.csv',index=False)
