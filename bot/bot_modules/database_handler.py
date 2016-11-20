import os
import sqlite3
import traceback

from utils import times
from utils import database
from utils.subscription import Subscription
from os import path
from definitions import DB_LOCATION
from utils import files


class DatabaseHandler:
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        try:
            print('PATH: ' + DB_LOCATION)
            if not path.isfile(DB_LOCATION):
                files.create_file(DB_LOCATION)
            connection = sqlite3.connect(DB_LOCATION)
            connection.text_factory = str
            connection.execute('PRAGMA foreign_keys = ON;')
            cursor = connection.cursor()
            cursor.execute(database.CREATE_TABLE_SUBSCRIPTIONS)
            cursor.execute(database.CREATE_TABLE_MATCHES)
            cursor.execute(database.CREATE_TABLE_ALL_MATCHES)
            cursor.execute(database.CREATE_TABLE_ALL_USERS)
            cursor.execute(database.CREATE_TABLE_ALERTS)
            return connection
        except:
            raise DatabaseHandlerException('Error Connecting to Database\n\n' + traceback.format_exc())

    def disconnect(self):
        try:
            if self.connection:
                self.connection.rollback()
                self.connection.close()
            self.connection = None
        except:
            raise DatabaseHandlerException('Error Disconnecting from Database\n\n' + traceback.format_exc())

    def reset(self):
        try:
            self.disconnect()
            self.connection = self.connect()
        except:
            DatabaseHandlerException('Error resetting connection to database\n\n' + traceback.format_exc())

    def commit(self):
        self.connection.commit()

    # ==============================================================================
    #           SUBSCRIPTIONS
    # ==============================================================================
    def insert_subscription(self, username, message_id, sub_data, timestamp):
        print('Insert subscription')
        try:
            sub = [username, message_id, sub_data, timestamp]
            self.connection.cursor().execute(database.INSERT_ROW_SUBSCRIPTIONS, sub)
            self.connection.cursor().execute(database.INSERT_ROW_ALL_USERS, [username])
            # Commit is handled after the message is sent
        except:
            raise DatabaseHandlerException('ERROR - insert_subscription')

    def get_subscriptions(self):
        print('Getting subscriptions')
        subs = []
        results = self.connection.cursor().execute(database.GET_ALL_SUBSCRIPTIONS).fetchall()
        for sub in results:
            item = sub[database.COL_SUB_ITEM]
            username = sub[database.COL_SUB_USERNAME]
            message_id = sub[database.COL_SUB_MESSAGE_ID]
            subscription = Subscription(item, username, message_id)
            if subscription.status == Subscription.STATUS_VALID:
                subs.append(subscription)
            else:
                print("INVALID SUB:   " + subscription.to_string())
                self.remove_subscription(subscription)  # TODO Should this really be here?
                raise DatabaseHandlerException('ERROR - get_subscriptions - Subscription not valid')
        return subs

    def get_subscriptions_by_user(self, username):
        print('Get Subs By Username')
        subs = []
        result = self.connection.cursor().execute(database.GET_SUBSCRIPTIONS_BY_USERNAME, [username]).fetchall()
        for sub in result:
            item = sub[database.COL_SUB_ITEM]
            username = sub[database.COL_SUB_USERNAME]
            message_id = sub[database.COL_SUB_MESSAGE_ID]
            subscription = Subscription(item, username, message_id)
            if subscription.status == Subscription.STATUS_VALID:
                subs.append(subscription)
            else:
                print("INVALID SUB:   " + subscription.to_string())
                self.remove_subscription(subscription)  # TODO Should this really be here?
                raise DatabaseHandlerException('ERROR - get_subscriptions - subscription not valid')
        return subs

    def get_subscriptions_by_message_id(self, username, message_id):
        try:
            result = self.connection.cursor().execute(database.GET_SUBSCRIPTION_BY_MESSAGE_ID, [username, message_id]).fetchall()
            subs = []
            for sub in result:
                item = sub[database.COL_SUB_ITEM]
                username = sub[database.COL_SUB_USERNAME]
                message_id = sub[database.COL_SUB_MESSAGE_ID]
                subscription = Subscription(item, username, message_id)
                print('BY MESSAGE ID: ' + subscription.to_string())
                subs.append(subscription)
            return subs
        except:
            print(traceback.format_exc())
            raise DatabaseHandlerException('Error - get_subscription_by_message_id')

    def remove_subscriptions_by_message_id(self, username, message_id):
        try:
            subs = self.get_subscriptions_by_message_id(username, message_id)
            self.connection.cursor().execute(database.REMOVE_SUBSCRIPTION_BY_MESSAGE_ID, [username, message_id])
            self.commit()
            return subs
        except:
            raise DatabaseHandlerException('Error - get_subscription_by_message_id')

    def remove_subscription(self, subscription):
        try:
            return self.remove_subscriptions_by_message_id(subscription.username, subscription.message_id)
        except:
            return []

    def remove_subscription_by_number(self, username, sub_num):
        try:
            subs = self.get_subscriptions_by_user(username)
            if sub_num > len(subs) or sub_num <= 0:
                return None
            sub = subs[sub_num - 1]
            self.remove_subscription(sub)
            return sub
        except:
            return None

    def get_num_subscriptions_by_user(self, username):
        return len(self.get_subscriptions_by_user(username))

    def remove_all_subscriptions(self, username):
        try:
            if self.get_num_subscriptions_by_user(username) >= 1:
                self.connection.cursor().execute(database.REMOVE_ALL_SUBSCRIPTIONS_BY_USERNAME, [username])
                self.commit()
                return True
            else:
                return False
        except:
            raise DatabaseHandlerException('ERROR - remove_all_subscriptions')

    def count_all_subscriptions(self):
        subs = 0
        try:
            subs = len(self.connection.cursor().execute(database.GET_ALL_SUBSCRIPTIONS).fetchall())
        except:
            subs = -1
            print('Error counting all subscriptions')
        return subs

    def count_unique_subscriptions(self):
        subs = 0
        try:
            subs = len(self.connection.cursor().execute(database.GET_UNIQUE_SUBSCRIPTIONS).fetchall())
        except:
            subs = -1
            print('Error counting unique subscriptions')
        return subs

    # ==============================================================================
    #           MATCHES
    # ==============================================================================

    def insert_match(self, username, item, permalink):
        try:
            match = [username, item, permalink, times.get_current_timestamp()]
            self.connection.cursor().execute(database.INSERT_ROW_MATCHES, match)
            self.connection.cursor().execute(database.INSERT_ROW_ALL_MATCHES, match)
            # NOTE: Commit is called after message is sent
        except:
            raise DatabaseHandlerException('Error - insert_match')

    def count_total_matches(self):
        matches = 0
        try:
            matches = len(self.connection.cursor().execute(database.GET_ALL_MATCHES).fetchall())
        except:
            matches = -1
            print('Error counting all matches')
        return matches

    def check_if_match_exists(self, username, item, permalink):
        try:
            return len(self.connection.cursor().execute(database.GET_MATCH, [username, item, permalink]).fetchall()) >= 1
        except:
            print('ERROR - Couldn\'t figure out if match existed')
            return True

    def purge_old_matches(self):
        print('purging')
        current_time = times.get_current_timestamp()
        quarter_of_year = 31557600 / 4
        marked_old_time = current_time - quarter_of_year
        try:
            self.connection.cursor().execute(database.PURGE_OLD_MATCHES, [marked_old_time])
            self.commit()
        except:
            raise DatabaseHandlerException('ERROR - purge_old_matches')

    # ==============================================================================
    #           USERS
    # ==============================================================================

    def count_all_users(self):
        users = 0
        try:
            users = len(self.connection.cursor().execute(database.GET_ALL_USERS).fetchall())
        except:
            user = -1
            print('Error counting all users')
        return users

    def count_current_users(self):
        users = 0
        try:
            users = len(self.connection.cursor().execute(database.GET_ACTIVE_USERS).fetchall())
        except:
            users = -1
            print('Error counting current users')
        return users

    # ==============================================================================
    #           SUBREDDITS
    # ==============================================================================

    # TAG_DEFAULT_SUBREDDIT
    def get_unique_subreddits(self):
        dict = {}
        try:
            subscriptions = self.get_subscriptions()
            for sub in subscriptions:
                if len(sub.data[Subscription.SUBREDDITS]) == 0 and 'buildapcsales' not in dict.keys():
                    dict['buildapcsales'] = 1
                for subreddit in sub.data[Subscription.SUBREDDITS]:
                    if subreddit in dict:
                        dict[subreddit] += 1
                    else:
                        dict[subreddit] = 1
        except:
            return {}
        return sorted(dict.items(), key=lambda x: x[1])


class DatabaseHandlerException(Exception):
    INTEGRITY_ERROR = 'Integrity Error - Row already exists'

    def __init__(self, error_args):
        Exception.__init__(self, "DBHelper Exception: {0}".format(error_args))
        self.errorArgs = error_args
