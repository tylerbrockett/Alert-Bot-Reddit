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

from data import dbhelper

SLEEP_SECONDS = 5
subreddit = 'buildapcsales'
botname = login.username
subscriptions = []
db = None
cursor = None


def main():
    initialize()
    while True:
        read_inbox()
        get_subscriptions()
        print colors.FORE_YELLOW + 'Starting to do work boss!' + colors.FORE_RESET
        crawl_subreddit(subreddit)
        sleep()


def crawl_subreddit(subreddit):
    submissions = r.get_subreddit(subreddit).get_new(limit=50)
    for submission in submissions:
        #print "\nTITLE\n", submission.title.lower(), "\nBODY\n", submission.selftext.lower()
        check_for_subscription(submission)


def handle_part_match(username, part, title, url):
    print colors.FORE_MAGENTA + \
        "\n-------- SUBMISSION MATCH DETAILS ---------\n" \
        "USERNAME:\t\t" + username + "\n"   + \
        "PART:\t\t\t"   + part +     "\n"   + \
        "LINK:\t\t\t"   + url +     "\n\n" + \
        colors.FORE_RESET

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
            print colors.FORE_RED + str(cursor.fetchall()) + colors.FORE_RESET
            if len(cursor.fetchall()) > 0:
                for match in cursor.fetchall():
                    handle_part_match(match[dbhelper.COL_SUB_USERNAME],
                                      match[dbhelper.COL_SUB_ITEM],
                                      title,
                                      url)
            else:
                print colors.FORE_RED + 'YOU SHOULD NOT SEE THIS EVER.' + colors.FORE_RESET
        else:
            print 'No matches for this submission'


def get_subscriptions():
    global subscriptions, db, cursor
    subscriptions = []
    cursor = db.cursor()
    cursor = db.execute(dbhelper.SELECT_DISTINCT_PARTS)
    for item in cursor.fetchall():
        subscriptions.append(item[0])
        print colors.FORE_MAGENTA + 'APPENDED!!!!!!!!!!!!!' + colors.FORE_RESET
    if len(subscriptions) == 0:
        print colors.FORE_RED + 'WHY ARE THERE NO SUBSCRIPTIONS?!?!' + colors.FORE_RESET


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
        elif body == 'unsubscribe' and body != '':
            cursor.execute(dbhelper.REMOVE_ROW_SUBSCRIPTIONS, (username, subject))
            db.commit()
            unread_message.reply("You have unsubscribed from the item '" + subject + "'. Thanks for using me!" +
                                 "\n\n-\nsales__bot")
        elif body == 'subscribe' and body != '' and body.replace(' ', '') != '':
            print colors.FORE_GREEN + \
                  '-------------------------------' + \
                    'New Subscription:\n' + \
                    'username: ' + username + "\n" + \
                    'message_id: ' + message_id + '\n' + \
                    'subject: ' + subject + '\n' + \
                    'body: ' + body + '\n' + \
                  '-------------------------------' + \
                  '\n\n\n' + \
                colors.FORE_RESET

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
    #print 'done.'


def open_or_create_database():
    conn = sqlite3.connect(dbhelper.DATABASE_LOCATION)
    conn.execute(dbhelper.CREATE_TABLE_SUBSCRIPTIONS)
    conn.execute(dbhelper.CREATE_TABLE_MATCHES)
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
        if i % 2 == 0:
            print "ZZzzZZzzZZzzZZzz"
        else:
            print "zzZZzzZZzzZZzzZZ"
        time.sleep(2)
    print 'Yaaaaaawn... That was a nice nap!\n\n' + colors.FORE_RESET


__author__ = 'tyler'
if __name__ == "__main__":
    main()
