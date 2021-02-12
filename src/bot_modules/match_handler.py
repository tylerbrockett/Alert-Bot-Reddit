"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

from utils import output, inbox
import traceback
from utils.logger import Logger
from utils.color import Color
from bot_modules.crash_handler import handle_crash


class MatchHandler:

    @staticmethod
    def send_messages(reddit, database, matches):
        Logger.log('Handling matches...', Color.GREEN)
        index = 0
        for subscription, submission in matches:
            index += 1
            Logger.log('Handling match ' + str(index) + '/' + str(len(matches)), Color.BLUE)
            try:
                subs = database.get_subscriptions_by_user(subscription.username)
                message = reddit.get_message(subscription.message_id)
                message.reply(inbox.compose_match_message(subscription, submission, subs))
                database.insert_match(subscription.username, subscription.to_string(), submission.permalink)
                database.commit()
                output.match(subscription, submission)
            except Exception as e:
                if (hasattr(e, 'error_type') and e.error_type == 'INVALID_USER'):
                    Logger.log('Invalid User - ' + subscription.username, Color.RED)
                else:
                    handle_crash(traceback.format_exc(), message_dev=False, reddit=reddit, database=database)

class MatchHandlerException(Exception):

    def __init__(self, error_args):
        Exception.__init__(self, 'MatchHandlerException: {0}'.format(error_args))
        self.errorArgs = error_args
