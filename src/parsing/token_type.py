"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""


class TokenType:
    # SUBSCRIPTION TOKENS
    BODY = 1
    IGNORE_BODY = 5
    TITLE = 2
    IGNORE_TITLE = 6
    REDDITORS = 3
    IGNORE_REDDITORS = 7
    SUBREDDITS = 4
    EMAIL = 8
    NSFW = 9
    COMMA = 10

    # MESSAGE TOKENS
    STATISTICS = 20
    SUBSCRIPTIONS = 21
    UNSUBSCRIBE = 22
    ALL = 23
    SUBSCRIBE = 24
    EDIT = 25
    HELP = 26
    FEEDBACK = 27
    NUM_SYMBOL = 28

    # EDIT TOKENS
    NUM = 30

    # OTHER
    ERROR = 100
    EOF = 101
    NO_TOKEN = 102
    TOKEN = 103
