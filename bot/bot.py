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
from helpers.exceptionhelper import ExceptionHelper

SLEEP_SECONDS = 5
subreddit = 'buildapcsales'
botname = accountinfo.username
subscriptions = []

db = None
cursor = None
file_helper = None
gmail_helper = None
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


def handle_part_match(username, part, title, url):
    colorhelper.printcolor(
        'magenta',
        "\n-------- SUBMISSION MATCH DETAILS ---------\n" \
        "USERNAME:\t\t" + username + "\n"   + \
        "PART:\t\t\t"   + part +     "\n"   + \
        "LINK:\t\t\t"   + url +     "\n\n")

    # TODO: SEND MESSAGE HERE

    cursor.execute(dbhelper.INSERT_ROW_MATCHES, (username, part, url))
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
        colorhelper.printcolor('magenta', 'APPENDED!!!!!!!!!!!!!')
    if len(subscriptions) == 0:
        colorhelper.printcolor('red', 'WHY ARE THERE NO SUBSCRIPTIONS?!?!')


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
            unread_message.reply('Sorry to see you go. Thanks for giving me a shot though!' +
                                 "\n\n-\nsales__bot")
        elif body == 'unsubscribe' and subject != '':
            cursor.execute(dbhelper.REMOVE_ROW_SUBSCRIPTIONS, (username, subject))
            db.commit()
            unread_message.reply("You have unsubscribed from the item '" + subject + "'. Thanks for using me!" +
                                 "\n\n-\nsales__bot")
        # Subject can't be empty, and must be longer than 2 non-space characters.
        elif body == 'subscribe' and subject.replace(' ', '') != '' and len(subject.replace(' ', '')) > 2:
            colorhelper.printcolor('green',
                                   '-------------------------------' +
                                   'New Subscription:\n' +
                                   'username: ' + username + "\n" +
                                   'message_id: ' + message_id + '\n' +
                                   'subject: ' + subject + '\n' +
                                   'body: ' + body + '\n' +
                                   '-------------------------------' +
                                   '\n\n\n')

            cursor.execute(dbhelper.INSERT_ROW_SUBMISSIONS, request)
            db.commit()
            unread_message.reply("Thanks for your subscription to '" + subject + "'. " +
                                 "You will continue to receive updates to part sales that contain that " +
                                 "in its title until you send me a message with the subject as 'Unsubscribe' " +
                                 "and the message body the same as the subscription message you sent to me." +
                                 "\n\n-\nsales__bot")
            unread_message.mark_as_read()

        elif subject == 'information':
            cursor.execute(dbhelper.GET_SUBSCRIPTIONS_BY_USERNAME, username)
            reply = "Thanks for your interest in my abilities! This is how I work \n\n" + \
                                \
                                 "SUBSCRIBING\n" + \
                                 "Send me a private message with the subject line as the exact string you " + \
                                 "want me to keep an eye out for, and the body as 'subscribe'. Keep it " + \
                                 "semi-general as to not limit my search too much. For example, use " + \
                                 "'i5-4590' instead of 'Intel Core i5-4590 3.3GHz LGA 1150'. \n\n" + \
                                \
                                 "WHAT I DO\n" + \
                                 "I will send you a message that contains a link to that item each time " + \
                                 "I come across a post in /r/buildapcsales that matches. It will be a reply " + \
                                 "to the original message you sent. This will happen until you send me a " + \
                                 "message unsubscribing from the part, which is described more in the next " + \
                                 "line. \n\n" + \
                                \
                                 "UNSUBSCRIBING\n" + \
                                 "If or when you want to unsubscribe, send me another private message with " + \
                                 "the subject line as the item you want to unsubscribe from, and the body as " + \
                                 "'Unsubscribe'. If you want to unsubscribe from ALL of the parts you are " + \
                                 "subscribed to, make the body of the pm 'unsubscribe all' and the subject line " + \
                                 "can be whatever four letter word you can think of. /s, kinda :D \n\n" + \
                                \
                                 "GETTING HELP\n" + \
                                 "Remember that you can always send me a message with the subject line as " + \
                                 "'Information' to get this message, and all of the parts you are subscribed to. " + \
                                 "If you want more specific help, send me a private message with the subject " + \
                                 "'Help' and the body as whatever you need help with and I will try my absolute " + \
                                 "best to keep up with my mail and help you out.\n\n" + \
                                \
                                 "FEEDBACK\n" + \
                                 "I am always open to feedback, requests, or things of that nature. While I am " + \
                                 "very much still in the process of learning, I will try my best to take your " + \
                                 "feedback into consideration. Sending me feedback should use the subject line " + \
                                 "'Feedback'."

            if len(cursor.fetchall()) > 0:
                reply += "\n\n--------------------------\n" \
                            "\tYour Subscription(s):\n"
                for item in cursor.fetchall():
                    reply += "Part:\t\t" + item[dbhelper.COL_SUB_ITEM] + "\n"
                reply += "\n\n--------------------------\n\n"

            reply += "\n\n-\nsales__bot"

            unread_message.reply(reply)

        elif subject == 'feedback':
            unread_message.reply("Hi " + username + ",\n\n" + \
                                 "Thank you very much for your feedback, however nice or harsh it may be! " + \
                                 "I am still a student, in the process of learning, but I am open to whatever " + \
                                 "requests the community makes. If your message is urgent, please feel free to " + \
                                 "PM me at /u/XdrummerXboy.\n\n Thanks again, \n" + botname)
        else:
            unread_message.reply("There was an error processing your request. Please review your message and " +
                                 "make sure it follows the guidelines I have set. Please private message me " +
                                 "with the subject 'Information' to get detailed information on how I work, " +
                                 "or message me with tne subject line 'Help' if you want specialized help " +
                                 "or have any questions for me. Thank you for your patience! \n\n" +

                                 "Your request: \n" +
                                 "Subject: " + subject + "\n" +
                                 "Body   : " + body +
                                 "\n\n-\nsales__bot")
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
    global exception_helper, file_helper, db, cursor
    exception_helper = ExceptionHelper()
    file_helper = FileHelper()
    # Setup process_id.pid
    file_helper.writeToFile(filehelper.PROCESS_ID, str(os.getpid()))
    gmail_helper = GmailHelper()
    connect_to_reddit()
    db = open_or_create_database()
    cursor = db.cursor()


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
