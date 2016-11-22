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

from utils import database
from utils import inbox
from private import accountinfo
import definitions
from praw.errors import InvalidUser


NOTIFICATION =  \
"# Alert Bot \n\n\
\
There have been ***BIG*** changes to the bot for /r/buildapcsales. Please visit \
[This post](https://www.reddit.com/r/BuildAPCSalesMeta/comments/5e9pzu/alert_bot_the_new_and_improved_sales_bot/) for more detailed information than what's contained in this message. \
First off, it's getting a new name and subreddit, /u/Alert_Bot and /r/Alert_Bot. This is due to the fact \
that the bot is no longer just for /r/buildapcsales, and has been opened up to ANY subreddit, so it's no longer just for sales! Read below to find out all the new features! \
You ***should*** be able to continue using the bot exactly as you have (except for the username you send it to), but... I'd strongly recommend becoming familiar with the new \
way the bot handles things. Also, the database from /u/sales__bot has been backed up, then migrated to work with the new bot. If for whatever reason things go horribly south, \
We'll just revert back to the old bot with the backed up database. \n\n\
With the new bot, subscriptions to the bot should all be ***INLINE in the body section of the message.*** Use the subject to give yourself a brief description of what the \
subscription is about. ***PLEASE view [the Readme file in GitHub](https://github.com/tylerbrockett/Alert-Bot-Reddit/blob/master/README.md) to learn how the syntax for messages to the bot should be.*** \
\
\n\n\
#### Parameters\n\n\
There are now parameters you can add to your subscriptions. Most parameters can take a single value, or a list of values.\n\n\
* ***-title*** --> Specifies words or phrases to watch out for in the title of the post. Multiple '-title' parameters can be specified, the user will be notified of the post even if only ***ONE*** of the '-title' parameters match.\n\n\
* ***-body*** --> Specifies words or phrases to watch out for in the body of the post. This could be used for selftext ***OR*** links, the '-body' parameter will figure out which post type it is. Multiple '-body' parameters can be specified, the user will be notified of the post even if only ***ONE*** of the '-body' parameters match. This parameter is especially useful for filtering URLs from posts, such as if you only want to be notified of posts that link to *'amazon.com'*.\n\n\
* ***-redditors*** --> Use this parameter to only be notified for posts when they are by specified users. It should go without saying, but if multiple redditors are specified, there only needs to be a match for one to constitute a match. **NOTE:** The '/u/' or 'u/' prefixes for redditors will be stripped, so it doesn't matter if you include it or not.\n\n\
* ***-ignore-title*** --> Specified words or phrases to ignore in the title of the post. If any single word or phrase in this parameter is found in the title of the post, the post will be ignored.\n\n\
* ***-ignore-body*** --> Specified words or phrases to ignore in the body of the post. This could be used for selftexts ***OR*** links. If any single word or phrase in this parameter is found in the body of the post, the post will be ignored.\n\n\
* ***-ignore-redditors*** --> Use this parameter to ignore posts when they are by specified users. It should go without saying, but if multiple redditors are specified, there only needs to be a match for one in order to ignore the post. **NOTE:** The '/u/' or 'u/' prefixes for redditors will be stripped, so it doesn't matter if you include it or not.\n\n\
* ***-subreddit*** --> Specifies which subreddits to look in to match against the other parameters. Multiple subreddits can be specified, separated by a comma, and the bot will look in all of them. Although you can technically subscribe to /r/all, I wouldn't recommend it, because some posts will inevitably slip through the cracks. Also, it could hog the bots resources sending out messages to all the posts, so I may remove the ability to do this later depending on how it goes. ***NOTE:*** If no subreddit is specified here, /r/buildapcsales will be used by default, because that what the subreddit that gave this bot life to begin with. Also note that the '/r/' or 'r/' prefixes for subreddits will be stripped, so it doesn't matter if you include it or not.\n\n\
\
#### Flags\n\n\
* ***-nsfw*** --> By default, the bot will ignore posts that are marked as NSFW. Some subreddits use this tag to mark posts as expired and for other reasons. This tag will ***NOT*** ignore these posts.\n\n\
\
#### Unsubscribe\n\n\
There are 3 ways to unsubscribe from posts.\n\n\
* ***Unsubscribe All -*** Send the bot a message with the body as 'unsubscribe all' in order to stop being notified of any posts.\n\n\
* ***Unsubscribe by reply -*** Reply to an alert with 'unsubscribe' in order to remove that subscription.\n\n\
* ***Unsubscribe by subscription number -*** Send the bot a message with 'ubsubscribe {subscription #}' (where the brackets are the actual subscription number) in order to remove that subscription.\n\n\
\
#### Getting Help\n\n\
To get detailed information on how the bot works, send the bot a message with the subject or body as 'help'.\n\n\
\
#### Send feedback\n\n\
To send me feedback, send the bot a message with the subject as 'Feedback' and the body whatever you want, or empty. Another way is to have the subject be whatever you want, and the body be 'Feedback {Feedback message here}' where the brackets are replaced with your actual feedback message. Or, you can just message me directly at /u/tylerbrockett or post at /r/Alert_Bot. \n\n\
\
#### Reject message\n\n\
If you send a message that doesn't follow the above guidelines, you will get an error message from the bot saying the request wasn't recognized.\n\n\
\
#### Developer Info\n\n\
Developer Name: Tyler Brockett\n\n\
\
Bot Code: [Github Repository](https://github.com/tylerbrockett/Alert-Bot-Reddit)\n\n\
\
Bot Subreddit: [/r/Alert_Bot](https://reddit.com/r/Alert_Bot)\n\n\
\
Reddit: [/u/tylerbrockett](https://reddit.com/u/tylerbrockett)\n\n\
\
Email: tylerbrockett@gmail.com\n\n\
\
"

