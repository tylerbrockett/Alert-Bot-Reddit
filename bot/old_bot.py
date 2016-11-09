"""
==========================================
Author:         Tyler Brockett
Description:    Reddit Bot - buildapcsales
Date:           11/13/2015
==========================================
"""

import os
import time
import praw
import sqlite3
import traceback
from sys import stdout

from utils import logger, times, database, inbox, output
from private import accountinfo

SLEEP_SECONDS = 45
NUM_POSTS_TO_CRAWL = 20
bot = accountinfo.username

connection = None
reddit = None
start_time = None


def run_bot():
    global start_time
    while True:
        try:
            read_inbox()
        except KeyboardInterrupt:
            logger.log('red', 'Interrupted')
            exit()
        except:
            handle_crash(traceback.format_exc())
        sleep(SLEEP_SECONDS)


def check_for_commands():
    global reddit, run

    unread_messages = []
    try:
        unread_messages = reddit.get_unread(limit=None)
    except:
        output.read_inbox_exception()
        reddit.send_message(accountinfo.developerusername, "Bot Exception - Read Inbox", traceback.format_exc())

    for unread_message in unread_messages:
        username, message_id, subject, body = \
            (str(unread_message.author).lower(),
             unread_message.id,
             inbox.format_subject(unread_message.subject.lower()),
             unread_message.body.lower())

        if username == accountinfo.developerusername:

            if subject == 'kill' or subject == 'stop' or subject == 'pause':
                run = False
                try:
                    unread_message.reply("Standing by for further instructions.")
                    unread_message.mark_as_read()
                    logger.log('red', '--------- Bot paused by developer ---------')
                except:
                    handle_crash(traceback.format_exc())
            if subject == 'run' or subject == 'start' or subject == 'resume':
                run = True
                try:
                    unread_message.reply("Thanks, I was getting bored!")
                    unread_message.mark_as_read()
                    logger.log('green', '--------- Bot resumed by developer ---------')
                except:
                    handle_crash(traceback.format_exc())

            if subject == 'test':
                logger.log('blue', '--------- I am being tested ---------')
                try:
                    if run:
                        unread_message.reply("Bot is active!")
                    else:
                        unread_message.reply("Bot is INACTIVE!")
                    unread_message.mark_as_read()
                except:
                    handle_crash(traceback.format_exc())


def crawl_subreddit(subreddit):
    global reddit
    submissions = []
    try:
        submissions = reddit.get_subreddit(subreddit).get_new(limit=NUM_POSTS_TO_CRAWL)
    except:
        output.get_submissions_exception()
        reddit.send_message(accountinfo.developerusername, "Bot Exception - Crawl Subreddit", traceback.format_exc())
    for submission in submissions:
        # Make sure sale is not expired!
        if not submission.over_18:
            check_for_subscription(submission)


def handle_item_match(username, item, message_id, title, permalink, url):
    global connection, reddit
    try:
        message = reddit.get_message(message_id)
        connection.cursor().execute(database.INSERT_ROW_MATCHES,
                                    (username, item, permalink, times.get_current_timestamp()))
        message.reply(inbox.compose_match_message(username, item, title, permalink, url))
        connection.commit()
        output.match(username, item, message_id, title, permalink, url)
    except:
        connection.rollback()
        output.match_exception(username, item, message_id, title, permalink, url)
        reddit.send_message(accountinfo.developerusername, "Bot Exception - Handle Item Match", traceback.format_exc())
    sleep(2)


def check_for_subscription(submission):
    global connection

    title = submission.title.lower()
    text = submission.selftext.lower()
    permalink = submission.permalink
    url = submission.url

    for item in connection.cursor().execute(database.SELECT_DISTINCT_ITEMS).fetchall():
        if item[0] in title or item[0] in text:
            matches = connection.cursor().execute(database.GET_SUBSCRIBED_USERS_WITHOUT_LINK,
                                                  (item[0], permalink)).fetchall()
            for match in matches:
                handle_item_match(match[database.COL_SUB_USERNAME],
                                  match[database.COL_SUB_ITEM],
                                  match[database.COL_SUB_MESSAGE_ID],
                                  title,
                                  permalink,
                                  url)


