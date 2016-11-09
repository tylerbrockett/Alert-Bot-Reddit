from parsing.message_token_type import MessageTokenType


class MessageLexer:
    FALSE = 0
    original_string = ''
    active_index = 0
    EOF = False
    active_token = False
    token = ''
    token_type = MessageTokenType.NO_TOKEN
    whitespace = [' ', '\n', '\r']
    reserved_tokens = [
        '',
        'subscribe',
        'unsubscribe',
        'unsubscribe all',
        'edit', 'change',
    ]

    def __init__(self, message):
        self.original_string = message

    def skip_space(self):
        c = self.get_char()
        while not self.EOF and c in self.whitespace:
            c = self.get_char()
        if not self.EOF:
            self.unget_char()

    def is_keyword(self, token):
        if token.lower() in ['subscribe']:
            return MessageTokenType.SUBSCRIBE
        elif token.lower() in ['unsubscribe']:
            return MessageTokenType.UNSUBSCRIBE
        elif token.lower() in ['unsubscribe all']:
            return MessageTokenType.UNSUBSCRIBE_ALL
        elif token.lower() in ['edit', 'change']:
            return MessageTokenType.EDIT
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
        self.token_type = MessageTokenType.NO_TOKEN
        c = self.get_char()
        while c not in self.whitespace and c is not '' and c not in self.reserved_tokens:
            self.token += c
            c = self.get_char()
        if not self.EOF:
            self.unget_char()
        self.token_type = self.is_keyword(self.token)
        if self.token_type == self.FALSE:
            self.token_type = MessageTokenType.TOKEN
        return self.token_type

    def scan_number(self):
        c = self.get_char()
        while self.is_num(c):
            self.token += c
            c = self.get_char()
        if c not in self.whitespace and c != MessageTokenType.EOF:
            raise MessageLexerException('Error - whitespace or EOF expected after number')
        self.unget_char()
        return MessageTokenType.NUM

    def get_token(self):
        if self.active_token:
            self.active_token = False
            return self.token_type

        self.skip_space()
        self.token = ''

        c = self.get_char()
        if self.EOF:
            self.token_type = MessageTokenType.EOF
        elif self.is_num(c):
            self.unget_char()
            self.token_type = self.scan_number()
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
            while self.token_type != MessageTokenType.EOF:
                token = self.get_token()
                tokens.append(token)
            return tokens
        except:
            raise MessageLexerException("Exception occurred")


class MessageLexerException(Exception):
    def __init__(self, errorArgs):
        Exception.__init__(self, "Message Lexer Exception: {0}".format(errorArgs))
        self.errorArgs = errorArgs
