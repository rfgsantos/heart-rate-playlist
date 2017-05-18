from datetime import datetime, timedelta
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

class Processor:
    def __init__(self, creds_file="../configs/credentials.json"):
        self.db_creds = get_database_credentials(creds_file)
        self.sp_creds = get_spotify_credentials(creds_file)
        self.conn = connector.Connector(sp_creds)
        self.manager = spotify_manager.Manager(db_creds)

    def register_user(self, code, expiration):
        access_token, refresh_token = self.manager.parse_code(code)
        user_id = self.manager.get_user_id(access_token)
        self.conn.insert_user(user_id, access_token, refresh_token, expiration)        
        
    def register_reaction(self, information):
        # handle information
        pass
    
    def create_playlist(self):
        #creates playlist for a user
        #needs to connect to database and create playlist
        #needs to connect to database and create recommendations
        #needs to create playlist through spotify API
        pass