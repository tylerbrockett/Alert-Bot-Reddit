
from parsing.subscription_parser import SubscriptionParser


if __name__ == '__main__':
    sub = 'this is a test; of how well , the, parser actually works; yay! Site: google.com, youtube.com Items: funny cat videos Subreddits: funny, all, videos Sites: vine Ignore Items: cats being mean, cats getting hurt Ignore Sites: somevideosite.com Email'
    parser = SubscriptionParser(sub)
    print('\n\n\n')
    print('------------ DATA ------------')
    print("Items:\t\t\t" + str(parser.items))
    print("Sites:\t\t\t" + str(parser.sites))
    print("Ignore Items:\t" + str(parser.ignore_items))
    print("Ignore Sites:\t" + str(parser.ignore_sites))
    print("Subreddits:\t\t" + str(parser.subreddits))
    print("Settings:\t\t" + str(parser.settings))
    print("------------ END ------------")
