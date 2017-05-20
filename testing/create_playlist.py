import sys
sys.path.append("../")
sys.path.append("../libs/")

import json
import spotipy
from libs.core_engine import *
from datetime import datetime, timedelta

if __name__ == "__main__":

    user_id = "11122241033" #tomaz azinhal

    processor = Processor()
    processor.create_playlist(user_id)
    
    token = processor.user_token(user_id)
    sp = spotipy.Spotify(auth=token)
    
    #getting playlists
    playlists = sp.current_user_playlists()
    playlist_names = [p['name'] for p in playlists['items']]
    print(playlist_names)