from utils import inbox, times
from bot_modules.sleep_handler import SleepHandler
from bot_modules.database_handler import DatabaseHandlerException
from utils.logger import Logger
from utils.color import Color
from private import accountinfo
from utils.subscription import Subscription
from parsing.message_parser import MessageParser
from parsing.message_lexer import MessageLexer
import json
import traceback


class InboxHandler:

    @staticmethod
    def handle_message_from_reddit(reddit, message):
        print('Message from reddit')
        reddit.send_message(accountinfo.developerusername, 'FWD: ' + message.subject, message.body)
        reddit.send_message(accountinfo.developerusername2, 'FWD: ' + message.subject, message.body)
        message.mark_as_read()

    @staticmethod
    def handle_statistics_message(database, message):
        print('Stats message')
        formatted_message = inbox.compose_statistics(
            str(message.author),
            database.count_current_users(),
            database.count_all_users(),
            database.count_unique_subscriptions(),
            database.count_all_subscriptions(),
            len(database.get_unique_subreddits()),
            database.count_total_matches(),
            database.get_unique_subreddits())
        message.reply(formatted_message)
        message.mark_as_read()

    @staticmethod
    def handle_get_subscriptions_message(database, message):
        print('Get subs message')
        subscriptions = database.get_subscriptions_by_user(str(message.author))
        formatted_message = inbox.compose_all_subscriptions_message(str(message.author), subscriptions)
        message.reply(formatted_message)
        message.mark_as_read()

    @staticmethod
    def handle_subscription_message(database, reddit, message, payload):
        print('Sub message')
        new_sub = Subscription(payload, str(message.author), message.id)
        existing_subs = database.get_subscriptions_by_user(str(message.author))
        if new_sub.status == Subscription.STATUS_INVALID:
            message.reply(inbox.compose_reject_message(str(message.author), message.subject, message.body))
            message.mark_as_read()
            return
        elif new_sub.status == Subscription.STATUS_TOO_GENERIC:
            message.reply(inbox.compose_too_generic_message(str(message.author)))
            message.mark_as_read()
            return
        duplicate_subs = new_sub.check_against_existing(existing_subs)
        if duplicate_subs:
            Logger.log(Color.RED, 'Subscription already exists')
            message.reply(inbox.compose_duplicate_subscription_message(
                str(message.author),
                duplicate_subs[0],
                new_sub))
            message.mark_as_read()
            return
        invalid_subreddits = reddit.check_invalid_subreddits(new_sub.data[Subscription.SUBREDDITS])
        if invalid_subreddits:
            Logger.log(Color.RED, 'Subreddit(s) invalid: ' + str(invalid_subreddits))
            message.reply(inbox.compose_invalid_subreddit_message(str(message.author), invalid_subreddits, message))
            message.mark_as_read()
            return
        database.insert_subscription(str(message.author), str(message.id), new_sub.to_string(), times.get_current_timestamp())
        existing_subs.append(new_sub)
        subreddit_not_specified = len(new_sub.data[Subscription.SUBREDDITS]) == 0
        message.reply(inbox.compose_subscribe_message(str(message.author), new_sub, existing_subs, subreddit_not_specified))
        database.commit()
        message.mark_as_read()

    @staticmethod
    def handle_unsubscribe_message(reddit, database, message):
        print('Unsub message')
        message_id = reddit.get_original_message(message, database).id
        removed_subs = database.remove_subscriptions_by_message_id(str(message.author), message_id)
        subs = database.get_subscriptions_by_user(str(message.author))
        if len(removed_subs) > 0:
            message.reply(inbox.compose_unsubscribe_message(str(message.author), removed_subs, subs))
        else:
            message.reply(inbox.compose_unsubscribe_invalid_sub_message(str(message.author), subs))
        message.mark_as_read()

    @staticmethod
    def handle_unsubscribe_from_num_message(database, message, payload):
        print("Unsub from num")
        removed = database.remove_subscription_by_number(str(message.author), int(payload))
        subs = database.get_subscriptions_by_user(str(message.author))
        if removed:
            message.reply(inbox.compose_unsubscribe_from_num_message(str(message.author), removed, subs))
        else:
            message.reply(inbox.compose_unsubscribe_invalid_sub_message(str(message.author), subs))
        message.mark_as_read()

    @staticmethod
    def handle_edit_message(database, message, payload):
        print('Edit message')
        message.reply(inbox.compose_edit_message(str(message.author)))
        message.mark_as_read()

    # TODO Handle if there are 0 subs for user
    @staticmethod
    def handle_unsubscribe_all_message(database, message):
        print('Unsub all message')
        had_subscriptions = database.remove_all_subscriptions(str(message.author))
        message.reply(inbox.compose_unsubscribe_all_message(str(message.author)))
        message.mark_as_read()

    @staticmethod
    def handle_help_message(database, message):
        print('Help message')
        subs = database.get_subscriptions_by_user(str(message.author))
        message.reply(inbox.compose_help_message(str(message.author), subs))
        message.mark_as_read()

    @staticmethod
    def handle_feedback_message(reddit, message):
        print('Feedback message')
        reddit.send_message(accountinfo.developerusername,  'FEEDBACK', inbox.compose_feedback_forward(str(message.author), message.body))
        reddit.send_message(accountinfo.developerusername2, 'FEEDBACK', inbox.compose_feedback_forward(str(message.author), message.body))
        message.reply(inbox.compose_feedback_message(str(message.author)))
        message.mark_as_read()

    @staticmethod
    def handle_username_mention_message(reddit, message):
        print('Username mention message')
        reddit.send_message(accountinfo.developerusername,  'USERNAME MENTION', inbox.compose_username_mention_forward(str(message.author), message.body))
        reddit.send_message(accountinfo.developerusername2, 'USERNAME MENTION', inbox.compose_username_mention_forward(str(message.author), message.body))
        message.mark_as_read()

    @staticmethod
    def handle_post_reply_message(reddit, message):
        reddit.send_message(accountinfo.developerusername, 'USERNAME MENTION', inbox.compose_username_mention_forward(str(message.author), message.body))
        reddit.send_message(accountinfo.developerusername, 'USERNAME MENTION', inbox.compose_username_mention_forward(str(message.author), message.body))
        message.mark_as_read()
        print('Post reply message')

    @staticmethod
    def handle_reject_message(reddit, message):
        print('handle reject message')
        message.reply(inbox.compose_reject_message(str(message.author), message.subject, message.body))
        reddit.send_message(accountinfo.developerusername,  'REJECT MESSAGE - ' + str(message.author), inbox.compose_reject_message(str(message.author), message.subject, message.body))
        reddit.send_message(accountinfo.developerusername2, 'REJECT MESSAGE - ' + str(message.author), inbox.compose_reject_message(str(message.author), message.subject, message.body))
        message.mark_as_read()

    # TODO Add the ability to EDIT existing subscriptions
    @staticmethod
    def read_inbox(database, reddit):
        print('Reading inbox...')
        unread = []
        try:
            unread = reddit.get_unread()
        except:
            unread = []

        num_messages = 0
        for message in unread:
            num_messages += 1
            username = str(message.author).lower()
            subject  = inbox.format_subject(str(message.subject).lower())
            body     = str(message.body).lower()
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
                    valid = m.data[MessageParser.KEY_VALID]
                    action = m.data[MessageParser.KEY_ACTION]
                    payload = m.get_payload()

                    print(json.dumps(m.data, 2))

                    if valid and action == MessageParser.ACTION_STATISTICS:
                        InboxHandler.handle_statistics_message(database, message)
                    elif valid and action == MessageParser.ACTION_GET_SUBSCRIPTIONS:
                        InboxHandler.handle_get_subscriptions_message(database, message)
                    elif valid and action == MessageParser.ACTION_UNSUBSCRIBE_ALL:
                        InboxHandler.handle_unsubscribe_all_message(database, message)
                    elif valid and action == MessageParser.ACTION_UNSUBSCRIBE:
                        InboxHandler.handle_unsubscribe_message(reddit, database, message)
                    elif valid and action == MessageParser.ACTION_UNSUBSCRIBE_FROM_NUM:
                        InboxHandler.handle_unsubscribe_from_num_message(database, message, payload)
                    elif valid and action == MessageParser.ACTION_SUBSCRIBE:
                        InboxHandler.handle_subscription_message(database, reddit, message, payload)
                    elif valid and action == MessageParser.ACTION_EDIT:
                        InboxHandler.handle_edit_message(database, message, payload)
                    elif valid and action == MessageParser.ACTION_HELP:
                        InboxHandler.handle_help_message(database, message)
                    elif valid and action == MessageParser.ACTION_FEEDBACK:
                        InboxHandler.handle_feedback_message(reddit, message)
                    else:
                        print('VALID: ' + str(valid))
                        print('REJECT:\nSubject:\t' + str(message.subject) + '\nBODY:\t\t' + str(message.body))
                        InboxHandler.handle_reject_message(reddit, message)

            except DatabaseHandlerException as ex:
                if ex.errorArgs == DatabaseHandlerException.INTEGRITY_ERROR:
                    message.mark_as_read()
                    reddit.send_message(accountinfo.developerusername,
                                        'Integrity Error',
                                        'SUBJECT: ' + str(inbox.format_subject(message.subject)) +
                                        'BODY:\n' + str(message.body))
                    continue
                else:
                    raise
            except:
                print(traceback.format_exc())
                raise InboxHandlerException('Error handling inbox message')

            SleepHandler.sleep(2)
        Logger.log(Color.CYAN, str(num_messages) + ' unread messages handled')


class InboxHandlerException(Exception):
    READ_MESSAGES_EXCEPTION = 'Error reading messages'

    def __init__(self, error_args, traceback=None):
        Exception.__init__(self, "InboxHandlerException: {0}".format(error_args))
        self.errorArgs = error_args
        print(traceback)
