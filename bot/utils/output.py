import traceback
from utils.logger import Logger
from utils.color import Color


def subscribe_exception(username, item):
    Logger.log(
        Color.RED,
        'subscribe exception caught\n' +
        "username:   " + username + "\n" +
        "item:       " + item + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def unsubscribe_all_exception(username):
    Logger.log(
        Color.RED,
        'unsubscribe all exception caught\n' +
        "username:   " + username + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def unsubscribe_exception(username, item):
    Logger.log(
        Color.RED,
        'unsubscribe exception caught\n' +
        "username:   " + username + "\n" +
        "item:       " + item + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def default_exception(username, subject, body):
    Logger.log(
        Color.RED,
        'unsubscribe exception caught\n' +
        "username:   " + username + "\n" +
        "subject:    " + subject + "\n" +
        "body:       " + body + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def information_exception(username):
    Logger.log(
        Color.RED,
        'information exception caught\n' +
        "username:   " + username + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def subscriptions_exception(username):
    Logger.log(
        Color.RED,
        'subscriptions exception caught\n' +
        "username:   " + username + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def feedback_exception(username, user_feedback):
    Logger.log(
        Color.RED,
        'feedback exception caught\n' +
        "username:   " + username + "\n" +
        "feedback:   " + "\n" + user_feedback + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def match_exception(username, item, message_id, title, permalink, url):
    Logger.log(
        Color.RED,
        "match exception caught\n" +
        "username:   " + username + "\n" +
        "message id: " + message_id + "\n" +
        "item:       " + item + "\n" +
        "title:      " + title + "\n" +
        "reddit url: " + permalink + "\n" +
        "sale link:  " + url + "\n" +
        "stacktrace:\n" + traceback.format_exc() + "\n\n")


def get_submissions_exception():
    Logger.log(
        Color.RED,
        "get submissions exception caught\n" +
        "stacktrace:\n" + traceback.format_exc() + "\n\n")


def read_inbox_exception():
    Logger.log(
        Color.RED,
        "read inbox exception caught\n" +
        "stacktrace:\n" + traceback.format_exc() + "\n\n")


def subscribe(username, item):
    Logger.log(
        Color.GREEN,
        '-------------------------------\n' +
        '           SUBSCRIBE\n' +
        'username: ' + username + "\n" +
        'item:     ' + item + "\n" +
        '-------------------------------\n\n')


def unsubscribe_all(username):
    Logger.log(
        Color.RED,
        '-------------------------------\n' +
        '         UNSUBSCRIBE ALL\n' +
        'username: ' + username + "\n" +
        '-------------------------------\n\n')


def unsubscribe(username, item):
    Logger.log(
        Color.RED,
        '-------------------------------\n' +
        '           UNSUBSCRIBE\n' +
        'username: ' + username + "\n" +
        'item:     ' + item + '\n' +
        '-------------------------------\n\n')


def information(username):
    Logger.log(
        Color.GREEN,
        '-------------------------------\n' +
        '         INFORMATION\n' +
        'username: ' + username + "\n" +
        '-------------------------------\n\n')


def subscriptions(username):
    Logger.log(
        Color.GREEN,
        '-------------------------------\n' +
        '         SUBSCRIPTIONS\n' +
        'username: ' + username + "\n" +
        '-------------------------------\n\n')


def feedback(username, user_feedback):
    Logger.log(
        Color.GREEN,
        '-------------------------------\n' +
        '            FEEDBACK\n' +
        'username: ' + username + "\n" +
        'feedback: ' + user_feedback + "\n" +
        '-------------------------------\n\n')


def default(username, subject, body):
    Logger.log(
        Color.YELLOW,
        '-------------------------------\n' +
        "             DEFAULT\n" +
        "username: " + username + "\n" +
        "subject:  " + subject + "\n" +
        "body:     " + body + "\n" +
        '-------------------------------\n\n')


def match(subscription, submission):
    Logger.log(
        Color.MAGENTA,
        "-------------------------------\n" +
        "        SUBMISSION MATCH\n" +
        "username:   " + subscription.username + "\n" +
        "message id: " + subscription.message_id + "\n" +
        "item:       " + subscription.to_string() + "\n" +
        "title:      " + submission.title + "\n" +
        "Body:       " + submission.selftext + "\n" +
        "reddit url: " + submission.permalink + "\n" +
        '-------------------------------\n\n')


def statistics(username, users, subscriptions, items, matches):
    Logger.log(
        Color.GREEN,
        "-------------------------------\n" +
        "        STATISTICS\n" +
        "username:      " + username + "\n" +
        "user count:    " + str(users) + "\n" +
        "subscriptions: " + str(subscriptions) + "\n" +
        "unique items:  " + str(items) + "\n" +
        "matches:       " + str(matches) + "\n" +
        '-------------------------------\n\n')


def username_mention(username, body):
    Logger.log(
        Color.GREEN,
        "-------------------------------\n" +
        "        USERNAME MENTION\n" +
        "username: " + username + "\n" +
        "body:     " + body + "\n" +
        "-------------------------------\n\n")


def post_reply(username, body):
    Logger.log(
        Color.GREEN,
        "-------------------------------\n" +
        "        POST REPLY\n" +
        "username: " + username + "\n" +
        "body:     " + body + "\n" +
        "-------------------------------\n\n")


def about_message():
    Logger.log(
        Color.YELLOW,
        "================================================================\n" +
        "\t\tSALES__BOT - A Sales Notifier Bot\n" +
        "================================================================\n\n")
    Logger.log(
        Color.BLUE,
        '\n--------------------------------------------------\n' +
        '\t\twww.reddit.com/r/buildapcsales' + '\n' +
        '--------------------------------------------------\n')
