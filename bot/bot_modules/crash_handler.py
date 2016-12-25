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

from accounts.accountinfo import bot, bot_errors
from bot_modules.sleep_handler import SleepHandler
from utils.logger import Logger
from utils.color import Color


def handle_crash(stacktrace, reddit, database, message_dev):
    reset = False
    while not reset:
        SleepHandler.sleep(30)
        try:
            print('Trying to handle error \n\n' + stacktrace)
            reddit.reset()
            database.reset()
            if message_dev:
                print('Messaging Dev - Crash Handler')
                reddit.send_message(bot_errors['username'], bot['username'] + ' - Exception Handled', stacktrace)
            reset = True
        except:
            Logger.log('Failed to restart bot. Trying again in 30 seconds.', Color.RED)
