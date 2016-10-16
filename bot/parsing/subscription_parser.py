from subscription_lexer import SubscriptionLexer
from subscription_lexer import SubscriptionLexerException
from token_type import TokenType


class SubscriptionParser:
    statement_token_types = [TokenType.ITEMS, TokenType.SITES, TokenType.REDDITORS, TokenType.SUBREDDITS, TokenType.IGNORE_ITEMS,
                             TokenType.IGNORE_SITES, TokenType.IGNORE_REDDITORS, TokenType.EMAIL]

    statement_tokens = ['-site', '-sites', '-item', '-items', '-subreddit', '-subreddits', '-ignore-site', '-ignore-sites',
                        '-ignore-item', '-ignore-items', '-ignore-subreddit', '-ignore-subreddits', '-email', '-hide-nsfw']

    def unget_token(self):
        self.index -= 1

    def get_token(self):
        self.index += 1
        if self.index >= len(self.tokens) or self.index < 0:
            raise SubscriptionParserException('Error - Index out of bounds [' + str(self.index) + ']')
        return self.tokens[self.index]

    def __init__(self, sub):
        self.items = []
        self.sites = []
        self.ignore_items = []
        self.ignore_sites = []
        self.redditors = []
        self.ignore_redditors = []
        self.subreddits = []
        self.settings = []
        self.index = -1
        self.tokens = []
        try:
            self.tokens = SubscriptionLexer(sub).tokenize()
        except:
            raise SubscriptionLexerException("Error - subscription __init __ - Lexing Subscription")
        self.parse_subscription()

    def parse_subscription(self):
        token, ttype = self.get_token()
        if ttype is TokenType.TOKEN:
            self.unget_token()
            self.parse_items_list()
        elif ttype in SubscriptionParser.statement_token_types:
            self.unget_token()
            self.parse_statement_list()
        elif ttype is TokenType.EOF:
            return
        self.parse_subscription()

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
        if ttype is TokenType.ITEMS:
            self.parse_items_list()
        elif ttype is TokenType.SITES:
            self.parse_sites_list()
        elif ttype is TokenType.REDDITORS:
            self.parse_redditors_list()
        elif ttype is TokenType.SUBREDDITS:
            self.parse_subreddits_list()
        elif ttype is TokenType.IGNORE_ITEMS:
            self.parse_ignore_items_list()
        elif ttype is TokenType.IGNORE_SITES:
            self.parse_ignore_sites_list()
        elif ttype is TokenType.IGNORE_REDDITORS:
            self.parse_ignore_redditors_list()
        elif ttype is TokenType.EMAIL:
            self.parse_email()
        elif ttype is TokenType.NSFW:
            self.parse_hide_nsfw()
        else:
            raise SubscriptionParserException('Error - parse_statement_list - Expected ' + str(SubscriptionParser.statement_tokens))

    def parse_items_list(self):
        self.items += self.parse_list([])

    def parse_sites_list(self):
        self.sites += self.parse_list([])

    def parse_redditors_list(self):
        self.redditors += self.parse_list([])

    def parse_subreddits_list(self):
        self.subreddits += self.parse_list([])

    def parse_email(self):
        self.settings += ['email', True]

    def parse_hide_nsfw(self):
        self.settings += ['hide-nsfw', True]

    def parse_ignore_items_list(self):
        self.ignore_items += self.parse_list([])

    def parse_ignore_sites_list(self):
        self.ignore_sites += self.parse_list([])

    def parse_ignore_redditors_list(self):
        self.ignore_redditors += self.parse_list([])

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
