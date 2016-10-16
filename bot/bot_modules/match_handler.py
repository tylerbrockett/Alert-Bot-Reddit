

class MatchHandler:

    @staticmethod
    def handle_matches(reddit, database, matches):
        print('Handling matches...')
        for username, message_id, sub, post in matches:
            message = reddit.get_message(message_id)
            database.insert_match(username, message.subject, )
