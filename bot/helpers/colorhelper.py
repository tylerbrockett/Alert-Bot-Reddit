
RESET = '\033[39m'

colors = [['black', '\033[30m'], ['red', '\033[31m'],     ['green', '\033[32m'], ['yellow', '\033[33m'],
          ['blue', '\033[34m'],  ['magenta', '\033[35m'], ['cyan', '\033[36m'],  ['white', '\033[37m']]


def printcolor(c, string):
    col = [color for color in colors if color[0] == c.lower()]
    if len(col) != 1:
        printcolor('red', 'Color not defined')
        exit()
    print col[0][1] + str(string) + RESET
