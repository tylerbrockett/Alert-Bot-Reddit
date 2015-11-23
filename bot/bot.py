"""
==========================================
Author:         Tyler Brockett
Description:    Reddit Bot - buildapcsales
Date:           11/13/2015
==========================================
"""

import os
import praw
import time
import sqlite3
from data import dbhelper
from helpers import filehelper
from helpers import colorhelper
from private import accountinfo
from helpers.filehelper import FileHelper
from helpers.gmailhelper import GmailHelper
from helpers.inboxhelper import InboxHelper
from helpers.exceptionhelper import ExceptionHelper

SLEEP_SECONDS = 5
subreddit = 'buildapcsales'
botname = accountinfo.username
subscriptions = []

db = None
cursor = None
file_helper = None
gmail_helper = None
inbox_helper = None
exception_helper = None

def run_bot():
    colorhelper.printcolor(
        'yellow',
        "================================================================\n" +
        "\t\tSALES__BOT - A Sales Notifier Bot\n" +
        "================================================================\n\n")

    colorhelper.printcolor(
        'blue',
        '\n--------------------------------------------------\n' +
        '\t\twww.reddit.com/r/' + str(subreddit) + '\n' +
        '--------------------------------------------------\n')

    while True:
        read_inbox()
        get_subscriptions()
        colorhelper.printcolor('yellow', 'Starting to do work boss!')
        crawl_subreddit(subreddit)
        sleep()


def crawl_subreddit(subreddit):
    submissions = r.get_subreddit(subreddit).get_new(limit=50)
    for submission in submissions:
        #print "\nTITLE\n", submission.title.lower(), "\nBODY\n", submission.selftext.lower()
        check_for_subscription(submission)


def handle_part_match(username, item, message_id, title, url):
    colorhelper.printcolor(
        'magenta',
        "\n-------- SUBMISSION MATCH DETAILS ---------\n" \
        "USERNAME:\t\t" + username + "\n"   + \
        "MESSAGE ID:\t" + message_id + "\n" + \
        "PART:\t\t\t"   + item +     "\n"   + \
        "TITLE:\t\t"    + title +    "\n"   + \
        "LINK:\t\t\t"   + url +     "\n\n")

    # TODO: SEND MESSAGE HERE

    cursor.execute(dbhelper.INSERT_ROW_MATCHES, (username, item, url))
    db.commit()


# TODO: I see the message 'you should not see this ever.' Fix it.
def check_for_subscription(submission):
    global db, cursor, subscriptions

    title = submission.title.lower()
    text = submission.selftext.lower()
    url = submission.url

    for item in subscriptions:
        if item in title:
            cursor = db.execute(dbhelper.GET_SUBSCRIBED_USERS_WITHOUT_LINK, (item, url))
            colorhelper.printcolor('red', str(cursor.fetchall()))
            if len(cursor.fetchall()) > 0:
                for match in cursor.fetchall():
                    handle_part_match(match[dbhelper.COL_SUB_USERNAME],
                                      match[dbhelper.COL_SUB_ITEM],
                                      match[dbhelper.COL_SUB_MESSAGE_ID],
                                      title,
                                      url)
            else:
                colorhelper.printcolor('red', 'YOU SHOULD NOT SEE THIS EVER.')
        else:
            print 'No matches for this submission'


def get_subscriptions():
    global subscriptions, db, cursor
    subscriptions = []
    cursor = db.cursor()
    cursor = db.execute(dbhelper.SELECT_DISTINCT_PARTS)
    for item in cursor.fetchall():
        subscriptions.append(item[0])
        colorhelper.printcolor('magenta', 'APPENDED ' + item)
    if len(subscriptions) == 0:
        colorhelper.printcolor('red', 'NO SUBSCRIPTIONS')


