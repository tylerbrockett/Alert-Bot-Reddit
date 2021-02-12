"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       03/06/2020
Date Last Edited:   03/06/2020
Version:            v3.0
==========================================
"""

from utils.color import Color
from utils.logger import Logger
from bot_modules.crash_handler import handle_crash
from accounts.accountinfo import accounts
from bot_modules.reddit_handler import RedditHandler


class MarkRead:

    def __init__(self, bot_name):
        self.reddit = RedditHandler(accounts['developer'])
        self.bot_account = accounts[bot_name]['username']

    def reset(self):
        reset = False
        while not reset:
            self.reddit.reset()
            reset = True

    def mark_read(self):
        Logger.log('Reading inbox...', Color.GREEN)
        unread = self.reddit.get_unread()
        unread.reverse() # back to original order

        Logger.log(str(len(unread)) + ' Unread Messages', Color.GREEN)

        num_messages = 0
        num_marked_read = 0
        for message in unread:
            num_messages += 1
            username = str(message.author).lower()
            if username == self.bot_account and message.subject == self.bot_account + ' - Exception Handled':
                message.mark_read()
                num_marked_read += 1
                Logger.log(str(num_marked_read) + ' marked read')

        Logger.log(str(num_messages) + ' unread ERROR messages handled', Color.YELLOW)
        Logger.log(str(num_marked_read) + ' ERROR messages marked read', Color.YELLOW)

        return num_marked_read
