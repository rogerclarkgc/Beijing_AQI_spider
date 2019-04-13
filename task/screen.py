# coding: utf-8
# Author: rogerclark

from selenium import webdriver
from selenium.webdriver import ActionChains

from get_screen.bjmemc import Screenshotbjmemc
from basicset import selector


class AcquirePollutantsData(object):

    def __init__(self, pollutant, base_url, need_zoom):

        self.pollutants = pollutant
        self.base_url = base_url
        self.points = selector.POINT_LIST
        self.frame = selector.POLLUTANTS[pollutant]
        self.bjmemc = Screenshotbjmemc(self.base_url)
        self.needzoom = need_zoom
        self.filename = ["{}-{}.png".format(self.pollutants, str(i))
                         for i in range(1, len(self.points)+1)]

    def get_data(self):
        print("Acquire Data from {} frame".format(self.pollutants))
        for index, point in enumerate(self.points):
            self.bjmemc.switchFrameButton(self.frame, wait=3)
            if index in self.needzoom:
                print("find special points, set zoom level to 10")
                self.bjmemc.setZoom(wait=3)
            self.bjmemc.switchFrameButton(point, wait=3)
            self.bjmemc.captureScreen(filename=self.filename[index])
            print("capture screen:{}".format(self.filename[index]))
            self.bjmemc.refreshDriver()

    def close_task(self):
        print("closing task...")
        self.bjmemc.closeDriver()





if __name__ == "__main__":

    base_url = "http://zx.bjmemc.com.cn/getAqiList.shtml?timestamp=1555138830130"
    task = AcquirePollutantsData(pollutant="NO2",
                                 base_url = base_url,
                                 need_zoom=[0,18, 20])
    task.get_data()
    task.close_task()
