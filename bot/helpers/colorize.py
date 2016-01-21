from random import randint

RESET = '\033[39m'

colors = [['black', '\033[30m'], ['red', '\033[31m'],     ['green', '\033[32m'], ['yellow', '\033[33m'],
          ['blue', '\033[34m'],  ['magenta', '\033[35m'], ['cyan', '\033[36m'],  ['white', '\033[37m']]


def colorize(c, string):
    try:
        col = None
        if c == 'random':
            r = randint(1, len(colors) - 1)
            col = colors[r][1]
        else:
            match = [color for color in colors if color[0] == c.lower()]
            if len(match) != 1:
                colorize('red', 'Color not defined')
                exit()
            else:
                col = match[0][1]

        print col + string + RESET
    except:
        print str(string)
