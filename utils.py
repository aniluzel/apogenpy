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


def folder_name_changer(domain):
    invalid = '<>:"/\|?* '
    for char in invalid:
        domain = domain.replace(char, '')
    return domain