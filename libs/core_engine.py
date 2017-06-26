from datetime import datetime, timedelta
import json
import spotify_manager
import db_connector
import sys
sys.path.append("../")
from util.hrv import *

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
    def __init__(self, creds_file="configs/credentials.json"):
        self.db_creds = get_database_credentials(creds_file)
        self.sp_creds = get_spotify_credentials(creds_file)
        self.conn = db_connector.Connector(self.db_creds)
        self.manager = spotify_manager.Manager(self.sp_creds)

    def register_user(self, code, expiration):
        access_token, refresh_token = self.manager.parse_code(code)
        user_id = self.manager.get_user_id(access_token)
        self.conn.insert_user(user_id, access_token, refresh_token, expiration)        
        
    def register_reaction(self, reaction):# handle reaction
        try:
            print(reaction)
            print(type(reaction['heart_rate']))
            print(str(reaction['heart_rate']))
            print(type(reaction['heart_rate'][0]))
        except:
            print("reaction process failed")
        parsed = self.parse_reaction(reaction)
        self.create_reaction(parsed)
        
    def parse_reaction(self, reaction):
        #create text from list of strings containing the RR intervals
        if reaction['heart_rate']:
            float_heart_rate = []
            hr = reaction['heart_rate'][0].split(", ")
            float_heart_rate = [float(val) for val in hr]
        
            #float_heart_rate = [float(val) for val in reaction['heart_rate']]
            time_heart_rate = [0]
            for val in float_heart_rate:
                time_heart_rate.append(time_heart_rate[len(time_heart_rate) - 1] + val)
            str_heart_rate = ",".join(["{:.4f}".format(val) for val in time_heart_rate])
        ts = RR = HR = its = iRR = iHR = f1 = pwr1 = Vpca1 = features_aux = []
        try:
            ts,RR,HR,its,iRR,iHR, f1, pwr1,Vpca1, features_aux = hrv(time_heart_rate,256)
        except ValueError:
            print("Not enough R peaks.")

        #parse reaction datetime into SQL datetime format
        date, time = reaction['datetime'].split(" ")
        day, month, year = date.split('.')
        new_datetime = "-".join((year, month, day)) + " " + time
        new_reaction = {
            'user_id': reaction['user_id'], #string
            'track_id': reaction['track_id'], #string
            'location': reaction['location'], #string
            'datetime': new_datetime, #string
            'heart_rate': str_heart_rate, #string
            'ts': ts, #array
            'RR': RR, #array
            'HR': HR, #array
            'its': its, #array
            'iRR': iRR, #array
            'iHR': iHR, #array
            'f1': f1, #array
            'pwr1': pwr1, #array
            'Vpca1': Vpca1, #array
            'features_aux': features_aux #dict
        }
        return new_reaction
    
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
        reactions = self.conn.get_user_reactions(user_id)
        good = []
        for reaction in reactions:
            result = self.eval_reaction(reaction)
            if self.is_good(result):
                good.append(result)
        if len(good) < 5:
            return #not enough tracks to make a decent playlist
        recommendations = self.manager.create_recommendations(good)
        return recommendations
    
    def is_good(self, track):
        return True

    def add_track(self, track_id):
        duration, danceability, energy, loudness, track_key, liveness, valence, tempo, time_signature = self.manager.track_features(track_id)
        self.conn.insert_track(track_id, duration, danceability, energy, loudness, track_key, liveness, valence, tempo, time_signature)
    
    def eval_reaction(self, reaction):
        pass

    def create_reaction(self, reaction):
        self.add_track(reaction['track_id'])
        self.conn.insert_reaction(reaction['user_id'], reaction['track_id'], reaction['location'], reaction['datetime'], reaction['heart_rate'])