import time
import random
import threading

from basicset.selector import (POINT_LIST, POLLUTANTS)
from get_screen import bjmemc


class MultiThreadingTask(threading.Thread):

    def __init__(self, selector, base_url, filename):

        threading.Thread.__init__(self)
        self.selector = selector
        self.base_url = base_url
        self.filename = filename

    def run(self):

        print("thread: {} start at:{}".format(self.filename, time.ctime()))
        bj = bjmemc.Screenshotbjmemc(base_url=self.base_url)
        bj.switchFrameButton(selector=self.selector)
        bj.captureScreen(filename=self.filename)
        print("thread: {} end at:{}".format(self.filename, time.ctime()))


if __name__ == "__main__":

    base_url = "http://zx.bjmemc.com.cn/getAqiList.shtml?timestamp=1555030832581"
    thread_list = [MultiThreadingTask(selector=value[1],
                                      base_url=base_url,
                                      filename="{}.png".format(value[0])) for value in POLLUTANTS.items()]

    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()