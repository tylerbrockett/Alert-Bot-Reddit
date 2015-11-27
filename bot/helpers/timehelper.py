import time
from datetime import datetime


def getCurrentTimestamp():
    return time.time()


def getTimePassed(time):
    now = datetime.now()
    then = datetime.fromtimestamp(time)
    delta = now - then

    days = delta.days
    seconds = delta.seconds

    if days == 0 and seconds == 0:
        return "0s "
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    result = ''
    if days > 0:
        result += '%sd ' % days
    if hours > 0:
        result += '%sh ' % hours
    if minutes > 0:
        result += '%sm ' % minutes
    if seconds > 0:
        result += '%ss' % seconds

    return result