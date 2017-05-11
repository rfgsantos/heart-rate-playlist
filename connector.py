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

    def insert_user(self, user_id, refresh_token, access_token, lifespan):
        query = "INSERT INTO user (id, refresh_token, access_token, lifespan) VALUES(\""
        query += "\", \"".join([user_id, refresh_token, access_token]) + "\", " + str(lifespan)
        query += ") ON DUPLICATE KEY UPDATE access_token=\"" + access_token + "\", refresh_token=\"" + refresh_token + "\", lifespan=" + str(lifespan)
        print(query)

    def update_user(self, user_id, refresh_token, access_token, lifespan):
        self.insert_user(user_id, refresh_token, access_token, lifespan)

    def insert_playlist(self):
        pass

    def update_playlist(self):
        pass

    def insert_music(self):
        pass

    def insert_reaction(self):
        pass

    def insert_recommendation(self):
        pass

