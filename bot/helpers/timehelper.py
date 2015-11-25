import time
from datetime import datetime


def getCurrentTimestamp():
    return time.time()


def getTimePassed(time):
    now = datetime.now()
    then = datetime.fromtimestamp(time)
    delta = now - then
    seconds = delta.seconds

    if seconds == 0:
        return '0s'

    months, remainder = divmod(seconds, 2592000)
    days, remainder = divmod(remainder, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    result = ''
    if months > 0:
        result += '%smo ' % months
    if days > 0:
        result += '%sd ' % days
    if hours > 0:
        result += '%sh ' % hours
    if minutes > 0:
        result += '%sm ' % minutes
    if seconds > 0:
        result += '%ss' % seconds

    return result