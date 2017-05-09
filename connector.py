import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

class Connector():
    def __init__(self, username, passwd, host="localhost", database="heart-rate-playlist"):
        self.db=MySQLdb.connect(user=username, passwd=passwd, host=host, database=database)
        self.cursor=self.db.cursor()

    def create_database(self):
        pass

    def delete_database(self):
        pass

    def drop_database(self):
        pass

    def insert_user(self):
        pass

    def update_user(self):
        pass

    def insert_playlist(self):
        pass

    def update_playlist(self):
        pass

    def insert_music(self):
        pass

    def 