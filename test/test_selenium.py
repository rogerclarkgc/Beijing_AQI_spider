from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.keys import Keys
import time
base_url = "http://106.37.208.233:20035/"
test_url = "https://www.seleniumhq.org/docs/"

driver = webdriver.Ie()
driver.get(base_url)
#driver.set_window_size(30000, 30000)
driver.maximize_window()
# fisrt image
time.sleep(10)
driver.get_screenshot_as_file("11.png")
print("saved image1")
# find silverlight frame
ob = driver.find_element_by_css_selector("object")
scroll_down = ActionChains(driver)
scroll_down.move_to_element(ob).move_by_offset(400, 0).click()
scroll_down.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN)
print("first scroll")
scroll_down.key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN)
print("second scroll")
scroll_down.perform()
driver.get_screenshot_as_file("12.png")
print("saved image2")