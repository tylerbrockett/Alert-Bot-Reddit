from Tkinter import Button

from workers.thread_bot import ThreadBot
import tkMessageBox


class Run:
    def __init__(self, gui):
        self.gui = gui
        self.text = Button(gui.frame, text="Run", command=self.run)
        self.text.pack()

    def run(self):
        if self.gui.bot.force_kill and not self.gui.bot.run:
            self.gui.bot_thread.start()
            print 'run'
        else:
            tkMessageBox.showerror("Kill Process First",
                                   "You must kill the running process(es) first before running 'Refresh'")