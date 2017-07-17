import sys
sys.path.append("../libs/")
#sys.path.append("../configs/")
import spotipy.util
import core_engine

username = "irrelevant"

creds = core_engine.get_spotify_credentials("../configs/credentials.json")
app_id = creds['SPOTIFY_APP_ID']
app_secret = creds['SPOTIFY_APP_SECRET']
redirect_uri = creds['SPOTIFY_REDIRECT_URI']
scope = creds['SPOTIFY_SCOPE']

if __name__ == "__main__":

    token = spotipy.util.prompt_for_user_token(username, scope=scope, client_id=app_id, client_secret=app_secret, redirect_uri=redirect_uri)
    print("Token: ", token)
