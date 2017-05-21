from datetime import datetime, timedelta
import json
import spotify_manager
import db_connector

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

def is_expired(expires_at):
    if datetime.now() > expires_at:
        print("User token is expired.")
        return True
    return False
     

class Processor:
    def __init__(self, creds_file="../configs/credentials.json"):
        self.db_creds = get_database_credentials(creds_file)
        self.sp_creds = get_spotify_credentials(creds_file)
        self.conn = db_connector.Connector(self.db_creds)
        self.manager = spotify_manager.Manager(self.sp_creds)

    def register_user(self, code, expiration):
        access_token, refresh_token = self.manager.parse_code(code)
        user_id = self.manager.get_user_id(access_token)
        self.conn.insert_user(user_id, access_token, refresh_token, expiration)        
        
    def register_reaction(self, information):# handle information
        pass
    
    def user_token(self, user_id):
        access_token, refresh_token, expires_at = self.conn.get_user(user_id)
        if is_expired(expires_at):
            access_token, refresh_token = self.manager.refresh_user_token(refresh_token)
            expires_at = datetime.now() + timedelta(hours=1)
            expires_at = expires_at.strftime("%Y-%m-%d %H:%M:%S")
            self.conn.update_user(user_id, access_token, refresh_token, expires_at)
        return access_token

    def create_playlist(self, user_id):
        access_token = self.user_token(user_id)
        date = datetime.now().strftime("%Y-%m-%d")
        playlist_id = self.manager.create_playlist(access_token, date)
        self.conn.insert_playlist(playlist_id, user_id, "testing")
        #creates playlist for a user
        #needs to connect to database and create playlist
        #needs to connect to database and create recommendations
        #needs to create playlist through spotify API
        pass
    
    def create_recommendations(self, user_id):
        #for a user id
        #search all reactions and analyse them
        #and create recommendations based on this information
        #return list of track ids, which are the recommendations
        pass

    def add_track(self, track_id):
        duration, danceability, energy, loudness, track_key, liveness, valence, tempo, time_signature = self.manager.track_features(track_id)
        self.conn.insert_track(track_id, duration, danceability, energy, loudness, track_key, liveness, valence, tempo, time_signature)
        #TODO - insert track and check if track is inserted