"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

import traceback
from utils.logger import Logger
from utils.color import Color


def subscribe_exception(username, item):
    Logger.log(
        'subscribe exception caught\n' +
        'username:   ' + username + '\n' +
        'item:       ' + item + '\n' +
        'stacktrace: ' + '\n' +
        traceback.format_exc() + '\n\n',
        Color.RED)


def unsubscribe_all_exception(username):
    Logger.log(
        'unsubscribe all exception caught\n' +
        'username:   ' + username + '\n' +
        'stacktrace: ' + '\n' +
        traceback.format_exc() + '\n\n',
        Color.RED)


def unsubscribe_exception(username, item):
    Logger.log(
        'unsubscribe exception caught\n' +
        'username:   ' + username + '\n' +
        'item:       ' + item + '\n' +
        'stacktrace: ' + '\n' +
        traceback.format_exc() + '\n\n',
        Color.RED)


def default_exception(username, subject, body):
    Logger.log(
        'unsubscribe exception caught\n' +
        'username:   ' + username + '\n' +
        'subject:    ' + subject + '\n' +
        'body:       ' + body + '\n' +
        'stacktrace: ' + '\n' +
        traceback.format_exc() + '\n\n',
        Color.RED)


def information_exception(username):
    Logger.log(
        'information exception caught\n' +
        'username:   ' + username + '\n' +
        'stacktrace: ' + '\n' +
        traceback.format_exc() + '\n\n',
        Color.RED)


def subscriptions_exception(username):
    Logger.log(
        'subscriptions exception caught\n' +
        'username:   ' + username + '\n' +
        'stacktrace: ' + '\n' +
        traceback.format_exc() + '\n\n',
        Color.RED)


def feedback_exception(username, user_feedback):
    Logger.log(
        'feedback exception caught\n' +
        'username:   ' + username + '\n' +
        'feedback:   ' + '\n' + user_feedback + '\n' +
        'stacktrace: ' + '\n' +
        traceback.format_exc() + '\n\n',
        Color.RED)


def match_exception(username, item, message_id, title, permalink, url):
    Logger.log(
        'match exception caught\n' +
        'username:   ' + username + '\n' +
        'message id: ' + message_id + '\n' +
        'item:       ' + item + '\n' +
        'title:      ' + title + '\n' +
        'reddit url: ' + permalink + '\n' +
        'sale link:  ' + url + '\n' +
        'stacktrace:\n' + traceback.format_exc() + '\n\n',
        Color.RED)


def get_submissions_exception():
    Logger.log(
        'get submissions exception caught\n' +
        'stacktrace:\n' + traceback.format_exc() + '\n\n',
        Color.RED)


def read_inbox_exception():
    Logger.log(
        'read inbox exception caught\n' +
        'stacktrace:\n' + traceback.format_exc() + '\n\n',
        Color.RED)


def subscribe(username, item):
    Logger.log(
        '-------------------------------\n' +
        '           SUBSCRIBE\n' +
        'username: ' + username + '\n' +
        'item:     ' + item + '\n' +
        '-------------------------------\n\n',
        Color.GREEN)


def unsubscribe_all(username):
    Logger.log(
        '-------------------------------\n' +
        '         UNSUBSCRIBE ALL\n' +
        'username: ' + username + '\n' +
        '-------------------------------\n\n',
        Color.RED)


def unsubscribe(username, item):
    Logger.log(
        '-------------------------------\n' +
        '           UNSUBSCRIBE\n' +
        'username: ' + username + '\n' +
        'item:     ' + item + '\n' +
        '-------------------------------\n\n',
        Color.RED)


def information(username):
    Logger.log(
        '-------------------------------\n' +
        '         INFORMATION\n' +
        'username: ' + username + '\n' +
        '-------------------------------\n\n',
        Color.GREEN)


def subscriptions(username):
    Logger.log(
        '-------------------------------\n' +
        '         SUBSCRIPTIONS\n' +
        'username: ' + username + '\n' +
        '-------------------------------\n\n',
        Color.GREEN)


def feedback(username, user_feedback):
    Logger.log(
        '-------------------------------\n' +
        '            FEEDBACK\n' +
        'username: ' + username + '\n' +
        'feedback: ' + user_feedback + '\n' +
        '-------------------------------\n\n',
        Color.GREEN)


def default(username, subject, body):
    Logger.log(
        '-------------------------------\n' +
        '             DEFAULT\n' +
        'username: ' + username + '\n' +
        'subject:  ' + subject + '\n' +
        'body:     ' + body + '\n' +
        '-------------------------------\n\n',
        Color.YELLOW)


def match(subscription, submission):
    Logger.log(
        '-------------------------------\n' +
        '        SUBMISSION MATCH\n' +
        'username:   ' + subscription.username + '\n' +
        'message id: ' + subscription.message_id + '\n' +
        'item:       ' + subscription.to_string() + '\n' +
        'title:      ' + submission.title + '\n' +
        'Body:       ' + submission.selftext + '\n' +
        'URL:        ' + submission.url + '\n' +
        'reddit url: ' + submission.permalink + '\n' +
        '-------------------------------\n\n',
        Color.MAGENTA)


def statistics(username, users, subs, items, matches):
    Logger.log(
        '-------------------------------\n' +
        '        STATISTICS\n' +
        'username:      ' + username + '\n' +
        'user count:    ' + str(users) + '\n' +
        'subscriptions: ' + str(subs) + '\n' +
        'unique items:  ' + str(items) + '\n' +
        'matches:       ' + str(matches) + '\n' +
        '-------------------------------\n\n',
        Color.GREEN)


def username_mention(username, body):
    Logger.log(
        '-------------------------------\n' +
        '        USERNAME MENTION\n' +
        'username: ' + username + '\n' +
        'body:     ' + body + '\n' +
        '-------------------------------\n\n',
        Color.GREEN)


def post_reply(username, body):
    Logger.log(
        '-------------------------------\n' +
        '        POST REPLY\n' +
        'username: ' + username + '\n' +
        'body:     ' + body + '\n' +
        '-------------------------------\n\n',
        Color.GREEN)


def startup_message(bot_username):
    Logger.log(
        '================================================================\n' +
        '\t\tStarting /u/' + bot_username + '\n' +
        '================================================================\n',
        Color.GREEN)
