import json

from message_lexer import MessageLexer
from message_lexer import MessageLexerException
from parsing.subscription_parser import SubscriptionParser
from parsing.edit_parser import EditParser
from parsing.token_type import TokenType


class MessageParser:
    ACTION_UNKNOWN = 'action_unknown'
    ACTION_STATISTICS = 'action_statistics'
    ACTION_GET_SUBSCRIPTIONS = 'action_get_subscriptions'
    ACTION_UNSUBSCRIBE_ALL = 'action_unsubscribe_all'
    ACTION_UNSUBSCRIBE = 'action_unsubscribe'
    ACTION_UNSUBSCRIBE_FROM_NUM = 'action_unsubscribe_from_num'
    ACTION_SUBSCRIBE = 'action_subscribe'
    ACTION_EDIT = 'action_edit'
    ACTION_HELP = 'action_help'
    ACTION_FEEDBACK = 'action_feedback'

    KEY_ACTION = 'action'
    KEY_PAYLOAD = 'payload'

    def unget_token(self):
        self.index -= 1

    def get_token(self):
        self.index += 1
        if self.index >= len(self.tokens) or self.index < 0:
            raise MessageParserException('Error - Index out of bounds [' + str(self.index) + ']')
        return self.tokens[self.index]

    def __init__(self, message, username, message_id):
        self.message = message
        self.username = username
        self.message_id = message_id
        self.index = -1
        self.tokens = []
        self.data = json.loads('{"action":"' + MessageParser.ACTION_UNKNOWN + '"}')
        try:
            self.tokens = MessageLexer(message.body).tokenize()
        except:
            raise MessageLexerException("Error - message __init __ - Lexing Message")
        self.parse_message()

    def parse_message(self):
        token, ttype, index = self.get_token()

        if ttype == TokenType.STATISTICS:
            self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_STATISTICS
            token, ttype, index = self.get_token()
            if ttype != TokenType.EOF:
                raise MessageParserException(MessageParserException.MALFORMED_REQUEST)
        elif ttype == TokenType.SUBSCRIPTIONS:
            self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_GET_SUBSCRIPTIONS
            token, ttype, index = self.get_token()
            if ttype != TokenType.EOF:
                raise MessageParserException(MessageParserException.MALFORMED_REQUEST)
        elif ttype == TokenType.UNSUBSCRIBE:
            token, ttype, index = self.get_token()
            if ttype == TokenType.ALL:
                self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_UNSUBSCRIBE_ALL
                token, ttype, index = self.get_token()
                if ttype != TokenType.EOF:
                    raise MessageParserException(MessageParserException.MALFORMED_REQUEST)
            elif ttype == TokenType.NUM:
                self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_UNSUBSCRIBE_FROM_NUM
                self.data[MessageParser.KEY_PAYLOAD] = str(token)
                token, ttype, index = self.get_token()
                if ttype != TokenType.EOF:
                    raise MessageParserException(MessageParserException.MALFORMED_REQUEST)
            elif ttype != TokenType.EOF:
                raise MessageParserException(MessageParserException.MALFORMED_REQUEST)
            else:
                self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_UNSUBSCRIBE
        elif ttype == TokenType.SUBSCRIBE:
            subscription = SubscriptionParser(self.message[index:])
            self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_SUBSCRIBE
            self.data[MessageParser.KEY_PAYLOAD] = subscription.to_json()
        elif ttype == TokenType.EDIT:
            edits = EditParser(self.message[index:])
            self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_EDIT


class MessageParserException(Exception):
    MALFORMED_REQUEST = 'Malformed Request'

    def __init__(self, errorArgs):
        Exception.__init__(self, "Message Parser Exception: {0}".format(errorArgs))
        self.errorArgs = errorArgs
