from utils import output, inbox
import traceback


class MatchHandler:

    @staticmethod
    def send_messages(reddit, database, matches):
        print('Handling matches...')
        for subscription, submission in matches:
            try:
                subs = database.get_subscriptions_by_user(subscription.username)
                print(subscription.message_id)
                message = reddit.get_message(subscription.message_id)
                message.reply(inbox.compose_match_message(subscription, submission, subs))
                database.insert_match(subscription.username, subscription.to_string(), submission.permalink)
                database.commit()
                output.match(subscription, submission)
            except:
                print(traceback.format_exc())
                raise MatchHandlerException('handle_matches')


class MatchHandlerException(Exception):

    def __init__(self, error_args):
        Exception.__init__(self, "MatchHandlerException: {0}".format(error_args))
        self.errorArgs = error_args
