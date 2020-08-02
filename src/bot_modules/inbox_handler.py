"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

from utils import inbox, times
from bot_modules.sleep_handler import SleepHandler
from bot_modules.database_handler import DatabaseHandlerException
from utils.logger import Logger
from utils.color import Color
from utils.env import env, DEV_USERNAME
from utils.subscription import Subscription
from parsing.message_parser import MessageParser
from parsing.message_lexer import MessageLexer
import json
import traceback


class InboxHandler:

    @staticmethod
    def reply(message, response):
        Logger.log('Replying to message: ' + message.id)
        message.reply(response[0: min(len(response), 10000)])

    @staticmethod
    def handle_message_from_reddit(reddit, message):
        Logger.log('Message from reddit')
        reddit.send_message(env(DEV_USERNAME), 'FWD: ' + message.subject, message.body)
        message.mark_read()

    @staticmethod
    def handle_statistics_message(database, message):
        Logger.log('Stats message')
        formatted_message = inbox.compose_statistics(
            str(message.author),
            database.count_current_users(),
            database.count_all_users(),
            database.count_unique_subscriptions(),
            database.count_all_subscriptions(),
            len(database.get_unique_subreddits()),
            database.count_total_matches(),
            database.get_unique_subreddits())
        InboxHandler.reply(message, formatted_message)
        message.mark_read()

    @staticmethod
    def handle_get_subscriptions_message(database, message):
        Logger.log('Get subs message')
        subscriptions = database.get_subscriptions_by_user(str(message.author))
        formatted_message = inbox.compose_all_subscriptions_message(str(message.author), subscriptions)
        InboxHandler.reply(message, formatted_message)
        message.mark_read()

    @staticmethod
    def handle_subscription_message(database, reddit, message, payload):
        Logger.log('Sub message')
        new_sub = Subscription(payload, str(message.author), message.id)
        existing_subs = database.get_subscriptions_by_user(str(message.author))
        duplicate_subs = new_sub.check_against_existing(existing_subs)
        if duplicate_subs:
            Logger.log('Subscription already exists', Color.RED)
            InboxHandler.reply(message, inbox.compose_duplicate_subscription_message(
                str(message.author),
                duplicate_subs[0],
                new_sub))
            message.mark_read()
            return
        invalid_subreddits = reddit.check_invalid_subreddits(new_sub.data[Subscription.SUBREDDITS])
        if invalid_subreddits:
            Logger.log('Subreddit(s) invalid: ' + str(invalid_subreddits), Color.RED)
            InboxHandler.reply(message, inbox.compose_invalid_subreddit_message(str(message.author), invalid_subreddits, message))
            message.mark_read()
            return
        database.insert_subscription(str(message.author), new_sub.message_id, new_sub.to_string(),
                                     times.get_current_timestamp())
        existing_subs.append(new_sub)
        # TODO Remove subreddit not specified stuff, taken care of in SubscriptionParser.py
        subreddit_not_specified = len(new_sub.data[Subscription.SUBREDDITS]) == 0
        InboxHandler.reply(message,
            inbox.compose_subscribe_message(str(message.author), new_sub, existing_subs, subreddit_not_specified))
        database.commit()
        message.mark_read()

    @staticmethod
    def handle_unsubscribe_message(reddit, database, message):
        Logger.log('Unsub message')
        parent_m_id = reddit.get_original_message_id(message, database)
        removed_subs = database.remove_subscriptions_by_message_id(str(message.author), parent_m_id)
        subs = database.get_subscriptions_by_user(str(message.author))
        if len(removed_subs) > 0:
            InboxHandler.reply(message, inbox.compose_unsubscribe_message(str(message.author), removed_subs, subs))
        else:
            InboxHandler.reply(message, inbox.compose_unsubscribe_invalid_sub_message(str(message.author), subs))
        message.mark_read()

    @staticmethod
    def handle_unsubscribe_from_num_message(database, message, payload):
        Logger.log('Unsub from num')
        removed = database.remove_subscription_by_number(str(message.author), int(payload))
        subs = database.get_subscriptions_by_user(str(message.author))
        if removed:
            InboxHandler.reply(message, inbox.compose_unsubscribe_from_num_message(str(message.author), removed, subs))
        else:
            InboxHandler.reply(message, inbox.compose_unsubscribe_invalid_sub_message(str(message.author), subs))
        message.mark_read()

    @staticmethod
    def handle_edit_message(database, message, payload):
        Logger.log('Edit message')
        InboxHandler.reply(message, inbox.compose_edit_message(str(message.author)))
        message.mark_read()

    # TODO Handle if there are 0 subs for user
    @staticmethod
    def handle_unsubscribe_all_message(database, message):
        Logger.log('Unsub all message')
        removed_subscriptions = database.remove_all_subscriptions(str(message.author))
        InboxHandler.reply(message, inbox.compose_unsubscribe_all_message(str(message.author)))
        message.mark_read()

    @staticmethod
    def handle_help_message(database, message):
        Logger.log('Help message')
        subs = database.get_subscriptions_by_user(str(message.author))
        InboxHandler.reply(message, inbox.compose_help_message(str(message.author), subs))
        message.mark_read()

    @staticmethod
    def handle_feedback_message(reddit, message):
        Logger.log('Feedback message')
        reddit.send_message(
            env(DEV_USERNAME),
            'FEEDBACK',
            inbox.compose_feedback_forward(env(DEV_USERNAME), str(message.author), message.body)
        )
        InboxHandler.reply(message, inbox.compose_feedback_message(str(message.author)))
        message.mark_read()

    @staticmethod
    def handle_username_mention_message(reddit, message):
        Logger.log('Username mention message')
        try:
            InboxHandler.reply(message, inbox.compose_username_mention_reply(str(message.author)))
            message.mark_read()
            reddit.send_message(
                env(DEV_USERNAME),
                'USERNAME MENTION',
                inbox.compose_username_mention_forward(env(DEV_USERNAME), str(message.author), message.body)
            )
        except Exception as e:  # Figure out more specific exception thrown (praw.exceptions.APIException?)
            Logger.log(str(e), Color.RED)
            Logger.log('Handled RateLimitExceeded praw error - Commenting too frequently', Color.RED)

    @staticmethod
    def handle_post_reply_message(reddit, message):
        Logger.log('Post reply message')
        reddit.send_message(
            env(DEV_USERNAME),
            'USERNAME MENTION',
            inbox.compose_username_mention_forward(env(DEV_USERNAME), str(message.author), message.body)
        )
        message.mark_read()

    @staticmethod
    def handle_reject_message(reddit, message, error):
        Logger.log('Handle reject message')
        reject_message = inbox.compose_reject_message(str(message.author), message.subject, message.body, error)
        InboxHandler.reply(message, reject_message)
        message.mark_read()
        reddit.send_message(
            env(DEV_USERNAME),
            'REJECT MESSAGE - ' + str(message.author),
            reject_message
        )

    # TODO Add the ability to EDIT existing subscriptions
    @staticmethod
    def read_inbox(database, reddit):
        Logger.log('Reading inbox...', Color.GREEN)
        unread = []
        try:
            unread = reddit.get_unread()
        except:
            unread = []

        num_messages = 0
        for message in unread:
            num_messages += 1
            username = str(message.author).lower()
            subject = inbox.format_subject(str(message.subject).lower())
            body = str(message.body).lower()
            try:
                if username == 'reddit':
                    InboxHandler.handle_message_from_reddit(reddit, message)
                elif subject == 'username mention':
                    InboxHandler.handle_username_mention_message(reddit, message)
                elif subject == 'post reply':
                    InboxHandler.handle_post_reply_message(reddit, message)
                elif subject in MessageLexer.feedback_keywords:
                    InboxHandler.handle_feedback_message(reddit, message)
                elif subject in MessageLexer.help_keywords:
                    InboxHandler.handle_help_message(database, message)
                else:
                    m = MessageParser(message)
                    action = m.data[MessageParser.KEY_ACTION]
                    error = m.data[MessageParser.KEY_ERROR]
                    payload = m.get_payload()

                    Logger.log(json.dumps(m.data, indent=2), Color.MAGENTA)

                    if error:
                        Logger.log(
                            'REJECT:\n' +
                            'Error:\t' + str(error) + '\n' +
                            'Subject:\t' + str(message.subject) + '\n' +
                            'Body:\t\t' + str(message.body)
                        )
                        InboxHandler.handle_reject_message(reddit, message, error)
                    elif action == MessageParser.ACTION_STATISTICS:
                        InboxHandler.handle_statistics_message(database, message)
                    elif action == MessageParser.ACTION_GET_SUBSCRIPTIONS:
                        InboxHandler.handle_get_subscriptions_message(database, message)
                    elif action == MessageParser.ACTION_UNSUBSCRIBE_ALL:
                        InboxHandler.handle_unsubscribe_all_message(database, message)
                    elif action == MessageParser.ACTION_UNSUBSCRIBE:
                        InboxHandler.handle_unsubscribe_message(reddit, database, message)
                    elif action == MessageParser.ACTION_UNSUBSCRIBE_FROM_NUM:
                        InboxHandler.handle_unsubscribe_from_num_message(database, message, payload)
                    elif action == MessageParser.ACTION_SUBSCRIBE:
                        InboxHandler.handle_subscription_message(database, reddit, message, payload)
                    elif action == MessageParser.ACTION_EDIT:
                        InboxHandler.handle_edit_message(database, message, payload)
                    elif action == MessageParser.ACTION_HELP:
                        InboxHandler.handle_help_message(database, message)
                    elif action == MessageParser.ACTION_FEEDBACK:
                        InboxHandler.handle_feedback_message(reddit, message)

            except DatabaseHandlerException as ex:
                Logger.log(traceback.format_exc(), Color.RED)
                if ex.errorArgs == DatabaseHandlerException.INTEGRITY_ERROR:
                    message.mark_read()
                    reddit.send_message(env(DEV_USERNAME),
                                        'Integrity Error',
                                        'SUBJECT: ' + str(inbox.format_subject(message.subject)) + '\n\n' +
                                        'BODY:\n' + str(message.body))
            except:
                Logger.log(traceback.format_exc(), Color.RED)
                reddit.send_message(env(DEV_USERNAME),
                                    'ERROR HANDLING MESSAGE - POTENTIALLY STUCK IN INBOX',
                                    'Should NOT be seeing this message anymore hopefully...\t \n' +
                                    'AUTHOR: /u/' + str(message.author) + '\t \n' +
                                    'SUBJECT: ' + str(message.subject) + '\t \n' +
                                    'BODY:\n' + str(message.body))
            SleepHandler.sleep(2)
        Logger.log(str(num_messages) + ' unread messages handled', Color.CYAN)


class InboxHandlerException(Exception):
    READ_MESSAGES_EXCEPTION = 'Error reading messages'

    def __init__(self, error_args, traceback=None):
        Exception.__init__(self, 'InboxHandlerException: {0}'.format(error_args))
        self.errorArgs = error_args
        print(traceback)
