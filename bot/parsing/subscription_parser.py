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

from parsing.subscription_lexer import SubscriptionLexer
from utils.subscription import Subscription
from parsing.token_type import TokenType
import json


class SubscriptionParser:
    statement_token_types = [TokenType.TITLE, TokenType.BODY, TokenType.REDDITORS, TokenType.SUBREDDITS, TokenType.IGNORE_TITLE,
                             TokenType.IGNORE_BODY, TokenType.IGNORE_REDDITORS, TokenType.EMAIL, TokenType.NSFW]

    statement_tokens = [
        # TITLE
        '-title', '-item', '-items',
        # BODY
        '-body', '-site', '-sites', '-url',
        # SUBREDDIT
        '-subreddit', '-subreddits',
        # REDDITORS
        '-redditor', '-redditors',
        # IGNORE BODY
        '-ignore-body', '-ignore-site', '-ignore-sites',
        # IGNORE TITLE
        '-ignore-title', '-ignore-item', '-ignore-items',
        # IGNORE REDDITORS
        '-ignore-redditor', '-ignore-redditors',
        # FLAGS
        '-nsfw',
        '-email'
    ]

    def unget_token(self):
        self.index -= 1

    def get_token(self):
        self.index += 1
        if self.index >= len(self.tokens) or self.index < 0:
            raise SubscriptionParserException('Error - Index out of bounds [' + str(self.index) + ']')
        return self.tokens[self.index]

    def __init__(self, sub):
        self.index = -1
        self.data = {
            Subscription.TITLE: [],
            Subscription.BODY: [],
            Subscription.IGNORE_TITLE: [],
            Subscription.IGNORE_BODY: [],
            Subscription.REDDITORS: [],
            Subscription.IGNORE_REDDITORS: [],
            Subscription.SUBREDDITS: [],
            Subscription.NSFW: False,
            Subscription.EMAIL: False,
            Subscription.SCHEMA_VERSION: Subscription.CURRENT_SCHEMA_VERSION
        }
        try:
            self.tokens = SubscriptionLexer(sub).tokenize()
            self.parse_subscription()
            self.final_checks()
            self.data[Subscription.VALID] = True
        except:
            raise SubscriptionParserException('SubscriptionParser __init__ - Malformed Subscription')

    def get_data(self):
        return self.data

    def to_json(self):
        return json.dumps(self.data, indent=2)

    def final_checks(self):
        for term_list in self.data[Subscription.TITLE]:
            if len(term_list) == 1 and term_list[0] == '*':
                self.data[Subscription.TITLE] = []
                return
        if not self.data[Subscription.SUBREDDITS]:
            self.data[Subscription.SUBREDDITS] = ['buildapcsales']

    def parse_subscription(self):
        token, ttype = self.get_token()
        if ttype is TokenType.TOKEN:
            self.unget_token()
            self.parse_title_list()
            t, tt = self.get_token()
            if tt != TokenType.EOF:
                self.parse_statement_list()
            else:
                self.unget_token()
        elif ttype in SubscriptionParser.statement_token_types:
            self.unget_token()
            self.parse_statement_list()
        token, ttype = self.get_token()
        if ttype != TokenType.EOF:
            raise SubscriptionParserException('Expecting EOF')

    def parse_statement_list(self):
        token, ttype = self.get_token()
        if ttype in SubscriptionParser.statement_token_types:
            self.unget_token()
            self.parse_statement()
            token, ttype = self.get_token()
            if ttype in SubscriptionParser.statement_token_types:
                self.unget_token()
                self.parse_statement_list()
            else:
                self.unget_token()
        else:
            raise SubscriptionParserException('Error - parse_statement_list - Expected ' + str(SubscriptionParser.statement_tokens))

    def parse_statement(self):
        token, ttype = self.get_token()
        if ttype is TokenType.TITLE:
            self.parse_title_list()
        elif ttype is TokenType.BODY:
            self.parse_body_list()
        elif ttype is TokenType.REDDITORS:
            self.parse_redditors_list()
        elif ttype is TokenType.SUBREDDITS:
            self.parse_subreddits_list()
        elif ttype is TokenType.IGNORE_TITLE:
            self.parse_ignore_title_list()
        elif ttype is TokenType.IGNORE_BODY:
            self.parse_ignore_body_list()
        elif ttype is TokenType.IGNORE_REDDITORS:
            self.parse_ignore_redditors_list()
        elif ttype is TokenType.EMAIL:
            self.parse_email()
        elif ttype is TokenType.NSFW:
            self.parse_nsfw()
        else:
            raise SubscriptionParserException('Error - parse_statement_list - Expected ' + str(SubscriptionParser.statement_tokens))

    def parse_title_list(self):
        title_list = sorted(set(self.parse_list([])))
        if title_list not in self.data[Subscription.TITLE]:
            self.data[Subscription.TITLE].append(title_list)
            self.data[Subscription.TITLE].sort()

    def parse_body_list(self):
        body_list = sorted(set(self.parse_list([])))
        if body_list not in self.data[Subscription.BODY]:
            self.data[Subscription.BODY].append(body_list)
            self.data[Subscription.BODY].sort()

    def parse_redditors_list(self):
        redditor_list = self.parse_list([])
        redditor_list = [r.lower().replace('/u/', '') for r in redditor_list]
        redditor_list = [r.lower().replace('u/', '') for r in redditor_list]
        redditor_list = sorted(set(redditor_list))
        for redditor in redditor_list:
            if redditor not in self.data[Subscription.REDDITORS]:
                self.data[Subscription.REDDITORS].append(redditor)
                self.data[Subscription.REDDITORS].sort()

    def parse_subreddits_list(self):
        subreddit_list = self.parse_list([])
        subreddit_list = [s.lower().replace('/r/', '') for s in subreddit_list]
        subreddit_list = [s.lower().replace('r/', '') for s in subreddit_list]
        subreddit_list = sorted(set(subreddit_list))
        for subreddit in subreddit_list:
            if subreddit not in self.data[Subscription.SUBREDDITS]:
                self.data[Subscription.SUBREDDITS].append(subreddit)
                self.data[Subscription.SUBREDDITS].sort()

    def parse_email(self):
        self.data[Subscription.EMAIL] = True

    def parse_nsfw(self):
        self.data[Subscription.NSFW] = True

    def parse_ignore_title_list(self):
        ignore_list = sorted(set(self.parse_list([])))
        for item in ignore_list:
            if item not in self.data[Subscription.IGNORE_TITLE]:
                self.data[Subscription.IGNORE_TITLE].append(item)
                self.data[Subscription.IGNORE_TITLE].sort()

    def parse_ignore_body_list(self):
        ignore_list = sorted(set(self.parse_list([])))
        for item in ignore_list:
            if item not in self.data[Subscription.IGNORE_BODY]:
                self.data[Subscription.IGNORE_BODY].append(item)
                self.data[Subscription.IGNORE_BODY].sort()

    def parse_ignore_redditors_list(self):
        ignore_list = self.parse_list([])
        ignore_list = [r.lower().replace('/u/', '') for r in ignore_list]
        ignore_list = [r.lower().replace('u/', '') for r in ignore_list]
        ignore_list = sorted(set(ignore_list))
        for item in ignore_list:
            if item not in self.data[Subscription.IGNORE_REDDITORS]:
                self.data[Subscription.IGNORE_REDDITORS].append(item)
                self.data[Subscription.IGNORE_REDDITORS].sort()

    def parse_list(self, ret):
        token, ttype = self.get_token()
        if ttype is TokenType.TOKEN:
            self.unget_token()
            ret += [self.parse_element('')]
            token, ttype = self.get_token()
            if ttype is TokenType.COMMA:
                token, ttype = self.get_token()
                if ttype is TokenType.TOKEN:
                    self.unget_token()
                    return self.parse_list(ret)
                else:
                    raise SubscriptionParserException('Error - parse_list - Expected TOKEN after COMMA or SEMICOLON')
            else:
                self.unget_token()
                return ret
        else:
            raise SubscriptionParserException('Error - parse_list - Expected TOKEN')

    def parse_element(self, ret):
        token, ttype = self.get_token()
        if ttype is TokenType.TOKEN:
            if ret is '':
                ret += token
            else:
                ret += ' ' + token
            token, ttype = self.get_token()
            if ttype is TokenType.TOKEN:
                self.unget_token()
                return self.parse_element(ret)
            else:
                self.unget_token()
            return ret
        else:
            raise SubscriptionParserException('Error - parse_element - Expected TOKEN')


class SubscriptionParserException(Exception):
    def __init__(self, errorArgs):
        Exception.__init__(self, "Subscription Parser Exception: {0}".format(errorArgs))
        self.errorArgs = errorArgs
