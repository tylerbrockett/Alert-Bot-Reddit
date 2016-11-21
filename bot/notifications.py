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

from utils import database, logger
from utils import inbox
from private import accountinfo

connection = None
reddit = None

subject = "Alert_Bot (formerly sales__bot for buildapcsales) - message from developer"
signature = "\n\t \n\t \n-tylerbrockett"

select_users = ['XdrummerXboy']


def compose_alert(username):
    # Insert alert message here!
    result = inbox.compose_greeting(username) + \
        "I just wanted to inform the users of /u/sales__bot that there have been ***MASSIVE*** changes to the way " + \
        "the bot operates, and the features that it has. I essentially re-wrote the entire bot! Please read below " + \
        "to see the main changes." + \
        "\n\n" + \
        \
        "#ITS IN BETA AS /u/Alert_Bot_Beta\n" + \
        "Read about the name change below, but here's the deal... Since there have been so many changes to the " + \
        "bot, I want to start it off with a beta. The beta will be using /u/Alert_Bot_Beta. The actual new bot " + \
        "will go live sometime later, when it seems things are going smoothly. But I haven't decided whether or " + \
        "not I'd migrate the database from the beta to the official, but I'm leaning towards no, just in case " + \
        "there were some serious issues with the design of the bot, since this was such a big update. **So, starting " + \
        "today, please feel free to use the bot.** I will notify everyone once /u/Alert_Bot (non-beta) is up." + \
        "\n\n" + \
        \
        "#Name Change\n" + \
        "The bot has been changed to /u/Alert_Bot (only **one** underscore now), and there is " + \
        "now a subreddit dedicated to it, /r/Alert_Bot, which is a work in progress. Any help with how to configure " + \
        "the subreddit would be appreciated too!" + \
        "\n\n" + \
        \
        "#Format of messages to /u/Alert_Bot\n" + \
        "Now, instead of putting the item you want to subscribe to in the subject and the action in the body, it is " + \
        "now all inline in the body of the message with no need for the subject.\n" + \
        "Syntax Examples (body of message):\n" + \
        "subscribe 6700k\n" + \
        "subscribe intel 6700k" + \
        "\n\n" + \
        \
        "#Better matching\n" + \
        "Instead of searching for exact matches to an entire string (like 'ASUS MOTHERBOARD'), you can now specify " + \
        "a list of search terms separated by a comma. All the terms in the list need to be in the post in order to " + \
        "match, but the order does ***not*** matter. The example below will look for all motherboards made by Asus.\n" + \
        "Syntax Example:\n" + \
        "subscribe [CPU], 6700k" + \
        "\n\n" + \
        \
        "#Specify multiple items to subscribe to in one subscription\n" + \
        "You can use the item portion as it has been, or specify multiple '-item' parameters in order to watch " + \
        "for multiple items at the same time. This is handy (and more efficient for the bot) if all your items " + \
        "have the same other parameters, such as the same subreddits and terms to ignore. Each '-item' parameter " + \
        "will add another item to watch for.\n" + \
        "**Note:** If no items are specified, you will be notified of ALL posts within the specified subreddit. " + \
        "You can also specify 'all' for -item to be notified of all posts within the subreddit(s).\n" + \
        "Syntax Examples:\n" + \
        "subscribe -item 6700k -item 6500k\n" + \
        "subscribe 6700k -item 6500k          (equivalent to above)\n" + \
        "subscribe -item [CPU], 6700k -item [CPU], 6500k" + \
        "\n\n" + \
        \
        "#Specify items to ignore\n" + \
        "One of the things I noticed when using the bot was every so often I would get notifications for the wrong " + \
        "thing, because the term I was searching for was contained in another item. For example, I wanted a " + \
        "Fractal Define R5, so I subscribed to 'R5'. This wound up sending me a lot of posts about GPUs with " + \
        "GDD**R5** memory. This can be remedied using the '-ignore-item' parameter.\n" + \
        "subscribe -item r5 -ignore-item gddr5" + \
        "\n\n" + \
        \
        "#Specify subreddit(s) to search\n" + \
        "Yup. Now you can be notified about anything in ***ANY*** subreddit! If no subreddits are specified, it " + \
        "defaults to /r/buildapcsales. This means that you can now use regional buildapcsales subreddits such as " + \
        "/r/buildapcsalesuk. Another one some of you may be interested is /r/hardwareswap. Again, any subreddit " + \
        "should work though, even /r/all and /r/frontpage! (although given that /r/all has A LOT of posts, I can't " + \
        "guarantee the bot will be able to search through them all, sorry)\nHelp spread the word!\n" + \
        "**Note:** Multiple subreddits can be specified, separated by a comma.\n" + \
        "**Note:** It doesn't matter if '/r/' is included, the bot filters it out anyways.\n" + \
        "Syntax Example:\n" + \
        "subscribe 6700k -subreddit hardwareswap, buildapcsales" + \
        "\n\n" + \
        \
        "#Whitelist/Blacklist URLs and selftext" + \
        "This was by far the most highly requested feature. You can now filter posts by what the " + \
        "URL or Selftext contains. This means you can receive notifications for just amazon.com or ignore posts from " + \
        "amazon.co.uk, etc.\n" + \
        "**Note:** Multiple terms/URLs can be combined, separated by a comma\n\n" + \
        "Syntax Example:\n" + \
        "subscribe 6700k -url amazon.com\n" + \
        "subscribe 6700k -url amazon.com, jet.com\n" + \
        "subscribe 6700k -ignore-url amazon.com.uk" + \
        "\n\n" + \
        \
        "#Whitelist/Blacklist redditors\n" + \
        "Many users have also requested a bot for /r/hardwareswap, which got me thinking of their needs. I know " + \
        "there is quite a problem with scam accounts on that subreddit, so I figured adding this feature might be " + \
        "useful.\n" + \
        "**Note:** Multiple redditors can be specified, separated by a comma.\n" + \
        "**Note:** It doesn't matter if '/u/' is included, the bot filters it out anyways.\n" + \
        "Syntax Examples:\n" + \
        "subscribe 6700k -redditor tylerbrockett\n" + \
        "subscribe 6700k -ignore-redditors tylerbrockett" + \
        "\n\n" + \
        \
        "#Flags\n" + \
        "There is currently only one flag that is functional, which is '-nsfw'. When I originally developed the " + \
        "bot, there was no sense in notifying users for expired sales (denoted by the NSFW flag on Reddit). " + \
        "However, now that I am opening the bot up to all subreddits, I think it may be a good idea to leave that " + \
        "as an option. NSFW posts will be ***HIDDEN*** by default, and the '-nsfw' tag will include NSFW posts in " + \
        "the search. In the future, I wish to add an '-email' flag as well, in case users wish to be notified of " + \
        "posts by email as well. I will come up with an automated way to confirm the email belongs to users though. " + \
        "If I do include this feature in the future, I vow to never sell your email or make it public in any way. " + \
        "may encrypt the data as well if there is a lot of concern." + \
        "\n\n\n\n" + \
        \
        "Well... I believe that about sums up the changes. Sorry it has taken me so long to get these things " + \
        "implemented, as I know I have been promising them for quite some time. Graduating from school, having a " + \
        "family, moving, and starting a new job will kind of do that to you! If you have any questions or concerns " + \
        "about the bot, *please* let me know!" + \
        "\n\n" + \
        "Have a great day,\n"
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
                logger.log('blue', 'message sent to ' + username)
                i += 1
            except:
                logger.log('red', "ALERT FAILED: " + username + \
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
                logger.log('blue', 'message sent to ' + username)
                i += 1
            except:
                logger.log('red', "ALERT FAILED: " + username + \
                                  "\n\t \n\t \n" + traceback.format_exc())
            sleep(2)
    print "Sent message to " + str(i) + "/" + str(num) + " users."


def compose_salutation():
    result = signature + "\n\t \n\t \n" + \
             "[code](https://github.com/tylerbrockett/reddit-alert-bot)" + \
             " | /u/" + accountinfo.developerusername + "\n"
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
    logger.log('red', stacktrace)
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

