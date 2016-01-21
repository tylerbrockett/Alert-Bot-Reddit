from Tkinter import *


class Status:
    def __init__(self, gui):
        self.gui = gui
        self.text = Text(gui.frame, height=1, width=60)
        self.text.config()
        self.text.pack()
        self.update_status("GUI Initialized")

    def update_status(self, text):
        self.text.delete("1.0", END)
        self.text.insert(INSERT, text)
