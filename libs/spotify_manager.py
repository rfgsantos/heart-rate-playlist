import spotipy, spotipy.oauth2

class Manager():
    def __init__(self, creds):
        self.app_id = creds['SPOTIFY_APP_ID']
        self.app_secret = creds['SPOTIFY_APP_SECRET']
        self.redirect_uri = creds['SPOTIFY_REDIRECT_URI']
        self.scope = creds['SPOTIFY_SCOPE']
    
    def app_credentials(self):
        scc = spotipy.oauth2.SpotifyClientCredentials(client_id=self.app_id, client_secret=self.app_secret)
        token = scc.get_access_token()
        return scc, token

    def parse_code(self, code):
        soa = spotipy.oauth2.SpotifyOAuth(client_id=self.app_id, client_secret=self.app_secret,redirect_uri=self.redirect_uri, scope=self.scope)
        response = soa.get_access_token(str(code))
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

    def create_playlist(self, user_token, date):
        sp = spotipy.Spotify(auth=user_token)
        id = sp.me()['id']# user id is required
        playlist_name = "HRP-{}".format(date)
        resp = sp.user_playlist_create(id, playlist_name)
        return resp['id']

    def add_tracks(self, tracks, playlist_id, user_token):
        token = self.get_user_id(user_token)
        sp = spotipy.Spotify(auth=token)
        sp.user_playlist_add_tracks(user_id, playlist_id, tracks)

    def track_features(self, track_id):
        client_credentials, token = self.app_credentials()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials)
        features = sp.audio_features(track_id)[0]
        duration = int(features['duration_ms']) / 1000.
        danceability = features['danceability']
        energy = features['energy']
        loudness = features['loudness']
        track_key = features['key']
        liveness = features['liveness']
        valence = features['valence']
        tempo = features['tempo']
        time_signature = features['time_signature']
        return (duration, danceability, energy, loudness, track_key, liveness, valence, tempo, time_signature)

    def create_recommendations(self, tracks):
        token = self.app_credentials()[1]
        sp = spotipy.Spotify(auth=token)
        json = sp.recommendations(seed_tracks=tracks, limit=10)
        recommendations = list(map(lambda track : track['id'], json['tracks']))
        return recommendations