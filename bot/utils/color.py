from random import randint


class Color:
    BLACK = '\033[30m'
    WHITE = '\033[37m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'

    RANDOM = -1

    colors = [BLACK, WHITE, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]

    @staticmethod
    def random():
        r = randint(1, len(Color.colors) - 1)
        color = Color.colors[r]
        return color
