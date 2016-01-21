from Tkinter import *


class Uptime:
    def __init__(self, gui):
        self.gui = gui
        self.text = Text(gui.frame, height=1, width=60)
        self.text.pack()
        self.set_uptime("0s")

    def set_uptime(self, text):
        self.text.delete("1.0", END)
        self.text.insert(INSERT, text)
