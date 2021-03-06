# coding:utf-8
# Author:rogerclark

import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from basicset import selector
from basicset import spider_config as cfg


class Screenshotbjmemc(object):

    def __init__(self, base_url, headless, wait=20, retry=3):

        chrome_options = Options()
        if cfg.load_image:
            print("Chromedriver will not load image beacause cfg.load_image==False")
            prefs = {'profile.default_content_setting_values': {'images': 2}}
            chrome_options.add_experimental_option('prefs', prefs)
        if headless:
            print("Initiate chromedriver in headless mode...")
            chrome_options.add_argument('window-size={}'.format(cfg.resolution))
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('user-agent={}'.format(cfg.ua))

            self.driver = webdriver.Chrome(chrome_options=chrome_options)
            #self.driver.maximize_window()
        else:
            #chrome_options = Options()
            #prefs = {'profile.default_content_setting_values':{'images':2}}
            #chrome_options.add_experimental_option('prefs', prefs)
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
            self.driver.maximize_window()
        self.retry = retry
        while self.retry > 0:
            try:
                self.driver.get(base_url)
                WebDriverWait(self.driver, wait).until(EC.visibility_of_element_located((By.TAG_NAME, 'svg')))
                break
            except exceptions.TimeoutException:
                print("Failed to load the page, retry in 5 seconds...")
                self.retry -= 1
                time.sleep(10)
        if self.retry <= 0:
            raise RuntimeError("Spider has reached the max retry times, page get failed.")



    def switchFrameButton(self, selector, wait=5):

        switch = ActionChains(self.driver)
        try:
            button = self.driver.find_element_by_css_selector(selector)
            switch.move_to_element(button).click().perform()
            time.sleep(wait)
        except exceptions.NoSuchElementException:
            raise RuntimeError("Can not find the element in page")


    def captureScreen(self, filename):

        self.driver.get_screenshot_as_file(filename)

    def getPageSource(self, filename=None, save=False):

        page = self.driver.page_source
        if save:
            print('writing page source in file:{}'.format(filename))
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(page)
        else:
            return page

    def setZoom(self, up=True, val=10, wait=5):
        self.driver.execute_script("map.setZoom({})".format(str(val)))
        time.sleep(wait)

    def refreshDriver(self, wait=5, retry=5):
        retry_t = retry
        while retry_t >0:
            try:
                self.driver.refresh()
                time.sleep(5)
                break
            except exceptions.TimeoutException:
                print('refreshDriver: time out failure, retry in 10 sec')
                time.sleep(10)
                retry_t = retry_t - 1
        if retry_t <= 0:
            raise RuntimeError('refreshDriver: reached the max retry times, quit thread')

    def closeDriver(self):

        self.driver.close()


if __name__ == "__main__":

    base_url = "http://zx.bjmemc.com.cn/getAqiList.shtml?timestamp=1555030832581"
    #point_list = [selector.POINT_LIST[i] for i in [0, 18, 20]]
    #names_list = ["{}-3.png".format(str(i)) for i in [0, 18, 20]]
    point_list = selector.POINT_LIST
    pollutants = selector.POLLUTANTS
    #names_list = ["{}-4.png".format(str(i)) for i in range(0, 35)]
    special_point = [0, 18, 20]
    bj = Screenshotbjmemc(base_url=base_url)

    for pollutant, selector in pollutants.items():
        names_list = ["test-{}-{}.png".format(pollutant, str(i)) for i in range(1, 35)]
        print("switch to {}".format(pollutant))
        for index, point in enumerate(point_list[0:3]):
            bj.switchFrameButton(selector)
            if index in special_point:
                print("find special, set zoom to 10")
                bj.setZoom()
            bj.switchFrameButton(point)
            bj.captureScreen(filename=names_list[index])
            print("capture screen:{}".format(names_list[index]))
            bj.refreshDriver()



    bj.closeDriver()