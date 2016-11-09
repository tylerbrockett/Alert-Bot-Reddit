from parsing.subscription_parser import SubscriptionParser
from parsing.subscription_parser import SubscriptionParserException


class Subscription:

    def __init__(self, original_string, username, message_id):
        self.original_string = original_string
        self.username = username
        self.message_id = message_id
        self.title = []
        self.ignore_title = []
        self.body = []
        self.ignore_body = []
        self.redditors = []
        self.ignore_redditors = []
        self.subreddits = []
        self.flags = []
        self.valid = False
        self.parse()
        self.sort()

    def parse(self):
        try:
            parser = SubscriptionParser(self.original_string)
            self.title = list(set(parser.title))
            self.ignore_title = list(set(parser.ignore_title))
            self.body = list(set(parser.body))
            self.ignore_body = list(set(parser.ignore_body))
            self.redditors = list(set(parser.redditors))
            self.ignore_redditors = list(set(parser.ignore_redditors))
            self.subreddits = list(set(parser.subreddits))
            self.flags = list(set(parser.flags))
            self.valid = True
        except SubscriptionParserException:
            self.valid = False

    def sort(self):
        self.title.sort()
        self.ignore_title.sort()
        self.body.sort()
        self.ignore_body.sort()
        self.redditors.sort()
        self.ignore_redditors.sort()
        self.subreddits.sort()
        self.flags.sort()

    def format_settings(self):
        ret = ''
        for setting in self.flags:
            ret += (str(setting[0]) + '|' + str(setting[1])) + '\n'
        return ret

    @staticmethod
    def format_list(lis):
        if len(lis) is 0:
            return 'N/A'
        return str(lis).replace('[', '').replace(']', '')

    def format_terms(self):
        ret = ''
        i = 1
        for term_set in self.title:
            ret += 'Item ' + str(i) + '|' + Subscription.format_list(term_set)
            i += 1
        return ret

    def to_string(self, title):
        ret = \
            '###' + title + '\n' + \
            'Detail|Value\n' + \
            '--:|:--:' + '\n' + \
            self.format_terms() + \
            'Ignore Title Terms|' + Subscription.format_list(self.ignore_title) + '\n' + \
            'Body Terms|' + Subscription.format_list(self.body) + '\n' + \
            'Ignore Body Terms|' + Subscription.format_list(self.ignore_body) + '\n' + \
            'Whitelist Redditors|' + Subscription.format_list(self.redditors) + '\n' + \
            'Ignore Redditors|' + Subscription.format_list(self.ignore_redditors) + '\n' + \
            'Subreddits|' + Subscription.format_list(self.subreddits) + '\n' + \
            'Flags|' + Subscription.format_list(self.flags)
        return ret

    # TODO I think this method is incorrect
    @staticmethod
    def compare_lists(list1, list2):
        for val in list1:
            if val in list2:
                return True
        return False

    def compare_to(self, sub):
        compare_title = Subscription.compare_lists(self.title, sub.title)
        compare_ig_title = Subscription.compare_lists(self.ignore_title, sub.ignore_title)
        compare_body = Subscription.compare_lists(self.body, sub.body)
        compare_ig_body = Subscription.compare_lists(self.ignore_body, sub.ignore_body)
        compare_redditors = Subscription.compare_lists(self.redditors, sub.redditors)
        compare_ig_redditors = Subscription.compare_lists(self.ignore_redditors, sub.ignore_redditors)
        compare_flags = Subscription.compare_lists(self.flags, sub.flags)
        return (compare_title and
                compare_ig_title and
                compare_body and
                compare_ig_body and
                compare_redditors and
                compare_ig_redditors and
                compare_flags)
