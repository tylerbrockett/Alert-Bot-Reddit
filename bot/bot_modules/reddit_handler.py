import praw
import traceback

from private import accountinfo


class RedditHandler:

    def __init__(self):
        self.reddit = self.connect()

    def connect(self):
        try:
            self.reddit = praw.Reddit(user_agent=accountinfo.user_agent)
            # TODO Use OAuth instead of this login method
            self.reddit.login(accountinfo.username, accountinfo.password, disable_warning=True)
            return self.reddit
        except:
            raise RedditHelperException('Error connecting to Reddit\n\n' + traceback.format_exc())

    def disconnect(self):
        self.reddit = None

    def reset(self):
        try:
            self.disconnect()
            self.reddit = self.connect()
        except:
            raise RedditHelperException(RedditHelperException.RESET_EXCEPTION + '\n\n' + traceback.format_exc())

    def get_unread(self):
        unread = self.reddit.get_unread(limit=None)
        return unread

    def send_message(self, redditor, subject, body):
        try:
            self.reddit.send_message(redditor, subject, body)
        except:
            raise RedditHelperException(RedditHelperException.SEND_MESSAGE_EXCEPTION)


class RedditHelperException(Exception):
    SEND_MESSAGE_EXCEPTION = 'Error sending message'
    RESET_EXCEPTION = 'Error resetting connection to Reddit'

    def __init__(self, error_args):
        Exception.__init__(self, "Reddit Exception: {0}".format(error_args))
        self.errorArgs = error_args
