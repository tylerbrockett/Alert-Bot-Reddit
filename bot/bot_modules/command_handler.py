from utils import inbox
from utils.color import Color
from utils.logger import Logger
from private import accountinfo


class CommandHandler:
    TEST = 0
    RUN = 1
    PAUSE = 2
    KILL = 3

    @staticmethod
    def get_dev_messages(reddit):
        dev_messages = []
        unread_messages = reddit.get_unread(limit=None)
        for message in unread_messages:
            username = str(message.author).lower()
            if username == accountinfo.developerusername:
                dev_messages.append(message)
        return dev_messages

    @staticmethod
    def get_commands(reddit):
        commands = []
        try:
            messages = CommandHandler.get_dev_messages(reddit)
            for message in messages:
                subject, body = inbox.format_subject(message.subject.lower()), message.body.lower()
                if subject in ['run', 'start', 'resume']:
                    Logger.log(Color.GREEN, '--------- Bot resumed by developer ---------')
                    message.reply('Thanks, I was getting bored!')
                    commands.append(CommandHandler.RUN)
                    message.mark_as_read()
                elif subject in ['stop', 'pause']:
                    Logger.log(Color.YELLOW, '--------- Bot paused by developer ---------')
                    message.reply('Standing by for further instructions.')
                    commands.append(CommandHandler.PAUSE)
                    message.mark_as_read()
                elif subject in ['kill']:
                    Logger.log(Color.RED, '--------- Bot killed by developer ---------')
                    message.reply('Bot has been killed')
                    commands.append(CommandHandler.KILL)
                elif subject in ['test']:
                    Logger.log(Color.GREEN, '--------- Bot is being tested ---------')
                    message.reply('')
                    message.mark_as_read()
                    commands.append(CommandHandler.TEST)
        except:
            raise CommandHandlerException('Error occurred reading commands')
        return commands


class CommandHandlerException(Exception):
    def __init__(self, error_args):
        Exception.__init__(self, "CommandHandlerException: {0}".format(error_args))
        self.errorArgs = error_args
