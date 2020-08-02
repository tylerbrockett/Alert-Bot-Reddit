"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

from sys import stdout
import time


class SleepHandler:

    @staticmethod
    def sleep(seconds):
        seconds += 1
        for i in range(1, seconds):
            stdout.write('\033[K\r')
            if i % 4 == 0:
                stdout.write('sleeping (' + str(seconds - i) + ') |')
            elif i % 4 == 1:
                stdout.write('sleeping (' + str(seconds - i) + ') /')
            elif i % 4 == 2:
                stdout.write('sleeping (' + str(seconds - i) + ') -')
            elif i % 4 == 3:
                stdout.write('sleeping (' + str(seconds - i) + ') \\')
            stdout.flush()
            time.sleep(1)
        stdout.write('\r \r')
        stdout.flush()
