"""
==========================================
Author:         Tyler Brockett
Description:    Reddit Bot - buildapcsales
Date:           11/13/2015
==========================================
"""

import os
import time
import praw
import sqlite3
import traceback
from sys import stdout

from utils import inbox
from utils.color import Color
from utils.logger import Logger
from private import accountinfo

SLEEP_SECONDS = 45
NUM_POSTS_TO_CRAWL = 20

connection = None
reddit = None
start_time = None


def run_bot():
    global start_time
    while True:
        try:
            read_inbox()
        except KeyboardInterrupt:
            Logger.log(Color.RED, 'Interrupted')
            exit()
        except:
            handle_crash(traceback.format_exc())
        sleep(SLEEP_SECONDS)


def read_inbox():
    global connection, reddit
    i = 0

    unread_messages = []
    try:
        unread_messages = reddit.get_unread(limit=None)
    except:
        reddit.send_message(accountinfo.developerusername, "SALES_BOT Exception - Read Inbox", traceback.format_exc())

    for unread_message in unread_messages:
        username, message_id, subject, body = \
            (str(unread_message.author).lower(),
             unread_message.id,
             inbox.format_subject(unread_message.subject.lower()),
             unread_message.body.lower())

        reddit.send_message(accountinfo.developerusername, "FORWARD: " + subject + ' USERNAME: ' + username, body)

        if subject == 'username mention':
            unread_message.mark_as_read()
            reddit.send_message(accountinfo.developerusername, "Bot - Username Mention", 'username: ' + username + '\n\n' + body)

        elif subject == 'post reply':
            unread_message.mark_as_read()
            reddit.send_message(accountinfo.developerusername, "Bot - Post Reply", 'username: ' + username + '\n\n' + body)
        else:
            try:
                unread_message.reply()
                unread_message.mark_as_read()
            except:
                reddit.send_message(accountinfo.developerusername, "Bot Exception - Default", traceback.format_exc())
        sleep(2)


def compose_message(username):
    ret = 'Hi /u/' + username + ',\n' \
        'There have been ***HUGE*** changes to the /r/buildapcsales bot. \n\t\n' \
        'First off, it has changed to /u/AlertBot. Even with this change, the new bot still has all your ' \
        'previous subscriptions (if you had any).\n\n' \
        'You can continue to use /u/AlertBot exactly as you have been, but there have been MANY new features ' \
        'you may want to take note of:\n\n' \
        '1. Ability to specify ***multiple*** subreddits to check in (if none are specified, it defaults to ' \
        '/r/buildapcsales. For example, you can now search for games in /r/GameDeals\n' \
        '2. Specify sites to whitelist or blacklist (e.g. Amazon.com or Jet.com)\n' \
        '3. Specify multiple terms to check against in the post. This way you don\'t have to worry of an exact string match.\n' \
        '4. Specify specific redditors to whitelist or blacklist (helpful for /r/HardwareSwap because of scammers)\n' \
        ''


def open_database():
    global connection
    connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + database.DATABASE_LOCATION)
    cursor = connection.cursor()
    cursor.execute(database.CREATE_TABLE_SUBSCRIPTIONS)
    cursor.execute(database.CREATE_TABLE_MATCHES)
    cursor.execute(database.CREATE_TABLE_ALERTS)


def connect_to_reddit():
    global reddit
    # Connecting to Reddit
    user_agent = 'SALES__B0T - A Sales Notifier R0B0T'
    reddit = praw.Reddit(user_agent=user_agent)
    # TODO Use OAuth instead of this login method
    reddit.login(accountinfo.username, accountinfo.password, disable_warning=True)


def sleep(seconds):
    print 'Sleeping',
    for i in range(seconds):
        stdout.write(".")
        stdout.flush()
        time.sleep(1)
    print ''


def initialize():
    connect_to_reddit()
    open_database()


def destroy():
    global reddit, connection
    if connection:
        connection.close()
    connection = None
    reddit = None
    logger.log('red', '----------------- DESTROYED -----------------')


def handle_crash(stacktrace):
    global connection, reddit
    destroy()
    reset = False
    while not reset:
        try:
            initialize()
            reddit.send_message(accountinfo.developerusername, "Exception Handled", stacktrace)
            reset = True
        except:
            sleep(15)


__author__ = 'tyler'
if __name__ == "__main__":
    try:
        global start_time
        start_time = times.get_current_timestamp()
        initialize()
        run_bot()
    except KeyboardInterrupt:
        logger.log('red', 'Interrupted')
        exit()
    except:
        logger.log('red', traceback.format_exc())
        exit()

