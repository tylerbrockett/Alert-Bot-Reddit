from sys import stdout
import time


class SleepHandler:

    @staticmethod
    def sleep(seconds):
        print 'Sleeping',
        for i in range(seconds):
            stdout.write(".")
            stdout.flush()
            time.sleep(1)
        print ''
