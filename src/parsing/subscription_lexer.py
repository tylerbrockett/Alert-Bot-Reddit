"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

from parsing.token_type import TokenType
import traceback


class SubscriptionLexer:
    FALSE = 0
    original_string = ''
    active_index = 0
    EOF = False
    active_token = False
    token = ''
    token_type = TokenType.NO_TOKEN
    whitespace = [' ', '\n', '\r']

    title_keywords = ['-title', '-item', '-items']
    body_keywords = ['-body', '-site', '-sites', '-url', '-content', '-selftext', '-link']
    redditors_keywords = ['-redditor', '-redditors', '-user', '-users']
    ignore_title_keywords = ['-ignore-title', '-ignore-item', '-ignore-items']
    ignore_body_keywords = ['-ignore-body', '-ignore-site', '-ignore-sites', '-ignore-url', '-ignore-content', '-ignore-selftext', '-ignore-link']
    ignore_redditors_keywords = ['-ignore-redditor', '-ignore-redditors', '-ignore-user', '-ignore-users']
    subreddit_keywords = ['-subreddit', '-subreddits', '-sub', '-subs', '-reddit', '-red']
    nsfw_keywords = ['-nsfw', '-show-nsfw']
    email_keywords = ['-email']
    symbols_keywords = [',']

    reserved_tokens = sum(
        [title_keywords, body_keywords, redditors_keywords,
         ignore_title_keywords, ignore_body_keywords, ignore_redditors_keywords,
         subreddit_keywords,
         nsfw_keywords, email_keywords,
         symbols_keywords],
        [])

    def __init__(self, sub):
        self.original_string = sub

    def skip_space(self):
        c = self.get_char()
        while not self.EOF and (c == ' ' or c == '\n' or c == '\r'):
            c = self.get_char()
        if not self.EOF:
            self.unget_char()

    def is_keyword(self, token):
        if token.lower() in SubscriptionLexer.title_keywords:
            return TokenType.TITLE
        elif token.lower() in SubscriptionLexer.body_keywords:
            return TokenType.BODY
        elif token.lower() in SubscriptionLexer.redditors_keywords:
            return TokenType.REDDITORS
        elif token.lower() in SubscriptionLexer.ignore_title_keywords:
            return TokenType.IGNORE_TITLE
        elif token.lower() in SubscriptionLexer.ignore_body_keywords:
            return TokenType.IGNORE_BODY
        elif token.lower() in SubscriptionLexer.ignore_redditors_keywords:
            return TokenType.IGNORE_REDDITORS
        elif token.lower() in SubscriptionLexer.subreddit_keywords:
            return TokenType.SUBREDDITS
        elif token.lower() in SubscriptionLexer.email_keywords:
            return TokenType.EMAIL
        elif token.lower() in SubscriptionLexer.nsfw_keywords:
            return TokenType.NSFW
        return self.FALSE

    def unget_token(self):
        self.active_token = True

    def unget_char(self):
        self.active_index -= 1

    def get_char(self):
        if self.active_index < len(self.original_string):
            char = str(self.original_string[self.active_index])
            self.active_index += 1
            return char
        else:
            self.EOF = True
            return ''

    def scan_token(self):
        self.token_type = TokenType.NO_TOKEN
        c = self.get_char()
        while c not in SubscriptionLexer.whitespace and c != '' and c not in self.reserved_tokens:
            self.token += c
            c = self.get_char()
        if not self.EOF:
            self.unget_char()
        self.token_type = self.is_keyword(self.token)
        if self.token_type == self.FALSE:
            self.token_type = TokenType.TOKEN
        return self.token_type

    def get_token(self):
        if self.active_token:
            self.active_token = False
            return self.token_type

        self.skip_space()
        self.token = ''

        c = self.get_char()
        if c == ',':
            self.token_type = TokenType.COMMA
            self.token = c
        else:
            if self.EOF:
                self.token_type = TokenType.EOF
            else:
                self.unget_char()
                self.token_type = self.scan_token()
        return self.token, self.token_type

    def is_alpha(self, char):
        return isinstance(char, str)

    def is_num(self, char):
        return isinstance(char, (int, long, float, complex))

    def is_alpha_num(self, char):
        if self.is_alpha(char) or self.is_num(char):
            return True
        return False

    def tokenize(self):
        tokens = []
        try:
            while self.token_type != TokenType.EOF:
                token = self.get_token()
                tokens.append(token)
            return tokens
        except:
            print(traceback.format_exc())
            raise SubscriptionLexerException('Exception occurred')


class SubscriptionLexerException(Exception):
    def __init__(self, errorArgs):
        Exception.__init__(self, 'Subscription Lexer Exception: {0}'.format(errorArgs))
        self.errorArgs = errorArgs
