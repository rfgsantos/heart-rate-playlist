import json

import spotipy
import spotipy.util

def get_app_credentials(filename):
    data = None
    with open(filename, "r") as creds:
        data = json.load(creds)
    creds.close()
    return data['spotify_credentials']


CREDENTIALS_FILE = "configs/credentials.json"
creds = get_app_credentials(CREDENTIALS_FILE)
SPOTIFY_APP_ID = creds['SPOTIFY_APP_ID']
SPOTIFY_APP_SECRET = creds['SPOTIFY_APP_SECRET']
SPOTIFY_REDIRECT_URI = creds['SPOTIFY_REDIRECT_URI']
SPOTIFY_SCOPE = creds['SCOPE']

username = "tomazinhal"

token = spotipy.util.prompt_for_user_token(username, scope=SPOTIFY_SCOPE, client_id=SPOTIFY_APP_ID, client_secret=SPOTIFY_APP_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)

print("Token: ", token)

sp = spotipy.Spotify(auth=token)
results = sp.current_user_playlists()
print(results)
