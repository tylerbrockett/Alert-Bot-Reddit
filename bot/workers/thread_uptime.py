from helpers import times
import threading
from Tkinter import *
import time


class ThreadUptime(threading.Thread):
    def __init__(self, gui):
        threading.Thread.__init__(self)
        self.start_time = -1
        self.running = False
        self.gui = gui

    def run(self):
        self.running = True
        while self.running:
            if self.start_time > 0:
                self.gui.uptime.set_uptime(times.get_time_passed(self.start_time))
            else:
                self.gui.uptime.set_uptime("0s")
            time.sleep(1)
        self.on_stop_running()

    def is_running(self):
        return self.running

    def kill(self):
        self.running = False

    def on_stop_running(self):
        self.gui.uptime.set_uptime("0s")
        print 'Uptime stopped'
