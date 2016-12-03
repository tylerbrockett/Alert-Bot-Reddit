"""
==========================================
Author:         Tyler Brockett
Description:    Reddit Bot - buildapcsales
Date:           11/13/2015
==========================================
"""

import time
import praw
import traceback
from sys import stdout

from utils import inbox
from utils.color import Color
from utils.logger import Logger
from accounts import accountinfo

reddit = None


def run_bot():
    global start_time
    while True:
        try:
            read_inbox()
        except KeyboardInterrupt:
            Logger.log('Interrupted', Color.RED)
            exit()
        except:
            handle_crash(traceback.format_exc())
        sleep(60)


def compose_message(username):
    ret = 'Hi /u/' + username + ',\n' \
        'There have been ***HUGE*** changes to the /r/buildapcsales bot. \n\t\n' \
        'First off, it has changed to /u/' + accountinfo.username + '\n\nUnfortunately, the new bot doesn\t have ' \
        'your old subscriptions. Subscriptions were tied to the message ID of your subscription message to the bot, ' \
        'and the new bot couldn\'t reply to the old bot\'s messages. This makes total sense now, but it hadn\'t ' \
        'occurred to me when I started this update. If you want to know your old subscriptions, let me know ' \
        '(/u/' + accountinfo.developerusername + ' and I can send them to you.\n\t \n' \
        'You should be able to use /u/' + accountinfo.username + ' exactly as you have been using /u/' + \
        accountinfo.old_username + ', but there have been MANY new features you may want to take note of. ' \
        '[Take a look here](https://github.com/tylerbrockett/Alert-Bot-Reddit/blob/master/README.md) \n\n'
    return ret


def read_inbox():
    global reddit
    i = 0

    unread_messages = []
    try:
        unread_messages = reddit.get_unread(limit=None)
    except:
        reddit.send_message(accountinfo.developerusername, "SALES__BOT Exception - Read Inbox", traceback.format_exc())

    for unread_message in unread_messages:
        username, message_id, subject, body = \
            (str(unread_message.author).lower(),
             unread_message.id,
             inbox.format_subject(unread_message.subject.lower()),
             unread_message.body.lower())
        Logger.log('message from ' + username)
        if subject == 'username mention':
            unread_message.mark_as_read()
            reddit.send_message(accountinfo.developerusername, "SALES__BOT - Username Mention", 'username: ' + username + '\n\n' + body)

        elif subject == 'post reply':
            unread_message.mark_as_read()
            reddit.send_message(accountinfo.developerusername, "SALES__BOT - Post Reply", 'username: ' + username + '\n\n' + body)
        else:
            try:
                Logger.log('sending message to ' + username)
                text = compose_message(username)
                Logger.log('TEXT: ' + text)
                unread_message.reply(text)
                Logger.log('message sent')
                unread_message.mark_as_read()
            except:
                Logger.log('message failed to send - ' + traceback.format_exc())
                reddit.send_message(accountinfo.developerusername, "SALES__BOT Exception - Default", traceback.format_exc())
        sleep(2)


def connect_to_reddit():
    global reddit
    # Connecting to Reddit
    user_agent = 'SALES__B0T - A Sales Notifier R0B0T'
    reddit = praw.Reddit(user_agent=user_agent)
    # TODO Use OAuth instead of this login method
    reddit.login(accountinfo.old_username, accountinfo.password, disable_warning=True)


def sleep(seconds):
    print 'Sleeping',
    for i in range(seconds):
        stdout.write(".")
        stdout.flush()
        time.sleep(1)
    print ''


def initialize():
    connect_to_reddit()


def destroy():
    global reddit
    reddit = None
    Logger.log('----------------- DESTROYED -----------------', Color.RED)


def handle_crash(stacktrace):
    global reddit
    destroy()
    reset = False
    while not reset:
        try:
            Logger.log('Trying to reset')
            initialize()
            reddit.send_message(accountinfo.bot_errors, "Exception Handled", stacktrace)
            reset = True
        except:
            sleep(15)


__author__ = 'tyler'
if __name__ == '__main__':
    global start_time
    try:
        initialize()
        run_bot()
    except KeyboardInterrupt:
        Logger.log('Interrupted', Color.RED)
        exit()
    except:
        Logger.log(traceback.format_exc(), Color.RED)
        exit()
