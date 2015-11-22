import time
import random
from helpers import filehelper
from helpers import colorhelper
from private import accountinfo
from helpers.ledhelper import LedHelper
from helpers.filehelper import FileHelper
from helpers.timehelper import TimeHelper
from helpers.gmailhelper import GmailHelper
from helpers.exceptionhelper import ExceptionHelper

exception_helper = None
led_helper = None
gmail_helper = None
time_helper = None
file_helper = None

CHECK_INTERVAL = 2  # interval between checks
QUIET_START = 8  # AM
QUIET_STOP = 8   # PM


def check_time():
    global time_helper
    if time_helper.checkTime():
        if time_helper.isQuietHours:
            led_helper.turnOff()
        else:
            led_helper.turnOn()


def check_on_bot():
    def handle_bot_is_running():
        global CHECK_INTERVAL
        if not led_helper.getGreenState():
            colorhelper.printcolor('green', 'BOT STARTED RUNNING')
            led_helper.setGreenState(True)
            CHECK_INTERVAL = 2
            gmail_helper.sendEmail(accountinfo.tyler_email, 'Boss, the bot is running again', 'The bot started running at ' + time_helper.getFormattedTime())
        print 'Carry on.'

    def handle_bot_not_running():
        global CHECK_INTERVAL
        if led_helper.getGreenState():
            colorhelper.printcolor('red', 'BOT NOT RUNNING ANYMORE')
            led_helper.setGreenState(False)
            CHECK_INTERVAL = 4
            stacktrace = file_helper.readFile(filehelper.STACKTRACE)
            file_helper.eraseContents(filehelper.STACKTRACE)
            gmail_helper.sendEmail(accountinfo.tyler_email, 'Boss, the bot crashed', 'The bot crashed at ' +
                                   time_helper.getFormattedTime() + "\n\n\nThe Stacktrace is: \n\n\n" + stacktrace)
        print 'Bot not running.'

    print 'Checking...'
    contents = file_helper.readFile(filehelper.PROCESS_ID)
    if contents == '':
        print 'PID: EMPTY'
        handle_bot_not_running()
    else:
        print 'PID: ', contents
        handle_bot_is_running()
    print '\n'


def initialize():
    global exception_helper, led_helper, gmail_helper, time_helper, file_helper
    exception_helper = ExceptionHelper()
    led_helper = LedHelper()
    gmail_helper = GmailHelper()
    time_helper = TimeHelper()
    file_helper = FileHelper()


def handle_crash():
    global exception_helper
    colorhelper.printcolor('red', "Monitor Crashed")
    led_helper.monitorCrashed()
    stacktrace = exception_helper.getStacktrace()
    gmail_helper.sendEmail(accountinfo.tyler_email, "Boss... The monitor crashed", "The monitor crashed at " +
                           time_helper.getFormattedTime() + "\n\n\nHere's the stacktrace\n\n\n" + stacktrace)


def main():
    while True:
        time.sleep(CHECK_INTERVAL)
        # Just to make following the output easier, since all output is basically the same.
        print 'Random', str(50 * random.random())
        check_on_bot()


def crash():
    for i in range(10):
        print 'ZzZzZzZzZzZzZz...'
        time.sleep(2)
    print 'Crashing...'
    a = [0,1,2,3,4]
    for i in range(0, len(a) + 5, 1):
        a[i] = i


__author__ = 'tyler'
if __name__ == "__main__":
    try:
        initialize()
        #crash()
        main()
    except:
        handle_crash()

