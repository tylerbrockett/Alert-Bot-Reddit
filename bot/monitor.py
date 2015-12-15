import times
import traceback
from helpers import files
from helpers import color
from private import accountinfo
from helpers.led_lights import LedHelper
from helpers.files import FileHelper
from helpers.times import TimeHelper
from helpers.gmail import GmailHelper

led_helper = None
gmail_helper = None
time_helper = None
file_helper = None

CHECK_INTERVAL = 2  # interval between checks
QUIET_START = 8  # AM
QUIET_STOP = 8   # PM


def check_time():
    global time_helper
    if time_helper.check_time():
        if time_helper.isQuietHours:
            led_helper.turn_off()
        else:
            led_helper.turn_on()


def check_on_bot():
    def handle_bot_is_running():
        global CHECK_INTERVAL
        if not led_helper.get_green_state():
            color.print_color('green', 'BOT STARTED RUNNING')
            led_helper.set_green_state(True)
            CHECK_INTERVAL = 2
            gmail_helper.send_email(accountinfo.developeremail, 'Boss, the bot is running again', 'The bot started running at ' + time_helper.get_formatted_time())
        print 'Carry on.'

    def handle_bot_not_running():
        global CHECK_INTERVAL
        if led_helper.get_green_state():
            color.print_color('red', 'BOT NOT RUNNING ANYMORE')
            led_helper.set_green_state(False)
            CHECK_INTERVAL = 4
            stacktrace = file_helper.read_file(files.STACKTRACE)
            file_helper.eraseContents(files.STACKTRACE)
            gmail_helper.send_email(accountinfo.developeremail, 'Boss, the bot crashed', 'The bot crashed at ' +
                                    time_helper.get_formatted_time() + "\n\n\nThe Stacktrace is: \n\n\n" + stacktrace)
        print 'Bot not running.'

    color.print_color('random', 'Checking')
    contents = file_helper.read_file(files.PROCESS_ID)
    if contents == '':
        print 'PID: EMPTY'
        handle_bot_not_running()
    else:
        print 'PID: ', contents
        handle_bot_is_running()
    print '\n'


def initialize():
    global exception_helper, led_helper, gmail_helper, time_helper, file_helper
    led_helper = LedHelper()
    gmail_helper = GmailHelper()
    time_helper = TimeHelper()
    file_helper = FileHelper()


def handle_crash(stacktrace):
    global exception_helper
    color.print_color('red', "Monitor Crashed")
    led_helper.monitor_crashed()
    gmail_helper.send_email(accountinfo.developeremail, "Boss... The monitor crashed", "The monitor crashed at " +
                            time_helper.get_formatted_time() + "\n\n\nHere's the stacktrace\n\n\n" + stacktrace)


def main():
    while True:
        times.sleep(CHECK_INTERVAL)
        # Just to make following the output easier, since all output is basically the same.
        check_on_bot()

__author__ = 'tyler'
if __name__ == "__main__":
    try:
        initialize()
        main()
    except:
        handle_crash(traceback.format_exc())

