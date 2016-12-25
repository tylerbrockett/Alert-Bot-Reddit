"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   12/20/2016
Version:            v2.0
==========================================
"""

from bot_modules.command_handler import CommandHandler
from bot_modules.database_handler import DatabaseHandler
from bot_modules.inbox_handler import InboxHandler
from bot_modules.match_handler import MatchHandler
from bot_modules.reddit_handler import RedditHandler
from bot_modules.sleep_handler import SleepHandler
from bot_modules.match_finder import MatchFinder
import traceback
from utils import times
from utils.color import Color
from utils.logger import Logger
from bot_modules.crash_handler import handle_crash
from accounts.accountinfo import bot


class AlertBot:
    def __init__(self):
        self.start_time = times.get_current_timestamp()
        self.run = True
        self.database = DatabaseHandler()
        self.reddit = RedditHandler(bot)

    def start(self):
        Logger.log('Starting bot...', Color.GREEN)
        while True:
            try:
                self.check_for_commands()
                if self.run:
                    InboxHandler.read_inbox(self.database, self.reddit)
                    subscriptions = self.database.get_subscriptions()
                    Logger.log(str(len(subscriptions)) + ' Subs')
                    matches = MatchFinder.find_matches(subscriptions, self.reddit, self.database)
                    Logger.log(str(len(matches)) + ' Matches')
                    MatchHandler.send_messages(self.reddit, self.database, matches)
                    self.database.purge_old_matches()
                    Logger.log(times.get_time_passed(self.start_time), Color.YELLOW)
                SleepHandler.sleep(20)
            except KeyboardInterrupt:
                Logger.log('Keyboard Interrupt - Bot killed', Color.RED)
                exit()
            except:
                handle_crash(traceback.format_exc(), self.reddit, self.database, True)

    def check_for_commands(self):
        Logger.log('Checking for commands')
        commands = CommandHandler.get_commands(self.reddit)
        if CommandHandler.PAUSE in commands:
            self.run = False
        if CommandHandler.RUN in commands:
            self.run = True
        if CommandHandler.KILL in commands:
            exit()

if __name__ == '__main__':
    bot = AlertBot()
    bot.start()
