import os
import sqlite3
import traceback

from utils import database


class DatabaseHandler:
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        try:
            connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + database.DATABASE_LOCATION)
            cursor = self.connection.cursor()
            cursor.execute(database.CREATE_TABLE_SUBSCRIPTIONS)
            cursor.execute(database.CREATE_TABLE_MATCHES)
            cursor.execute(database.CREATE_TABLE_ALERTS)
            return connection
        except:
            raise DBHelperException('Error Connecting to Database\n\n' + traceback.format_exc())

    def disconnect(self):
        try:
            if self.connection:
                self.connection.rollback()
                self.connection.close()
            self.connection = None
        except:
            raise DBHelperException('Error Disconnecting from Database\n\n' + traceback.format_exc())

    def reset(self):
        self.disconnect()
        self.connect()

    def get_subscriptions(self):
        print('Getting subscriptions')

    def purge_old_matches(self):
        print('purging')

    def get(self, query):
        print()

    def insert(self, table, values):
        print()

    def remove(self, table, id):
        print()

    def commit(self):
        try:
            self.connection.commit()
        except:
            raise DBHelperException('Error Committing changes to Database')

    def get_subscriptions_by_user(self, username):
        return []

    def insert_subscription(self, username, sub):
        return True

    def remove_subscription(self, username, sub):
        return True

    def remove_all_subscriptions(self, username):
        return True

    def count_all_users(self):
        users = 0
        return users

    def count_current_users(self):
        users = 0
        return users

    def count_all_subscriptions(self):
        subs = 0
        return subs

    def count_unique_subscriptions(self):
        subs = 0
        return subs

    def count_unique_subreddits(self):
        subreddits = 0
        return subreddits

    def count_total_matches(self):
        matches = 0
        return matches


class DBHelperException(Exception):
    def __init__(self, error_args):
        Exception.__init__(self, "DBHelper Exception: {0}".format(error_args))
        self.errorArgs = error_args
