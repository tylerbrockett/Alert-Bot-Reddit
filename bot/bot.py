import os
import praw
import time
import sqlite3
import traceback
from private import accounts
from helpers import database, inbox, times, log
from helpers.colorize import colorize


class RedditBot:

    def __init__(self, gui):
        self.force_kill = True
        self.run = False
        self.gui = gui
        self.num_posts = 20
        self.sleep_seconds = 45
        self.start_time = 0
        self.database = None
        self.reddit = None
        self.reddit = praw.Reddit(user_agent=accounts.user_agent)
        self.reddit.set_oauth_app_info(client_id=accounts.client_id,
                                       client_secret=accounts.client_secret,
                                       redirect_uri=accounts.redirect_uri)
        self.last_refreshed = 0
        self.refresh_token()

    def update_status(self, message):
        self.gui.status.update_status(message)

    def start(self):
        self.start_time = times.get_current_timestamp()
        self.gui.uptime_thread.start_time = times.get_current_timestamp()
        self.initialize()
        while not self.force_kill:
            while self.run:
                try:
                    self.check_token_refresh()
                    self.check_for_commands()
                    if self.run:
                        self.read_inbox()
                        self.crawl_subreddit("buildapcsales")
                except KeyboardInterrupt:
                    log.interrupted()
                    exit()
                except:
                    self.handle_crash(traceback.format_exc())
                self.sleep(self.sleep_seconds, "Sleeping")

    '''
    ========================================
            Check For Commands
    ========================================
    '''
    def check_for_commands(self):
        self.update_status("Checking commands")
        unread_messages = []
        try:
            unread_messages = self.reddit.get_unread(limit=None)
        except:
            log.read_inbox_exception()
            self.reddit.send_message(accounts.developer, "Exception Handled - Read Inbox", traceback.format_exc())

        for unread_message in unread_messages:
            self.check_token_refresh()  # Potentially long-running operation, check between each message read
            username, message_id, subject, body = \
                (str(unread_message.author).lower(),
                 unread_message.id,
                 inbox.format_subject(unread_message.subject.lower()),
                 unread_message.body.lower())

            if username == accounts.developer:
                if subject == 'kill' or subject == 'stop' or subject == 'pause':
                    self.run = False
                    try:
                        unread_message.reply("Standing by for further instructions.")
                        unread_message.mark_as_read()
                        colorize('red', '--------- Bot paused by developer ---------')
                    except:
                        self.handle_crash(traceback.format_exc())
                if subject == 'run' or subject == 'start' or subject == 'resume':
                    self.run = True
                    try:
                        unread_message.reply("Thanks, I was getting bored!")
                        unread_message.mark_as_read()
                        colorize('green', '--------- Bot resumed by developer ---------')
                    except:
                        self.handle_crash(traceback.format_exc())

                if subject == 'test':
                    colorize('blue', '--------- I am being tested ---------')
                    try:
                        if self.run:
                            unread_message.reply("Bot is active!")
                        else:
                            unread_message.reply("Bot is INACTIVE!")
                        unread_message.mark_as_read()
                    except:
                        self.handle_crash(traceback.format_exc())

    '''
    ========================================
            Reddit Authentication
    ========================================
    '''

    def check_token_refresh(self):
        self.update_status("Checking token")
        # Check if last token refresh was 60+ minutes ago, give it some buffer though: 3600->3500 seconds
        if times.get_current_timestamp() - self.last_refreshed >= 3500:
            self.refresh_token()

    def refresh_token(self):
        self.update_status("Refreshing token")
        self.reddit.refresh_access_information(accounts.refresh_token)
        self.last_refreshed = times.get_current_timestamp()

    '''
    ========================================
            Database Operations
    ========================================
    '''
    def open_database(self):
        self.update_status("Opening database")
        # Connect to database
        self.database = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + database.DATABASE_LOCATION)
        cursor = self.database.cursor()
        cursor.execute(database.CREATE_TABLE_SUBSCRIPTIONS)
        cursor.execute(database.CREATE_TABLE_MATCHES)
        cursor.execute(database.CREATE_TABLE_ALERTS)

    def close_database(self):
        self.update_status("Closing database")
        if self.database:
            self.database.close()
            self.database = None

    '''
    --------------------------------------------------------------------------------------------------------------------
               Read Inbox
    --------------------------------------------------------------------------------------------------------------------
    '''
    def read_inbox(self):
        self.update_status("Reading inbox")
        i = 0
        unread_messages = []
        try:
            temp = self.reddit.get_unread(limit=None)
            for t in temp:
                unread_messages.append(t)
        except:
            log.read_inbox_exception()
            self.reddit.send_message(accounts.developer, "Exception Handled - Read Inbox", traceback.format_exc())

        for unread_message in unread_messages:
            self.check_token_refresh()  # Potentially long-running operation, check between each message read

            i += 1

            username, message_id, subject, body = \
                (str(unread_message.author).lower(),
                 unread_message.id,
                 inbox.format_subject(unread_message.subject.lower()),
                 unread_message.body.lower())

            if username == "reddit":
                try:
                    self.reddit.send_message(accounts.developer, "FWD FROM REDDIT: " + subject, body)
                    unread_message.mark_as_read()
                except:
                    self.handle_crash(traceback.format_exc())

            elif ('unsubscribe' in body and 'all' in body) \
                    or ('unsubscribe' in subject and 'all' in subject):
                try:
                    cursor = self.database.cursor()
                    cursor.execute(database.REMOVE_ALL_SUBSCRIPTIONS_BY_USERNAME, (username,))
                    cursor.execute(database.REMOVE_ALL_MATCHES_BY_USERNAME, (username,))
                    unread_message.reply(inbox.compose_unsubscribe_all_message(accounts.username, username))
                    unread_message.mark_as_read()
                    self.database.commit()
                    log.unsubscribe_all(username)
                except:
                    self.database.rollback()
                    log.unsubscribe_all_exception(username)
                    self.reddit.send_message(accounts.developer, "Bot Exception - Unsubscribe All", traceback.format_exc())

            elif (body == 'unsubscribe' or body == 'unsub') and subject.replace(' ', '') != '':
                try:
                    cursor = self.database.cursor()
                    cursor.execute(database.REMOVE_ROW_SUBSCRIPTIONS, (username, subject))
                    cursor.execute(database.REMOVE_MATCHES_BY_USERNAME_AND_SUBJECT, (username, subject))
                    unread_message.reply(inbox.compose_unsubscribe_message(accounts.username, username, subject))
                    unread_message.mark_as_read()
                    self.database.commit()
                    log.unsubscribe(username, subject)
                except:
                    self.database.rollback()
                    log.unsubscribe_exception(username, subject)
                    self.reddit.send_message(accounts.developer, "Bot Exception - Unsubscribe", traceback.format_exc())

            # Item must be longer than 2 non-space characters.
            elif (body == 'subscribe' or body == 'sub') and len(inbox.format_subject(subject).replace(' ', '')) > 1:
                subscription = (username, message_id, subject, times.get_current_timestamp())
                try:
                    cursor = self.database.cursor()
                    cursor.execute(database.INSERT_ROW_SUBMISSIONS, subscription)
                    unread_message.reply(inbox.compose_subscribe_message(accounts.username, username, subject))
                    unread_message.mark_as_read()
                    self.database.commit()
                    log.subscribe(username, subject)
                except:
                    self.database.rollback()
                    log.subscribe_exception(username, subject)
                    self.reddit.send_message(accounts.developer, "Bot Exception - Subscribe", traceback.format_exc())

            elif subject == 'information' or subject == 'help' or subject == 'info':
                try:
                    cursor = self.database.cursor()
                    cursor.execute(database.GET_SUBSCRIPTIONS_BY_USERNAME, (username,))
                    unread_message.reply(inbox.compose_information_message(accounts.username, username, cursor.fetchall()))
                    unread_message.mark_as_read()
                    log.information(username)
                except:
                    log.information_exception(username)
                    self.reddit.send_message(accounts.developer, "Bot Exception - Information", traceback.format_exc())

            elif subject == 'subscriptions' or subject == 'subs':
                try:
                    cursor = self.database.cursor()
                    cursor.execute(database.GET_SUBSCRIPTIONS_BY_USERNAME, (username,))
                    unread_message.reply(inbox.compose_subscriptions_message(accounts.username, username, cursor.fetchall()))
                    unread_message.mark_as_read()
                    log.subscriptions(username)
                except:
                    log.subscriptions_exception(username)
                    self.reddit.send_message(accounts.developer, "Bot Exception - Subscriptions", traceback.format_exc())

            elif subject == 'feedback':
                try:
                    self.reddit.send_message(accounts.developer, "Feedback for sales__bot",
                                             inbox.compose_feedback_forward(accounts.username, username, body))
                    unread_message.reply(inbox.compose_feedback_message(accounts.username, username))
                    unread_message.mark_as_read()
                    log.feedback(username, body)
                except:
                    log.feedback_exception(username, body)
                    self.reddit.send_message(accounts.developer, "Bot Exception - Feedback", traceback.format_exc())
            else:
                try:
                    unread_message.reply(inbox.compose_default_message(accounts.username, username, subject, body))
                    unread_message.mark_as_read()
                    log.default(username, subject, body)
                except:
                    log.default_exception(username, subject, body)
                    self.reddit.send_message(accounts.developer, "Bot Exception - Default", traceback.format_exc())
            self.sleep(2, "Reading inbox (" + str(i) + "/" + str(len(unread_messages)) + ")  ")
        # colorize('cyan', str(i) + ' unread messages')

    '''
    --------------------------------------------------------------------------------------------------------------------
               Crawl Subreddit
    --------------------------------------------------------------------------------------------------------------------
    '''
    def crawl_subreddit(self, subreddit):
        submissions = []
        try:
            submissions = self.reddit.get_subreddit(subreddit).get_new(limit=self.num_posts)
        except:
            log.get_submissions_exception()
            self.reddit.send_message(accounts.developer, "Bot Exception - Crawl Subreddit", traceback.format_exc())
        for submission in submissions:
            self.update_status("Checking submission")
            # Make sure sale is not expired!
            if not submission.over_18:
                self.check_for_subscription(submission)

    '''
    --------------------------------------------------------------------------------------------------------------------
               Check Submission for Subscription
    --------------------------------------------------------------------------------------------------------------------
    '''
    def check_for_subscription(self, submission):
        title = submission.title.lower()
        text = submission.selftext.lower()
        permalink = submission.permalink
        url = submission.url

        for item in self.database.cursor().execute(database.SELECT_DISTINCT_ITEMS).fetchall():
            if item[0] in title or item[0] in text:
                matches = self.database.cursor().execute(database.GET_SUBSCRIBED_USERS_WITHOUT_LINK,
                                                         (item[0], permalink)).fetchall()
                i = 0
                for match in matches:
                    i += 1
                    self.handle_item_match(match[database.COL_SUB_USERNAME],
                                           match[database.COL_SUB_ITEM],
                                           match[database.COL_SUB_MESSAGE_ID],
                                           title,
                                           permalink,
                                           url, i, len(matches))

    '''
    --------------------------------------------------------------------------------------------------------------------
               Handle Subscription/Submission Match
    --------------------------------------------------------------------------------------------------------------------
    '''
    def handle_item_match(self, username, item, message_id, title, permalink, url, match_num, num_matches):
        self.check_token_refresh()  # Potentially long-running operation, check between each match
        try:
            message = self.reddit.get_message(message_id)
            self.database.cursor().execute(database.INSERT_ROW_MATCHES,
                                           (username, item, permalink, times.get_current_timestamp()))
            message.reply(inbox.compose_match_message(accounts.username, username, item, title, permalink, url))
            self.database.commit()
            log.match(username, item, message_id, title, permalink, url)
        except:
            self.database.rollback()
            log.match_exception(username, item, message_id, title, permalink, url)
            self.reddit.send_message(accounts.developer, "Exception Handled - Handle Item Match", traceback.format_exc())
        self.sleep(2, "Handling match (" + str(match_num) + "/" + str(num_matches) + ")  ")

    '''
    ====================================================================================================================
               Other Useful Functions
    ====================================================================================================================
    '''
    def sleep(self, seconds, message):
        for i in range(seconds, 0, -1):
            if self.run:
                self.update_status(message + ' (' + str(i) + ')')
                time.sleep(1)

    '''
    =======================================================================
            Crash-Handling Stuff
    =======================================================================
    '''

    def initialize(self):
        self.update_status("Initializing..")
        self.destroy()  # In case the bot was previously running.
        self.refresh_token()
        self.open_database()

    def destroy(self):
        self.update_status("Destroying..")
        self.close_database()
        colorize("red", "---------------------- DESTROYED ----------------------")

    def handle_crash(self, stacktrace):
        self.update_status("Handing Crash..")
        self.destroy()
        reset = False
        while not reset:
            try:
                self.initialize()
                self.reddit.send_message(accounts.developer, "Exception Handled", stacktrace)
            except:
                self.sleep(15, "Bot crashed, sleeping")
