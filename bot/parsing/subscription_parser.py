from subscription_lexer import SubscriptionLexer
from subscription_lexer import SubscriptionLexerException
from token_type import TokenType


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
        '-email',
        '-nsfw', '-show-nsfw'
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
        self.tokens = []
        self.title = []
        self.body = []
        self.ignore_title = []
        self.ignore_body = []
        self.redditors = []
        self.ignore_redditors = []
        self.subreddits = []
        self.flags = []
        try:
            self.tokens = SubscriptionLexer(sub).tokenize()
        except:
            raise SubscriptionLexerException("Error - subscription __init __ - Lexing Subscription")
        self.parse_subscription()

    def parse_subscription(self):
        token, ttype = self.get_token()
        if ttype is TokenType.TOKEN:
            self.unget_token()
            self.parse_title_list()
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
        title_list = self.parse_list([])
        if len(list) == 1 and list[0].lower() == 'all':
            title_list = []
        self.title += title_list

    def parse_body_list(self):
        self.body += self.parse_list([])

    def parse_redditors_list(self):
        redditors = self.parse_list([])
        self.redditors += [r.lower().replace('/u/', '') for r in redditors]

    def parse_subreddits_list(self):
        subreddits = self.parse_list([])
        self.subreddits += [s.lower().replace('/r/', '') for s in subreddits]

    def parse_email(self):
        self.flags += ['email', True]

    def parse_nsfw(self):
        self.flags += ['nsfw', True]

    def parse_ignore_title_list(self):
        self.ignore_title += self.parse_list([])

    def parse_ignore_body_list(self):
        self.ignore_body += self.parse_list([])

    def parse_ignore_redditors_list(self):
        redditors = self.parse_list([])
        self.ignore_redditors += [r.lower().replace('/u/', '') for r in redditors]

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
