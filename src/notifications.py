"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

import time
import traceback
from utils.color import Color
from utils.logger import Logger
from utils.env import env, BOT_USERNAME, DEV_USERNAME, SUBREDDIT
from bot_modules.database_handler import DatabaseHandler
from bot_modules.reddit_handler import RedditHandler


class Notifications:

    def __init__(self):
        # self.needs_alert = [[developer['username'], 0]]
        self.needs_alert = []
        self.errors = []
        self.invalid_users = []
        self.db = DatabaseHandler(env(BOT_USERNAME))
        self.reddit = RedditHandler(env(DEV_USERNAME))

    def reset(self):
        reset = False
        while not reset:
            self.reddit.reset()
            self.db.reset()
            reset = True

    def run_alerts(self):
        # if selected_users is empty, send to all, otherwise just send to selected_users
        if not self.needs_alert:
            self.needs_alert = self.db.get_redditors_needing_notification()
            Logger.log(str(len(self.needs_alert)) + '  USERS NEED ALERT')
            time.sleep(20)
        i = 0
        for row in self.needs_alert:
            username = row[0]
            try:
                self.reddit.send_message(username, Notifications.MESSAGE_SUBJECT, Notifications.MESSAGE_BODY)
                self.db.insert_into_notifications(username, 1)
                Logger.log('message sent to ' + username, Color.CYAN)
                i += 1
            except:
                self.errors.append(username)
                Logger.log('ALERT FAILED: ' + username + '\n\t \n\t \n' + traceback.format_exc(), Color.RED)
                exit()

        Logger.log('\n\nSent to ' + str(i) + ' / ' + str(len(self.needs_alert)))
        Logger.log('\n\nExceptions')
        for user in self.invalid_users:
            Logger.log(user)

    def finish_up(self):
        self.db.drop_table_notifications()
        self.db.disconnect()

    MESSAGE_SUBJECT = 'Alert_Bot - Message from developer'
    MESSAGE_BODY = \
        'Hi everyone,' \
        '\t \n\t \n' \
        'Just wanted to give you an update on a couple things.' \
        '\t \n\t \n' \
        'First off, last night I finished updating the bot to use a newer version of the PRAW API for the bot, which ' \
        'was a complete re-write on their end, so many things changed. With this updated API, reddit permalinks ' \
        'changed from the format "https://reddit.com/r/subreddit/blah" to "/r/subreddit/blah". The bot uses the ' \
        'permalink to see if you\'ve already been notified of the post, so to the bot it appeared that no one had ' \
        'received alerts for their subscriptions yet. This means you all got duplicate alerts. I apologize for that, ' \
        'but at least it\'s working "as it should". I was puzzled for a while last night (more like this morning) as ' \
        'to why that was happening, but after a few hours of sleep and a clear mind I had a light bulb moment' \
        '\t \n\t \n' \
        'Secondly, earlier this month I made some changes to the subscription lexer (how the bot parses the messages ' \
        'you all send it). In this process, I removed the comma from the list of reserved tokens by accident, which ' \
        'means it was treated just like a normal character. This means messages like "subscribe -title GTX, 1070" ' \
        'would literally check for the comma in between too (i.e. it would check for exactly "GTX, 1070" in the ' \
        'title). Unfortunately, I didn\'t realize that until yesterday, a couple weeks after the bug was introduced. ' \
        'I only found that out after trying to create a subscription to two subreddits within one subscription ' \
        'yesterday, and it threw some weird exceptions. Luckily I was able to trace it back to the root cause ' \
        'though. That bug "only" affected probably 5 of you (still way more than I\'d have liked...) who used that ' \
        'feature in the last two weeks or so. Unfortunately, that means that you could have missed out on awesome ' \
        'deals during the holiday season, so again I\'m very sorry. I went through the bot\'s messages and manually ' \
        'checked to see who it affected, and updated the database accordingly. I\'m pretty positive I got them all, ' \
        'but if you\'re at all concerned, feel free to re-subscribe to any subscription that has a comma for any ' \
        'parameter.' \
        '\t \n\t \n' \
        'As always, thanks for using the bot everyone, and thanks for your patience! If you have ' \
        'any questions feel free to ask. Happy holidays!' \
        '\t \n\t \n' + \
        \
        '\n\t \n\t \n' \
        '-/u/' + env(DEV_USERNAME) + \
        '\n\t \n\t \n' + \
        env(SUBREDDIT) + ' | [Bot Code](https://github.com/tylerbrockett/Alert-Bot-Reddit)\n'


notifications = Notifications()
try:
    notifications.run_alerts()
    notifications.finish_up()
except:
    Logger.log(traceback.format_exc(), Color.YELLOW)
