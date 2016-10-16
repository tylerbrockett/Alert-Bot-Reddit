import os
import sqlite3
import traceback

from utils import times
from utils import database
from utils.subscription import Subscription


class DatabaseHandler:
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        try:
            connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + database.DATABASE_LOCATION)
            cursor = self.connection.cursor()
            cursor.execute(database.CREATE_TABLE_SUBSCRIPTIONS)
            cursor.execute(database.CREATE_TABLE_MATCHES)
            cursor.execute(database.CREATE_TABLE_ALL_MATCHES)
            cursor.execute(database.CREATE_TABLE_ALL_USERS)
            cursor.execute(database.CREATE_TABLE_ALERTS)
            return connection
        except:
            raise DBHandlerException('Error Connecting to Database\n\n' + traceback.format_exc())

    def disconnect(self):
        try:
            if self.connection:
                self.connection.rollback()
                self.connection.close()
            self.connection = None
        except:
            raise DBHandlerException('Error Disconnecting from Database\n\n' + traceback.format_exc())

    def reset(self):
        self.disconnect()
        self.connect()

    def commit(self):
        self.connection.commit()

    def get_subscriptions(self):
        print('Getting subscriptions')
        subs = []
        results = self.connection.cursor().execute(database.GET_ALL_SUBSCRIPTIONS).fetchall()
        for temp in results:
            username = temp[database.COL_SUB_USERNAME]
            message_id = temp[database.COL_SUB_MESSAGE_ID]
            sub = Subscription(temp[database.COL_SUB_ITEM])
            timestamp = temp[database.COL_SUB_TIMESTAMP]
            if sub.valid:
                subs.append((username, message_id, sub, timestamp))
            else:
                raise DBHandlerException('ERROR - get_subscriptions')
        return subs

    def insert_match(self, username, item, permalink):
        try:
            self.connection.cursor().execute(database.INSERT_ROW_MATCHES,
                                             (username, item, permalink, times.get_current_timestamp()))
            self.connection.cursor().execute(database.INSERT_ROW_ALL_MATCHES,
                                             (username, item, permalink, times.get_current_timestamp()))
            self.connection.commit()  # TODO Move this to where method is called.
        except:
            raise DBHandlerException('Error - insert_match')

    def purge_old_matches(self):
        print('purging')
        current_time = times.get_current_timestamp()
        quarter_of_year = 31556926 / 4
        marked_old_time = current_time - quarter_of_year
        try:
            self.connection.cursor().execute(database.PURGE_OLD_MATCHES, (marked_old_time,))
            self.connection.commit()
        except:
            raise DBHandlerException('ERROR - purge_old_matches')

    def get_subscriptions_by_user(self, username):
        print('Get Subs By Username')
        subs = []
        result = self.connection.cursor().execute(database.GET_SUBSCRIPTIONS_BY_USERNAME, (username,)).fetchall()
        for temp in result:
            sub = Subscription(temp[database.COL_SUB_ITEM])
            if sub.valid:
                subs.append(sub)
            else:
                raise DBHandlerException('ERROR - get_subscriptions - subscription not valid')
        return subs

    def insert_subscription(self, username, message_id, sub, timestamp):
        print('Insert subscription')
        try:
            self.connection.cursor().execute(database.INSERT_ROW_SUBSCRIPTIONS, (username, message_id, sub, timestamp))
            self.connection.commit()
        except:
            raise DBHandlerException('ERROR - insert_subscription')

    def remove_subscription(self, username, sub):
        try:
            self.connection.cursor().execute(database.REMOVE_ROW_SUBSCRIPTIONS, (username, sub,))
            self.connection.commit()
        except:
            raise DBHandlerException('ERROR - remove_subscription')

    def remove_all_subscriptions(self, username):
        try:
            self.connection.cursor().execute(database.REMOVE_ALL_SUBSCRIPTIONS_BY_USERNAME, (username,))
            self.connection.commit()
        except:
            raise DBHandlerException('ERROR - remove_all_subscriptions')

    def count_all_users(self):
        users = 0
        try:
            users = len(self.connection.cursor().execute(database.GET_ALL_USERS).fetchall())
        except:
            raise DBHandlerException('ERROR - count_all_users')
        return users

    def count_current_users(self):
        users = 0
        try:
            users = len(self.connection.cursor().execute(database.GET_ACTIVE_USERS).fetchall())
        except:
            raise DBHandlerException('ERROR - count_active_users')
        return users

    def count_all_subscriptions(self):
        subs = 0
        try:
            subs = len(self.connection.cursor().execute(database.GET_ALL_SUBSCRIPTIONS).fetchall())
        except:
            raise DBHandlerException('ERROR - count_all_subscriptions')
        return subs

    def count_unique_subscriptions(self):
        subs = 0
        try:
            subs = len(self.connection.cursor().execute(database.GET_UNIQUE_SUBSCRIPTIONS).fetchall())
        except:
            raise DBHandlerException('ERROR - count_unique_subscriptions')
        return subs

    def count_subreddits(self):
        dict = {}
        try:
            subscriptions = self.get_subscriptions()
            for sub in subscriptions:
                for subreddit in sub.subreddits:
                    if subreddit in dict:
                        dict[subreddit] += 1
                    else:
                        dict[subreddit] = 1
        except:
            raise DBHandlerException('ERROR - count_subreddits')
        return sorted(dict.items(), key=lambda x: x[1])

    def count_total_matches(self):
        matches = 0
        try:
            matches = len(self.connection.cursor().execute(database.GET_ALL_MATCHES).fetchall())
        except:
            raise DBHandlerException('ERROR - count_total_matches')
        return matches


class DBHandlerException(Exception):
    INTEGRITY_ERROR = 'Integrity Error - Row already exists'

    def __init__(self, error_args):
        Exception.__init__(self, "DBHelper Exception: {0}".format(error_args))
        self.errorArgs = error_args
