"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   10/6/2016
Version:            v0.1
==========================================
"""

from bot_modules.command_handler import CommandHandler
from bot_modules.database_handler import DatabaseHandler
from bot_modules.inbox_handler import InboxHandler
from bot_modules.match_handler import MatchHandler
from bot_modules.reddit_handler import RedditHandler
from bot_modules.sleep_handler import SleepHandler
from bot_modules.subscription_handler import SubscriptionHandler
from private import accountinfo
import traceback
from utils import times
from utils.color import Color
from utils.logger import Logger


class AlertBot:
    def __init__(self):
        self.start_time = times.get_current_timestamp()
        self.run = True
        self.sleep_seconds = 45
        self.num_posts = 20
        self.database = DatabaseHandler()
        self.reddit = RedditHandler()

    def run(self):
        Logger.log(Color.GREEN, 'Starting bot...')
        while True:
            try:
                self.check_for_commands()
                if self.run:
                    InboxHandler.read_inbox(self.database, self.reddit)
                    subscriptions = self.database.get_subscriptions()
                    matches = SubscriptionHandler.find_matches(subscriptions)
                    MatchHandler.handle_matches(self.reddit, self.database, matches)
                    self.database.purge_old_matches()
                    Logger.log(Color.YELLOW, times.get_time_passed(self.start_time))
            except KeyboardInterrupt:
                Logger.log(Color.RED, 'Keyboard Interrupt - Bot killed')
                exit()
            except:
                self.handle_crash(traceback.format_exc())
            SleepHandler.sleep(self.sleep_seconds)

    def check_for_commands(self):
        Logger.log('Checking for commands')
        commands = CommandHandler.get_commands(self.reddit)
        if CommandHandler.PAUSE in commands:
            self.run = False
        if CommandHandler.RUN in commands:
            self.run = True
        if CommandHandler.KILL in commands:
            exit()

    def handle_crash(self, stacktrace):
        reset = False
        while not reset:
            try:
                self.reddit.reset()
                self.database.reset()
                self.reddit.send_message(accountinfo.developerusername, "Exception Handled", stacktrace)
                reset = True
            except:
                SleepHandler.sleep(15)
