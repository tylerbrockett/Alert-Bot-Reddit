from message_lexer import MessageLexer
from message_lexer import MessageLexerException
from message_token_type import MessageTokenType
from utils.subscription import Subscription


class MessageParser:
    action_token_types = [MessageTokenType.SUBSCRIBE, MessageTokenType.UNSUBSCRIBE,
                          MessageTokenType.UNSUBSCRIBE_ALL, MessageTokenType.EDIT]

    reserved_tokens = [
        'subscribe',
        'unsubscribe',
        'unsubscribe all',
        'edit', 'change',
    ]
    categories = {
        '-title'            : ['-title', '-item', '-items'],
        '-body'             : ['-body', '-site', '-sites', '-url'],
        '-subreddits'       : ['-subreddit', '-subreddits'],
        '-redditors'        : ['-redditor', '-redditors'],
        '-ignore-body'      : ['-ignore-body', '-ignore-site', '-ignore-sites'],
        '-ignore-title'     : ['-ignore-title', '-ignore-item', '-ignore-items'],
        '-ignore-redditors' : ['-ignore-redditor', '-ignore-redditors'],
        '-flags'            : ['-email', '-nsfw', '-show-nsfw']
    }

    def unget_token(self):
        self.index -= 1

    def get_token(self):
        self.index += 1
        if self.index >= len(self.tokens) or self.index < 0:
            raise SubscriptionParserException('Error - Index out of bounds [' + str(self.index) + ']')
        return self.tokens[self.index]

    def __init__(self, message):
        self.message = message
        self.action = None
        self.subscription = None
        self.edits = {}
        self.index = -1
        self.tokens = []
        try:
            self.tokens = MessageLexer(message.body).tokenize()
        except:
            raise MessageLexerException("Error - message __init __ - Lexing Message")
        self.parse_message()

    def parse_message(self):
        token, ttype = self.get_token()
        self.action = ttype
        if ttype == MessageTokenType.SUBSCRIBE:
            self.subscription = Subscription(self.message.body[9:], self.message.author, self.message.message_id)
        elif ttype == MessageTokenType.UNSUBSCRIBE:
            self.subscription = Subscription(self.message.body[9:], self.message.author, self.message.message_id)
        elif ttype == MessageTokenType.UNSUBSCRIBE_ALL:
            return
        elif ttype == MessageTokenType.EDIT:
            self.parse_edit_list()

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
            raise SubscriptionParserException('Error - parse_statement_list - Expected ' + str(SubscriptionParser.statement_tokens))

    def parse_edit_add(self):
        token, ttype = self.get_token()
        if token != 'add':
            raise MessageParserException('Error - parse_edit_add - Expected \'add\'')
        list = self.parse_list([])

    def parse_edit_remove(self):
        token, ttype = self.get_token()
        if token != 'remove':
            raise MessageParserException('Error - parse_edit_remove - Expected \'remove\'')
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
            raise SubscriptionParserException('Error - parse_statement_list - Expected ' + str(SubscriptionParser.statement_tokens))

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
                    raise MessageParserException('Error - parse_list - Expected TOKEN after COMMA or SEMICOLON')
            else:
                self.unget_token()
                return ret
        else:
            raise MessageParserException('Error - parse_list - Expected TOKEN')

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
            raise MessageParserException('Error - parse_element - Expected TOKEN')


class MessageParserException(Exception):
    def __init__(self, errorArgs):
        Exception.__init__(self, "Message Parser Exception: {0}".format(errorArgs))
        self.errorArgs = errorArgs
