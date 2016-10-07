"""
==========================================
Author:         Tyler Brockett
Description:    Sales Bot
Date:           10/6/2016
==========================================
"""

import os
import time
import praw
import sqlite3
import traceback
from sys import stdout

from helpers import color, times, database, inbox, output
from private import accountinfo
from bot_modules.database_helper import DBHelper


class SalesBot:
    def __init__(self):
        self.run = True
        self.sleep_seconds = 45
        self.num_posts = 20
        self.db = DBHelper()
        self.reddit = self.connect_to_reddit()
        self.subscriptions = []


    def destroy(self):

        self.reddit = None
        color.print_color('red', '----------------- DESTROYED -----------------')

    def initialize(self):
        self.connection = self.connect_to_database()
        self.reddit = self.connect_to_reddit()

    def handle_crash(stacktrace):
        global connection, reddit
        destroy()
        reset = False
        while not reset:
            try:
                initialize()
                reddit.send_message(accountinfo.developerusername, "Exception Handled", stacktrace)
                reset = True
            except:
                sleep(15)

    def sleep(self, seconds):
        print 'Sleeping',
        for i in range(seconds):
            stdout.write(".")
            stdout.flush()
            time.sleep(1)
        print ''
