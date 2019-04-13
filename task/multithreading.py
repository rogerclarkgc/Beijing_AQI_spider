import time
import random
import threading

from task.screen import AcquirePollutantsData

class AcquireTask(threading.Thread):

    def __init__(self, pollutant, base_url, need_zoom):

        threading.Thread.__init__(self)
        self.pollutant = pollutant
        self.base_url = base_url
        self.need_zoom = need_zoom

    def run(self):
        print("thread: task-{} start at {}".format(self.pollutant, time.ctime()))
        task = AcquirePollutantsData(pollutant=self.pollutant,
                                     base_url=self.base_url,
                                     need_zoom=self.need_zoom)
        task.get_data()
        task.close_task()


def runTask(base_url, pollutant, need_zoom, max_delay=5):

    thread_list = [AcquireTask(pollutant = p,
                               base_url=base_url,
                               need_zoom=need_zoom) for p in pollutant]
    for thread in thread_list:
        thread.start()
        time.sleep(random.randint(1, max_delay))

    for thread in thread_list:
        thread.join()


if __name__ == "__main__":

    base_url = "http://zx.bjmemc.com.cn/getAqiList.shtml?timestamp=1555138830130"
    need_zoom = [0,18, 20]
    task = ['AQI', "NO2", "PM25"]
    runTask(base_url=base_url,
            pollutant=task,
            need_zoom=need_zoom,
            max_delay=5)