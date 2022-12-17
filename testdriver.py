import os

import utils
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service


class ChromeDriver:
    def __init__(self):
        service = Service(utils.chromedriver_path_name())
        self.driver = webdriver.Chrome(service=service)


# class ExecuteTest:
#     def __init__(self, param, driver):
#         self.param = param
#
#         try:
#             self.object = driver.find_element(By.ID, self.param)
#             print('Found ID')
#
#         except NoSuchElementException:
#             print('Trying to find element by linktext')
#         try:
#             self.object = driver.find_element(By.PARTIAL_LINK_TEXT, self.param)
#             print('Found Partial Link Text')
#         except NoSuchElementException:
#             print('Trying to find element by classname')
#         try:
#             self.object = driver.find_element(By.CLASS_NAME, self.param)
#             print('Found classname')
#         except NoSuchElementException:
#             print('Trying to find element by CSSSelect')
#         try:
#             self.object = driver.find_element(By.CSS_SELECTOR, self.param)
#             print('Found CSSSelect')
#         except NoSuchElementException:
#             print('Trying to find element by Xpath')
#         try:
#             # self.object=driver.find_element(By.XPATH,"//button[text()=\'"+self.param+"\']")
#             self.object = driver.find_element(By.XPATH, self.param)
#             print('Found XpathSelect')
#
#         except NoSuchElementException:
#             print('Cannot find element')


def selenium(param, input, timeout, driver,type):

    try:
        if type == utils.nonhtmltdata[0] :
            path = driver.find_element(By.ID,param)
        elif type == utils.nonhtmltdata[1]:
            path = driver.find_element(By.CLASS_NAME,param)
        elif type == utils.htmldata[0]:
            path = driver.find_element(By.XPATH,param)
            path = driver.find_element(By.PARTIAL_LINK_TEXT,param)
            path = driver.find_element(By.LINK_TEXT, param)

    except NoSuchElementException:
        print("Cannot find element")


    utils.time.sleep(timeout)

    if not input:

        path.click()

    else:

        path.send_keys(input)

Driver = ChromeDriver()

url= "http://localhost:8080/owners/2/pets/new"
Driver.driver.get(url)
#Driver.driver.get("http://localhost:8080/owners/new")
Driver.driver.find_element(By.XPATH, "//button[normalize-space(text()) = 'Add Pet']").click()
