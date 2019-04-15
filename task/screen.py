# coding: utf-8
# Author: rogerclark

from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup

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

    def get_data_by_image(self):

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

    def get_data_by_source(self):

        print("Acquire Data from {} frame".format(self.pollutants))
        for index, point in enumerate(self.points):
            self.bjmemc.switchFrameButton(self.frame, wait=2)
            if index in self.needzoom:
                print("find special points, set zoom level to 10")
                self.bjmemc.setZoom(wait=2)
            self.bjmemc.switchFrameButton(point, wait=2)
            page = self.bjmemc.getPageSource()
            soup = BeautifulSoup(page, 'lxml')
            if self.pollutants=="AQI":
                data = self.get_data_aqi(soup=soup)
            else:
                data = self.get_data_pollutant(soup=soup)
            print(data)
            self.bjmemc.refreshDriver(wait=3)


    def get_data_aqi(self, soup):

        loc = self.parse_location(soup)
        aqi = self.parse_aqi(soup)
        air_quality = self.parse_air_quality(soup)
        primary_pollutants = self.parse_primary_pollutants(soup)
        data_time = self.parse_datatime(soup)

        data = {"location": loc,
                "AQI": aqi,
                "air_quality": air_quality,
                "primary_pollutants": primary_pollutants,
                "data_time": data_time,
                "type": self.pollutants}

        return data

    def get_data_pollutant(self, soup):

        loc = self.parse_location(soup)
        iaqi = self.parse_aqi(soup)
        pollutants_concentration = self.parse_pollutans_concentration(soup)
        data_time = self.parse_datatime(soup)

        data = {"location": loc,
                "IAQI": iaqi,
                "concentration": pollutants_concentration,
                "data_time": data_time,
                "type": self.pollutants}

        return data

    def parse_location(self, soup):

        find = soup.find_all('td', 'show_name')
        if len(find) <= 0:
            print("can not find tag: show_name")
            res = 'NONE'
        else:
            res = find[0].text
        return res

    def parse_datatime(self, soup):
        return('blank')

    def parse_aqi(self, soup):

        find = soup.find_all('td', 'show_aqi')
        if len(find) <= 0:
            print("can not find tag: show_aqi")
            res = 'NONE'
        else:
            res = find[0].text
        return res

    def parse_primary_pollutants(self, soup):

        find = soup.find_all('td', 'show_sw')
        if len(find) <= 0:
            print("can not find tag: show_sw")
            res = 'NONE'
        else:
            res = find[0].text
        return res

    def parse_air_quality(self, soup):

        find = soup.find_all('td', 'show_zk')
        if len(find) <= 0:
            print("can not find tag: show_zk")
            res = 'NONE'
        else:
            res = find[0].text
        return res

    def parse_pollutans_concentration(self, soup):

        find = soup.find_all('td', 'show_aqi')
        if len(find) <= 0:
            print("can not find tag: show_aqi")
            res = 'NONE'
        else:
            res = find[1].text
        return res

    def close_task(self):
        print("closing task...")
        self.bjmemc.closeDriver()





if __name__ == "__main__":

    base_url = "http://zx.bjmemc.com.cn/getAqiList.shtml?timestamp=1555138830130"
    task = AcquirePollutantsData(pollutant="PM25",
                                 base_url = base_url,
                                 need_zoom=[0,18, 20])
    task.get_data_by_source()
    task.close_task()
