# coding: utf-8
# Author: rogerclark

from get_screen.bjmemc import Screenshotbjmemc
from basicset import selector


class Aquiredata(object):

    def __init__(self, base_url):

        self.driver = Screenshotbjmemc(base_url)


    def click_screenshot(self, selector, filename):

        self.driver.switchFrameButton(selector)
        self.driver.captureScreen(filename)
