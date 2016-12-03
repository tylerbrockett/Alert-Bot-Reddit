"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   12/2/2016
Version:            v2.0
==========================================
"""

import json

from utils.inbox import format_subject
from parsing.message_lexer import MessageLexer
from parsing.subscription_parser import SubscriptionParser
from parsing.token_type import TokenType
import traceback


class MessageParser:

    KEY_ACTION = 'action'
    KEY_PAYLOAD = 'payload'
    KEY_VALID = 'valid'

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

    def unget_token(self):
        self.index -= 1
        return self.tokens[self.index]

    def get_token(self):
        self.index += 1
        if self.index >= len(self.tokens) or self.index < 0:
            raise MessageParserException('Error - Index out of bounds [' + str(self.index) + ']')
        return self.tokens[self.index]

    def __init__(self, message):
        self.message = message
        self.index = -1
        self.tokens = []
        self.data = {
            MessageParser.KEY_ACTION: MessageParser.ACTION_UNKNOWN,
            MessageParser.KEY_PAYLOAD: {},
            MessageParser.KEY_VALID: False
        }
        try:
            self.tokens = MessageLexer(str(message.body)).tokenize()
            self.parse_message()
            self.data[MessageParser.KEY_VALID] = True
        except:
            self.data[MessageParser.KEY_VALID] = False

    def get_data(self):
        return self.data

    def get_payload(self):
        return self.data[MessageParser.KEY_PAYLOAD]

    def to_json(self):
        return json.dumps(self.data, indent=2)

    def parse_message(self):
        token, ttype, index = self.get_token()
        if ttype == TokenType.STATISTICS:
            self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_STATISTICS
            token, ttype, index = self.get_token()
            if ttype != TokenType.EOF:
                raise MessageParserException(MessageParserException.MALFORMED_REQUEST)
        elif ttype == TokenType.HELP:
            self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_HELP
            token, ttype, index = self.get_token()
            if ttype != TokenType.EOF:
                raise MessageParserException(MessageParserException.MALFORMED_REQUEST)
        elif ttype == TokenType.SUBSCRIPTIONS:
            self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_GET_SUBSCRIPTIONS
            token, ttype, index = self.get_token()
            if ttype != TokenType.EOF:
                raise MessageParserException(MessageParserException.MALFORMED_REQUEST)
        elif ttype == TokenType.UNSUBSCRIBE:
            self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_UNSUBSCRIBE
            token, ttype, index = self.get_token()
            if ttype == TokenType.ALL:
                self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_UNSUBSCRIBE_ALL
                token, ttype, index = self.get_token()
                if ttype != TokenType.EOF:
                    raise MessageParserException(MessageParserException.MALFORMED_REQUEST)
            elif ttype == TokenType.NUM:
                self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_UNSUBSCRIBE_FROM_NUM
                self.data[MessageParser.KEY_PAYLOAD] = token
                token, ttype, index = self.get_token()
                if ttype != TokenType.EOF:
                    raise MessageParserException(MessageParserException.MALFORMED_REQUEST)
            elif ttype != TokenType.EOF:
                raise MessageParserException(MessageParserException.MALFORMED_REQUEST)
            else:
                self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_UNSUBSCRIBE
        elif ttype == TokenType.SUBSCRIBE:
            self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_SUBSCRIBE
            token, ttype, index = self.get_token()
            if ttype == TokenType.EOF:
                subscription = SubscriptionParser(format_subject(self.message.subject))
                self.data[MessageParser.KEY_PAYLOAD] = subscription.get_data()
            else:
                token, ttype, index = self.unget_token()
                subscription = SubscriptionParser(self.message.body[index:])
                self.data[MessageParser.KEY_PAYLOAD] = subscription.get_data()
        elif ttype == TokenType.FEEDBACK:
            self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_FEEDBACK
            self.data[MessageParser.KEY_PAYLOAD] = str(self.message.body)
        elif ttype == TokenType.EDIT:
            # edits = EditParser(self.message[index:])
            self.data[MessageParser.KEY_ACTION] = MessageParser.ACTION_EDIT
            # TODO Add edit stuff here
        else:
            print(traceback.format_exc())
            raise MessageParserException(MessageParserException.MALFORMED_REQUEST)


class MessageParserException(Exception):
    MALFORMED_REQUEST = 'Malformed Request'

    def __init__(self, errorArgs):
        Exception.__init__(self, 'Message Parser Exception: {0}'.format(errorArgs))
        self.errorArgs = errorArgs