def read_inbox():
    global connection, reddit
    i = 0

    unread_messages = []
    try:
        unread_messages = reddit.get_unread(limit=None)
    except:
        output.read_inbox_exception()
        reddit.send_message(accountinfo.developerusername, "Bot Exception - Read Inbox", traceback.format_exc())

    for unread_message in unread_messages:
        i += 1
        username, message_id, subject, body = \
            (str(unread_message.author).lower(),
             unread_message.id,
             inbox.format_subject(unread_message.subject.lower()),
             unread_message.body.lower())

        if username == 'reddit':
            try:
                reddit.send_message(accountinfo.developerusername, "FORWARD: " + subject, body)
                unread_message.mark_as_read()
            except:
                handle_crash(traceback.format_exc())

        elif subject == 'statistics' or subject == 'stats':
            try:
                cursor = connection.cursor()

                cursor.execute(database.COUNT_USERS)
                users = len(cursor.fetchall())
                cursor.execute(database.COUNT_SUBSCRIPTIONS)
                subscriptions = len(cursor.fetchall())
                cursor.execute(database.COUNT_UNIQUE_SUBSCRIPTIONS)
                items = len(cursor.fetchall())
                cursor.execute(database.COUNT_MATCHES)
                matches = len(cursor.fetchall())

                output.statistics(username, users, subscriptions, items, matches)
                unread_message.reply(inbox.compose_statistics(username, users, subscriptions, items, matches))
                unread_message.mark_as_read()
            except:
                connection.rollback()
                output.subscribe_exception(username, subject)
                reddit.send_message(accountinfo.developerusername, "Bot Exception - Subscribe", traceback.format_exc())

        elif subject == 'subscriptions' or subject == 'subs':
            try:
                cursor = connection.cursor()
                cursor.execute(database.GET_SUBSCRIPTIONS_BY_USERNAME, (username,))
                unread_message.reply(inbox.compose_all_subscriptions_message(username, cursor.fetchall()))
                unread_message.mark_as_read()
                output.subscriptions(username)
            except:
                output.subscriptions_exception(username)
                reddit.send_message(accountinfo.developerusername, "Bot Exception - Subscriptions", traceback.format_exc())

        elif subject == 'username mention':
            output.username_mention(username, body)
            unread_message.mark_as_read()
            reddit.send_message(accountinfo.developerusername, "Bot - Username Mention", 'username: ' + username + '\n\n' + body)

        elif subject == 'post reply':
            output.post_reply(username, body)
            unread_message.mark_as_read()
            reddit.send_message(accountinfo.developerusername, "Bot - Post Reply", 'username: ' + username + '\n\n' + body)

        elif ('unsubscribe' in body and 'all' in body) \
                or ('unsubscribe' in subject and 'all' in subject):
            try:
                cursor = connection.cursor()
                cursor.execute(database.REMOVE_ALL_SUBSCRIPTIONS_BY_USERNAME, (username,))
                cursor.execute(database.REMOVE_ALL_MATCHES_BY_USERNAME, (username,))
                unread_message.reply(inbox.compose_unsubscribe_all_message(username))
                unread_message.mark_as_read()
                connection.commit()
                output.unsubscribe_all(username)
            except:
                connection.rollback()
                output.unsubscribe_all_exception(username)
                reddit.send_message(accountinfo.developerusername, "Bot Exception - Unsubscribe All", traceback.format_exc())

        elif body == 'unsubscribe' and subject.replace(' ', '') != '':
            try:
                cursor = connection.cursor()
                cursor.execute(database.REMOVE_ROW_SUBSCRIPTIONS, (username, subject))
                cursor.execute(database.REMOVE_MATCHES_BY_USERNAME_AND_SUBJECT, (username, subject))
                unread_message.reply(inbox.compose_unsubscribe_message(username, subject))
                unread_message.mark_as_read()
                connection.commit()
                output.unsubscribe(username, subject)
            except:
                connection.rollback()
                output.unsubscribe_exception(username, subject)
                reddit.send_message(accountinfo.developerusername, "Bot Exception - Unsubscribe", traceback.format_exc())

        # Item must be 1+ non-space characters.
        elif body == 'subscribe' and len(inbox.format_subject(subject).replace(' ', '')) > 0:
            subscription = (username, message_id, subject, times.get_current_timestamp())
            try:
                cursor = connection.cursor()
                cursor.execute(database.INSERT_ROW_SUBSCRIPTIONS, subscription)
                cursor = connection.cursor()
                cursor.execute(database.GET_SUBSCRIPTIONS_BY_USERNAME, (username,))
                unread_message.reply(inbox.compose_subscribe_message(username, subject, cursor.fetchall()))
                unread_message.mark_as_read()
                connection.commit()
                output.subscribe(username, subject)
            except sqlite3.IntegrityError:
                unread_message.mark_as_read()
                reddit.send_message(accountinfo.developerusername, "Bot Exception - IntegrityError", traceback.format_exc())
            except:
                connection.rollback()
                output.subscribe_exception(username, subject)
                reddit.send_message(accountinfo.developerusername, "Bot Exception - Subscribe", traceback.format_exc())

        elif subject == 'information' or subject == 'help':
            try:
                cursor = connection.cursor()
                cursor.execute(database.GET_SUBSCRIPTIONS_BY_USERNAME, (username,))
                unread_message.reply(inbox.compose_help_message(username, cursor.fetchall()))
                unread_message.mark_as_read()
                output.information(username)
            except:
                output.information_exception(username)
                reddit.send_message(accountinfo.developerusername, "Bot Exception - Information", traceback.format_exc())

        elif subject == 'feedback':
            try:
                reddit.send_message(accountinfo.developerusername, "Feedback for sales__bot",
                                    inbox.compose_feedback_forward(username, body))
                unread_message.reply(inbox.compose_feedback_message(username))
                unread_message.mark_as_read()
                output.feedback(username, body)
            except:
                output.feedback_exception(username, body)
                reddit.send_message(accountinfo.developerusername, "Bot Exception - Feedback", traceback.format_exc())
        else:
            try:
                unread_message.reply(inbox.compose_default_message(username, subject, body))
                unread_message.mark_as_read()
                output.default(username, subject, body)
            except:
                output.default_exception(username, subject, body)
                reddit.send_message(accountinfo.developerusername, "Bot Exception - Default", traceback.format_exc())
        sleep(2)
    logger.log('cyan', str(i) + ' UNREAD MESSAGES')


