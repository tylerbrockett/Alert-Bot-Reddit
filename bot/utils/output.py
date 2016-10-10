import traceback
from utils import logger


def subscribe_exception(username, item):
    logger.log(
        'red',
        'subscribe exception caught\n' +
        "username:   " + username + "\n" +
        "item:       " + item + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def unsubscribe_all_exception(username):
    logger.log(
        'red',
        'unsubscribe all exception caught\n' +
        "username:   " + username + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def unsubscribe_exception(username, item):
    logger.log(
        'red',
        'unsubscribe exception caught\n' +
        "username:   " + username + "\n" +
        "item:       " + item + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def default_exception(username, subject, body):
    logger.log(
        'red',
        'unsubscribe exception caught\n' +
        "username:   " + username + "\n" +
        "subject:    " + subject + "\n" +
        "body:       " + body + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def information_exception(username):
    logger.log(
        'red',
        'information exception caught\n' +
        "username:   " + username + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def subscriptions_exception(username):
    logger.log(
        'red',
        'subscriptions exception caught\n' +
        "username:   " + username + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def feedback_exception(username, user_feedback):
    logger.log(
        'red',
        'feedback exception caught\n' +
        "username:   " + username + "\n" +
        "feedback:   " + "\n" + user_feedback + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def match_exception(username, item, message_id, title, permalink, url):
    logger.log(
        'red',
        "match exception caught\n" +
        "username:   " + username + "\n" +
        "message id: " + message_id + "\n" +
        "item:       " + item + "\n" +
        "title:      " + title + "\n" +
        "reddit url: " + permalink + "\n" +
        "sale link:  " + url + "\n" +
        "stacktrace:\n" + traceback.format_exc() + "\n\n")


def get_submissions_exception():
    logger.log(
        'red',
        "get submissions exception caught\n" +
        "stacktrace:\n" + traceback.format_exc() + "\n\n")


def read_inbox_exception():
    logger.log(
        'red',
        "read inbox exception caught\n" +
        "stacktrace:\n" + traceback.format_exc() + "\n\n")


def subscribe(username, item):
    logger.log(
        'green',
        '-------------------------------\n' +
        '           SUBSCRIBE\n' +
        'username: ' + username + "\n" +
        'item:     ' + item + "\n" +
        '-------------------------------\n\n')


def unsubscribe_all(username):
    logger.log(
        'red',
        '-------------------------------\n' +
        '         UNSUBSCRIBE ALL\n' +
        'username: ' + username + "\n" +
        '-------------------------------\n\n')


def unsubscribe(username, item):
    logger.log(
        'red',
        '-------------------------------\n' +
        '           UNSUBSCRIBE\n' +
        'username: ' + username + "\n" +
        'item:     ' + item + '\n' +
        '-------------------------------\n\n')


def information(username):
    logger.log(
        'green',
        '-------------------------------\n' +
        '         INFORMATION\n' +
        'username: ' + username + "\n" +
        '-------------------------------\n\n')


def subscriptions(username):
    logger.log(
        'green',
        '-------------------------------\n' +
        '         SUBSCRIPTIONS\n' +
        'username: ' + username + "\n" +
        '-------------------------------\n\n')


def feedback(username, user_feedback):
    logger.log(
        'yellow',
        '-------------------------------\n' +
        '            FEEDBACK\n' +
        'username: ' + username + "\n" +
        'feedback: ' + user_feedback + "\n" +
        '-------------------------------\n\n')


def default(username, subject, body):
    logger.log(
        'yellow',
        '-------------------------------\n' +
        "             DEFAULT\n" +
        "username: " + username + "\n" +
        "subject:  " + subject + "\n" +
        "body:     " + body + "\n" +
        '-------------------------------\n\n')


def match(username, item, message_id, title, permalink, url):
    logger.log(
        'magenta',
        "-------------------------------\n" +
        "        SUBMISSION MATCH\n" +
        "username:   " + username + "\n" +
        "message id: " + message_id + "\n" +
        "item:       " + item + "\n" +
        "title:      " + title + "\n" +
        "reddit url: " + permalink + "\n" +
        "sale link:  " + url + "\n" +
        '-------------------------------\n\n')


def statistics(username, users, subscriptions, items, matches):
    logger.log(
        'green',
        "-------------------------------\n" +
        "        STATISTICS\n" +
        "username:      " + username + "\n" +
        "user count:    " + str(users) + "\n" +
        "subscriptions: " + str(subscriptions) + "\n" +
        "unique items:  " + str(items) + "\n" +
        "matches:       " + str(matches) + "\n" +
        '-------------------------------\n\n')


def username_mention(username, body):
    logger.log(
        'green',
        "-------------------------------\n" +
        "        USERNAME MENTION\n" +
        "username: " + username + "\n" +
        "body:     " + body + "\n" +
        "-------------------------------\n\n")


def post_reply(username, body):
    logger.log(
        'green',
        "-------------------------------\n" +
        "        POST REPLY\n" +
        "username: " + username + "\n" +
        "body:     " + body + "\n" +
        "-------------------------------\n\n")


def about_message():
    logger.log(
        'yellow',
        "================================================================\n" +
        "\t\tSALES__BOT - A Sales Notifier Bot\n" +
        "================================================================\n\n")
    logger.log(
        'blue',
        '\n--------------------------------------------------\n' +
        '\t\twww.reddit.com/r/buildapcsales' + '\n' +
        '--------------------------------------------------\n')
