import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

class Connector():
    def __init__(self, username, passwd, host="localhost", database="heart-rate-playlist"):
        self.db_user = username
        self.db_passwdd = passwd
        self.db_host = host
        self.dn_name = database
        self.connect(username, passwd, host, database)

    def connect(self, username, passwd, host, database):
        self.db=MySQLdb.connect(user=username, passwd=passwd, host=host, database=database)
        self.cursor=self.db.cursor()
        print("Connected to Database.")

    def insert_user(self, user_id, username, refresh_token, access_token, expires):
        query = "INSERT INTO user (username, id, refresh_token, access_token, expires_at) VALUES(\""
        query += "\", \"".join([user_id, username, refresh_token, access_token]) + "\", " + expires
        query += ") ON DUPLICATE KEY UPDATE access_token=\"" + access_token + "\", refresh_token=\"" + refresh_token + "\", expires_at=" + expires
        print(query)

    def get_user(username, id=None):
        query = "SELECT * FROM users WHERE username=\"" + username + "\""
        print(query)

    def update_user(self, username, refresh_token, access_token, expires):
        self.get_user(username)
        # parse to get id
        id = ""
        self.insert_user(user_id=id, username=username, refresh_token=refresh_token, access_token=access_token, expires=expires)

    def insert_playlist(self, playlist_id, user_id, comment=None):
        query = "INSERT INTO playlist (id, user_id, comment) VALUES(\""
        query += "\", \"".join([playlist_id, user_id, comment]) + "\""
        print(query)

    def update_playlist(self):
        pass

    def insert_track(self):
        pass

    def insert_reaction(self):
        pass

    def insert_recommendation(self):
        pass

