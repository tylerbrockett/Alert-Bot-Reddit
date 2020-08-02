"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot
==========================================
"""

from utils.color import Color
import traceback
from random import randint


class Logger:

    @staticmethod
    def generate_color(string, color):
        return color + string + Color.RESET

    @staticmethod
    def generate_rainbow(string):
        ret = ''
        i = randint(0, len(Color.rainbow) - 1)
        forward = True
        for c in string:
            if c == ' ':
                ret += c
                continue
            ret += Color.rainbow[i] + c + Color.RESET
            if i <= 0:
                forward = True
            elif i >= len(Color.rainbow) - 1:
                forward = False
            if forward:
                i += 1
            else:
                i -= 1
        return ret

    @staticmethod
    def colorfy(string, col):
        if col == Color.RANDOM:
            col = Color.random()
            return Logger.generate_color(string, col)
        elif col == Color.RAINBOW:
            return Logger.generate_rainbow(string)
        elif col in Color.colors:
            return Logger.generate_color(string, col)
        else:
            return string

    @staticmethod
    def log(string, col=None):
        try:
            print(Logger.colorfy(string, col))
        except:
            print(traceback.format_exc())
            print(string)

    @staticmethod
    def aligntext(text, desired_spaces):
        additional_space = desired_spaces - len(text)
        while additional_space > 0:
            text += ' '
            additional_space -= 1
        return text
