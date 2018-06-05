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

from utils import output, inbox
import traceback
from utils.logger import Logger
from utils.color import Color


class MatchHandler:

    @staticmethod
    def send_messages(reddit, database, matches):
        Logger.log('Handling matches...', Color.GREEN)
        for subscription, submission in matches:
            try:
                subs = database.get_subscriptions_by_user(subscription.username)
                message = reddit.get_message(subscription.message_id)
                message.reply(inbox.compose_match_message(subscription, submission, subs))
                database.insert_match(subscription.username, subscription.to_string(), submission.permalink)
                database.commit()
                output.match(subscription, submission)
            except:
                Logger.log(traceback.format_exc(), Color.RED)
                raise MatchHandlerException('handle_matches')


class MatchHandlerException(Exception):

    def __init__(self, error_args):
        Exception.__init__(self, 'MatchHandlerException: {0}'.format(error_args))
        self.errorArgs = error_args
