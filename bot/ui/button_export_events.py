from Tkinter import Button
import tkMessageBox
import tkMessageBox


class ExportEvents:
    def __init__(self, gui):
        self.gui = gui
        self.text = Button(gui.frame, text="Export", command=self.export)
        self.text.config(highlightbackground="red", )
        self.text.pack()

    def export(self):
        print self.gui.buffer.to_string()
        tkMessageBox.showinfo("Success", "Export Successful!")
