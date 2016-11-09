from utils import output, inbox


class MatchHandler:

    @staticmethod
    def handle_matches(reddit, database, matches):
        print('Handling matches...')
        for subscription, submission in matches:
            try:
                message = reddit.get_message(subscription.message_id)
                message.reply(inbox.compose_match_message(subscription, submission))
                database.insert_match(subscription.username, message.subject, submission.permalink)
                output.match(subscription, submission)
            except:
                raise MatchHandlerException('handle_matches')


class MatchHandlerException(Exception):

    def __init__(self, error_args):
        Exception.__init__(self, "MatchHandlerException: {0}".format(error_args))
        self.errorArgs = error_args
