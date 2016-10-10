from utils import inbox
from bot_modules.sleep_handler import SleepHandler
from utils.logger import Logger
from utils.color import Color
from private import accountinfo
from utils.subscription import Subscription


class InboxHandler:

    @staticmethod
    def handle_reddit_message(reddit, message):
        print('message from reddit')
        reddit.send_message(accountinfo.developerusername, 'FORWARD: ' + message.subject, message.body)
        reddit.send_message(accountinfo.developerusername2, 'FORWARD: ' + message.subject, message.body)
        message.mark_as_read()

    @staticmethod
    def handle_statistics_message(database, message):
        current_users = database.count_current_users()
        all_users = database.count_all_users()
        unique_subs = database.count_unique_subscriptions()
        all_subs = database.count_all_subscriptions()
        unique_subreddits = database.count_unique_subreddits()
        all_matches = database.count_total_matches()
        formatted_message = inbox.compose_statistics(
            message.author,
            all_users,
            current_users,
            unique_subs,
            all_subs,
            unique_subreddits,
            all_matches)
        message.reply(formatted_message)
        message.mark_as_read()

    @staticmethod
    def handle_get_subscriptions_message(database, message):
        subscriptions = database.get_subscriptions_by_username(message.author)
        formatted_message = inbox.compose_subscriptions_message(message.author, subscriptions)
        message.reply(formatted_message)
        message.mark_as_read()

    @staticmethod
    def handle_subscription_message(database, message):
        new_sub = Subscription(inbox.format_subject(message.subject))
        if not new_sub.valid:
            message.reply(inbox.compose_invalid_subscription_message(message.username, message.subject))
            message.mark_as_read()
            return
        subscriptions = database.get_subscriptions_by_username(message.author)
        for existing_sub in subscriptions:
            if new_sub.compare_to(existing_sub) is True:
                Logger.log(Color.RED, 'Subscription already exists')
                message.reply(inbox.compose_duplicate_subscription_message(
                    message.author,
                    existing_sub.to_string(),
                    new_sub))
                message.mark_as_read()
                return
        database.insert_subscription(message.author, message.subject)
        message.reply(inbox.compose_subscriptions_message(message.author, new_sub.to_string()))
        message.mark_as_read()

    @staticmethod
    def handle_unsubscribe_message(database, message):
        database.remove_subscription(message.author, inbox.format_subject(message.subject))
        message.reply(inbox.compose_unsubscribe_message(message.author, message.subject))
        message.mark_as_read()

    @staticmethod
    def handle_unsubscribe_all_message(database, message):
        database.remove_all_subscriptions(message.author)
        message.reply(inbox.compose_unsubscribe_all_message(message.author))
        message.mark_as_read()

    @staticmethod
    def handle_help_message(database, message):
        subs = database.get_subscriptions_by_username(message.author)
        
        print('help message')

    @staticmethod
    def handle_feedback_message(reddit, message):
        print('feedback message')

    @staticmethod
    def handle_username_mention_message(message):
        print('username mention')

    @staticmethod
    def handle_post_reply_message(message):
        print('post reply')

    @staticmethod
    def handle_reject_message(message):
        print('handle reject message')

    @staticmethod
    def read_inbox(database, reddit):
        print('Reading inbox...')
        unread = []
        try:
            unread = reddit.get_unread()
        except:
            raise InboxHelperException(InboxHelperException.READ_MESSAGES_EXCEPTION)
        for message in unread:
            username = str(message.author).lower()
            subject  = inbox.format_subject(message.subject.lower())
            body     = message.body.lower()
            if username is 'reddit':
                InboxHandler.handle_reddit_message(reddit, message)
            elif subject in ['statistics', 'stats'] or body in ['statistics', 'stats']:
                InboxHandler.handle_statistics_message(database, message)
            elif subject in ['subscriptions', 'subs'] or body in ['subscriptions, subs']:
                InboxHandler.handle_get_subscriptions_message(database, message)
            elif subject is 'username mention':
                InboxHandler.handle_username_mention_message(message)
            elif subject is 'post reply':
                InboxHandler.handle_post_reply_message(message)
            elif ['unsubscribe', 'all'] in body or ['unsubscribe', 'all'] in subject:
                InboxHandler.handle_unsubscribe_all_message(database, message)
            elif body in ['unsubscribe', 'unsub'] and subject.replace(' ', '') != '':
                InboxHandler.handle_unsubscribe_message(database, message)
            elif body in ['subscribe', 'sub'] and len(inbox.format_subject(subject).replace(' ', '')) > 0:
                InboxHandler.handle_subscription_message(database, message)
            elif subject in ['information', 'info', 'help'] or body in ['information', 'info', 'help']:
                InboxHandler.handle_help_message(database, message)
            elif subject is 'feedback':
                InboxHandler.handle_feedback_message(reddit, message)
            else:
                InboxHandler.handle_reject_message(message)
            SleepHandler.sleep(2)
        Logger.log(Color.CYAN, str(len(unread)) + ' unread messages handled')


class InboxHelperException(Exception):
    READ_MESSAGES_EXCEPTION = 'Error reading messages'

    def __init__(self, error_args, traceback=None):
        Exception.__init__(self, "InboxHandlerException: {0}".format(error_args))
        self.errorArgs = error_args
        print(traceback)
