import Tkinter as tk
import logging

import sys
from Queue import LifoQueue
from threading import Thread


from driver.heart_rate_driver import read_cms50dplus


class HeartRateHub(object):

    def __init__(self, master, port, driver):
        self.master = master
        self.heart_rate_text = tk.StringVar()
        self.locked = False
        heart_rate_widget = tk.Label(
            self.master,
            textvariable=self.heart_rate_text,
            bg="red4",
            fg="white",
            font="Helvetica 24 bold")
        heart_rate_widget.pack()

        self.master.bind("<Control-l>", self.lock)

        self.heart_queue = LifoQueue()
        driver_thread = Thread(target=driver, args=(self.heart_queue, port))
        self.master.after(1000, self.update_heart_rate)
        driver_thread.start()

    def update_heart_rate(self):
        if not self.heart_queue.empty():
            heart_rate = self.heart_queue.get().pulseRate
            self.heart_rate_text.set(heart_rate)
            self.heart_queue.empty()
        self.master.after(1000, self.update_heart_rate)

    def lock(self, _):
        if self.locked:
            self.master.wm_overrideredirect(False)
            self.master.wm_attributes("-topmost", False)
        else:
            self.master.wm_overrideredirect(True)
            self.master.wm_attributes("-topmost", True)
        self.locked = not self.locked


def main(port):
    root = tk.Tk()
    HeartRateHub(root, port, read_cms50dplus)
    root.mainloop()


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    main(sys.argv[1])
