
class SubscriptionHandler:

    def is_match(self, subscription, submission):
        return True


    @staticmethod
    def find_matches(subscriptions, reddit, database):
        print('Finding matches...')
        subreddits = {}
        matches = []
        for subscription in subscriptions:
            subreds = subscription.subreddits
            for subreddit in subreds:
                if subreddit not in subreddits:
                    submissions = reddit.get_submissions(subreddit)
                    subreddits[subreddit] = submissions
                submissions = subreddits[subreddit]
                for submission in submissions:
                    if SubscriptionHandler.is_match(subscription, submission):
                        already_exists = database.check_if_match_exists(subscription.username,
                                                                        subscription.original_string,
                                                                        submission.permalink)
                        if not already_exists:
                            matches.append((subscription, submission))
        return matches
