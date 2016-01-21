from helpers.colorize import colorize
from helpers import times
import traceback


'''
============================================================
                USER INTERACTION
============================================================
'''


def subscribe(username, item):
    colorize("green",
             '-------------------------------\n' +
             '           SUBSCRIBE\n' +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             'username:  ' + username + '\n' +
             'item:      ' + item + '\n' +
             '-------------------------------')


def unsubscribe_all(username):
    colorize("red",
             '-------------------------------\n' +
             '         UNSUBSCRIBE ALL\n' +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             'username:  ' + username + '\n' +
             '-------------------------------')


def unsubscribe(username, item):
    colorize("red",
             '-------------------------------\n' +
             '           UNSUBSCRIBE\n' +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             'username:  ' + username + '\n' +
             'item:      ' + item + '\n' +
             '-------------------------------')


def information(username):
    colorize("green",
             '-------------------------------\n' +
             '         INFORMATION\n' +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             'username:  ' + username + '\n' +
             '-------------------------------')


def subscriptions(username):
    colorize("green",
             "-------------------------------\n" +
             "        SUBSCRIPTIONS\n" +
             "timestamp: " + times.get_formatted_time() + "\n" +
             "username:  " + username + "\n" +
             "-------------------------------")


def feedback(username, user_feedback):
    colorize("green",
             '-------------------------------\n' +
             '            FEEDBACK\n' +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             'username:  ' + username + '\n' +
             'feedback:  ' + user_feedback + '\n' +
             '-------------------------------\n')


def default(username, subject, body):
    colorize("yellow",
             '-------------------------------\n' +
             '             DEFAULT\n' +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             'username:  ' + username + '\n' +
             'subject:   ' + subject + '\n' +
             'body:      ' + body + '\n' +
             '-------------------------------\n')


def match(username, item, message_id, title, permalink, url):
    colorize("magenta",
             '-------------------------------\n' +
             '        SUBMISSION MATCH\n' +
             'timestamp:  ' + times.get_formatted_time() + "\n" +
             'username:   ' + username + '\n' +
             'message id: ' + message_id + '\n' +
             'item:       ' + item + '\n' +
             'title:      ' + title + '\n' +
             'reddit url: ' + permalink + '\n' +
             'sale link:  ' + url + '\n' +
             '-------------------------------\n')


'''
============================================================
                EXCEPTIONS
============================================================
'''


def subscribe_exception(username, item):
    colorize('red',
             'subscribe exception caught\n' +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             "username:   " + username + "\n" +
             "item:       " + item + "\n" +
             "stacktrace: " + "\n" + traceback.format_exc())


def unsubscribe_all_exception(username):
    colorize('red',
             'unsubscribe all exception caught\n' +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             "username:   " + username + "\n" +
             "stacktrace: " + "\n" + traceback.format_exc())


def unsubscribe_exception(username, item):
    colorize('red',
             'unsubscribe exception caught\n' +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             "username:   " + username + "\n" +
             "item:       " + item + "\n" +
             "stacktrace: " + "\n" + traceback.format_exc())


def default_exception(username, subject, body):
    colorize('red',
             'unsubscribe exception caught\n' +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             "username:   " + username + "\n" +
             "subject:    " + subject + "\n" +
             "body:       " + body + "\n" +
             "stacktrace: " + "\n" + traceback.format_exc())


def information_exception(username):
    colorize('red',
             'information exception caught\n' +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             "username:   " + username + "\n" +
             "stacktrace: " + "\n" + traceback.format_exc())


def subscriptions_exception(username):
    colorize('red',
             'subscriptions exception caught\n' +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             "username:   " + username + "\n" +
             "stacktrace: " + "\n" + traceback.format_exc())


def feedback_exception(username, user_feedback):
    colorize('red',
             'feedback exception caught\n' +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             "username:   " + username + "\n" +
             "feedback:   " + "\n" + user_feedback + "\n" +
             "stacktrace: " + "\n" + traceback.format_exc())


def match_exception(username, item, message_id, title, permalink, url):
    colorize('red',
             "match exception caught\n" +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             "username:   " + username + "\n" +
             "message id: " + message_id + "\n" +
             "item:       " + item + "\n" +
             "title:      " + title + "\n" +
             "reddit url: " + permalink + "\n" +
             "sale link:  " + url + "\n" +
             "stacktrace:\n" + traceback.format_exc())


def get_submissions_exception():
    colorize('red',
             "get submissions exception caught\n" +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             "stacktrace:\n" + traceback.format_exc())


def read_inbox_exception():
    colorize('red',
             "read inbox exception caught\n" +
             'timestamp: ' + times.get_formatted_time() + "\n" +
             "stacktrace:\n" + traceback.format_exc())


'''
============================================================
                OTHER
============================================================
'''


def interrupted():
    colorize('red',
             "Interrupted")
