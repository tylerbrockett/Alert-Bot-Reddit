from utils import database
from private import accountinfo


def format_subject(s):
    print(s[:3].lower())
    while len(s) >= 3 and s[:3].lower() == 're:':
        s = s[3:]
    while len(s) > 0 and s[0] == ' ':
        s = s[1:]
    return s


def compose_greeting(username):
    return "Hi " + username + ",\n\n"


def compose_salutation():
    result = SIGNATURE + "\n\t \n\t \n" + \
             "[code](https://github.com/tylerbrockett/reddit-bot-buildapcsales)" + \
             " | /u/" + accountinfo.developerusername + \
             " | /r/buildapcsales\n"
    return result


def compose_subscribe_message(username, item, subscriptions):
    result = compose_greeting(username) + \
             "Thanks for your subscription. " + \
             "You will continue to receive updates to part sales that contain '" + item + "' " + \
             "in its title. To unsubscribe, send me a message with the subject '" + item + "' " + \
             "and the message body 'Unsubscribe'.\n\nAlternatively, you can reply to this " + \
             "message or any replies from the bot in regards to this subscription and reply with " + \
             "'Unsubscribe' as the body.\n\n" + \
             format_subscriptions(subscriptions) + \
             compose_salutation()
    return result


def compose_subscriptions_message(username, new_sub, all_subscriptions):
    result = compose_greeting(username) + \
             format_subscriptions(all_subscriptions) + \
             compose_salutation()
    return result


def compose_invalid_subscription_message(username, sub):
    result = compose_greeting(username) + \
             '**OH NO!** It seems like you\'re not speaking the bot\'s language! Below is the text ' + \
             'the bot is trying to understand. If you believe there has been an error, please PM ' + \
             '/u/' + accountinfo.developeremail + '. \n\n' + sub + \
             compose_salutation()
    return result


def compose_duplicate_subscription_message(username, existing, new):
    result = compose_greeting(username) + \
             'We think you alread have an existing subscription matching the criteria specified. Below ' + \
             'both subscriptions are listed. If you believe there has been a mistake, please PM me at ' + \
             '/u/' + accountinfo.developerusername + ' and let me know.\n\n' + \
             '###Existing\n' + \
             existing.to_string() + '\n\n' + \
             '###New\n' + \
             new.to_string() + '\n' + \
             compose_salutation()
    return result


# TODO Change this to use subscription objects
def format_subscriptions(subscriptions):
    result = ''
    if len(subscriptions) > 0:
        result += "###Subscriptions\n\n" + \
                  "\# | Item" + "\n" + \
                  "--:|:--:" + "\n"
        for i in range(len(subscriptions)):
            result = result + str(i + 1) + " | " + subscriptions[i][database.COL_SUB_ITEM] + "\n"
    return result


def compose_help_message(username, subscriptions):
    result = compose_greeting(username) + \
             INFORMATION + "\n\n" + format_subscriptions(subscriptions) + \
             compose_salutation()
    return result


def compose_unsubscribe_message(username, item):
    result = compose_greeting(username) + \
             "You have unsubscribed from the item '" + item + "'." + \
             " Thanks for letting me help you!" + \
             compose_salutation()
    return result


def compose_unsubscribe_all_message(username):
    result = compose_greeting(username) + \
             "Sorry to see you go. Thanks for trying me though! I hope you'll be back soon!" + \
             compose_salutation()
    return result


def compose_feedback_message(username):
    result = compose_greeting(username) + \
             "Thank you very much for your feedback! " + \
             "I am still a student, in the process of learning, but I am open to whatever " + \
             "requests the community makes. If your message is urgent, please feel free to " + \
             "PM me at /u/" + accountinfo.developerusername + " or email me at the email address " + \
             "linked below. Thanks again!" + \
             compose_salutation()
    return result


def compose_reject_message(username, subject, body):
    result = compose_greeting(username) + \
             "**There was an error processing your request.** Please review your message and " + \
             "make sure it follows the guidelines that have been set. Please private message the bot " + \
             "with the subject 'Information' to get detailed information on how the bot works, " + \
             "or message /u/tylerbrockett if you want specialized help or have any " + \
             "questions for me. Thank you for your patience! \n\t \n\t \n" + \
             "**Your request:** \t \n" + \
             "Subject:\t" + subject + "\t \n" + \
             "Body:\t\t" + body + \
             compose_salutation()
    return result


