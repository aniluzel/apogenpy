import os

import utils
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import logging

log = logging.getLogger()


class ChromeDriver:
    def __init__(self):
        service = Service(utils.chromedriver_path_name())
        self.driver = webdriver.Chrome(service=service)


def selenium(driver, input, timeout, tag, type, value, index):

    try:
        path = driver.find_elements(By.XPATH, "//{}[{}='{}']".format(tag, type, value))[index]

    except IndexError:
        log.warning("You are trying to access element which is not on the list, replacing index with 0")
        path = driver.find_elements(By.XPATH, "//{}[{}='{}']".format(tag, type, value))[0]

    try:
        utils.time.sleep(timeout)

        if not input:
            path.click()
        else:
            path.send_keys(input)

    except (NoSuchElementException, ElementNotInteractableException) as e:
        if e == ElementNotInteractableException:
            log.warning("Element not interactable")
        else:
            log.warning("Element not found")


Driver = ChromeDriver()
