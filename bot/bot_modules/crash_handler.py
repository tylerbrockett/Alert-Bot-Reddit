"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   12/2/2016
Version:            v2.0
==========================================
"""

from accounts import accountinfo
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
                print('Message Dev')
                reddit.send_message(accountinfo.bot_errors, accountinfo.username + " - Exception Handled", stacktrace)
            reset = True
        except:
            Logger.log(Color.RED, 'Failed to restart bot. Trying again in 30 seconds.')
