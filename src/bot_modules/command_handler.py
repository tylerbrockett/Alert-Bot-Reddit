"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

from mark_all_read import MarkRead
from utils import inbox
from utils.color import Color
from utils.env import env, DEV_USERNAME
from utils.logger import Logger
import traceback


class CommandHandler:
    TEST = 0
    RUN = 1
    PAUSE = 2
    KILL = 3
    MARKREAD = 4

    run = ['run', 'start', 'resume']
    pause = ['stop', 'pause']
    kill = ['kill']
    test = ['test']
    mark_read = ['markread', 'readall']

    @staticmethod
    def get_dev_messages(reddit):
        dev_messages = []
        unread_messages = reddit.get_unread()
        for message in unread_messages:
            username = str(message.author).lower()
            if username == env(DEV_USERNAME):
                dev_messages.append(message)
        return dev_messages

    @staticmethod
    def get_commands(reddit):
        commands = []
        try:
            messages = CommandHandler.get_dev_messages(reddit)
            for message in messages:
                subject, body = inbox.format_subject(message.subject.lower()), message.body.lower()
                if body in CommandHandler.run or subject in CommandHandler.run:
                    Logger.log('--------- Bot resumed by developer ---------', Color.GREEN)
                    message.reply('Bot will be resumed')
                    commands.append(CommandHandler.RUN)
                    message.mark_read()
                elif body in CommandHandler.pause or subject in CommandHandler.pause:
                    Logger.log('--------- Bot paused by developer ---------', Color.YELLOW)
                    message.reply('Bot will be paused')
                    commands.append(CommandHandler.PAUSE)
                    message.mark_read()
                elif body in CommandHandler.kill or subject in CommandHandler.kill:
                    Logger.log('--------- Bot killed by developer ---------', Color.RED)
                    message.reply('Bot will be killed')
                    commands.append(CommandHandler.KILL)
                    message.mark_read()
                elif body in CommandHandler.test or subject in CommandHandler.test:
                    Logger.log('--------- Bot is being tested ---------', Color.GREEN)
                    message.reply('Bot is being tested')
                    commands.append(CommandHandler.TEST)
                    message.mark_read()
                elif body in CommandHandler.mark_read or subject in CommandHandler.mark_read:
                    Logger.log('--------- Errors being marked as read ---------', Color.GREEN)
                    message.reply('Messages will be marked as read')
                    mark_read = MarkRead()
                    num_read = mark_read.mark_read()
                    commands.append(CommandHandler.MARKREAD)
                    message.reply(str(num_read) + ' messaged were marked as read')
                    message.mark_read()
        except:
            Logger.log(traceback.format_exc(), Color.RED)
            raise CommandHandlerException('Error occurred reading commands')
        return commands


class CommandHandlerException(Exception):
    def __init__(self, error_args):
        Exception.__init__(self, 'CommandHandlerException: {0}'.format(error_args))
        self.errorArgs = error_args