def compose_match_message(username, item, title, permalink, url):
    result = compose_greeting(username) + \
             "We have found a match for your subscription to '" + item + "'! " + \
             "Below you will find the details:\n\t \n\t \n" + \
             "**Sale Title:**\t \n" + \
             title + "\t \n\t \n" + \
             "**Links:**\t \n" + \
             "[Reddit URL](" + permalink + ")" + "     |     " + \
             "[Sale URL](" + url + ")" + \
             compose_salutation()
    return result


def compose_statistics(username, current_users, all_users, unique_subs, all_subs, unique_subreddits, all_matches):
    result = compose_greeting(username) + \
        '###Statistics\n' + \
        'Statistic|Value\n' + \
        '--:|:--:' + '\n' + \
        'Current Users Subscribed|' + str(current_users) + '\n' + \
        'Total Users|' + str(all_users) + '\n' + \
        'Unique Subscriptions|' + str(unique_subs) + '\n' + \
        'Active Subscriptions|' + str(all_subs) + '\n' + \
        'Unique Subreddits|' + str(unique_subreddits) + '\n' + \
        "Total Matches to Date|" + str(all_matches) + "\n\n\n" + \
        "Thank ***YOU*** for being a part of that!\n" + \
        compose_salutation()
    return result


def compose_feedback_forward(username, body):
    result = compose_greeting(accountinfo.developerusername) + \
             "You have received feedback from /u/" + username + ". The feedback is quoted below:\n\n'" + \
             body + "'" + compose_salutation()
    return result


def compose_username_mention_forward(username, body):
    result = compose_greeting(accountinfo.developerusername) + \
             'The bot has been mentioned in a post! the body of the message is quoted below:\n\n' + \
             'USERNAME: ' + username + '\nBODY:\n' + body
    return result


def compose_post_reply_forward(username, body):
    result = compose_greeting(accountinfo.developerusername) + \
             'Someone has responded to a post by the bot! the comment is quoted below:\n\n' + \
             'USERNAME: ' + username + '\nBODY:\n' + body
    return result


SIGNATURE = '\n\t \n\t \n-' + accountinfo.username

INFORMATION = \
    "Thanks for your interest in the bot! This is how it works: \n\n" + \
    \
    "###Subscribing\n" + \
    "Send the bot a private message with the subject line as the exact string you " + \
    "want it to keep an eye out for, and the body as 'subscribe'. Keep it " + \
    "semi-general as to not limit the search too much. For example, use " + \
    "'i5-4590' instead of 'Intel Core i5-4590 3.3GHz LGA 1150'. \n\n" + \
    \
    "###What the bot does\n" + \
    "The bot will send you a message that contains a link to that item each time " + \
    "it come across a post in /r/buildapcsales that matches. It will be a reply " + \
    "to the original message you sent. This will happen until you send the bot a " + \
    "message unsubscribing from the part, which is described more in the next " + \
    "line. \n\n" + \
    \
    "###Unsubscribing\n" + \
    "If or when you want to unsubscribe, send the bot another private message with " + \
    "the subject line as the item you want to unsubscribe from, and the body as " + \
    "'Unsubscribe'. If you want to unsubscribe from ALL of the parts you are " + \
    "subscribed to, make the body of the pm 'unsubscribe all' and the subject line " + \
    "can be whatever you want. \n\n" + \
    \
    "###Getting Help\n" + \
    "Remember that you can always send the bot a message with the subject line as " + \
    "'Information' or 'Help' to get this message, and all of the parts you are " + \
    "subscribed to. If you want more specific help, send a private message to /u/" + \
    accountinfo.developerusername + " and I will try my absolute best to help you out.\n\n" + \
    \
    "###Feedback\n" + \
    "I am always open to feedback, requests, or things of that nature. While I am " + \
    "very much still in the process of learning, I will try my best to take your " + \
    "feedback into consideration. Sending me feedback should use the subject line " + \
    "'Feedback'."
