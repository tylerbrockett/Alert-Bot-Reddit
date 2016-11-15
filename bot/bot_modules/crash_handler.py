from private import accountinfo
from bot_modules.sleep_handler import SleepHandler


def handle_crash(stacktrace, reddit, database, message_dev):
    reset = False
    while not reset:
        try:
            reddit.reset()
            database.reset()
            if message_dev:
                reddit.send_message(accountinfo.developerusername, "Exception Handled", stacktrace)
            reset = True
        except:
            SleepHandler.sleep(30)
