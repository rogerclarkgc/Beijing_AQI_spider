import time

import schedule

from task.multithreading import *
from basicset import spider_config as cfg

def job_fetch():

    stamp = int(time.time() * 1000)
    base_url = "http://zx.bjmemc.com.cn/getAqiList.shtml?timestamp={}".format(stamp)
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
            max_delay=cfg.delay_max,
            min_delay=cfg.delay_min,
            database=login)
    print('Current time: {}'.format(time.ctime()))

schedule.every(cfg.schedule).minutes.do(job_fetch)

while True:
    schedule.run_pending()
    time.sleep(1)