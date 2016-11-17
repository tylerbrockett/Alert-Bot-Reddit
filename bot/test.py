from private import accountinfo
from parsing.subscription_parser import SubscriptionParser
from utils import inbox
import praw
from bot_modules.reddit_handler import RedditHandler
from bot_modules.database_handler import DatabaseHandler
from parsing.message_parser import MessageParser
from utils.subscription import Subscription
import json


class Message:
    def __init__(self, subject, body):
        self.subject = subject
        self.body = body

if __name__ == '__main__':
    m = Message(
        'Message1',
        "unsubscribe -item i5 6500k, 6700k -item 6700k, i5 6500k -item  bluetooth -body bodytext! -subreddit hardwareswap -nsfw -email -nsfw -email -subreddits /r/buildapcsales, r/hardwareswap -redditors u/tylerbrockett -ignore-title yaaaay, yooo -ignore-body yay -ignore-title test -ignore-redditors /u/tylerbrockett "
    )

    message = MessageParser(m)
    print(message.get_data())
    print(message.data[MessageParser.KEY_VALID])
    '''
    payload = message.get_payload()
    sub = Subscription(payload, 'tylerbrockett', '1')
    '''
