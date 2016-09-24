import traceback
from helpers import color


def subscribe_exception(username, item):
    color.print_color(
        'red',
        'subscribe exception caught\n' +
        "username:   " + username + "\n" +
        "item:       " + item + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def unsubscribe_all_exception(username):
    color.print_color(
        'red',
        'unsubscribe all exception caught\n' +
        "username:   " + username + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def unsubscribe_exception(username, item):
    color.print_color(
        'red',
        'unsubscribe exception caught\n' +
        "username:   " + username + "\n" +
        "item:       " + item + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def default_exception(username, subject, body):
    color.print_color(
        'red',
        'unsubscribe exception caught\n' +
        "username:   " + username + "\n" +
        "subject:    " + subject + "\n" +
        "body:       " + body + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def information_exception(username):
    color.print_color(
        'red',
        'information exception caught\n' +
        "username:   " + username + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def feedback_exception(username, user_feedback):
    color.print_color(
        'red',
        'feedback exception caught\n' +
        "username:   " + username + "\n" +
        "feedback:   " + "\n" + user_feedback + "\n" +
        "stacktrace: " + "\n" +
        traceback.format_exc() + "\n\n")


def match_exception(username, item, message_id, title, permalink, url):
    color.print_color(
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
    color.print_color(
        'red',
        "get submissions exception caught\n" +
        "stacktrace:\n" + traceback.format_exc() + "\n\n")


def read_inbox_exception():
    color.print_color(
        'red',
        "read inbox exception caught\n" +
        "stacktrace:\n" + traceback.format_exc() + "\n\n")


def subscribe(username, item):
    color.print_color(
        'green',
        '-------------------------------\n' +
        '           SUBSCRIBE\n' +
        'username: ' + username + "\n" +
        'item:     ' + item + "\n" +
        '-------------------------------\n\n')


def unsubscribe_all(username):
    color.print_color(
        'red',
        '-------------------------------\n' +
        '         UNSUBSCRIBE ALL\n' +
        'username: ' + username + "\n" +
        '-------------------------------\n\n')


def unsubscribe(username, item):
    color.print_color(
        'red',
        '-------------------------------\n' +
        '           UNSUBSCRIBE\n' +
        'username: ' + username + "\n" +
        'item:     ' + item + '\n' +
        '-------------------------------\n\n')


def information(username):
    color.print_color(
        'green',
        '-------------------------------\n' +
        '         INFORMATION\n' +
        'username: ' + username + "\n" +
        '-------------------------------\n\n')


def feedback(username, user_feedback):
    color.print_color(
        'yellow',
        '-------------------------------\n' +
        '            FEEDBACK\n' +
        'username: ' + username + "\n" +
        'feedback: ' + user_feedback + "\n" +
        '-------------------------------\n\n')


def default(username, subject, body):
    color.print_color(
        'yellow',
        '-------------------------------\n' +
        "             DEFAULT\n" +
        "username: " + username + "\n" +
        "subject:  " + subject + "\n" +
        "body:     " + body + "\n" +
        '-------------------------------\n\n')


def match(username, item, message_id, title, permalink, url):
    color.print_color(
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
    color.print_color(
        'green',
        "-------------------------------\n" +
        "        SUBMISSION MATCH\n" +
        "username:      " + username + "\n" +
        "user count:    " + str(users) + "\n" +
        "subscriptions: " + str(subscriptions) + "\n" +
        "unique items:  " + str(items) + "\n" +
        "matches:       " + str(matches) + "\n" +
        '-------------------------------\n\n')


def username_mention(username, body):
    color.print_color(
        'green',
        "-------------------------------\n" +
        "        USERNAME MENTION\n" +
        "username: " + username + "\n" +
        "body:     " + body + "\n" +
        "-------------------------------\n\n")


def post_reply(username, body):
    color.print_color(
        'green',
        "-------------------------------\n" +
        "        POST REPLY\n" +
        "username: " + username + "\n" +
        "body:     " + body + "\n" +
        "-------------------------------\n\n")


def about_message():
    color.print_color(
        'yellow',
        "================================================================\n" +
        "\t\tSALES__BOT - A Sales Notifier Bot\n" +
        "================================================================\n\n")
    color.print_color(
        'blue',
        '\n--------------------------------------------------\n' +
        '\t\twww.reddit.com/r/buildapcsales' + '\n' +
        '--------------------------------------------------\n')
