import datetime
import time
from helpers import colorhelper


class TimeHelper:
    def __init__(self, quietstart = 0, quietend = 0):
        if quietend < quietstart:
            colorhelper.printcolor('red', 'Invalid Quiet Hours.')
            exit()
        self.quietstart = quietstart
        self.quietstop = quietend
        self.isquiet = False

    # return true if state changes, false if it stays the same
    def checkTime(self):
        time = datetime.datetime.now().time()
        if self.quietstart <= time.hour <= self.quietstop:
            previous_state = self.isquiet
            self.isquiet = True
            if previous_state is False:
                return True
            else:
                return False
        else:
            previous_state = self.isquiet
            self.isquiet = False
            if previous_state is True:
                return True
            else:
                return False

    def getIsQuietHours(self):
        return self.isquiet

    def getFormattedTime(self):
        return time.strftime('%l:%M%p on %b %d, %Y')