# TODO For some reason, it sends out many messages at once. WEIRD.
def read_inbox():
    global db, cursor
    cursor = db.cursor()
    for unread_message in r.get_unread(limit=None):
        # print unread_message
        username, message_id, subject, body = (str(unread_message.author).lower(), unread_message.id, unread_message.subject.lower(), unread_message.body.lower())
        request = (username, message_id, subject)
        if body == 'unsubscribe all':
            cursor.execute(dbhelper.REMOVE_ALL_SUBSCRIPTIONS_BY_USERNAME, username)
            cursor.execute(dbhelper.REMOVE_ALL_MATCHES_BY_USERNAME, username)
            db.commit()
            unread_message.reply(inbox_helper.composeUnsubscribeAllMessaage(username))

        elif body == 'unsubscribe' and subject != '':
            cursor.execute(dbhelper.REMOVE_ROW_SUBSCRIPTIONS, (username, subject))
            db.commit()
            unread_message.reply(inbox_helper.composeUnsubscribeMessage(username, subject))

        # Subject can't be empty, and must be longer than 2 non-space characters.
        elif body == 'subscribe' and subject.replace(' ', '') != '' and len(subject.replace(' ', '')) > 2:
            cursor.execute(dbhelper.INSERT_ROW_SUBMISSIONS, request)
            db.commit()
            colorhelper.printcolor('green',
                                   '-------------------------------\n' +
                                   'New Subscription:\n' +
                                   'username: ' + username + "\n" +
                                   'message_id: ' + message_id + '\n' +
                                   'subject: ' + subject + '\n' +
                                   'body: ' + body + '\n' +
                                   '-------------------------------' +
                                   '\n\n\n')
            unread_message.reply(inbox_helper.composeSubscribeMessage(username, subject))

        elif subject == 'information':
            cursor.execute(dbhelper.GET_SUBSCRIPTIONS_BY_USERNAME, username)
            unread_message.reply(inbox_helper.composeInformationMessage(username, cursor.fetchall()))

        elif subject == 'feedback':
            unread_message.reply(inbox_helper.composeFeedbackMessage(username))
        else:
            unread_message.reply(inbox_helper.composeDefaultMessage(username, subject, body))
        unread_message.mark_as_read()


def open_or_create_database():
    print dbhelper.DATABASE_LOCATION
    conn = sqlite3.connect(os.path.dirname(__file__) + dbhelper.DATABASE_LOCATION)
    conn.execute(dbhelper.CREATE_TABLE_SUBSCRIPTIONS)
    conn.execute(dbhelper.CREATE_TABLE_MATCHES)
    return conn


def connect_to_reddit():
    # Connecting to Reddit
    user_agent = 'SALES__B0T - A Sales Notifier R0B0T'
    global r
    r = praw.Reddit(user_agent=user_agent)
    # TODO - TAKE OUT DISABLE WARNING AND FIGURE OUT REPLACEMENT CODE
    r.login(accountinfo.username, accountinfo.password, disable_warning=True)


def sleep():
    colorhelper.printcolor('yellow', "\n\nI'm exhausted, time to nap...")
    for i in range(0, SLEEP_SECONDS, 1):
        if i % 2 == 0:
            colorhelper.printcolor('yellow', 'ZZzzZZzzZZzzZZzz')
        else:
            colorhelper.printcolor('yellow', 'zzZZzzZZzzZZzzZZ')
        time.sleep(2)
    colorhelper.printcolor('yellow', 'Yaaaaaawn... That was a nice nap!\n\n')


def initialize():
    global exception_helper, gmail_helper, inbox_helper, file_helper, db, cursor
    exception_helper = ExceptionHelper()
    file_helper = FileHelper()
    # Setup process_id.pid
    file_helper.writeToFile(filehelper.PROCESS_ID, str(os.getpid()))
    gmail_helper = GmailHelper()
    connect_to_reddit()
    db = open_or_create_database()
    cursor = db.cursor()
    inbox_helper = InboxHelper()


def crash():
    print 'Starting...'
    time.sleep(15)
    print 'Crashing...'
    a = [0,1,2,3,4]
    for i in range(0, len(a) + 5, 1):
        a[i] = i


def handle_crash():
    stacktrace = exception_helper.getStacktrace()
    file_helper.eraseContents(filehelper.PROCESS_ID)
    file_helper.writeToFile(filehelper.STACKTRACE, stacktrace)
    exit()


__author__ = 'tyler'
if __name__ == "__main__":
    try:
        initialize()
        crash()
        run_bot()
    except:
        handle_crash()
