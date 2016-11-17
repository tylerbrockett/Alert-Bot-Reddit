from dict_compare import dict_compare
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
    VALID = 'valid'
    SCHEMA_VERSION = 'schema_version'

    STATUS_VALID = 'valid'
    STATUS_INVALID = 'invalid'
    STATUS_TOO_GENERIC = 'too_generic'

    CURRENT_SCHEMA_VERSION = 1

    def __init__(self, subscription, username, message_id):
        self.username = username
        self.message_id = message_id
        self.status = Subscription.STATUS_INVALID
        self.data = {}
        try:
            if type(subscription) == dict:
                self.data = subscription
            elif type(subscription) == str:
                self.data = json.loads(subscription)
            self.sort()
            self.status = Subscription.STATUS_VALID
        except:
            print(traceback.format_exc())
            self.valid = Subscription.STATUS_INVALID
        self.check_too_generic()

    def check_too_generic(self):
        if not self.data[Subscription.TITLE] and 'all' in self.data[Subscription.SUBREDDITS]:
            self.status = Subscription.STATUS_TOO_GENERIC

    def sort(self):
        for i in range(0, len(self.data[Subscription.TITLE])):
            self.data[Subscription.TITLE][i].sort()
        self.data[Subscription.TITLE].sort()
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

    @staticmethod
    def format_list(lis):
        if len(lis) is 0:
            return 'N/A'
        return str(lis).replace('[', '').replace(']', '')

    def format_terms(self):
        ret = ''
        i = 1
        for term_set in self.data[Subscription.TITLE]:
            ret += 'Item ' + str(i) + '|' + Subscription.format_list(term_set) + '\n'
            i += 1
        return ret

    def to_string(self):
        return json.dumps(self.data, 2)

    def to_table(self, title):
        ret = \
            '###' + title + '\n' + \
            'Detail|Value\n' + \
            '--:|:--:' + '\n' + \
            self.format_terms() + \
            'Body Terms|' + Subscription.format_list(self.data[Subscription.BODY]) + '\n' + \
            'Subreddits|' + Subscription.format_list(self.data[Subscription.SUBREDDITS]) + '\n' + \
            'Ignore Title Terms|' + Subscription.format_list(self.data[Subscription.IGNORE_TITLE]) + '\n' + \
            'Ignore Body Terms|' + Subscription.format_list(self.data[Subscription.IGNORE_BODY]) + '\n' + \
            'Whitelist Redditors|' + Subscription.format_list(self.data[Subscription.REDDITORS]) + '\n' + \
            'Ignore Redditors|' + Subscription.format_list(self.data[Subscription.IGNORE_REDDITORS]) + '\n' + \
            'NSFW|' + str(self.data[Subscription.NSFW]) + '\n' + \
            'Email|' + str(self.data[Subscription.EMAIL])

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
