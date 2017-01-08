"""
==========================================
Author:         Tyler Brockett
Description:    Reddit Bot - buildapcsales
Date Created:   11/13/2015
Date Modified:  01/08/2017
==========================================
"""

import time
import traceback
from sys import stdout
from bot_modules.sleep_handler import SleepHandler
from utils import inbox, times
from utils.color import Color
from utils.logger import Logger
from accounts.accountinfo import bot, old_bot, developer
from bot_modules.reddit_handler import RedditHandler
from bot_modules.crash_handler import handle_crash


class OldBot:
    def __init__(self):
        self.reddit = RedditHandler(old_bot)
        self.start_time = times.get_current_timestamp()

    def start(self):
        while True:
            try:
                unread_messages = self.reddit.get_unread()
                self.handle_messages(unread_messages)
                SleepHandler.sleep(60)
            except KeyboardInterrupt:
                Logger.log('Keyboard Interrupt - Bot Killed', Color.RED)
                exit()
            except:
                handle_crash(traceback.format_exc(), old_bot, reddit=self.reddit)
                Logger.log(traceback.format_exc(), Color.RED)

    def handle_messages(self, unread_messages):
        for message in unread_messages:
            subject = inbox.format_subject(message.subject).lower()
            author = str(message.author).lower()
            if author == 'reddit':
                self.handle_reddit_message(message)
            if subject == 'username mention':
                self.handle_username_mention(message)
            elif subject == 'post reply':
                self.handle_post_reply(message)
            else:
                self.handle_normal_message(message)

    def handle_reddit_message(self, message):
        self.reddit.send_message(developer['username'], 'SALES__BOT - Message from Reddit', message.body)
        message.mark_read()

    def handle_post_reply(self, message):
        author = str(message.author)
        body = message.body
        self.reddit.send_message(developer['username'], "SALES__BOT - Post Reply", 'username: /u/' + author + '\n\n' + body)
        message.mark_read()

    def handle_username_mention(self, message):
        author = str(message.author)
        body = message.body
        self.reddit.send_message(developer['username'], "SALES__BOT - UN Mention", 'username: /u/' + author + '\n\n' + body)
        message.mark_read()

    @staticmethod
    def handle_normal_message(message):
        message.reply(OldBot.compose_message(str(message.author)))
        message.mark_read()
        Logger.log('message from ' + str(message.author) + ' - ' + times.get_formatted_time(), Color.RAINBOW)

    @staticmethod
    def compose_message(username):
        ret = 'Hi /u/' + username + ',\n\t \n' \
            'There have been ***HUGE*** changes to the /r/buildapcsales bot. \n\t\n' \
            'First off, it has changed to /u/' + bot['username'] + '\n\nUnfortunately, the new bot doesn\t have ' \
            'your old subscriptions. Subscriptions were tied to the message ID of your subscription message to the ' \
            'bot, and the new bot couldn\'t reply to the old bot\'s messages. This makes total sense now, but it ' \
            'hadn\'t occurred to me when I started this update. If you want to know your old subscriptions, let me ' \
            'know (/u/' + developer['username'] + ' and I can send them to you.\n\t \n' \
            'You should be able to use /u/' + bot['username'] + ' exactly as you have been using /u/' + \
            old_bot['username'] + ', but there have been MANY new features you may want to take note of. ' \
            '[Take a look here](https://github.com/tylerbrockett/Alert-Bot-Reddit/blob/master/README.md) \n\n'
        return ret


if __name__ == '__main__':
    sales__bot = OldBot()
    sales__bot.start()
