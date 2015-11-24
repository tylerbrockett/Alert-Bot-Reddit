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
NUM_POSTS_TO_CRAWL = 100
subreddit = 'buildapcsales'
botname = accountinfo.username

db = None
cursor = None
file_helper = None
gmail_helper = None
inbox_helper = None
exception_helper = None
items = []


def run_bot():
    global items
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
        colorhelper.printcolor('yellow', 'Starting to do work boss!')
        items = db.execute(dbhelper.SELECT_DISTINCT_ITEMS).fetchall()
        crawl_subreddit(subreddit)
        sleep()


def crawl_subreddit(subreddit):
    global NUM_POSTS_TO_CRAWL
    submissions = r.get_subreddit(subreddit).get_new(limit=NUM_POSTS_TO_CRAWL)
    for submission in submissions:
        # Make sure sale is not expired!
        if not submission.over_18:
            check_for_subscription(submission)


def handle_item_match(username, item, message_id, title, permalink, url):
    colorhelper.printcolor(
        'magenta',
        "\n-------- SUBMISSION MATCH DETAILS ---------\n" \
        "USERNAME:\t\t" + username + "\n"   + \
        "MESSAGE ID:\t" + message_id + "\n" + \
        "ITEM:\t\t\t"   + item +     "\n"   + \
        "TITLE:\t\t"    + title +    "\n"   + \
        "REDDIT URL:\t" + permalink+ "\n"   + \
        "LINK:\t\t\t"   + url +     "\n\n")

    try:
        message = r.get_message(message_id)
        message.reply(inbox_helper.composeMatchMessage(username, item, title, permalink, url))
    except:
        colorhelper.printcolor('red', 'SEND MESSAGE FAILED')

    cursor.execute(dbhelper.INSERT_ROW_MATCHES, (username, item, url))


def check_for_subscription(submission):
    global db, cursor, items

    title = submission.title.lower()
    text = submission.selftext.lower()
    url = submission.url

    for item in items:
        if item[0] in title or item[0] in text:
            cursor = db.execute(dbhelper.GET_SUBSCRIBED_USERS_WITHOUT_LINK, (item[0], url))
            for match in cursor.fetchall():
                handle_item_match(match[dbhelper.COL_SUB_USERNAME],
                                  match[dbhelper.COL_SUB_ITEM],
                                  match[dbhelper.COL_SUB_MESSAGE_ID],
                                  title,
                                  submission.permalink,
                                  url)


def read_inbox():
    def formatsubject(subject):
        temp = subject.replace('re:', '')
        while len(temp) > 0 and temp[0] == ' ':
            temp = temp[1:]
        return temp

    global db, cursor
    i = 0
    for unread_message in r.get_unread(limit=None):
        i += 1
        # print unread_message
        username, message_id, subject, body = (str(unread_message.author).lower(), unread_message.id,
                                               formatsubject(unread_message.subject.lower()), unread_message.body.lower())
        request = (username, message_id, subject)

        if 'unsubscribe' in body and 'all' in body:
            cursor.execute(dbhelper.REMOVE_ALL_SUBSCRIPTIONS_BY_USERNAME, (username,))
            cursor.execute(dbhelper.REMOVE_ALL_MATCHES_BY_USERNAME, (username,))
            db.commit()
            unread_message.reply(inbox_helper.composeUnsubscribeAllMessage(username))

        elif body == 'unsubscribe' and subject.replace(' ', '') != '':
            cursor.execute(dbhelper.REMOVE_ROW_SUBSCRIPTIONS, (username, subject))
            cursor.execute(dbhelper.REMOVE_MATCHES_BY_USERNAME_AND_SUBJECT, (username, subject))
            db.commit()
            unread_message.reply(inbox_helper.composeUnsubscribeMessage(username, subject))

        # Subject must be longer than 2 non-space characters.
        elif body == 'subscribe' and len(formatsubject(subject).replace(' ', '')) > 2:
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
    colorhelper.printcolor('cyan', str(i) + ' UNREAD MESSAGES')


def open_or_create_database():
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


def handle_crash():
    stacktrace = exception_helper.getStacktrace()
    file_helper.eraseContents(filehelper.PROCESS_ID)
    file_helper.writeToFile(filehelper.STACKTRACE, stacktrace)
    db.close()
    exit()


__author__ = 'tyler'
if __name__ == "__main__":
    try:
        initialize()
        run_bot()
    except:
        handle_crash()
