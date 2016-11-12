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
            connection.execute('PRAGMA foreign_keys = ON;') #TODO CHECK IF NEEDED!
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

    # ==============================================================================
    #           SUBSCRIPTIONS
    # ==============================================================================
    def insert_subscription(self, username, message_id, sub, timestamp):
        print('Insert subscription')
        try:
            sub = (username, message_id, sub, timestamp,)
            self.connection.cursor().execute(database.INSERT_ROW_SUBSCRIPTIONS, sub)
            self.connection.commit()
        except:
            raise DBHandlerException('ERROR - insert_subscription')

    def get_subscriptions(self):
        print('Getting subscriptions')
        subs = []
        results = self.connection.cursor().execute(database.GET_ALL_SUBSCRIPTIONS).fetchall()
        for temp in results:
            item = temp[database.COL_SUB_ITEM]
            username = temp[database.COL_SUB_USERNAME]
            message_id = temp[database.COL_SUB_MESSAGE_ID]
            sub = Subscription(item, username, message_id)
            if sub.valid:
                subs.append((username, message_id, sub))
            else:
                raise DBHandlerException('ERROR - get_subscriptions - Subscription not valid')
        return subs

    def get_subscriptions_by_user(self, username):
        print('Get Subs By Username')
        subs = []
        result = self.connection.cursor().execute(database.GET_SUBSCRIPTIONS_BY_USERNAME, (username,)).fetchall()
        for temp in result:
            item = temp[database.COL_SUB_ITEM]
            username = temp[database.COL_SUB_USERNAME]
            message_id = temp[database.COL_SUB_MESSAGE_ID]
            sub = Subscription(item, username, message_id)
            if sub.valid:
                subs.append((username, message_id, sub))
            else:
                raise DBHandlerException('ERROR - get_subscriptions - subscription not valid')
        return subs

    # TODO - Check if subscription exists first
    def remove_subscription(self, username, sub):
        try:
            self.connection.cursor().execute(database.REMOVE_ROW_SUBSCRIPTIONS, (username, sub))
            self.connection.commit()
        except:
            raise DBHandlerException('ERROR - remove_subscription')

    def remove_subscription_by_number(self, username, sub_num):
        try:
            subs = self.get_subscriptions_by_user(username)
            if (sub_num - 1) >= len(subs) or sub_num <= 0:
                raise DBHandlerException('ERROR - Invalid subscription #. Requested Subscription: ' + str(sub_num) + '  Number of subscriptions: ' + str(len(subs)))
            sub = subs[sub_num - 1]
            self.remove_subscription(username, sub[2]) # (username, message_id, sub)
        except:
            raise DBHandlerException('Error - remove_subscription_by_number')

    # TODO - Check if subscription exists first
    def remove_all_subscriptions(self, username):
        try:
            self.connection.cursor().execute(database.REMOVE_ALL_SUBSCRIPTIONS_BY_USERNAME, (username,))
            self.connection.commit()
        except:
            raise DBHandlerException('ERROR - remove_all_subscriptions')

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

    # ==============================================================================
    #           MATCHES
    # ==============================================================================

    def insert_match(self, username, item, permalink):
        try:
            match = (username, item, permalink, times.get_current_timestamp())
            self.connection.cursor().execute(database.INSERT_ROW_MATCHES, match)
            self.connection.cursor().execute(database.INSERT_ROW_ALL_MATCHES, match)
            self.connection.commit()  # TODO Move this to where method is called.
        except:
            raise DBHandlerException('Error - insert_match')

    def count_total_matches(self):
        matches = 0
        try:
            matches = len(self.connection.cursor().execute(database.GET_ALL_MATCHES).fetchall())
        except:
            raise DBHandlerException('ERROR - count_total_matches')
        return matches

    def check_if_match_exists(self, username, item, permalink):
        try:
            return len(self.connection.cursor().execute(database.GET_MATCH, (username, item, permalink)).fetchall()) >= 1
        except:
            print('ERROR - Couldn\'t figure out if match existed')
            return True

    def purge_old_matches(self):
        print('purging')
        current_time = times.get_current_timestamp()
        quarter_of_year = 31557600 / 4
        marked_old_time = current_time - quarter_of_year
        try:
            self.connection.cursor().execute(database.PURGE_OLD_MATCHES, (marked_old_time,))
            self.commit()
        except:
            raise DBHandlerException('ERROR - purge_old_matches')

    # ==============================================================================
    #           USERS
    # ==============================================================================

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

    # ==============================================================================
    #           SUBREDDITS
    # ==============================================================================

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


class DBHandlerException(Exception):
    INTEGRITY_ERROR = 'Integrity Error - Row already exists'

    def __init__(self, error_args):
        Exception.__init__(self, "DBHelper Exception: {0}".format(error_args))
        self.errorArgs = error_args
