"""
==========================================
Author:         Tyler Brockett
Description:    Reddit Alerts Bot
Date:           12/14/2015
==========================================
"""

import os
import sqlite3
import time
import traceback
from sys import stdout
import praw

from helpers.colorize import colorize
from helpers import database
from helpers import inbox
from private import accounts

connection = None
reddit = None

subject = "buildapcsales bot - message from developer"
signature = "\n\t \n\t \n-tylerbrockett"

select_users = []


def compose_alert(username):
    # Insert alert message here!
    result = inbox.compose_greeting(username) + \
        "As you're probably aware, the buildapcsales bot has been offline for the " + \
        "last week or so due to a pretty severe bug. Many users were receiving several " + \
        "messages for the same item match. I have been looking through the database to try " + \
        "to figure out if there was a pattern to what was causing it. I found a handful of " + \
        "duplicate subscriptions, which would cause some problems, but didn't explain the " + \
        "rest of the users' problems. I made some changes to the code and made the database " + \
        "more robust which should fix the duplicate database entry bug. Hopefully these changes " + \
        "will fix the issue, but if it doesn't, it will certainly help me isolate it so I can " + \
        "diagnose it a bit more easily. The major changes are done, and the bot will be back up " + \
        "shortly, but I will be making minor tweaks for a while. Feel free to reply to this " + \
        "message if you have any questions or anything. Thank you for your patience! :)"
    result += compose_salutation()
    return result


def run_alerts():
    global connection, select_users
    # if selected_users is empty, send to all, otherwise just send to selected_users
    if not select_users:
        needs_alert = connection.cursor().execute(database.GET_USERNAMES_THAT_NEED_ALERT).fetchall()
        for row in needs_alert:
            username = row[database.COL_ALERTS_USERNAME]
            entry = (username, 1)  # 1 == True
            try:
                connection.cursor().execute(database.INSERT_ROW_ALERTS, entry)
                reddit.send_message(username, subject, compose_alert(username))
                connection.commit()
                colorize('blue', 'message sent to ' + username)
            except:
                colorize('red', traceback.format_exc())
                connection.rollback()
                connection.close()
                exit()
            sleep(2)
    else:
        for username in select_users:
            try:
                reddit.send_message(username, subject, compose_alert(username))
            except:
                colorize('red', "ALERT FAILED: " + username)


def compose_salutation():
    result = signature + "\n\t \n\t \n" + \
        "[Github Repository](https://github.com/tylerbrockett/reddit-bot-buildapcsales) | " + \
        "[Developer Email](mailto://" + accounts.developeremail + ")\n"
    return result


def open_database():
    global connection
    connection = sqlite3.connect(os.path.realpath('.') + database.DATABASE_LOCATION)
    cursor = connection.cursor()
    cursor.execute(database.CREATE_TABLE_SUBSCRIPTIONS)
    cursor.execute(database.CREATE_TABLE_MATCHES)
    cursor.execute(database.CREATE_TABLE_ALERTS)


def connect_to_reddit():
    global reddit
    # Connecting to Reddit
    user_agent = 'tylerbrockett - developer'
    reddit = praw.Reddit(user_agent=user_agent)
    # TODO - TAKE OUT DISABLE WARNING AND FIGURE OUT REPLACEMENT CODE
    reddit.login(accounts.developer, accounts.developerpassword, disable_warning=True)


def sleep(seconds):
    print 'Sleeping',
    for i in range(seconds):
        stdout.write(".")
        stdout.flush()
        time.sleep(1)
    print ''


def initialize():
    open_database()
    connect_to_reddit()


def finish_up():
    global connection
    connection.cursor().execute(database.DROP_TABLE_ALERTS)
    connection.commit()
    connection.close()


def handle_crash(stacktrace):
    global connection, reddit
    colorize('red', stacktrace)
    reddit.send_message(accounts.developer, "Bot Alerts Crashed", stacktrace)
    connection.close()
    exit()


if __name__ == "__main__":
    try:
        initialize()
        run_alerts()
        finish_up()
    except:
        handle_crash(traceback.format_exc())
