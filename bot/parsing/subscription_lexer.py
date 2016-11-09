from parsing.token_type import TokenType


class SubscriptionLexer:
    FALSE = 0
    original_string = ''
    active_index = 0
    EOF = False
    active_token = False
    token = ''
    token_type = TokenType.NO_TOKEN
    reserved_tokens = [
        '',
        # TITLE
        '-title',
        '-site',
        '-sites',
        # BODY
        '-url',
        '-item',
        '-items',
        '-body',
        # SUBREDDIT
        '-subreddit',
        '-subreddits',
        # REDDITORS
        '-redditor',
        '-redditors',
        # IGNORE BODY
        '-ignore-site',
        '-ignore-sites',
        '-ignore-body',
        # IGNORE TITLE
        '-ignore-item',
        '-ignore-items',
        '-ignore-title',
        # IGNORE SUBREDDITS
        '-ignore-subreddit',
        '-ignore-subreddits',
        '-nsfw',
        '-email',
        ','
    ]

    def __init__(self, sub):
        self.original_string = sub

    def skip_space(self):
        c = self.get_char()
        while not self.EOF and (c == ' ' or c == '\n' or c == '\r'):
            c = self.get_char()
        if not self.EOF:
            self.unget_char()

    def is_keyword(self, token):
        if token.lower() in ['-body', '-site', '-sites', '-url']:
            return TokenType.BODY
        elif token.lower() in ['-title', '-item', '-items']:
            return TokenType.TITLE
        elif token.lower() in ['-subreddit', '-subreddits']:
            return TokenType.SUBREDDITS
        elif token.lower() in ['-redditor', '-redditors']:
            return TokenType.REDDITORS
        elif token.lower() in ['-ignore-body', '-ignore-site', '-ignore-sites']:
            return TokenType.IGNORE_BODY
        elif token.lower() in ['-ignore-title', '-ignore-item', '-ignore-items']:
            return TokenType.IGNORE_TITLE
        elif token.lower() in ['-ignore-redditor', '-ignore-redditors']:
            return TokenType.IGNORE_REDDITORS
        elif token.lower() in ['-email']:
            return TokenType.EMAIL
        elif token.lower() in ['-nsfw', '-show-nsfw']:
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
        while c is not ' ' and c is not '' and c not in self.reserved_tokens:
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
            raise SubscriptionLexerException("Exception occurred")


class SubscriptionLexerException(Exception):
    def __init__(self, errorArgs):
        Exception.__init__(self, "Subscription Lexer Exception: {0}".format(errorArgs))
        self.errorArgs = errorArgs
