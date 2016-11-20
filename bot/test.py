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
    reddit = RedditHandler()
    invalid = reddit.check_invalid_subreddits(['sdfsdfsdfsdfsdfdsdfadas'])
    print(','.join(invalid))