def open_database():
    global connection
    connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + database.DATABASE_LOCATION)
    cursor = connection.cursor()
    cursor.execute(database.CREATE_TABLE_SUBSCRIPTIONS)
    cursor.execute(database.CREATE_TABLE_MATCHES)
    cursor.execute(database.CREATE_TABLE_ALERTS)


def connect_to_reddit():
    global reddit
    # Connecting to Reddit
    user_agent = 'SALES__B0T - A Sales Notifier R0B0T'
    reddit = praw.Reddit(user_agent=user_agent)
    # TODO Use OAuth instead of this login method
    reddit.login(accountinfo.username, accountinfo.password, disable_warning=True)


def sleep(seconds):
    print 'Sleeping',
    for i in range(seconds):
        stdout.write(".")
        stdout.flush()
        time.sleep(1)
    print ''


def initialize():
    connect_to_reddit()
    open_database()


def destroy():
    global reddit, connection
    if connection:
        connection.close()
    connection = None
    reddit = None
    logger.log('red', '----------------- DESTROYED -----------------')


def handle_crash(stacktrace):
    global connection, reddit
    destroy()
    reset = False
    while not reset:
        try:
            initialize()
            reddit.send_message(accountinfo.developerusername, "Exception Handled", stacktrace)
            reset = True
        except:
            sleep(15)


__author__ = 'tyler'
if __name__ == "__main__":
    try:
        global start_time
        start_time = times.get_current_timestamp()
        initialize()
        run_bot()
    except KeyboardInterrupt:
        logger.log('red', 'Interrupted')
        exit()
    except:
        logger.log('red', traceback.format_exc())
        exit()

