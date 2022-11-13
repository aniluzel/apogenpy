import os
import sys

import time
from bs4 import BeautifulSoup
import requests
import csv
from urllib.parse import urlparse
import chromedriver_autoinstaller
from html.parser import HTMLParser

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

#path = r"C:\Users\ozgun\Desktop\apogen\PetClinic __ a Spring Framework demonstration.html"

def chromedriver_checker():
    if chromedriver_autoinstaller.utils.get_chrome_version().split(".")[0] in os.listdir():
        return True
    else:
        return False
class MyHTMLParser(HTMLParser):
    data_text =[]
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)
        self.data_text.append(data)

parser = MyHTMLParser()