from data import dbhelper
from private import accountinfo


class InboxHelper:
    def __init__(self):
        self.temp = -1

    def composeGreeting(self, username):
        return "Hi " + username + ",\n\n"

    def composeSubscribeMessage(self, username, item):
        result = self.composeGreeting(username) + \
            "Thanks for your subscription to '" + item + "'. " + \
            "You will continue to receive updates to part sales that contain that " + \
            "in its title until you send me a message with the subject as 'Unsubscribe' " + \
            "and the message body the same as the subscription message you sent to me." + \
            self.composeSalutation()
        return result

    def composeInformationMessage(self, username, subscriptions):
        result = self.composeGreeting(username) + \
            INFORMATION + "\n\n" + self.formatsubscriptions(subscriptions) + \
            self.composeSalutation()
        return result

    def formatsubscriptions(self, subscriptions):
        result = ''
        if len(subscriptions) > 0:
            result += "\n\n--------------------------\n" + \
                        "\tYour Subscription(s):\n"
            for item in subscriptions:
                result += "Item:\t\t" + item[dbhelper.COL_SUB_ITEM] + "\n"
            result += "\n\n--------------------------\n\n"
        return result

    def composeUnsubscribeMessage(self, username, item):
        result = self.composeGreeting(username) + \
            "You have unsubscribed from the item '" + item + "'." + \
            " Thanks for letting me help you!" + \
            self.composeSalutation()
        return result

    def composeUnsubscribeAllMessage(self, username):
        result = self.composeGreeting(username) + \
            "Sorry to see you go. Thanks for trying me though! I hope you'll be back soon!" + \
            self.composeSalutation()
        return result

    def composeFeedbackMessage(self, username):
        result = self.composeGreeting(username) + \
            "Thank you very much for your feedback, however nice or harsh it may be! " + \
            "I am still a student, in the process of learning, but I am open to whatever " + \
            "requests the community makes. If your message is urgent, please feel free to " + \
            "PM me at /u/XdrummerXboy or email me at the email address linked below. Thanks " + \
            "again!" + self.composeSalutation()
        return result

    def composeDefaultMessage(self, username, item, request):
        result = self.composeGreeting(username) + \
            "**There was an error processing your request.** Please review your message and " + \
            "make sure it follows the guidelines I have set. Please private message me " + \
            "with the subject 'Information' to get detailed information on how I work, " + \
            "or message me with tne subject line 'Help' if you want specialized help " + \
            "or have any questions for me. Thank you for your patience! \n\t \n\t \n" + \
            "**Your request:** \t \n" + \
            "Subject:\t" + item + "\t \n" + \
            "Body:\t\t" + request + \
            self.composeSalutation()
        return result

    def composeSalutation(self):
        result = SIGNATURE + "\n\t \n\t \n" + \
            "[Github Repository](https://github.com/tylerbrockett/reddit-bot-buildapcsales) | " + \
            accountinfo.developeremail + "\n"
        return result

    def composeMatchMessage(self, username, item, title, permalink, url):
        result = self.composeGreeting(username) + \
            "We have found a match for your subscription to '" + item + "'! " + \
            "Below you will find the details:\n\t \n " + \
            "**Sale Title:**\t \n" + \
            title + "\t \n" + \
            "[Reddit URL](" + permalink + ")" + "     |     " + \
            "[Sale URL](" + url + ")" + "\n\t \n\t \n" + \
            self.composeSalutation()
        return result

SIGNATURE = "\n\t \n\t \n-sales__bot"

INFORMATION = "Thanks for your interest in my abilities! This is how I work \n\n" + \
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
