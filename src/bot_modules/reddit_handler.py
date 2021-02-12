"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   03/07/2020
Version:            v3.0
==========================================
"""

import praw
import traceback
from utils.logger import Logger
from utils.color import Color
from utils import output
from prawcore.exceptions import Redirect
from prawcore.exceptions import Forbidden
from prawcore.exceptions import NotFound


class RedditHandler:

    def __init__(self, credentials):
        output.startup_message(credentials)
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

    def get_instance(self):
        return self.reddit

    def get_unread(self):
        ret = []
        unread = self.reddit.inbox.unread(limit=None)
        for message in unread:
            ret.append(message)
        ret.reverse()
        return ret

    def get_message(self, message_id):
        Logger.log('Getting message: ' + message_id)
        return self.reddit.inbox.message(message_id)

    def send_message(self, redditor, subject, body):
        Logger.log('Sending message to: ' + redditor + ', subject: ' + subject)
        try:
            self.reddit.redditor(redditor).message(subject, body)
        except:
            Logger.log(traceback.format_exc(), Color.RED)
            raise RedditHelperException(RedditHelperException.SEND_MESSAGE_EXCEPTION)

    def get_submissions(self, subreddit, index, num_subs):
        submissions = []
        posts = 200 if (subreddit == 'all') else self.NUM_POSTS
        try:
            subs = self.reddit.subreddit(subreddit).new(limit=posts)
            for submission in subs:
                submissions.append(submission)
            Logger.log(Logger.aligntext(subreddit.lower(), 30) + '(' + str(index) + '/' + str(num_subs) + ')', Color.CYAN)
        except Forbidden as e:
            Logger.log(Logger.aligntext(subreddit.lower(), 30) + 'Forbidden (403)', Color.RED)
        except NotFound as e:
            Logger.log(Logger.aligntext(subreddit.lower(), 30) + 'NotFound (404)', Color.RED)
        except Exception as e:
            Logger.log(Logger.aligntext(subreddit.lower(), 30) + str(e), Color.RED)
        return submissions

    def get_original_message_id(self, received_message, database):
        Logger.log('Finding original message with subscription: ' + received_message.id)
        message = received_message
        while message.parent_id and len(database.get_subscriptions_by_message_id(str(message.author), message.id)) == 0:
            message = self.reddit.inbox.message(message.parent_id[3:])
        return message.id

    def check_invalid_subreddits(self, subreddits):
        invalid = []
        for subreddit in subreddits:
            try:
                for submission in self.reddit.subreddit(subreddit).new(limit=1):
                    print('subreddit is valid')
            except Redirect:  # was praw.errors.InvalidSubreddit without 'len()' around call in the try block
                Logger.log(traceback.format_exc(), Color.RED)
                invalid.append(subreddit)
        return invalid


class RedditHelperException(Exception):
    SEND_MESSAGE_EXCEPTION = 'Error sending message'
    RESET_EXCEPTION = 'Error resetting connection to Reddit'
    GET_SUBMISSIONS_EXCEPTION = 'Error getting submissions'

    def __init__(self, error_args):
        Exception.__init__(self, 'Reddit Exception: {0}'.format(error_args))
        self.errorArgs = error_args
