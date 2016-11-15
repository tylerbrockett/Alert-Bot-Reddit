from private import accountinfo
from parsing.subscription_parser import SubscriptionParser
from utils import inbox
import praw
from bot_modules.reddit_handler import RedditHandler
from bot_modules.database_handler import DatabaseHandler
import json

if __name__ == '__main__':
    '''
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
    '''
    '''
    s = 'RE:RE:RE: YOOOOO re: yooooo'
    print('FORMAT: ' + s)
    print(inbox.format_subject(s))
    '''
    '''
    r = praw.Reddit(user_agent=accountinfo.user_agent)
    r.login(accountinfo.old_username, accountinfo.password, disable_warning=True)

    r = RedditHandler()

    messages = r.get_inbox(limit=None)
    i = 0
    for message in messages:
        i += 1
        print('Message #: ' + str(i))
        print('Message ID:   ' + str(message.id))
        print('Message Body: ' + message.body)
    print('\n\n\nFinal Count: ' + str(i))

    test = ['yes', 'no', 'maybe', ['yes', 'no', 'maybe']]
    s = '{"test":' + json.dumps(test) + '}'
    j = json.loads(s)
    print(json.dumps(j))
    '''
    test = "-item 6700k, i5 6500k -item bluetooth -body bodytext! -nsfw -email -nsfw -email -subreddits /r/buildapcsales, r/hardwareswap -redditors u/tylerbrockett -ignore-title yaaaay, yooo -ignore-body yay -ignore-title test -ignore-redditors /u/tylerbrockett "
    sub = SubscriptionParser(test)
    print(sub.to_json())
