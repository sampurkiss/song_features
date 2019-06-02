# -*- coding: utf-8 -*-
"""
Created on Mon May 27 09:33:46 2019

@author: Sam Purkiss
"""
import pandas as pd
import spotipy
import spotipy.util as util
from credentials import CLIENT_ID,CLIENT_SECRET

#Login for playlist
scope = 'playlist-modify-public'
token = util.prompt_for_user_token('sampurkiss', 
                                   scope,
                                   client_id = CLIENT_ID,
                                   client_secret = CLIENT_SECRET,
                                   redirect_uri = 'https://accounts.spotify.com/authorize'
                                   )
sp = spotipy.Spotify(auth=token)

name_vector = pd.read_csv('grouped_songs.csv')


cluster_summary = name_vector.groupby('cluster_grouping').mean().reset_index()

SONG_CODES = list(name_vector[name_vector['cluster_grouping']==269]['track_id'])
PLAYLIST_ID  = '44XNhDnuvKuw9DIM7GntNP'


def update_playlist(playlist_id, song_codes):
    """
    playlist_id: id of playlist to be updated
    song_codes: a list of song ids (must be in list form)
    Doesn't return anything, it just updates a playlist 
    with new song codes and deletes existing songs from 
    playlist.
    """
    #############################
    #Get list of songs currently in playlist and remove em
    tracks_in_playlist = sp.user_playlist_tracks(user='sampurkiss',
                            playlist_id = playlist_id)
    
    
    tracks_in_playlist = [item['track']['id'] for item in tracks_in_playlist['items']]
    
    sp.user_playlist_remove_all_occurrences_of_tracks(user='sampurkiss',
                                                      playlist_id = playlist_id,
                                                      tracks= tracks_in_playlist)
    
    ###############################
    #Add new songs to playlist
    sp.user_playlist_add_tracks(user='sampurkiss', 
                                     playlist_id=playlist_id, 
                                     tracks=song_codes)

    return print("Playlist updated")

update_playlist(PLAYLIST_ID, SONG_CODES)
