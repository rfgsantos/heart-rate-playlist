import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

class Connector:
    def __init__(self, creds):
        self.user = db_creds['user']
        self.password = db_creds['password']
        self.host = db_creds['host']
        self.database = db_creds['database']

    def connect(self):
        self.db=MySQLdb.connect(user=self.user, passwd=self.password, host=self.host, database=self.database)
        self.cursor=self.db.cursor()
        print("Connected to Database.")
    
    def insert_user(self, user_id, access_token, refresh_token, expiration):
        query = "INSERT INTO user (id, refresh_token, access_token, expires_at) VALUES(\""
        query += "\", \"".join([user_id, refresh_token, access_token, expiration]) + "\""
        query += ")ON DUPLICATE KEY UPDATE access_token=\"" + access_token + "\", refresh_token=\"" + refresh_token + "\", expires_at=\"" + expiration + "\""
        self.cursor.execute(query)
        self.db.commit()
    
    def update_user(self, user_id, access_token, refresh_token, expiration):
        self.insert_user(user_id, access_token, refresh_token, expiration)

    def insert_playlist(self, playlist_id, user_id, comment=""):
        query = "INSERT INTO playlist (id, user_id, comment) VALUES(\""
        query += "\", \"".join([playlist_id, user_id, comment]) + "\")"
        print(query)

    def update_playlist(self, comment):
        pass
    
    def insert_track(self, track_id, duration_sec, danceability, energy, loudness, track_key, liveness, valence, tempo, time_signature):
        query = "INSERT INTO track VALUES(\"{}\", {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
        query.format(track_id, duration_sec, danceability, energy, loudness, track_key, liveness, valence, tempo, time_signature)
        print(query)

    def insert_reaction(self):
        pass

    def insert_recommended(self, playlist_id, track_id):
        query = "INSERT INTO recommended VALUES(\""
        query += ""