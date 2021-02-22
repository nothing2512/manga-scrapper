import mysql.connector as mysql
from utils.constants import *


class Connection(object):

    def __init__(self):
        self.__db = mysql.connect(
            host=HOST,
            user=USER,
            passwd=PASS,
            auth_plugin=PLUGIN
        )
        self.fetch("DROP DATABASE IF EXISTS %s" % DB)
        self.fetch("CREATE DATABASE %s" % DB)
        self.__db.database = DB

    def fetch(self, query):
        cursor = self.__db.cursor()
        cursor.execute(query)
        return cursor.fetchone()

    def fetchall(self, query):
        cursor = self.__db.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def execute(self, query):
        cursor = self.__db.cursor()
        cursor.execute(query)
        self.__db.commit()

    def lastinsertid(self):
        return self.fetch("SELECT LAST_INSERT_ID()")[0]
