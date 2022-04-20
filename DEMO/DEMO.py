from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
import csv
from csv import reader

href = []
ids = []
buttons = []
classes = []
tables = []
title = []


with open('DEMO_CSV.csv', 'r') as read_obj:
    csv_reader = reader(read_obj, delimiter=',')
    header = next(csv_reader)

    if header is not None:
        for row in csv_reader:
            url = row[0]
            page_html = requests.get(url).text
            print("parsing: " + row[0])
            soup = BeautifulSoup(page_html, "html.parser")
            testSoup = soup.find_all('a')
            divSoup = soup.find_all('div')

            # href data
            for i in testSoup:
                test = i.get('href')
                if test is not None and test not in href:
                    href.append(test)
            print("HREF DATA")
            print(href)
            #csv_writer('xpath',href)

            # id data
            for i in divSoup:
                for foo in soup.find_all('div', attrs={'class': 'foo'}):
                    foo_descendants = foo.descendants
                    for d in foo_descendants:
                        if d.name == 'div' and d.get('class', '') == ['bar']:
                            print(d.text)
                test = i.get('id')
                if test is not None and test not in test:
                    ids.append(test)
            print("ID DATA")
            print(ids)
            #csv_writer(ids)

            # button data
            for i in divSoup:
                buttonSoup = str(soup.find_all('button'))
                if buttonSoup is not None and buttonSoup not in buttons:
                    buttons.append(buttonSoup)
            print("BUTTON DATA")
            print(buttons)
            #csv_writer(buttons)

            # class data
            for i in testSoup:
                test = i.get('class')
                if test is not None and test not in classes:
                    classes.append(test)
            print("CLASS DATA")
            print(classes)
            #csv_writer(classes)

            # table data
            for i in testSoup:
                tableSoup = str(soup.find_all('tbody'))
                if tableSoup is not None and tableSoup not in tables:
                    tables.append(tableSoup)
            print("TABLE DATA")
            print(tables)
            #csv_writer(tables)

            # title data
            for i in testSoup:
                test = i.get('title')
                if test is not None and test not in title:
                    title.append(test)
            print("TITLE DATA")
            print(title)
            #csv_writer(title)