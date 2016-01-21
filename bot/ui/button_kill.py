from Tkinter import Button

from helpers import times
import tkMessageBox


class Kill:
    def __init__(self, gui):
        self.gui = gui
        self.text = Button(gui.frame, text="Kill", command=self.kill)
        self.text.pack()

    def kill(self):
        if not self.gui.bot.force_kill and self.gui.bot.run:
            self.gui.bot_thread.kill()
            print "Successfully killing"
        else:
            tkMessageBox.showerror("Start Process First",
                                   "Have the decency to start the bot before you try to kill it!")
