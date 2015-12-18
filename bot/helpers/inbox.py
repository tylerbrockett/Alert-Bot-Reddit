from helpers import database
from private import accountinfo


def format_subject(s):
    temp = s.replace('re:', '')
    while len(temp) > 0 and temp[0] == ' ':
        temp = temp[1:]
    return temp


def compose_greeting(username):
    return "Hi " + username + ",\n\n"


def compose_salutation():
    result = SIGNATURE + "\n\t \n\t \n" + \
             "[Github Repository](https://github.com/tylerbrockett/reddit-bot-buildapcsales)" + \
             " | /u/" + accountinfo.developerusername + \
             " | " + accountinfo.developeremail + \
             " | r/buildapcsales\n"
    return result


def compose_subscribe_message(username, item):
    result = compose_greeting(username) + \
             "Thanks for your subscription. " + \
             "You will continue to receive updates to part sales that contain '" + item + "' " + \
             "in its title. To unsubscribe, send me a message with the subject '" + item + "' " + \
             "and the message body 'Unsubscribe'." + \
             compose_salutation()
    return result


def format_subscriptions(subscriptions):
    result = ''
    if len(subscriptions) > 0:
        if len(subscriptions) > 1:
            result += "###Subscriptions\n\n" + \
                      "\# | Item" + "\n" + \
                      "--:|:--:" + "\n"
        for i in range(len(subscriptions)):
            result = result + str(i + 1) + " | " + subscriptions[i][database.COL_SUB_ITEM] + "\n"
    return result


def compose_information_message(username, subscriptions):
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


def compose_default_message(username, item, request):
    result = compose_greeting(username) + \
             "**There was an error processing your request.** Please review your message and " + \
             "make sure it follows the guidelines I have set. Please private message me " + \
             "with the subject 'Information' to get detailed information on how I work, " + \
             "or message me with tne subject line 'Help' if you want specialized help " + \
             "or have any questions for me. Thank you for your patience! \n\t \n\t \n" + \
             "**Your request:** \t \n" + \
             "Subject:\t" + item + "\t \n" + \
             "Body:\t\t" + request + \
             compose_salutation()
    return result


def compose_match_message(username, item, title, permalink, url):
    result = compose_greeting(username) + \
             "We have found a match for your subscription to '" + item + "'! " + \
             "Below you will find the details:\n\t \n " + \
             "**Sale Title:**\t \n" + \
             title + "\t \n" + \
             "[Reddit URL](" + permalink + ")" + "     |     " + \
             "[Sale URL](" + url + ")" + "\n\t \n\t \n" + \
             compose_salutation()
    return result


def compose_feedback_forward(username, message):
    result = compose_greeting(accountinfo.developerusername) + \
             "You have received feedback from /u/" + username + ". The feedback is quoted below:\n\n'" + \
             message + "'" + compose_salutation()
    return result


SIGNATURE = "\n\t \n\t \n-sales__bot"

INFORMATION = \
    "Thanks for your interest in my abilities! This is how I work: \n\n" + \
    \
    "###Subscribing\n" + \
    "Send me a private message with the subject line as the exact string you " + \
    "want me to keep an eye out for, and the body as 'subscribe'. Keep it " + \
    "semi-general as to not limit my search too much. For example, use " + \
    "'i5-4590' instead of 'Intel Core i5-4590 3.3GHz LGA 1150'. \n\n" + \
    \
    "###What I do\n" + \
    "I will send you a message that contains a link to that item each time " + \
    "I come across a post in /r/buildapcsales that matches. It will be a reply " + \
    "to the original message you sent. This will happen until you send me a " + \
    "message unsubscribing from the part, which is described more in the next " + \
    "line. \n\n" + \
    \
    "###Unsubscribing\n" + \
    "If or when you want to unsubscribe, send me another private message with " + \
    "the subject line as the item you want to unsubscribe from, and the body as " + \
    "'Unsubscribe'. If you want to unsubscribe from ALL of the parts you are " + \
    "subscribed to, make the body of the pm 'unsubscribe all' and the subject line " + \
    "can be whatever you want. \n\n" + \
    \
    "###Getting Help\n" + \
    "Remember that you can always send me a message with the subject line as " + \
    "'Information' or 'Help' to get this message, and all of the parts you are " + \
    "subscribed to. If you want more specific help, send a private message to /u/" + \
    accountinfo.developerusername + " and I will try my absolute best to help you out.\n\n" + \
    \
    "###Feedback\n" + \
    "I am always open to feedback, requests, or things of that nature. While I am " + \
    "very much still in the process of learning, I will try my best to take your " + \
    "feedback into consideration. Sending me feedback should use the subject line " + \
    "'Feedback'."
