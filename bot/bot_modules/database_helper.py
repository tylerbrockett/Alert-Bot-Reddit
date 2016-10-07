import os
import sqlite3
import traceback

from helpers import database


class DBHelper:
    def __init__(self):
        self.connection = self.connect_to_database()

    def connect_to_database(self):
        try:
            connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + database.DATABASE_LOCATION)
            cursor = self.connection.cursor()
            cursor.execute(database.CREATE_TABLE_SUBSCRIPTIONS)
            cursor.execute(database.CREATE_TABLE_MATCHES)
            cursor.execute(database.CREATE_TABLE_ALERTS)
            return connection
        except:
            raise DBHelperException('Error Connecting to Database\n\n' + traceback.format_exc())

    def disconnect_from_database(self):
        try:
            if self.connection:
                self.connection.close()
            self.connection = None
        except:
            raise DBHelperException('Error Disconnecting from Database\n\n' + traceback.format_exc())

    def reset(self):
        self.disconnect_from_database()
        self.connect_to_database()

    def get(self, query):
        print()

    def insert(self, table, values):
        print()

    def remove(self, table, id):
        print()

class DBHelperException(Exception):
    def __init__(self, error_args):
        Exception.__init__(self, "DBHelper Exception: {0}".format(error_args))
        self.errorArgs = error_args
