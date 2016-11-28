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

    # EDIT TOKENS
    NUM = 30

    # OTHER
    ERROR = 100
    EOF = 101
    NO_TOKEN = 102
    TOKEN = 103
