import spotipy
import connector
import json
from datetime import datetime, timedelta

def add_user(username, access_token, refresh_token):
    sp = spotipy.Spotify(auth=access_token)
    user_id = sp.me()['id']
    expires_at = datetime.now() + timedelta(hours=1)
    connector.add_user(username, user_id, access_token, refresh_token, expires_at)

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