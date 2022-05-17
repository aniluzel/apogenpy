from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time

#chrome_driver_path = r'C:\chromedriver.exe'

#mac
chrome_driver_path = r'/Users/denis/Documents/CS401/'

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
