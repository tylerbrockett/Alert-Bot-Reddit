from subscription_lexer import SubscriptionLexer
from subscription_lexer import SubscriptionLexerException
from token_type import TokenType


class SubscriptionParser:

    def ungetToken(self):
        self.index -= 1

    def getToken(self):
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
        token, ttype = self.getToken()
        if ttype is TokenType.TOKEN:
            self.ungetToken()
            self.parse_item_list(False)
        elif ttype in [TokenType.ITEM, TokenType.ITEMS, TokenType.SITE, TokenType.SITES, TokenType.IGNORE, TokenType.EMAIL, TokenType.SUBREDDIT, TokenType.SUBREDDITS]:
            self.ungetToken()
            self.parse_statement_list()
        elif ttype is TokenType.EOF:
            return
        self.parse_subscription()

    def parse_statement_list(self):
        token, ttype = self.getToken()
        if ttype in [TokenType.ITEM, TokenType.ITEMS, TokenType.SITE, TokenType.SITES, TokenType.IGNORE, TokenType.EMAIL, TokenType.SUBREDDIT, TokenType.SUBREDDITS]:
            self.ungetToken()
            self.parse_statement()
            token, ttype = self.getToken()
            if ttype in [TokenType.ITEM, TokenType.ITEMS, TokenType.SITE, TokenType.SITES, TokenType.IGNORE, TokenType.EMAIL, TokenType.SUBREDDIT, TokenType.SUBREDDITS]:
                self.ungetToken()
                self.parse_statement_list()
            else:
                self.ungetToken()
        else:
            raise SubscriptionParserException('Error - parse_statement_list - Expected "ITEM", "ITEMS", "SITE", "SITES", "IGNORE", "EMAIL", "SUBREDDIT", or "SUBREDDITS"')

    def parse_statement(self):
        token, ttype = self.getToken()
        if ttype is TokenType.ITEM or ttype is TokenType.ITEMS:
            token, ttype = self.getToken()
            if ttype is TokenType.COLON:
                self.parse_item_list(False)
            else:
                raise SubscriptionParserException('Error - parse_statement - Expected COLON')
        elif ttype is TokenType.SITE or ttype is TokenType.SITES:
            token, ttype = self.getToken()
            if ttype is TokenType.COLON:
                self.parse_site_list(False)
            else:
                raise SubscriptionParserException('Error - parse_statement - Expected COLON')
        elif ttype is TokenType.EMAIL:
            self.parse_email()
        elif ttype is TokenType.IGNORE:
            token, ttype = self.getToken()
            if ttype is TokenType.ITEM or ttype is TokenType.ITEMS:
                token, ttype = self.getToken()
                if ttype is TokenType.COLON:
                    self.parse_item_list(True)
                else:
                    raise SubscriptionParserException('Error - parse_statement - Expected COLON')
            elif ttype is TokenType.SITE or ttype is TokenType.SITES:
                token, ttype = self.getToken()
                if ttype is TokenType.COLON:
                    self.parse_site_list(True)
                else:
                    raise SubscriptionParserException('Error - parse_statement - Expected COLON')
            else:
                raise SubscriptionParserException('Error - parse_statement - Expected "ITEM", "ITEMS", "SITE", or "SITES"')
        elif ttype is TokenType.SUBREDDIT or ttype is TokenType.SUBREDDITS:
            token, ttype = self.getToken()
            if ttype is TokenType.COLON:
                self.parse_subreddit_list()
            else:
                raise SubscriptionParserException('Error - parse_statement - Expected COLON')
        else:
            raise SubscriptionParserException('Error - parse_statement_list - Expected "ITEM", "ITEMS", "SITE", "SITES", "IGNORE", "EMAIL", "SUBREDDIT", "SUBREDDITS"')

    def parse_item_list(self, ignore):
        itemList = self.parse_list([])
        if ignore:
            self.ignore_items += itemList
        else:
            self.items += itemList

    def parse_site_list(self, ignore):
        siteList = self.parse_list([])
        if ignore:
            self.ignore_sites += siteList
        else:
            self.sites += siteList

    def parse_email(self):
        self.settings += ['email', True]

    def parse_subreddit_list(self):
        subredditList = self.parse_list([])
        self.subreddits += subredditList

    def parse_list(self, ret):
        token, ttype = self.getToken()
        if ttype is TokenType.TOKEN:
            self.ungetToken()
            ret += [self.parse_element('')]
            token, ttype = self.getToken()
            if ttype in [TokenType.COMMA, TokenType.SEMICOLON]:
                token, ttype = self.getToken()
                if ttype is TokenType.TOKEN:
                    self.ungetToken()
                    return self.parse_list(ret)
                else:
                    raise SubscriptionParserException('Error - parse_list - Expected TOKEN after COMMA or SEMICOLON')
            else:
                self.ungetToken()
                return ret
        else:
            raise SubscriptionParserException('Error - parse_list - Expected TOKEN')

    def parse_element(self, ret):
        token, ttype = self.getToken()
        if ttype is TokenType.TOKEN:
            if ret is '':
                ret += token
            else:
                ret += ' ' + token
            token, ttype = self.getToken()
            if ttype is TokenType.TOKEN:
                self.ungetToken()
                return self.parse_element(ret)
            else:
                self.ungetToken()
            return ret
        else:
            raise SubscriptionParserException('Error - parse_element - Expected TOKEN')


class SubscriptionParserException(Exception):
    def __init__(self, errorArgs):
        Exception.__init__(self, "Subscription Parser Exception: {0}".format(errorArgs))
        self.errorArgs = errorArgs
