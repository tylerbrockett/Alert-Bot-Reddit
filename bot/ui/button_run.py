from Tkinter import Button

import tkMessageBox


class Run:
    def __init__(self, gui):
        self.gui = gui
        self.text = Button(gui.frame, text="Start", command=self.start)
        self.text.pack()

    def start(self):
        if self.gui.bot.force_kill and not self.gui.bot.run:
            self.gui.bot_thread.start()
            print 'start'
        else:
            tkMessageBox.showerror("Kill Process First",
                                   "You must kill the running process(es) first before running 'Refresh'")