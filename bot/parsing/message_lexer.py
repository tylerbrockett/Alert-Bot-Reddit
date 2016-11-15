from parsing.token_type import TokenType


class MessageLexer:
    FALSE = 0
    message = ''
    active_index = 0
    EOF = False
    active_token = False
    token = ''
    token_type = TokenType.NO_TOKEN
    whitespace = [' ', '\n', '\r']
    reserved_tokens = [
        'statistics', 'stats',
        'subscriptions', 'subs',
        'unsubscribe', 'unsub', 'all',
        'subscribe', 'sub',
        'edit', 'change',
        'help', 'info', 'information',
        'feedback', 'suggestion', 'suggestions', 'advice'
    ]

    def __init__(self, message):
        self.message = message

    def skip_space(self):
        c = self.get_char()
        while not self.EOF and c in self.whitespace:
            c = self.get_char()
        if not self.EOF:
            self.unget_char()

    def is_keyword(self, token):
        if token.lower() in ['statistics', 'stats']:
            return TokenType.STATISTICS
        if token.lower() in ['subscriptions', 'subs']:
            return TokenType.SUBSCRIPTIONS
        elif token.lower() in ['unsubscribe', 'unsub']:
            return TokenType.UNSUBSCRIBE
        elif token.lower() in ['all']:
            return TokenType.ALL
        elif token.lower() in ['subscribe', 'sub']:
            return TokenType.SUBSCRIBE
        elif token.lower() in ['edit', 'change']:
            return TokenType.EDIT
        elif token.lower() in ['help', 'info', 'information']:
            return TokenType.HELP
        elif token.lower() in ['feedback', 'suggestion', 'suggestions', 'advice']:
            return TokenType.FEEDBACK
        return self.FALSE

    def unget_token(self):
        self.active_token = True

    def unget_char(self):
        self.active_index -= 1

    def get_char(self):
        if self.active_index < len(self.message):
            char = str(self.message[self.active_index])
            self.active_index += 1
            return char
        else:
            self.EOF = True
            return ''

    def scan_token(self):
        self.token_type = TokenType.NO_TOKEN
        c = self.get_char()
        while c not in self.whitespace and c is not '' and c not in self.reserved_tokens:
            self.token += c
            c = self.get_char()
        if not self.EOF:
            self.unget_char()
        self.token_type = self.is_keyword(self.token)
        if self.token_type == self.FALSE:
            self.token_type = TokenType.TOKEN
        return self.token_type

    def scan_number(self):
        c = self.get_char()
        while self.is_num(c):
            self.token += c
            c = self.get_char()
        if c not in self.whitespace and c != TokenType.EOF:
            raise MessageLexerException('Error - whitespace or EOF expected after number')
        self.unget_char()
        return TokenType.NUM

    def get_token(self):
        if self.active_token:
            self.active_token = False
            return self.token_type

        self.skip_space()
        self.token = ''

        c = self.get_char()
        if self.EOF:
            self.token_type = TokenType.EOF
        elif self.is_num(c):
            self.unget_char()
            self.token_type = self.scan_number()
        else:
            self.unget_char()
            self.token_type = self.scan_token()
        return self.token, self.token_type, self.active_index

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
        while self.token_type != TokenType.EOF:
            token = self.get_token()
            tokens.append(token)
        return tokens


class MessageLexerException(Exception):

    def __init__(self, errorArgs):
        Exception.__init__(self, "Message Lexer Exception: {0}".format(errorArgs))
        self.errorArgs = errorArgs
