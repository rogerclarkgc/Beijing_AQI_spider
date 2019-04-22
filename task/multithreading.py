import time
import random
import threading

from task.screen import AcquirePollutantsData
from task.data import DataHandler

class AcquireTask(threading.Thread):

    def __init__(self, pollutant, base_url, need_zoom, database={}):

        threading.Thread.__init__(self)
        self.pollutant = pollutant
        self.base_url = base_url
        self.need_zoom = need_zoom
        self.database=database

    def run(self):
        print("thread: task-{} start at {}".format(self.pollutant, time.ctime()))
        task = AcquirePollutantsData(pollutant=self.pollutant,
                                     base_url=self.base_url,
                                     need_zoom=self.need_zoom)
        datalist = task.get_data_by_source()
        task.close_task()
        dh = DataHandler()
        dh.connect_database(database=self.database['database'],
                            collection=self.database['collection'],
                            host=self.database['host'],
                            username=self.database['username'],
                            passwd=self.database['passwd'])
        dh.add_in_database(datalist)
        dh.close_client()




def runAcquireTask(base_url, pollutant, need_zoom, database, max_delay=5):

    thread_list = [AcquireTask(pollutant = p,
                               base_url=base_url,
                               need_zoom=need_zoom,
                               database=database) for p in pollutant]
    for thread in thread_list:
        thread.start()
        time.sleep(random.randint(1, max_delay))

    for thread in thread_list:
        thread.join()






if __name__ == "__main__":

    base_url = "http://zx.bjmemc.com.cn/getAqiList.shtml?timestamp=1555663766187"
    need_zoom = [0,18, 20]
    task = ['AQI',"NO2", "PM25", "PM10", "CO", "SO2", "O3"]
    login = {'database':'test',
             'collection':'air',
             'host':None,
             'username':None,
             'passwd':None}
    print('Current time: {}'.format(time.ctime()))
    runAcquireTask(base_url=base_url,
            pollutant=task,
            need_zoom=need_zoom,
            max_delay=3,
            database=login)
    print('Current time: {}'.format(time.ctime()))