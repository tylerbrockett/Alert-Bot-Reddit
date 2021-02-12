"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   03/07/2020
Version:            v3.0
==========================================
"""

from accounts.accountinfo import accounts
from bot_modules.sleep_handler import SleepHandler
from utils.logger import Logger
from utils.color import Color


def handle_crash(stacktrace, bot_credentials, message_dev=False, reddit=None, database=None):
    reset = False
    while not reset:
        try:
            Logger.log('Trying to handle error\n', Color.GREEN)
            Logger.log(stacktrace, Color.RED)
            if reddit:
                reddit.reset()
            if database:
                database.reset()
            reddit.send_message(accounts['bot_errors']['username'], bot_credentials['username'] + ' - Exception Handled', stacktrace)
            if message_dev:
                reddit.send_message(accounts['developer']['username'], bot_credentials['username'] + ' - Exception Handled', stacktrace)
                print('Messaging Dev - Crash Handler')
            reset = True
        except:
            Logger.log('Failed to restart bot. Trying again in 30 seconds.', Color.RED)
        SleepHandler.sleep(15)
