from utils.color import Color
import traceback

class Logger:
    RESET = '\033[39m'

    @staticmethod
    def print_color(string, color):
        print(color + str(string) + Logger.RESET)

    @staticmethod
    def log(string, col=None):
        try:
            if col == Color.RANDOM:
                col = Color.random()
                Logger.print_color(string, col)
            elif col in Color.colors:
                Logger.print_color(string, col)
            else:
                print(str(string))
        # Handle terminals that don't support ANSI color codes I think?
        # I Don't remember if they throw an error or not.
        except:
            print(str(string))
