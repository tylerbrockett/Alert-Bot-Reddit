"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   11/28/2016
Version:            v2.0
==========================================
"""

from sys import stdout
import time


class SleepHandler:

    @staticmethod
    def sleep(seconds):
        print 'Sleeping',
        for i in range(seconds):
            stdout.write(".")
            stdout.flush()
            time.sleep(1)
        print ''
