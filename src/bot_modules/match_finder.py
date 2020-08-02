"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

from utils.subscription import Subscription
from utils.logger import Logger
from utils.color import Color


class MatchFinder:

    @staticmethod
    def is_title_match(subscription, submission):
        title_match = False
        # Empty title_list is automatically 'True' because it has no effect on result
        if len(subscription.data[Subscription.TITLE]) == 0:
            title_match = True
        for title_list in subscription.data[Subscription.TITLE]:
            title_list_match = True
            for item in title_list:
                if item.lower() not in submission.title.lower():
                    title_list_match = False
            title_match = title_match or title_list_match
        return title_match

    @staticmethod
    def is_body_match(subscription, submission):
        body_match = False
        # Empty body_list is automatically 'True' because it has no effect on result
        if len(subscription.data[Subscription.BODY]) == 0:
            body_match = True
        for body_list in subscription.data[Subscription.BODY]:
            body_list_match = True
            for item in body_list:
                body_content = submission.selftext.lower() if submission.is_self else submission.url.lower()
                if item.lower() not in body_content:
                    body_list_match = False
            body_match = body_match or body_list_match
        return body_match

    @staticmethod
    def is_redditor_match(subscription, submission):
        redditor_match = False
        if len(subscription.data[Subscription.REDDITORS]) == 0:
            redditor_match = True
        for redditor in subscription.data[Subscription.REDDITORS]:
            if redditor.lower() == str(submission.author).lower():
                redditor_match = True
        return redditor_match

    @staticmethod
    def is_ignore_title_match(subscription, submission):
        ignore_title_match = True
        for item in subscription.data[Subscription.IGNORE_TITLE]:
            if item.lower() in submission.title.lower():
                ignore_title_match = False
        return ignore_title_match

    @staticmethod
    def is_ignore_body_match(subscription, submission):
        ignore_body_match = True
        for item in subscription.data[Subscription.IGNORE_BODY]:
            body_content = submission.selftext.lower() if submission.is_self else submission.url.lower()
            if item.lower() in body_content:
                ignore_body_match = False
        return ignore_body_match

    @staticmethod
    def is_ignore_redditors_match(subscription, submission):
        ignore_redditors_match = True
        for redditor in subscription.data[Subscription.IGNORE_REDDITORS]:
            if redditor.lower() == str(submission.author).lower():
                ignore_redditors_match = False
        return ignore_redditors_match

    @staticmethod
    def is_nsfw_match(subscription, submission):
        if submission.over_18 and not subscription.data[Subscription.NSFW]:
            return False
        return True

    @staticmethod
    def is_match(subscription, submission):
        result = True
        mismatched_keys = []
        for key in subscription.data.keys():
            key_match = True
            if Subscription.TITLE == key:
                key_match = MatchFinder.is_title_match(subscription, submission)
            elif Subscription.BODY == key:
                key_match = MatchFinder.is_body_match(subscription, submission)
            elif Subscription.REDDITORS == key:
                key_match = MatchFinder.is_redditor_match(subscription, submission)
            elif Subscription.IGNORE_TITLE == key:
                key_match = MatchFinder.is_ignore_title_match(subscription, submission)
            elif Subscription.IGNORE_BODY == key:
                key_match = MatchFinder.is_ignore_body_match(subscription, submission)
            elif Subscription.IGNORE_REDDITORS == key:
                key_match = MatchFinder.is_ignore_redditors_match(subscription, submission)
            elif Subscription.NSFW == key:
                key_match = MatchFinder.is_nsfw_match(subscription, submission)
            if not key_match:
                mismatched_keys.append(key)
            result = result and key_match
        return result, sorted(set(mismatched_keys))

    @staticmethod
    def find_matches(subscriptions, reddit, database):
        Logger.log('Finding Matches...', Color.GREEN)
        subreddits = {}
        matches = []
        index = 0
        for subscription in subscriptions:
            index += 1
            subreds = subscription.data[Subscription.SUBREDDITS]
            for subreddit in subreds:
                if subreddit.lower() not in [k.lower() for k in subreddits.keys()]:
                    submissions = reddit.get_submissions(subreddit.lower(), index, len(subscriptions))
                    subreddits[subreddit.lower()] = submissions
                submissions = subreddits[subreddit.lower()]
                for submission in submissions:
                    is_match, mismatched_keys = MatchFinder.is_match(subscription, submission)
                    if is_match:
                        already_exists = database.check_if_match_exists(subscription.username,
                                                                        subscription.to_string(),
                                                                        submission.permalink)
                        if not already_exists:
                            matches.append((subscription, submission))
        return matches
