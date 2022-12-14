import os
import sys

import time
from html.entities import name2codepoint

from bs4 import BeautifulSoup
import requests
import csv
from urllib.parse import urlparse
import chromedriver_autoinstaller
from html.parser import HTMLParser

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

#path = r"C:\Users\ozgun\Desktop\apogen\PetClinic __ a Spring Framework demonstration.html"

def chromedriver_checker():
    if chromedriver_autoinstaller.utils.get_chrome_version().split(".")[0] in os.listdir():
        return True
    else:
        return False

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)

        self.ordered_data = ""

        
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        self.ordered_data = self.ordered_data+"Start tag:"+tag
        for attr in attrs:
            print("\n     attr:", attr)
            self.ordered_data = self.ordered_data+"\nattr:"+",".join(attr)




    def handle_endtag(self, tag):
        print("End tag  :", tag)
        self.ordered_data = self.ordered_data+"\nEnd tag:"+tag

    def handle_data(self, data):
        print("Data     :", data)
        self.ordered_data = self.ordered_data+"\nData:"+data

    def handle_comment(self, data):
        print("Comment  :", data)
        self.ordered_data = self.ordered_data + "\nComment:" + data

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)
        self.ordered_data = self.ordered_data + "\nNamed ent:" + c

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)
        self.ordered_data = self.ordered_data + "\nNum ent:" + c

    def handle_decl(self, data):
        print( "Decl    :", data)
        self.ordered_data = self.ordered_data + "\nDecl:" + data

    def return_data(self):
        return self.ordered_data
