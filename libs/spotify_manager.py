import spotipy, spotipy.oauth2

class Manager():
    def __init__(self, reds):
        self.app_id = creds['SPOTIFY_APP_ID']
        self.app_secret = creds['SPOTIFY_APP_SECRET']
        self.redirect_uri = creds['SPOTIFY_REDIRECT_URI']
        self.scope = creds['SPOTIFY_SCOPE']
    
    def get_app_token(self):
        scc = spotipy.oauth2.SpotifyClientCredentials(client_id=self.app_id, client_secret=self.app_secret)
        token = scc.get_access_token()
        return token

    def parse_code(self, code):
        soa = spotipy.oauth2.SpotifyOAuth(client_id=self.app_id, client_secret=self.app_secret,redirect_uri=self.redirect_uri, scope=self.scope)
        response = soa.get_access_token(str(auth_token))
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        return (access_token, refresh_token)

    def refresh_user_token(self, refresh_token):
        soa = spotipy.oauth2.SpotifyOAuth(client_id=self.app_id, client_secret=self.app_secret, redirect_uri=self.redirect_uri, scope=self.scope)
        response = soa.refresh_access_token(refresh_token)
        # user might have deauthorized app - TODO verifications
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        return (access_token, refresh_token)

    def get_user_id(self, access_token):
        sp = spotipy.Spotify(auth=access_token)
        user_id = None
        try:
            user_id = sp.me()['id']
        except:
            print("Access token expired.")
        return user_id
