from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time

class ObjectGen:
    def __init__(self,param,url):
        self.param = param
        service = Service(r'C:\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(url)
        try:
            self.object=self.driver.find_element(By.ID,self.param)
            print('Found ID')
        except NoSuchElementException:
            print('Trying to find element by linktext')
        try:
            self.object=self.driver.find_element(By.PARTIAL_LINK_TEXT,self.param)
            print('Found Partial Link Text')
        except NoSuchElementException:
            print('Trying to find element by classname')
        try:
            self.object=self.driver.find_element(By.CLASS_NAME,self.param)
            print('Found classname')
        except NoSuchElementException:
            print('Trying to find element by CSSSelect')
        try:
            self.object=self.driver.find_element(By.CSS_SELECTOR,self.param)
            print('Found CSSSelect')
        except NoSuchElementException:
            print('Cannot find element')


