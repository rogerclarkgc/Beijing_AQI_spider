# coding:utf-8
# Author:rogerclark

import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from basicset import selector

class Screenshotbjmemc(object):

    def __init__(self, base_url, wait=20, retry=3):

        print("Initiating Chromedriver...")
        self.driver = webdriver.Chrome()
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
                time.sleep(5)
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

    def closeDriver(self):

        self.driver.close()


if __name__ == "__main__":

    base_url = "http://zx.bjmemc.com.cn/getAqiList.shtml?timestamp="
    point_list = selector.POINT_LIST
    names_list = ["{}-2.png".format(str(i)) for i in range(1, 35)]
    bj = Screenshotbjmemc(base_url=base_url)
    for (index, sel) in enumerate(point_list):
        bj.switchFrameButton(sel)
        bj.captureScreen(names_list[index])
        bj.driver.refresh()
        time.sleep(5)
        print(sel)

    bj.closeDriver()