"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

from datetime import datetime
import time
from utils.logger import Logger
from utils.color import Color


class TimeHelper:
    def __init__(self, quiet_start=0, quiet_end=0):
        if quiet_end < quiet_start:
            Logger.log('Invalid Quiet Hours.', Color.RED)
            exit()
        self.quiet_start = quiet_start
        self.quiet_stop = quiet_end
        self.is_quiet = False

    # return true if state changes, false if it stays the same
    def check_time(self):
        t = datetime.now().time()
        if self.quiet_start <= t.hour <= self.quiet_stop:
            previous_state = self.is_quiet
            self.is_quiet = True
            if previous_state is False:
                return True
            else:
                return False
        else:
            previous_state = self.is_quiet
            self.is_quiet = False
            if previous_state is True:
                return True
            else:
                return False

    def is_quiet_hours(self):
        return self.is_quiet


def get_formatted_time():
    return time.strftime('%I:%M:%S%p on %A, %B %d, %Y')


def get_current_timestamp():
    return time.time()


def get_time_passed(timestamp):
    now = datetime.now()
    then = datetime.fromtimestamp(timestamp)
    delta = now - then

    days = delta.days
    seconds = delta.seconds

    if days == 0 and seconds == 0:
        return "0s "
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    result = ''
    if days > 0:
        result += '%sd ' % days
    if hours > 0:
        result += '%sh ' % hours
    if minutes > 0:
        result += '%sm ' % minutes
    if seconds > 0:
        result += '%ss' % seconds

    return result
