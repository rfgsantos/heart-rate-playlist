import json

import spotipy
import spotipy.util

#from connector import Connector 
from lib import *

CREDENTIALS_FILE = "configs/credentials.json"
creds = get_spotify_credentials(CREDENTIALS_FILE)
SPOTIFY_APP_ID = creds['SPOTIFY_APP_ID']
SPOTIFY_APP_SECRET = creds['SPOTIFY_APP_SECRET']
SPOTIFY_REDIRECT_URI = creds['SPOTIFY_REDIRECT_URI']
SPOTIFY_SCOPE = creds['SPOTIFY_SCOPE']

username = "jgbbarreiros"

db_creds = get_database_credentials(CREDENTIALS_FILE)
DB_USERNAME = db_creds['user']
DB_PASSWORD = db_creds['password']

soa = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIFY_APP_ID, client_secret=SPOTIFY_APP_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI, scope=SPOTIFY_SCOPE)

if __name__ == "__main__":

    token = spotipy.util.prompt_for_user_token(username, scope=SPOTIFY_SCOPE, client_id=SPOTIFY_APP_ID, client_secret=SPOTIFY_APP_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)

    print("Token: ", token)

    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_playlists()
    print(results)
