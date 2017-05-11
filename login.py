import json

import spotipy
import spotipy.util

from connector import Connector 

def get_database_credentials(filename):
    data = None
    with open(filename, "r") as creds:
        data = json.load(creds)
    creds.close()
    return data['database_credentials']

def get_spotify_credentials(filename):
    data = None
    with open(filename, "r") as creds:
        data = json.load(creds)
    creds.close()
    return data['spotify_credentials']

def get_cached_token(username):
    filename = ".cache-" + username
    with open(filename, "r+") as user_auth:
        data = json.load(user_auth)
    user_auth.close()
    user_access_token = ""
    user_access_token_lifespan = ""
    user_refresh_token = ""
    try:
        user_access_token = data['access_token']
        user_access_token_lifespan = data['expires_in']
        user_refresh_token = data['refresh_token']
    except:
        print("Something went wrong.")
    return (user_refresh_token, user_access_token, user_access_token_lifespan)


CREDENTIALS_FILE = "configs/credentials.json"
creds = get_spotify_credentials(CREDENTIALS_FILE)
SPOTIFY_APP_ID = creds['SPOTIFY_APP_ID']
SPOTIFY_APP_SECRET = creds['SPOTIFY_APP_SECRET']
SPOTIFY_REDIRECT_URI = creds['SPOTIFY_REDIRECT_URI']
SPOTIFY_SCOPE = creds['SCOPE']

username = "tomazinhal"

db_creds = get_database_credentials(CREDENTIALS_FILE)
DB_USERNAME = db_creds['user']
DB_PASSWORD = db_creds['password']

if __name__ == "__main__":

    token = spotipy.util.prompt_for_user_token(username, scope=SPOTIFY_SCOPE, client_id=SPOTIFY_APP_ID, client_secret=SPOTIFY_APP_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)

    print("Token: ", token)

    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_playlists()
    print(results)
