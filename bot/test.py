from private import accountinfo
from parsing.subscription_parser import SubscriptionParser
from utils import inbox
import praw
from bot_modules.reddit_handler import RedditHandler
from bot_modules.database_handler import DatabaseHandler
from parsing.message_parser import MessageParser
from utils.subscription import Subscription
import json
from bot_modules.subscription_handler import SubscriptionHandler


class Message:
    def __init__(self, subject, body):
        self.subject = subject
        self.body = body


class Submission:
    def __init__(self, title, selftext, author, over_18):
        self.title = title
        self.selftext = selftext
        self.author = author
        self.over_18 = over_18


if __name__ == '__main__':
    submission = Submission(
        'i5',
        'bodytext! this is blah cool!',
        'tylerbrockett',
        True
    )
    m = Message(
        'Message1',
        'Subscribe -item i5,6500 -subreddit buildapcsales'
    )
    message = MessageParser(m)
    payload = message.get_payload()
    sub = Subscription(payload, 'tylerbrockett', '1')

    print(json.dumps(payload), 2)

    print('VALID: ' + str(message.data[MessageParser.KEY_VALID]))
    # is_match, mismatched_keys = SubscriptionHandler.is_match(sub, submission)
    # print('MATCH -- ' + str(is_match) + '\n\nMismatched Keys: ' + str(mismatched_keys))
