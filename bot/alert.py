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

from helpers import database, color
from helpers import inbox
from private import accountinfo

connection = None
reddit = None

subject = "buildapcsales bot - message from developer"
signature = "\n\t \n\t \n-tylerbrockett"

select_users = []


def compose_alert(username):
    # Insert alert message here!
    result = inbox.compose_greeting(username) + \
        "**I have a question for you all!** And an apology for some. So let's start with the apology. " + \
        "One user requested that things like 'amazon' be subscribable (is that a word?) so I made " + \
        "a quick change to the code so it would check the URL of the submissions, and bestbuy " + \
        "happened to have a URL which contained the sku '11**6700**9'. You all " + \
        "can probably guess where I'm going with that. Sorry to all of you that were subscribed to " + \
        "that... \n\t \n\t \n" + \
        "***Anyways***, now to my question for you all. A few of you have requested being able to " + \
        "filter notifications by website. I currently see two options for that.\n\t \n\t \n" + \
        "1. People can just subscribe to something like 'amazon' as they normally would, and I " + \
        "put a check in the code to see if there is a match against a whitelist of sites, and if " + \
        "so THEN check the url against it. The catch here is that the site would ***have*** to be " + \
        "in the whitelist. \n" + \
        "2. People subscribe to something like 'site: amazon'. You could continue to " + \
        "subscribe to items for all sites the normal way, this would only matter for subscribing to " + \
        "all items only for a specific site. This would pave the way for being able to subscribe to " + \
        "something like 'site: amazon item: 6700' which is what a few of you have been requesting. " + \
        "\n\t \n\t \n" + \
        "I will be taking an unofficial vote by tallying responses. I may post in " + \
        "/r/buildapcsalesmeta as well, we'll see. **Unfortunately**, if I make any changes it " + \
        "probably won't happen until I'm out of school in a couple months. This is my last semester, " + \
        "and things are getting pretty crazy! I hope you all understand. \n\t \n\t \n" + \
        "Also, a random PSA I've been meaning to tell everyone. I used to have a length requirement " + \
        "of 2 (or 3?) characters for subscriptions to prevent stupid stuff from happening. But... it " + \
        "was pretty short-sighted. Now there is a length requirement of just 1 character, to prevent " + \
        "empty subscriptions, because who knows what would happen. But, what's cool, ***and I'm an " + \
        "idiot for not seeing it sooner***, is that you can subscribe to things like '**i3**', " + \
        "'**i5**', and '**i7**' now! Sorry if you guys tried to subscribe to those in the past. " + \
        "Also, I haven't tried it yet, but in theory if you wanted to be subscribed to ***ALL*** " + \
        "posts (some have wanted this, but be warned, you **will** get a lot of PMs), if you " + \
        "subscribe to '**[**' or '**]**' you can effectively achieve that because of the post flair " + \
        "like **[**CPU**]**. But again, that's untested and I make no guarantees, since weird stuff " + \
        "definitely happens. \n\t \n\t \n" + \
        "Thanks again for using the bot!"

    result += compose_salutation()
    return result


def run_alerts():
    global connection, select_users
    # if selected_users is empty, send to all, otherwise just send to selected_users
    i = 0
    num = 0
    if not select_users:
        needs_alert = connection.cursor().execute(database.GET_USERNAMES_THAT_NEED_ALERT).fetchall()
        num = len(needs_alert)
        for row in needs_alert:
            username = row[database.COL_ALERTS_USERNAME]
            entry = (username, 1)  # 1 == True
            try:
                reddit.send_message(username, subject, compose_alert(username))
                connection.cursor().execute(database.INSERT_ROW_ALERTS, entry)
                connection.commit()
                color.print_color('blue', 'message sent to ' + username)
                i += 1
            except:
                color.print_color('red', "ALERT FAILED: " + username + \
                                  "\n\t \n\t \n" + traceback.format_exc())
                connection.rollback()
                connection.close()
                exit()
            sleep(2)
    else:
        num = len(select_users)
        for username in select_users:
            try:
                reddit.send_message(username, subject, compose_alert(username))
                color.print_color('blue', 'message sent to ' + username)
                i += 1
            except:
                color.print_color('red', "ALERT FAILED: " + username + \
                                  "\n\t \n\t \n" + traceback.format_exc())
            sleep(2)
    print "Sent message to " + str(i) + "/" + str(num) + " users."


def compose_salutation():
    result = signature + "\n\t \n\t \n" + \
             "[code](https://github.com/tylerbrockett/reddit-bot-buildapcsales)" + \
             " | /u/" + accountinfo.developerusername + \
             " | /r/buildapcsales\n"
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
    reddit.login(accountinfo.developerusername, accountinfo.developerpassword, disable_warning=True)


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
    color.print_color('red', stacktrace)
    reddit.send_message(accountinfo.developerusername, "Bot Alerts Crashed", stacktrace)
    connection.close()
    exit()


if __name__ == "__main__":
    try:
        initialize()
        run_alerts()
        finish_up()
    except:
        handle_crash(traceback.format_exc())

