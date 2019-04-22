# coding: utf-8
# Author: rogerclark

"""
use this module to handle the data acquirement
"""
import re, time

from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup

from get_screen.bjmemc import Screenshotbjmemc
from basicset import selector
from basicset import spider_config as cfg


class AcquirePollutantsData(object):

    def __init__(self, pollutant, base_url, need_zoom):

        self.pollutants = pollutant
        self.base_url = base_url
        self.points = selector.POINT_LIST
        self.frame = selector.POLLUTANTS[pollutant]
        self.bjmemc = Screenshotbjmemc(base_url=base_url,
                                       wait=cfg.initial_wait,
                                       headless=cfg.headless,
                                       retry=cfg.retry)
        self.needzoom = need_zoom
        self.filename = ["{}-{}.png".format(self.pollutants, str(i))
                         for i in range(1, len(self.points)+1)]

    def get_data_by_image(self):

        print("Acquire Data from {} frame".format(self.pollutants))
        for index, point in enumerate(self.points):
            self.bjmemc.switchFrameButton(self.frame, wait=cfg.switch_wait)
            if index in self.needzoom:
                print("find special points, set zoom level to 10")
                self.bjmemc.setZoom(wait=cfg.zoom_wait)
            self.bjmemc.switchFrameButton(point, wait=cfg.switch_wait)
            self.bjmemc.captureScreen(filename=self.filename[index])
            print("capture screen:{}".format(self.filename[index]))
            self.bjmemc.refreshDriver()

    def get_data_by_source(self):

        print("Acquire Data from {} frame".format(self.pollutants))
        datalist = []
        for index, point in enumerate(self.points):
            self.bjmemc.switchFrameButton(self.frame, wait=cfg.switch_wait)
            if index in self.needzoom:
                print("find special points, set zoom level to 10")
                self.bjmemc.setZoom(wait=cfg.zoom_wait)
            self.bjmemc.switchFrameButton(point, wait=cfg.switch_wait)
            page = self.bjmemc.getPageSource()
            soup = BeautifulSoup(page, 'lxml')
            if self.pollutants=="AQI":
                data = self.get_data_aqi(soup=soup)
            else:
                data = self.get_data_pollutant(soup=soup)
            print(data)
            datalist.append(data)
            self.bjmemc.refreshDriver(wait=cfg.refresh_wait)
        return datalist

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
                "type": self.pollutants,
                "acquire_time": self.get_acquire_time()}

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
                "type": self.pollutants,
                "acquire_time": self.get_acquire_time()}

        return data

    def get_acquire_time(self):

        ts = time.localtime(time.time())
        acquire_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", ts)
        return acquire_time

    def parse_location(self, soup):

        find = soup.find_all('td', class_='show_name')
        if len(find) <= 0:
            print("can not find class attribute: show_name")
            res = 'NONE'
        else:
            res = find[0].text
        return res

    def parse_datatime(self, soup):

        find = soup.find_all('div', class_="gxDate")
        if len(find) <= 0:
            print("can not find class attribute: gxDate")
            datatimestr = "NONE"
        else:
            res = find[0].text
            res = ''.join(re.findall(r'\d', res))
            if res:
                datatime = time.strptime(res, "%Y%m%d%H%M")
            else:
                print('can not find data update time')
                datatime = "None"
            datatimestr = time.strftime("%Y-%m-%dT%H:%M:%SZ", datatime)
        return datatimestr

    def parse_aqi(self, soup):

        find = soup.find_all('td', class_='show_aqi')
        if len(find) <= 0:
            print("can not find class attribute: show_aqi")
            aqi = 'NONE'
        else:
            res = find[0].text
            aqi = ''.join(re.findall(r'\d', res))
        return aqi

    def parse_primary_pollutants(self, soup):

        find = soup.find_all('td', class_='show_sw')
        if len(find) <= 0:
            print("can not find class attribute: show_sw")
            primary = 'NONE'
        else:
            res = find[0].text
            primary = re.sub(pattern=r'.*?：', repl='', string=res)
        return primary

    def parse_air_quality(self, soup):

        find = soup.find_all('td', class_='show_zk')
        if len(find) <= 0:
            print("can not find class attribute: show_zk")
            quality = 'NONE'
        else:
            res = find[0].text
            quality = re.sub(pattern=r'.*?：', repl='', string=res)
        return quality

    def parse_pollutans_concentration(self, soup):

        find = soup.find_all('td', class_='show_aqi')
        if len(find) <= 0:
            print("can not find class attribute: show_aqi")
            concentration = 'NONE'
        else:
            res = find[1].text
            concentration = re.sub(pattern=r'.*?:', repl='', string=res)
        return concentration

    def close_task(self):
        print("closing task...")
        self.bjmemc.closeDriver()





if __name__ == "__main__":

    base_url = "http://zx.bjmemc.com.cn/getAqiList.shtml?timestamp=1555138830130"
    task = AcquirePollutantsData(pollutant="AQI",
                                 base_url = base_url,
                                 need_zoom=[0,18, 20])
    datalist = task.get_data_by_source()
    from task.data import DataHandler
    dh = DataHandler()
    dh.connect_database(database='test', collection='air')
    dh.add_in_database(datalist)
    task.close_task()
