import praw
import traceback

from private import accountinfo


class RedditHelper:
    def __init__(self):
        self.reddit = self.connect_to_reddit()

    def connect_to_reddit(self):
        try:
            user_agent = 'SALES__B0T - A Sales Notifier R0B0T'
            reddit = praw.Reddit(user_agent=user_agent)
            # TODO Use OAuth instead of this login method
            reddit.login(accountinfo.username, accountinfo.password, disable_warning=True)
            return reddit
        except:
            raise RedditHelperException('Error connecting to Reddit\n\n' + traceback.format_exc())

    def disconnect_from_reddit(self):
        self.reddit = None

    def reset(self):
        try:
            self.disconnect_from_reddit()
            self.reddit = self.connect_to_reddit()
        except:
            raise RedditHelperException('Error resetting connection to Reddit\n\n' + traceback.format_exc())


class RedditHelperException(Exception):
    def __init__(self, error_args):
        Exception.__init__(self, "Reddit Exception: {0}".format(error_args))
        self.errorArgs = error_args
