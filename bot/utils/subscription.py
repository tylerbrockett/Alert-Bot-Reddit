from parsing.subscription_parser import SubscriptionParser
from parsing.subscription_parser import SubscriptionParserException


class Subscription:

    def __init__(self, sub, username, message_id):
        self.original_string = sub
        self.username = username
        self.message_id = message_id
        self.items = []
        self.ignore_items = []
        self.sites = []
        self.ignore_sites = []
        self.redditors = []
        self.ignore_redditors = []
        self.subreddits = []
        self.settings = []
        self.valid = False
        self.parse_items()
        self.sort()

    def parse_items(self):
        try:
            parser = SubscriptionParser(self.original_string)
            self.items = list(set(parser.items))
            self.ignore_items = list(set(parser.ignore_items))
            self.sites = list(set(parser.sites))
            self.ignore_sites = list(set(parser.ignore_sites))
            self.redditors = list(set(parser.redditors))
            self.ignore_redditors = list(set(parser.ignore_redditors))
            self.subreddits = list(set(parser.subreddits))
            self.settings = list(set(parser.settings))
            self.valid = True
        except SubscriptionParserException:
            self.valid = False

    def sort(self):
        self.items.sort()
        self.ignore_items.sort()
        self.sites.sort()
        self.ignore_sites.sort()
        self.redditors.sort()
        self.ignore_redditors.sort()
        self.subreddits.sort()
        self.settings.sort()

    def format_settings(self):
        ret = ''
        for setting in self.settings:
            ret += (str(setting[0]) + '|' + str(setting[1])) + '\n'
        return ret

    @staticmethod
    def format_list(lis):
        if len(lis) is 0:
            return 'N/A'
        return str(lis).replace('[', '').replace(']', '')

    def to_string(self):
        ret = \
            '###Subscription Details\n' + \
            'Detail|Value\n' + \
            '--:|:--:' + '\n' + \
            'Items|' + Subscription.format_list(self.items) + '\n' + \
            'Ignore Items|' + Subscription.format_list(self.ignore_items) + '\n' + \
            'Sites|' + Subscription.format_list(self.sites) + '\n' + \
            'Ignore Sites|' + Subscription.format_list(self.ignore_sites) + '\n' + \
            'Redditors|' + Subscription.format_list(self.redditors) + '\n' + \
            'Ignore Redditors|' + Subscription.format_list(self.ignore_redditors) + '\n' + \
            'Subreddits|' + Subscription.format_list(self.subreddits) + '\n' + \
            self.format_settings()
        return ret

    @staticmethod
    def compare_lists(list1, list2):
        for val in list1:
            if val in list2:
                return True
        return False

    def compare_to(self, sub):
        compare_items = Subscription.compare_lists(self.items, sub.items)
        compare_ig_items = Subscription.compare_lists(self.ignore_items, sub.ignore_items)
        compare_sites = Subscription.compare_lists(self.sites, sub.sites)
        compare_ig_sites = Subscription.compare_lists(self.ignore_sites, sub.ignore_sites)
        compare_redditors = Subscription.compare_lists(self.redditors, sub.redditors)
        compare_ig_redditors = Subscription.compare_lists(self.ignore_redditors, sub.ignore_redditors)
        compare_settings = Subscription.compare_lists(self.settings, sub.settings)
        return (compare_items and compare_ig_items and compare_sites and compare_ig_sites and
                compare_redditors and compare_ig_redditors and compare_settings)
