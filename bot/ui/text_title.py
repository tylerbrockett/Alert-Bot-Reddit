from Tkinter import *


class Title:
    def __init__(self, gui):
        self.gui = gui
        self.text = Text(gui.frame, height=1, width=60)
        self.text.pack()
        self.set_title("Build A PC Sales Bot")

    def set_title(self, text):
        self.text.delete("1.0", END)
        self.text.insert(INSERT, text)
