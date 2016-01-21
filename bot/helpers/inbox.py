from helpers import database
from private import accounts


def format_subject(s):
    temp = s.replace('re:', '')
    while len(temp) > 0 and temp[0] == ' ':
        temp = temp[1:]
    return temp


def compose_greeting(username):
    return "Hi " + username + ",\n\n"


def compose_signature(account):
    return "\n\t \n\t \n-" + account


def compose_salutation(account):
    result = compose_signature(account) + "\n\t \n\t \n" + \
             "[code](https://github.com/tylerbrockett/reddit-bot-buildapcsales)" + \
             " | /u/" + accounts.developer + \
             " | r/buildapcsales\n"
    return result


def compose_subscribe_message(account, username, item):
    result = compose_greeting(username) + \
             "Thanks for your subscription. " + \
             "You will continue to receive updates to part sales that contain '**" + item + "**' " + \
             "in its title. To unsubscribe, send me a message with the subject '**" + item + "**' " + \
             "and the message body '**unsubscribe**'." + \
             compose_salutation(account)
    return result


def format_subscriptions(subscriptions):
    result = ''
    if len(subscriptions) > 0:
        result += "###Subscriptions\n\n" + \
                  "\# | Item" + "\n" + \
                  "--:|:--:" + "\n"
        for i in range(len(subscriptions)):
            result = result + str(i + 1) + " | " + subscriptions[i][database.COL_SUB_ITEM] + "\n"
    else:
        result = "No subscriptions"
    return result


def compose_subscriptions_message(account, username, subscriptions):
    result = compose_greeting(username) + \
             "Below you will find your subscriptions.\n\t \n" + \
             format_subscriptions(subscriptions) + \
             compose_salutation(account)
    return result


def compose_information_message(account, username, subscriptions):
    result = compose_greeting(username) + \
             INFORMATION + "\n\t \n" + \
             format_subscriptions(subscriptions) + \
             compose_salutation(account)
    return result


def compose_unsubscribe_message(account, username, item):
    result = compose_greeting(username) + \
             "You have unsubscribed from the item '**" + item + "**'." + \
             " Thanks for using the bot!" + \
             compose_salutation(account)
    return result


def compose_unsubscribe_all_message(account, username):
    result = compose_greeting(username) + \
             "Sorry to see you go. Thanks for trying the bot though! I hope you'll try it again soon!" + \
             compose_salutation(account)
    return result


def compose_feedback_message(account, username):
    result = compose_greeting(username) + \
             "Thank you very much for your feedback! " + \
             "I am still a student, in the process of learning, but I am open to whatever " + \
             "requests the community makes. If your message is urgent, please feel free to " + \
             "PM me at /u/" + accounts.developer + ". Thanks again!" + \
             compose_salutation(account)
    return result


def compose_default_message(account, username, item, request):
    result = compose_greeting(username) + \
             "**There was an error processing your request.** Please review your message and " + \
             "make sure it follows the guidelines I have set. Please private message me " + \
             "with the subject 'Information' to get detailed information on how I work, " + \
             "or message me with tne subject line 'Help' if you want specialized help " + \
             "or have any questions for me. Thank you for your patience! \n\t \n\t \n" + \
             "**Your request:** \t \n" + \
             "**Subject:\t" + item + "**\t \n" + \
             "**Body:\t\t" + request + "**" + \
             compose_salutation(account)
    return result


def compose_match_message(account, username, item, title, permalink, url):
    result = compose_greeting(username) + \
             "We have found a match for your subscription to '**" + item + "**'! " + \
             "Below you will find the details:\n\t \n" + \
             "**Sale Title:**\t \n" + \
             title + "\t \n\t \n" + \
             "**Links:**\t \n" + \
             "[Reddit URL](" + permalink + ")" + "     |     " + \
             "[Sale URL](" + url + ")" + \
             compose_salutation(account)
    return result


def compose_feedback_forward(account, username, message):
    result = compose_greeting(accounts.developer) + \
             "You have received feedback from /u/" + username + ". The feedback is quoted below:\n\n'" + \
             message + "'" + compose_salutation(account)
    return result


INFORMATION = \
    "Thanks for your interest in the bot! This is how it work: \n\n" + \
    \
    "###Subscribing\n" + \
    "Send the bot a private message with the subject line as the exact string you " + \
    "want it to keep an eye out for, and the body as 'subscribe'. Keep it " + \
    "semi-general as to not limit its search too much. For example, use " + \
    "'i5-4590' instead of 'Intel Core i5-4590 3.3GHz LGA 1150'. \n\n" + \
    \
    "###What the bot will do\n" + \
    "The bot will send you a message that contains a link to that item each time " + \
    "it comes across a post in /r/buildapcsales that matches. It will be a reply " + \
    "to the original message you sent. This will happen until you send the bot a " + \
    "message unsubscribing from the item, which is described more in the next " + \
    "line. \n\n" + \
    \
    "###Unsubscribing\n" + \
    "If or when you want to unsubscribe, send the bot another private message with " + \
    "the subject line as the item you want to unsubscribe from, and the body as " + \
    "'unsubscribe'. If you want to unsubscribe from ALL of the parts you are " + \
    "subscribed to, make the subject or body of the pm 'unsubscribe all' \n\n" + \
    \
    "###Getting Help\n" + \
    "Remember that you can always send the bot a message with the subject line as " + \
    "'Information' or 'Help' to get this message, and all of the items you are " + \
    "subscribed to. If you want more specific help, send a private message to /u/" + \
    accounts.developer + " and I will try my absolute best to help you out.\n\n" + \
    \
    "###Feedback\n" + \
    "I am always open to feedback, requests, or things of that nature. While I am " + \
    "very much still in the process of learning, I will try my best to take your " + \
    "feedback into consideration. Sending me feedback should use the subject line " + \
    "'feedback'."
