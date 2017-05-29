import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

class Connector:
    def __init__(self, creds):
        self.user = creds['user']
        self.password = creds['password']
        self.host = creds['host']
        self.database = creds['database']
        self.connect()

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

    def get_user(self, user_id):
        query = "SELECT access_token, refresh_token, expires_at FROM user WHERE id=\"{}\""
        self.cursor.execute(query.format(user_id))
        result = self.cursor.fetchall()[0]
        return result[0], result[1], result[2]

    def insert_playlist(self, playlist_id, user_id, comment=""):
        query = "INSERT INTO playlist (id, user_id, comment) VALUES(\""
        query += "\", \"".join([playlist_id, user_id, comment]) + "\")"
        print(query)
        self.cursor.execute(query)
        self.db.commit()

    def update_playlist(self, comment):
        pass
    
    def insert_track(self, track_id, duration_sec, danceability, energy, loudness, track_key, liveness, valence, tempo, time_signature):
        query = "INSERT INTO track (id, duration_sec, danceability, energy, loudness, track_key, liveness, valence, tempo, time_signature) VALUES(\"{0}\", {}, {}, {}, {}, {}, {}, {}, {}, {})"
        query += " ON DUPLICATE KEY UPDATE id=\"{0}\""
        query = query.format(track_id, duration_sec, danceability, energy, loudness, track_key, liveness, valence, tempo, time_signature)
        print(query)
        self.cursor.execute(query)
        self.db.commit()

    def insert_reaction(self):
        pass

    def insert_recommended(self, playlist_id, track_id):
        query = "INSERT INTO recommended (playlist_id, track_id) VALUES(\"{}\", \"{}\")"
        query = query.format(playlist_id, track_id)
        print(query)
        """
        self.cursor.execute(query)
        self.db.commit()
        """