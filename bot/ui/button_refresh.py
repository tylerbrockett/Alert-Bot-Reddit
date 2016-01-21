from Tkinter import Button
import tkMessageBox


class Refresh:
    def __init__(self, gui):
        self.gui = gui
        self.text = Button(gui.frame, text="Refresh", command=self.refresh)
        self.text.pack()

    def refresh(self):
        if self.gui.bot_thread and self.gui.bot_thread.is_running():
            tkMessageBox.showerror("Kill Process First",
                                   "You must kill the running process(es) first before running 'Refresh'")
        else:
            self.gui.bot.disconnect_from_database()
            self.gui.bot.refresh_token()
            self.gui.bot.connect_to_database()
            self.gui.status.update_status("Refreshed")
            self.gui.event_list.clear()
            tkMessageBox.showinfo("Success", "Refresh Successful!")
