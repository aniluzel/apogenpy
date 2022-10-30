import os
import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import requests
import csv
from urllib.parse import urlparse
import chromedriver_autoinstaller

def file_name_changer(subdomain):
    invalid = '<>:"/\|?* '
    for char in invalid:
        subdomain = subdomain.replace(char, '_')
    return subdomain[1:]


def folder_name_changer(domain):
    invalid = '<>:"/\|?* '
    for char in invalid:
        domain = domain.replace(char, '')
    return domain

def chrome_driver_downloader():
    chromedriver_autoinstaller.install(True)

def chromedriver_path_name():
    if sys.platform.startswith('linux'):
        path = chromedriver_autoinstaller.get_chrome_version().split(".")[0] +'/chromedriver'
    elif sys.platform == 'darwin':
        path = chromedriver_autoinstaller.get_chrome_version().split(".")[0] +'/chromedriver'
    elif sys.platform.startswith('win'):
        path = chromedriver_autoinstaller.get_chrome_version().split(".")[0] + '\chromedriver.exe'
    else:
        raise RuntimeError('Cannot determine platform')
    return path

print(chromedriver_path_name())


