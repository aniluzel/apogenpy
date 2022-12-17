import os
import sys
import time
from html.entities import name2codepoint
from bs4 import BeautifulSoup
import requests
import csv
from urllib.parse import urlparse
import chromedriver_autoinstaller
from html.parser import HTMLParser as Parser
from selenium import webdriver

nonhtmltdata=["id","class","href"]
htmldata=["xpath"]


def file_name_changer(subdomain):
    invalid = '<>:"/\|?*. '
    for char in invalid:
        subdomain = subdomain.replace(char, '_')
    return subdomain[1:]


def folder_name_changer(domain):
    invalid = '<>:"/\|?*. '
    for char in invalid:
        domain = domain.replace(char, '')
    return domain


def namechanger(name,type):
    if(type in nonhtmltdata):
        invalid = '<>:"/\|?* -.'
        for char in invalid:
            name = name.replace(char,'_')
    else:
         if '>' and '<' in name:
            name = (name.split(">"))[1].split("<")[0]
            if(len(name) > 1):
                name = name.replace(' ', '_')
    return name


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


def chromedriver_checker():
    if chromedriver_autoinstaller.utils.get_chrome_version().split(".")[0] in os.listdir():
        return True
    else:
        return False


class HTMLParser(Parser):
    def __init__(self):
        super().__init__()
        self.begin = True
        self.sub = "\t"
        self.sub_counter = 0
        self.html_data = ""
        self.main_tag = ""
        # self.sub_tags = []
        self.attrs = []
        # self.sub_attrs = []
        self.data = []

    def handle_starttag(self, tag, attrs):
        if self.begin and self.sub_counter == 0:
            self.begin = False
            self.html_data += "MAIN_BEGIN >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + tag + "\n"
            self.html_data += "main_tag: '" + tag + "'\n"
            self.main_tag = tag
            for attr in attrs:
                self.html_data += (self.sub * self.sub_counter) + "attr: (" + ": '".join(attr) + "')\n"
                self.attrs.append(attr)
        elif not self.begin:
            self.sub_counter += 1
            self.html_data += (self.sub * self.sub_counter) + "SUB_BEGIN >>>>>>>>>>>>>>>>>>>>>>> " + tag + "\n"
            self.html_data += (self.sub * self.sub_counter) + "sub_tag: '" + tag + "'\n"
            # self.sub_tags.append(tag)
            for attr in attrs:
                self.html_data += (self.sub * self.sub_counter) + "sub_attr: (" + ": '".join(attr) + "')\n"
                # self.sub_attrs.append(attr)

    def handle_endtag(self, tag):
        if not self.sub_counter == 0:
            self.html_data += (self.sub * self.sub_counter) + "SUB_END <<<<<<<<<<<<<<<<<<<<<<<<< " + tag + "\n"
            self.sub_counter -= 1
        elif self.sub_counter == 0:
            self.html_data += "MAIN_END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< " + tag + "\n"

    def handle_data(self, data):
        if data == "\n" or data == "\t" or data == "\br" or data == "\r":
            # self.html_data += self.sub + "data: " + "$backslash_operator" + "\n"
            self.html_data += ""
        elif len(data) > 0:
            self.html_data += (self.sub * self.sub_counter) + "data: '" + " ".join(data.split()) + "'\n"
            self.data.append(" ".join(data.split()))

    def handle_comment(self, data):
        self.html_data += (self.sub * self.sub_counter) + "comment: '" + data + "'\n"

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        self.html_data += (self.sub * self.sub_counter) + "ent_name: '" + name + "'\n"

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        self.html_data += (self.sub * self.sub_counter) + "ent_num: '" + c + "'\n"

    def handle_decl(self, data):
        self.html_data += (self.sub * self.sub_counter) + "decl: '" + data + "'\n"

    def return_data(self):
        return self.html_data
