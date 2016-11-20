from utils.subscription import Subscription


class SubscriptionHandler:

    @staticmethod
    def is_match(subscription, submission):
        result = True
        mismatched_keys = []
        for key in subscription.data.keys():
            if key == Subscription.TITLE:
                title_match = False  # Empty title_list is automatically 'True' because it has no effect on result
                for title_list in subscription.data[key]:
                    title_list_match = True
                    for item in title_list:
                        if item.lower() not in submission.title.lower():
                            title_list_match = False
                    title_match = title_match or title_list_match
                if not title_match:
                    mismatched_keys.append(key)
                result = result and title_match
            elif key == Subscription.BODY:
                body_match = True
                for item in subscription.data[key]:
                    print("VARS: \n\n" + str(vars(submission)))
                    body_content = submission.selftext.lower() if submission.is_self else submission.url.lower()
                    print('BODY CONTENT:  ' + body_content)
                    if item.lower() not in body_content:
                        body_match = False
                        mismatched_keys.append(key)
                result = result and body_match
            elif key == Subscription.REDDITORS:
                redditor_match = True
                for redditor in subscription.data[key]:
                    if redditor.lower() not in submission.author.lower():
                        redditor_match = False
                        mismatched_keys.append(key)
                result = result and redditor_match
            elif key == Subscription.IGNORE_TITLE:
                ignore_title_match = True
                for item in subscription.data[key]:
                    if item.lower() in submission.title.lower():
                        ignore_title_match = False
                        mismatched_keys.append(key)
                result = result and ignore_title_match
            elif key == Subscription.IGNORE_BODY:
                ignore_body_match = True
                for item in subscription.data[key]:
                    if item.lower() in submission.selftext.lower():
                        ignore_body_match = False
                        mismatched_keys.append(key)
                result = result and ignore_body_match
            elif key == Subscription.IGNORE_REDDITORS:
                ignore_redditors_match = True
                for redditor in subscription.data[key]:
                    if redditor.lower() in submission.author.lower():
                        ignore_redditors_match = False
                        mismatched_keys.append(key)
                result = result and ignore_redditors_match
            elif key == Subscription.NSFW:
                if submission.over_18 and not subscription.data[key]:
                    result = result and False
                    mismatched_keys.append(key)
        return result, sorted(set(mismatched_keys))

    @staticmethod
    def find_matches(subscriptions, reddit, database):
        print('Finding matches...')
        subreddits = {}
        matches = []
        for subscription in subscriptions:
            subreds = subscription.data[Subscription.SUBREDDITS]
            for subreddit in subreds:
                if reddit.check_invalid_subreddits([subreddit]):
                    print('INVALID SUBREDDIT - ' + subreddit)
                    continue
                if subreddit not in subreddits:
                    submissions = reddit.get_submissions(subreddit)
                    subreddits[subreddit] = submissions
                submissions = subreddits[subreddit]
                for submission in submissions:
                    is_match, mismatched_keys = SubscriptionHandler.is_match(subscription, submission)
                    if is_match:
                        already_exists = database.check_if_match_exists(subscription.username,
                                                                        subscription.to_string(),
                                                                        submission.permalink)
                        if not already_exists:
                            matches.append((subscription, submission))
        return matches
