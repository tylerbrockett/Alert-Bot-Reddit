"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   11/28/2016
Version:            v2.0
==========================================
"""

import praw
import traceback
from private import accountinfo


class RedditHandler:

    def __init__(self):
        self.reddit = self.connect()
        self.NUM_POSTS = 20

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

    def get_message(self, message_id):
        return self.reddit.get_message(message_id)

    def send_message(self, redditor, subject, body):
        try:
            self.reddit.send_message(redditor, subject, body)
        except:
            raise RedditHelperException(RedditHelperException.SEND_MESSAGE_EXCEPTION)

    def get_submissions(self, subreddit):
        submissions = []
        posts = 200 if (subreddit == 'all') else self.NUM_POSTS
        try:
            submissions = self.reddit.get_subreddit(subreddit).get_new(limit=posts)
        except:
            raise RedditHelperException(RedditHelperException.GET_SUBMISSIONS_EXCEPTION)
        return submissions

    def get_original_message(self, received_message, database):
        message = received_message
        while message.parent_id and len(database.get_subscriptions_by_message_id(str(message.author), message.id)) == 0:
            message = self.reddit.get_message(message.parent_id)
        return message

    def check_invalid_subreddits(self, subreddits):
        invalid = []
        for subreddit in subreddits:
            try:
                self.reddit.get_subreddit(subreddit, fetch=True).get_new(limit=1)
            except praw.errors.InvalidSubreddit:
                invalid.append(subreddit)
        return invalid


class RedditHelperException(Exception):
    SEND_MESSAGE_EXCEPTION = 'Error sending message'
    RESET_EXCEPTION = 'Error resetting connection to Reddit'
    GET_SUBMISSIONS_EXCEPTION = 'Error getting submissions'

    def __init__(self, error_args):
        Exception.__init__(self, "Reddit Exception: {0}".format(error_args))
        self.errorArgs = error_args
