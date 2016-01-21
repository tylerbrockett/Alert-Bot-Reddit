from Tkinter import *


class Events:
    def __init__(self, gui):
        self.gui = gui
        self.text = Text(gui.frame, height=10, width=60)
        self.text.config(highlightbackground="red")
        self.text.pack(side=LEFT, fill=BOTH, expand=YES)

    def get_y_view(self):
        return self.text.yview

    def add_event(self, color, event):
        self.gui.buffer.append((color, event))

    def clear(self):
        self.gui.buffer.clear()
        self.text.delete("1.0", END)