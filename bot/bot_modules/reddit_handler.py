"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   12/2/2016
Version:            v2.0
==========================================
"""

import praw
import traceback


class RedditHandler:

    def __init__(self, credentials):
        self.credentials = credentials
        self.reddit = self.connect()
        self.NUM_POSTS = 20

    def connect(self):
        try:
            reddit = praw.Reddit(
                client_id=self.credentials['client_id'],
                client_secret=self.credentials['client_secret'],
                password=self.credentials['password'],
                user_agent=self.credentials['user_agent'],
                username=self.credentials['username'])
            return reddit
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
        Exception.__init__(self, 'Reddit Exception: {0}'.format(error_args))
        self.errorArgs = error_args
