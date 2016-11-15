

class EditParser:

    def __init__(self, text):
        self.text = text
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

    def unget_token(self):
        self.index -= 1

    def get_token(self):
        self.index += 1
        if self.index >= len(self.tokens) or self.index < 0:
            raise SubscriptionParserException('Error - Index out of bounds [' + str(self.index) + ']')
        return self.tokens[self.index]


    def parse_edit_list(self):
        token, ttype = self.get_token()
        if token == 'add':
            self.unget_token()
            self.parse_edit_add()
        elif token == 'remove':
            self.unget_token()
            self.parse_edit_remove()
        token, ttype = self.get_token()
        if token == 'add' or token == 'remove':
            self.unget_token()
            self.parse_edit_list()
        else:
            raise EditParserException(' '))

    def parse_edit_add(self):
        token, ttype = self.get_token()
        if token != 'add':
            raise EditParserException('Error - parse_edit_add - Expected \'add\'')
        list = self.parse_list([])

    def parse_edit_remove(self):
        token, ttype = self.get_token()
        if token != 'remove':
            raise EditParserException('Error - parse_edit_remove - Expected \'remove\'')
        list = self.parse_list([])



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
            raise EditParserException('Error - parse_statement_list - Expected ' + str(SubscriptionParser.statement_tokens))

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
                    raise EditParserException('Error - parse_list - Expected TOKEN after COMMA or SEMICOLON')
            else:
                self.unget_token()
                return ret
        else:
            raise EditParserException('Error - parse_list - Expected TOKEN')

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
            raise EditParserException('Error - parse_element - Expected TOKEN')


class EditParserException(Exception):
    def __init__(self, errorArgs):
        Exception.__init__(self, "Edit Parser Exception: {0}".format(errorArgs))
        self.errorArgs = errorArgs