connection = None
reddit = None

subject = "Alert_Bot (formerly sales__bot for /r/buildapcsales) - message from developer"

select_users = []
errors = []

invalid_users = []


def compose_alert(username):
    # Insert alert message here!
    result = inbox.compose_greeting(username) + \
        NOTIFICATION
    return result


def run_alerts():
    global connection, reddit, select_users, errors
    # if selected_users is empty, send to all, otherwise just send to selected_users
    i = 0
    num = 0
    if not select_users:
        print('select users')
        needs_alert = connection.cursor().execute(database.GET_USERNAMES_THAT_NEED_ALERT).fetchall()
        num = len(needs_alert)
        for row in needs_alert:
            username = row[database.COL_ALERTS_USERNAME]
            entry = (username, 1)  # 1 == True
            try:
                reddit.send_message(username, subject, compose_alert(username))
                connection.cursor().execute(database.INSERT_ROW_ALERTS, entry)
                connection.commit()
                print('message sent to ' + username)
                i += 1
            except InvalidUser:
                invalid_users.append(username)
                print('Invalid User --> ' + username)
            except:
                errors.append(username)
                print("ALERT FAILED: " + username + "\n\t \n\t \n" + traceback.format_exc())
                connection.rollback()
                connection.close()
                exit()
    else:
        num = len(select_users)
        for username in select_users:
            try:
                reddit.send_message(username, subject, compose_alert(username))
                print('message sent to ' + username)
                i += 1
            except:
                errors.append(username)
                print("ALERT FAILED: " + username + "\n\t \n\t \n" + traceback.format_exc())
    print "Sent message to " + str(i) + "/" + str(num) + " users."
    if errors:
        print('\n\n' + str(len(errors)) + ' ERRORS: \n')
        for username in errors:
            print(str(username))

    print('\n\nInvalid Users')
    for user in invalid_users:
        print(user)


def open_database():
    global connection
    connection = sqlite3.connect(definitions.DB_LOCATION)
    cursor = connection.cursor()
    cursor.execute(database.CREATE_TABLE_SUBSCRIPTIONS)
    cursor.execute(database.CREATE_TABLE_MATCHES)
    cursor.execute(database.CREATE_TABLE_ALERTS)
    cursor.execute(database.CREATE_TABLE_ALL_MATCHES)
    cursor.execute(database.CREATE_TABLE_ALL_USERS)


def connect_to_reddit():
    global reddit
    # Connecting to Reddit
    user_agent = 'tylerbrockett - developer'
    reddit = praw.Reddit(user_agent=user_agent)
    # TODO - TAKE OUT DISABLE WARNING AND FIGURE OUT REPLACEMENT CODE
    reddit.login(accountinfo.developerusername, accountinfo.developerpassword, disable_warning=True)


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
    print(stacktrace)
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

