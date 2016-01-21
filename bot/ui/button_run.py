from Tkinter import Button

from workers.thread_uptime import ThreadUptime
from workers.thread_bot import ThreadBot
import tkMessageBox


class Run:
    def __init__(self, gui):
        self.gui = gui
        self.text = Button(gui.frame, text="Run", command=self.run)
        self.text.pack()

    def run(self):
        if not self.gui.uptime_thread and not self.gui.bot_thread:
            self.gui.uptime_thread = ThreadUptime(self.gui)
            self.gui.uptime_thread.daemon = True
            self.gui.bot_thread = ThreadBot(self.gui)
            self.gui.bot_thread.daemon = True

            self.gui.uptime_thread.start()
            self.gui.bot_thread.start()
            print 'run'
        else:
            tkMessageBox.showerror("Kill Process First",
                                   "You must kill the running process(es) first before running 'Refresh'")