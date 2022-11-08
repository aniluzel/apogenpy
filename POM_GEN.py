from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time
import utils

# new_path
# utils.chrome_driver_downloader()
#path utils.chromedriver_autoinstaller.get_chrome_version().split(".")[0]+'\chromedriver.exe
chrome_driver_path = utils.chromedriver_path_name()
print(chrome_driver_path)
# service = Service(chrome_driver_path)
# driver = webdriver.Chrome(service=service)
# driver.get("https://www.google.com")
# windows_old
# chrome_driver_path = r'C:\chromedriver.exe'

# mac_old
# chrome_driver_path = r'/Users/denis/Documents/CS401/'


class Driver:
    def __init__(self, url):
        self.url = url
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(url)


class ObjectGen:
    def __init__(self, param, driver):
        self.param = param

        try:
            self.object = driver.find_element(By.ID, self.param)
            print('Found ID')
        except NoSuchElementException:
            print('Trying to find element by linktext')
        try:
            self.object = driver.find_element(By.PARTIAL_LINK_TEXT, self.param)
            print('Found Partial Link Text')
        except NoSuchElementException:
            print('Trying to find element by classname')
        try:
            self.object = driver.find_element(By.CLASS_NAME, self.param)
            print('Found classname')
        except NoSuchElementException:
            print('Trying to find element by CSSSelect')
        try:
            self.object = driver.find_element(By.CSS_SELECTOR, self.param)
            print('Found CSSSelect')
        except NoSuchElementException:
            print('Trying to find element by Xpath')
        try:
            # self.object=driver.find_element(By.XPATH,"//button[text()=\'"+self.param+"\']")
            self.object = driver.find_element(By.XPATH, self.param)
            print('Found XpathSelect')

        except NoSuchElementException:
            print('Cannot find element')


service = Service(utils.chromedriver_path_name())
driver = webdriver.Chrome(service=service)
driver.get("https://www.google.com")