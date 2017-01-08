"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   01/08/2017
Version:            v2.0
==========================================
"""

from accounts.accountinfo import bot_errors, developer
from bot_modules.sleep_handler import SleepHandler
from utils.logger import Logger
from utils.color import Color


def handle_crash(stacktrace, bot_credentials, message_dev=False, reddit=None, database=None):
    reset = False
    while not reset:
        SleepHandler.sleep(30)
        try:
            print('Trying to handle error \n\n' + stacktrace)
            if reddit:
                reddit.reset()
            if database:
                database.reset()
            reddit.send_message(bot_errors['username'], bot_credentials['username'] + ' - Exception Handled', stacktrace)
            if message_dev:
                reddit.send_message(developer['username'], bot_credentials['username'] + ' - Exception Handled', stacktrace)
                print('Messaging Dev - Crash Handler')
            reset = True
        except:
            Logger.log('Failed to restart bot. Trying again in 30 seconds.', Color.RED)
