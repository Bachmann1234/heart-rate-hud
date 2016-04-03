import Tkinter as tk
import logging

import sys
from Queue import LifoQueue
from threading import Thread


from driver.heart_rate_driver import read_cms50dplus, read_simulated_cms50plus


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
        driver_thread.setDaemon(True)
        self.master.after(1000, self.update_heart_rate)
        driver_thread.start()

    def update_heart_rate(self):
        if not self.heart_queue.empty():
            data = self.heart_queue.get()
            self.heart_rate_text.set(data.pulseRate)
            logging.info(data)
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


def main(port, simulated=False):
    if simulated:
        driver = read_simulated_cms50plus
        logging.info("Using simulation")
    else:
        driver = read_cms50dplus
        logging.info("Using cms50dplus")
    root = tk.Tk()
    HeartRateHub(root, port, driver)
    root.mainloop()


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    # todo, ugh, argparse is a thing. Use it
    main(sys.argv[1], simulated=sys.argv[2] == '--simulated')
