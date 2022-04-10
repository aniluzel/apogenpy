from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time

class ObjectGen:
    def __init__(self,ID,linktext,classname,CSS,url):
        self.url=url
        self.CSS=CSS
        self.linktext=linktext
        self.classname=classname
        service = Service(r'C:\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(url)
        self.ID=ID
        try:
            self.object=self.driver.find_element(By.ID,self.ID)
            print('Found ID')
        except NoSuchElementException:
            print('Trying to find element by linktext')
        try:
            self.object=self.driver.find_element(By.PARTIAL_LINK_TEXT,self.linktext)
            print('Found Partial Link Text')
        except NoSuchElementException:
            print('Trying to find element by classname')
        try:
            self.object=self.driver.find_element(By.CLASS_NAME,self.classname)
            print('Found classname')
        except NoSuchElementException:
            print('Trying to find element by CSSSelect')
        try:
            self.object=self.driver.find_element(By.CSS_SELECTOR,self.CSS)
            print('Found CSSSelect')
        except NoSuchElementException:
            print('Cannot find element')


#obj=ObjectGen('firstNme','Add Owner','btn btn-primary','.btn-primary','http://localhost:8080/owners/new')
#obj.object.send_keys('test')
#obj.object.click()
