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
        try:
            self.db=MySQLdb.connect(user=self.user, passwd=self.password, host=self.host, database=self.database)
            self.cursor=self.db.cursor()
            print("Connected to Database.")
        except:
            print("Please turn on Database server.")
            exit(1)
    
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
        query = query.format(user_id)
        self.cursor.execute(query)
        result = self.cursor.fetchall()[0]
        return result[0], result[1], result[2]
    
    def get_users(self):
        query = "SELECT id, access_token, refresh_token FROM user"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_users_with_reactions(self):
        query = "SELECT id, access_token, refresh_token FROM user INNER JOIN reaction \
        ON user.id = reaction.user_id WHERE NOT (reaction.hrv <=> NULL)"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def create_playlist(self, playlist_id, user_id, comment=""):
        query = "INSERT INTO playlist (id, user_id, comment) VALUES(\""
        query += "\", \"".join([playlist_id, user_id, comment]) + "\")"
        print(query)
        self.cursor.execute(query)
        self.db.commit()
    
    def insert_track(self, track_id, duration_sec, danceability, energy, loudness, track_key, liveness, valence, tempo, time_signature):
        query = "INSERT INTO track \
        (id, duration_sec, danceability, energy, loudness, track_key, liveness, valence, tempo, time_signature) \
        VALUES(\"{0}\", {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}) \
        ON DUPLICATE KEY UPDATE id=\"{0}\""
        query = query.format(track_id, duration_sec, danceability, energy, loudness, track_key, liveness, valence, tempo, time_signature)
        print(query)
        self.cursor.execute(query)
        self.db.commit()

    def insert_reaction(self, user_id, track_id, location, datetime, heart_rate):
        query = "INSERT INTO reaction (user_id, track_id, hrv, date, gps) \
        VALUES(\"{0}\", \"{1}\", \"{2}\", \"{3}\", \"{4}\")"
        query = query.format(user_id, track_id, heart_rate, datetime, location)
        print(query)
        self.cursor.execute(query)
        self.db.commit()

    def insert_recommendation(self, playlist_id, track_id):
        query = "INSERT INTO recommendation (playlist_id, track_id) VALUES(\"{}\", \"{}\")"
        query = query.format(playlist_id, track_id)
        self.cursor.execute(query)
        self.db.commit()

    def get_user_reactions(self, user_id):
        query = "SELECT track.id as track_id, track.duration_sec as track_duration, \
        reaction.id as reaction_id, reaction.hrv, reaction.date as reaction_date, reaction.gps as location\
        FROM reaction INNER JOIN track ON reaction.track_id=track.id WHERE reaction.user_id=\"{}\""
        query = query.format(user_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()
