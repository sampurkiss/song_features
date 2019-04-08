# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:05:13 2019

@author: Sam Purkiss
"""
import os
os.chdir('C:/Users/sam purkiss/Documents/Code/Music/')


import pandas as pd
import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import CLIENT_ID,CLIENT_SECRET

#Need to create a credentials file with your spotify api keys

client_credentials_manager = SpotifyClientCredentials(CLIENT_ID,CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

names_giving_probs = ['21 savage & metro boomin featuring future',
                      '21 savage, offset  metro boomin ring quavo',
                      '21 savage, offset  metro boomin ring travis scott',
                      'Dont Trust Me',
                      'Hit It Again',
                      'a r rahman & the pussycat dolls featuring nicole scherzinger',
                      'A Change Is Gonna Come',
                      '\'N Sync']



def get_music_features(artist_name, song_name):
    """
    Spotify API caller to pull features for individual tracks.
    Paramaters:
        artist_name: name of artist
        song_name: song by artist of interest
    Returns: Pandas dataframe with variables identified in the API documentation:
        https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
        
    Usage:
        client_credentials_manager = SpotifyClientCredentials(CLIENT_ID,CLIENT_SECRET)
        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        song_features = get_music_features('the cure','Friday im in love')
    """
    
    
    #Use these lists to fix common problems in naming conventions
    words_to_remove = ['&.+',
                   'featuring.+',#the .+ is a regex expression that 
                   # will strip off words following the main word.
                   #Eg "Alvin And The Chipmunks Featuring Chris Classic"
                   #becomes just "Alvin And The Chipmunks." This is 
                   #necessary because Spotify search often has a hard time
                   #finding songs with multiple featured artists.
                   #This may cause an issue where songs that are have versions
                   #with and without different artists aren't distinguished 
                   #between
                   'feat..+',
                   'feat.+',
                   'with.+',
                   '(?<= )[\+](?= ).+',
                   'duet',
                   '(?<= )[xX](?= )',
                   #note that this will strip the x off any words that 
                   #end with x, but there aren't many and spotify will still recognize
                   #artist name
                   "'",
                   '\*',
                   "\(",
                   "\)"
                   ]

    words_to_remove_from_songs =["'",
                             '[a-zA-Z]+(\*)+(?P<named_group>).+(?= )',#used for capturing
                             #words that are censored eg N***s,
                            '\([a-zA-Z]+.+\)' #remove any words in brackets                             
                             ]
    
    artist = artist_name.lower()
    song = song_name
    for word in words_to_remove:
        artist = re.sub(word,'',artist)     
    for word in words_to_remove_from_songs:
        song = re.sub(word,'', song)

    #Generate database used to hold returned items
    song_details= pd.DataFrame()        
    

    try:

        query = 'track:%s artist:%s' %(song,artist)
        result = spotify.search(q=query)
        #Select the first item (assume spotify returns what I want on first result)
        first_result = result['tracks']['items'][0]
        #From first result, pull specific variables
        track_id = first_result['id']
        album_id = first_result['album']['id']
        artist_id = first_result['artists'][0]['id']
        release_date = first_result['album']['release_date']     

        #Add variables to dataframe
        song_details['Performer'] = [artist_name]
        song_details['Song'] = [song_name]
        song_details['track_id'] = [track_id]
        song_details['artist_id'] = [artist_id]
        song_details['album_id'] = [album_id]
        song_details['release_date'] = [release_date]
        song_details['search_query'] = [query]
        track_features = spotify.audio_features(tracks=track_id)
        if len(track_features)>1:
            print('multiple songs are returned for some reason')
            
        track_features = track_features[0]
        
        for key, value in track_features.items():
            song_details[key] = [value]
            
    except IndexError: #for few weird ones + cases where song isn't on spotify
        print("Search term \"%s\" is giving trouble" %(query))
        pass

    return(song_details)
    


