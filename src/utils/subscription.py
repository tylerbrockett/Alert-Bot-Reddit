"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

from utils.dict_compare import dict_compare
import traceback
import json


class Subscription:

    TITLE = 'title'
    BODY = 'body'
    IGNORE_TITLE = 'ignore_title'
    IGNORE_BODY = 'ignore_body'
    REDDITORS = 'redditors'
    IGNORE_REDDITORS = 'ignore_redditors'
    SUBREDDITS = 'subreddits'
    NSFW = 'nsfw'
    EMAIL = 'email'
    VALID = 'valid'  # TODO: Remove "VALID" from everywhere
    SCHEMA_VERSION = 'schema_version'

    CURRENT_SCHEMA_VERSION = 1

    def __init__(self, subscription, username, message_id):
        self.username = username
        self.message_id = message_id
        self.data = {}
        self.error = None
        try:
            if type(subscription) == dict:
                self.data = subscription
            else:
                self.data = json.loads(subscription)
            self.sort()
            self.check_too_generic()
        except Exception as e:
            print(traceback.format_exc())
            self.data = {}
            self.error = str(e)

    def format(self, key):
        result = ''
        data = self.data[key]
        if key == Subscription.TITLE:
            if data:
                i = 1
                for term_set in data:
                    result += 'Title Item ' + str(i) + '|' + ', '.join(term_set) + '\n'
                    i += 1
            else:
                result = 'Title Items|* (All)' + '\n'
        elif key == Subscription.BODY:
            if data:
                i = 1
                for term_set in data:
                    result += 'Body Item ' + str(i) + '|' + ', '.join(term_set) + '\n'
                    i += 1
            else:
                result = 'Body Items|Not specified' + '\n'
        elif key == Subscription.SUBREDDITS:
            if data:
                result = ", ".join(['/r/' + str(r) for r in data])
            else:
                result = '/r/buildapcsales'
        elif data and (key == Subscription.REDDITORS or key == Subscription.IGNORE_REDDITORS):
            result = ", ".join(['/u/' + str(u) for u in data])
        elif key == Subscription.NSFW or key == Subscription.EMAIL:
            if data:
                result = str(data)
            else:
                result = str(False)
        else:
            if not data:
                result = 'Not specified'
            else:
                result = ", ".join([str(element) for element in data])
        return result

    def check_too_generic(self):
        if not self.data[Subscription.TITLE] and 'all' in self.data[Subscription.SUBREDDITS]:
            raise Exception("Subscription too generic")

    def sort(self):
        for i in range(0, len(self.data[Subscription.TITLE])):
            self.data[Subscription.TITLE][i].sort()
        self.data[Subscription.TITLE].sort()
        for i in range(0, len(self.data[Subscription.BODY])):
            self.data[Subscription.BODY][i].sort()
        self.data[Subscription.BODY].sort()
        self.data[Subscription.REDDITORS].sort()
        self.data[Subscription.IGNORE_TITLE].sort()
        self.data[Subscription.IGNORE_BODY].sort()
        self.data[Subscription.IGNORE_REDDITORS].sort()
        self.data[Subscription.SUBREDDITS].sort()

    def check_schema_version(self):
        schema_version = self.data[Subscription.SCHEMA_VERSION]
        if schema_version != Subscription.CURRENT_SCHEMA_VERSION:
            self.data[Subscription.SCHEMA_VERSION] = Subscription.CURRENT_SCHEMA_VERSION
            return True
        return False

    def to_string(self):
        return json.dumps(self.data, sort_keys=True)

    def check_against_existing(self, existing_subs):
        duplicate_subs = []
        for existing_sub in existing_subs:
            if self.compare_to(existing_sub):
                duplicate_subs.append(existing_sub)
        return duplicate_subs

    def to_table(self, title):
        ret = \
            '####' + title + '\n' + \
            'Detail|Value\n' + \
            ':--|:--' + '\n' + \
            self.format(Subscription.TITLE) + \
            self.format(Subscription.BODY) + \
            'Subreddits|' + self.format(Subscription.SUBREDDITS) + '\n' + \
            'Ignore Title Terms|' + self.format(Subscription.IGNORE_TITLE) + '\n' + \
            'Ignore Body Terms|' + self.format(Subscription.IGNORE_BODY) + '\n' + \
            'Redditors|' + self.format(Subscription.REDDITORS) + '\n' + \
            'Ignore Redditors|' + self.format(Subscription.IGNORE_REDDITORS) + '\n' + \
            'Allow NSFW|' + self.format(Subscription.NSFW) + '\n'  # + \
            # 'Email|' + self.format(Subscription.EMAIL) + '\n'
        return ret

    @staticmethod
    def compare_lists(list1, list2):
        for val in list1:
            if val not in list2:
                return False
        for val in list2:
            if val not in list1:
                return False
        if len(list1) != len(list2):
            return False
        return True

    def compare_to(self, sub):
        self.sort()
        sub.sort()
        added, removed, modified, same = dict_compare(self.data, sub.data)
        if len(added) != 0 or len(removed) != 0 or len(modified) != 0:
            return False
        return True
