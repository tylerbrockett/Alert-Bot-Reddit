from Tkinter import Button

from helpers import times
import tkMessageBox


class Kill:
    def __init__(self, gui):
        self.gui = gui
        self.text = Button(gui.frame, text="Kill", command=self.kill)
        self.text.pack()

    def kill(self):
        if self.gui.uptime_thread and self.gui.uptime_thread:
            self.gui.uptime_thread.kill()
            self.gui.uptime_thread = None
            self.gui.bot_thread.kill()
            self.gui.bot_thread = None
            print "Successfully killing"
        elif self.gui.uptime_thread:
            self.gui.uptime_thread.kill()
            self.gui.uptime_thread = None
            print "ERROR - Only uptime thread was running"
            tkMessageBox.showerror("ERROR",
                                   "Only uptime thread was running, not bot thread.")
        elif self.gui.bot_thread:
            self.gui.bot_thread.kill()
            self.gui.bot_thread = None
            print "ERROR - Only bot thread was running"
            tkMessageBox.showerror("ERROR",
                                   "Only bot thread was running, not uptime thread.")
        else:
            tkMessageBox.showerror("Start Process First",
                                   "Have the decency to start the bot before you try to kill it!")
