"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   12/2/2016
Version:            v2.0
==========================================
"""

import sqlite3
import time
import traceback
import praw

from utils.color import Color
from utils.logger import Logger
from utils import database
from utils import inbox
from accounts import accountinfo
import definitions
from praw.errors import InvalidUser
from bot_modules.database_handler import DatabaseHandler

NOTIFICATION =  \
'Hey guys, one final message from me for a while (hopefully). Unfortunately, I wasn\'t able to get the old subscriptions working with the new ' + \
'bot, so we are going to have to start with a fresh database. Below are your old subscriptions, in case you would ' + \
'like to re-subscribe to them. I apologize for the inconvenience. \n\n-Tyler'


class Notifications:

    def connect_to_reddit(self):
        user_agent = 'tylerbrockett - developer'
        reddit = praw.Reddit(user_agent=user_agent)
        reddit.login(accountinfo.developerusername, accountinfo.developerpassword, disable_warning=True)
        return reddit

    def connect_to_db(self):
        connection = sqlite3.connect(definitions.DB_LOCATION)
        cursor = connection.cursor()
        cursor.execute(database.CREATE_TABLE_SUBSCRIPTIONS)
        cursor.execute(database.CREATE_TABLE_MATCHES)
        cursor.execute(database.CREATE_TABLE_ALERTS)
        cursor.execute(database.CREATE_TABLE_ALL_MATCHES)
        cursor.execute(database.CREATE_TABLE_ALL_USERS)
        return connection

    def __init__(self):
        self.subject = 'Alert_Bot - wiping database - need to resubscribe'
        self.needs_alert = [['XdrummerXboy', 0]]
        self.needs_alert = []
        self.errors = []
        self.invalid_users = []

        self.db = self.connect_to_db()
        self.reddit = self.connect_to_reddit()
        self.db_helper = DatabaseHandler()

    def send_message(self, username):
        subs = self.db_helper.get_subscriptions_by_user(username)
        Logger.log('\n\n' + str(len(subs)) + ' subs for user')
        sub_text = inbox.format_subscription_list(subs, 'Your Old Subscriptions')
        message = inbox.compose_greeting(username) + NOTIFICATION + "\n\n" + sub_text
        self.reddit.send_message(username, self.subject, message)

    def run_alerts(self):
        # if selected_users is empty, send to all, otherwise just send to selected_users
        if not self.needs_alert:
            self.needs_alert = self.db.cursor().execute(database.GET_USERNAMES_THAT_NEED_ALERT).fetchall()
            Logger.log(str(len(self.needs_alert)) + '  USERS NEED ALERT')
            time.sleep(20)
        num = len(self.needs_alert)
        i = 0
        for row in self.needs_alert:
            username = row[0]
            entry = (username, 1)  # 1 == True
            try:
                self.send_message(username)
                self.db.cursor().execute(database.INSERT_ROW_ALERTS, entry)
                self.db.commit()
                Logger.log('message sent to ' + username)
                i += 1
            except InvalidUser:
                self.invalid_users.append(username)
                Logger.log('Invalid User --> ' + username)
            except:
                self.errors.append(username)
                Logger.log('ALERT FAILED: ' + username + '\n\t \n\t \n' + traceback.format_exc())
                self.db.rollback()
                self.db.close()
                exit()

        Logger.log('\n\nInvalid Users')
        for user in self.invalid_users:
            Logger.log(user)

    def finish_up(self):
        self.db.cursor().execute(database.DROP_TABLE_ALERTS)
        self.db.commit()
        self.db.close()

    def handle_crash(self, stacktrace):
        print(stacktrace)
        self.reddit.send_message(accountinfo.developerusername, 'Bot Alerts Crashed', stacktrace)
        self.db.close()
        exit()


if __name__ == '__main__':
    notifications = Notifications()
    try:
        notifications.run_alerts()
        notifications.finish_up()
    except:
        notifications.handle_crash(traceback.format_exc())
