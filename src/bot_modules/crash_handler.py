"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

from bot_modules.sleep_handler import SleepHandler
from utils.logger import Logger
from utils.color import Color
from utils.env import env, ERROR_USERNAME, BOT_USERNAME, DEV_USERNAME

def handle_crash(stacktrace, message_dev=False, reddit=None, database=None):
    reset = False
    while not reset:
        try:
            Logger.log('Trying to handle error\n', Color.GREEN)
            Logger.log(stacktrace, Color.RED)
            if reddit:
                reddit.reset()
            if database:
                database.reset()
            reddit.send_message(env(ERROR_USERNAME), env(BOT_USERNAME) + ' - Exception Handled', stacktrace)
            if message_dev:
                reddit.send_message(env(DEV_USERNAME), env(BOT_USERNAME) + ' - Exception Handled', stacktrace)
                print('Messaging Dev - Crash Handler')
            reset = True
        except Exception as e:
            Logger.log('Failed to restart bot. Trying again in 30 seconds.', Color.RED)
        SleepHandler.sleep(15)
