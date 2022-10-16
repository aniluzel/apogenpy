# utility (file writer, name parser, folder generation etc.) bu dosyada olacak

import os
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
def file_name_changer(subdomain):
    invalid = '<>:"/\|?* '
    for char in invalid:
        subdomain = subdomain.replace(char, '_')
    return subdomain[1:]
#2nd index is subdomain (file names)
#1st index is network path(url) (directory names)
test = urlparse("http://localhost:8080/owners/find")


def folder_name_changer(domain):
    invalid = '<>:"/\|?* '
    for char in invalid:
        domain = domain.replace(char, '')
    return domain
