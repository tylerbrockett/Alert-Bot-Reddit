from Tkinter import *


class TimeStarted:
    def __init__(self, gui):
        self.gui = gui
        self.text = Text(gui.frame, height=1, width=60)
        self.text.pack()
        self.set_time_started("Not Started Yet")

    def set_time_started(self, text):
        self.text.delete("1.0", END)
        self.text.insert(INSERT, text)
