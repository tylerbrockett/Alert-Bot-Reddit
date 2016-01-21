from Tkinter import Button
import tkMessageBox


class Refresh:
    def __init__(self, gui):
        self.gui = gui
        self.text = Button(gui.frame, text="Refresh", command=self.refresh)
        self.text.pack()

    def refresh(self):
        if self.gui.bot.run and not self.gui.bot.force_kill:
            tkMessageBox.showerror("Kill Process First",
                                   "You must kill the running process(es) first before running 'Refresh'")
        else:
            self.gui.bot.destroy()
            self.gui.bot.initialize()
            self.gui.event_list.clear()
            tkMessageBox.showinfo("Success", "Refresh Successful!")
