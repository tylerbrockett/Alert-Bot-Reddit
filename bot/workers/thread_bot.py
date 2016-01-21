import threading


class ThreadBot(threading.Thread):
    def __init__(self, gui):
        threading.Thread.__init__(self)
        self.gui = gui
        self.bot = gui.bot

    def run(self):
        self.bot.run = True
        self.bot.force_kill = False
        self.bot.start()
        # BOT IS RUNNING HERE
        self.on_stop_running()

    def on_stop_running(self):
        self.gui.uptime_thread.time_started = -1

    def is_running(self):
        return self.bot.run

    def kill(self):
        self.gui.status.update_status("Killing...")
        self.bot.run = False
