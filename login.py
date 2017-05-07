import spotipy
import spotipy.util

SPOTIFY_APP_ID = '9efc6cfd070049e18043aee96ae5228a'
SPOTIFY_APP_SECRET = 'b6eea41f283446c78b0dbee02e3df4b7'
SPOTIFY_REDIRECT_URI = 'https://localhost:5000/callback'

username = "tomaz.spotipy"
scope = 'user-read-private user-read-email'


spotipy.util.prompt_for_user_token(username, scope=scope, clientconf_id=SPOTIFY_APP_ID, client_secret=SPOTIFY_APP_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI)