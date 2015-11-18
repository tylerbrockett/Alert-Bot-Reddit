"""
==========================================
Author:         Tyler Brockett
Description:    Reddit Bot - buildapcsales
Date:           11/13/2015
==========================================
"""

import sqlite3
import time

import praw
from private import login
from utils import colors

from data import database

SLEEP_SECONDS = 5
subreddit = 'buildapcsales'
subscriptions = []
db = None
cursor = None


def main():
    initialize()
    test_function()
    while True:
        read_inbox()
        print colors.FORE_YELLOW + 'Starting to do work boss!' + colors.FORE_RESET
        crawl_subreddit(subreddit)
        sleep()


def test_function():
    print 'TEST'
    read_inbox()
    print 'TEST COMPLETE'
    quit()


def crawl_subreddit(subreddit):
    submissions = r.get_subreddit(subreddit).get_new(limit=50)
    for submission in submissions:
        print "\nTITLE\n", submission.title.lower(), "\nBODY\n", submission.selftext.lower()
        check_for_subscription(submission)


def handle_part_match():
    print colors.FORE_MAGENTA + \
        "\n-------- SUBMISSION MATCH DETAILS ---------\n" + \
        colors.FORE_RESET


def check_for_subscription(submission):
    title = submission.title.lower()
    link = submission.selftext.lower()
    global db, cursor, subscriptions
    for part in subscriptions:
        if part in title:
            handle_part_match()

            '''
            SELECT *
            FROM SUBSCRIPTIONS, MATCHES
            WHERE PART = part and
            LINK != link

            SELECT *
            FROM SUBSCRIPTIONS
            WHERE PART = part and not
                (SELECT *
                 FROM MATCHES
                 WHERE LINK = link)
            '''


def get_subscriptions():
    global subscriptions, db, cursor
    subscriptions = []
    cursor = db.cursor()
    cursor = db.execute(database.SELECT_DISTINCT_PARTS)
    for item in cursor:
        subscriptions.append(item)


def read_inbox():
    global db, cursor
    cursor = db.cursor()
    for unread_message in r.get_unread(limit=None):
        # print unread_message
        username, message_id, subject, body = unread_message.id, unread_message.subject.lower(), unread_message.body.lower(), str(unread_message.author).lower()
        request = (message_id, subject, body)
        if subject is 'unsubscribe all':
            cursor.execute(database.REMOVE_ROW, message_id)
            db.commit()
            unread_message.reply('Sorry to see you go. Thanks for giving me a shot though!' +
                                 "\n\n-\nsales__bot")
        elif subject is 'unsubscribe' and body is not '':
            cursor.execute(database.REMOVE_ROW, (author, body))
            db.commit()
            unread_message.reply("You have unsubscribed from the part '" + body + "'. Thanks for using me!" +
                                 "\n\n-\nsales__bot")
        elif subject is 'subscribe' and body is not '':
            cursor.execute(database.INSERT_ROW, request)
            db.commit()
            unread_message.reply("Thanks for your subscription to '" + body + "'. " +
                                 "You will continue to receive updates to part sales that contain that " +
                                 "in its title until you send me a message with the subject as 'Unsubscribe' " +
                                 "and the message body the same as the subscription message you sent to me." +
                                 "\n\n-\nsales__bot")
        elif subject is 'information':
            cursor.execute(database.GET_REQUESTS_BY_USERNAME, author)
            unread_message.reply("Thanks for your interest in my abilities! This is how I work \n\n" +

                                 "SUBSCRIBING\n" +
                                 "Send me a private message with the subject line as 'subscribe' " +
                                 "and the body as the exact string you want me to keep an eye out for. " +
                                 "Keep it semi-general as to not limit my search too much. For example, " +
                                 "use 'i5-4590' instead of 'Intel Core i5-4590 3.3GHz LGA 1150'. \n\n" +

                                 "WHAT I DO\n" +
                                 "I will send you a message that contains a link to that item each time " +
                                 "I come across a post in /r/buildapcsales that matches. It will be a reply " +
                                 "to the original message you sent. This will happen until you send me a " +
                                 "message unsubscribing from the part. This is described more in the next " +
                                 "line. \n\n" +

                                 "UNSUBSCRIBING\n" +
                                 "If or when you want to unsubscribe, send me another private message with " +
                                 "the subject line 'Unsubscribe' and with the body of the message the string " +
                                 "of the part you are subscribed to. If you want to unsubscribe from ALL of " +
                                 "the parts you are subscribed to, make the subject of the pm 'unsubscribe all' " +
                                 "and the body can be whatever four letter word you can think of. /s, kinda :D " +
                                 "\n\n" +

                                 "GETTING HELP\n" +
                                 "Remember that you can always send me a message with the subject 'Information' " +
                                 "to get this message, and all of the parts you are subscribed to. If you " +
                                 "want more specific help, send me a private message with the subject 'Help' " +
                                 "and the body as whatever you need help with and I will try my absolute best " +
                                 "to keep up with my mail and help you out.\n\n" +

                                 "FEEDBACK\n" +
                                 "I am always open to feedback, requests, or things of that nature. While I am " +
                                 "very much still in the process of learning, I will try my best to take your " +
                                 "feedback into consideration. Sending me feedback should use the subject line " +
                                 "'Feedback'."
                                 "\n\n-\nsales__bot")
        else:
            unread_message.reply("There was an error processing your request. Please review your message and " +
                                 "make sure it follows the guidelines I have set. Please private message me " +
                                 "with the subject 'Information' to get detailed information on how I work, " +
                                 "or message me with tne subject line 'Help' if you want specialized help " +
                                 "or have any questions for me. Thank you for your patience!" +
                                 "\n\n-\nsales__bot")
        print 'inserted??'
    print 'done.'


def open_or_create_database():
    conn = sqlite3.connect(database.DATABASE_LOCATION)
    conn.execute(database.CREATE_TABLE_SUBSCRIPTIONS)
    conn.execute(database.CREATE_TABLE_MATCHES)
    return conn


def initialize():
    connect_to_reddit()
    print colors.FORE_YELLOW + \
        "================================================================\n" + \
        "\t\tSALES__BOT - A Sales Notifier Bot\n" + \
        "================================================================\n\n" + \
        colors.FORE_RESET

    global db, cursor
    db = open_or_create_database()
    cursor = db.cursor()
    print colors.FORE_BLUE + \
        '\n--------------------------------------------------\n' + \
        '\t\twww.reddit.com/r/' + str(subreddit) + '\n' + \
        '--------------------------------------------------\n' + \
        colors.FORE_RESET


def connect_to_reddit():
    # Connecting to Reddit
    user_agent = 'SALES__B0T - A Sales Notifier R0B0T'
    global r
    r = praw.Reddit(user_agent=user_agent)
    # TODO - TAKE OUT DISABLE WARNING AND FIGURE OUT REPLACEMENT CODE
    r.login(login.username, login.password, disable_warning=True)


def sleep():
    print "\n\n" + colors.FORE_YELLOW + "I'm exhausted, time to nap..."
    for i in range(0, SLEEP_SECONDS, 1):
        print ''
        if i % 2 == 0:
            print "ZZzzZZzzZZzzZZzz"
        else:
            print "zzZZzzZZzzZZzzZZ"
        time.sleep(2)
    print '\nYaaaaaawn... That was a nice nap!\n\n' + colors.FORE_RESET
