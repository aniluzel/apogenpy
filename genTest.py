from bs4 import BeautifulSoup
import requests
import json
from csv import reader

with open('output.csv', 'r') as read_obj:
    csv_reader = reader(read_obj, delimiter=',')
    header = next(csv_reader)
    href = []
    ids = []
    buttons = []
    classes = []
    tables = []
    title = []


    def json_appender(element_add, filename):
        with open(filename, mode='w') as f:
            json.dump(element_add, f)


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
            json_appender(href, 'scrappedHrefData.json')

            # id data
            for i in divSoup:
                test = i.get('id')
                if test is not None and test not in ids:
                    ids.append(test)
            json_appender(ids, 'scrappedIdData.json')

            # button data
            for i in divSoup:
                buttonSoup = str(soup.find_all('button'))
                if buttonSoup is not None and buttonSoup not in buttons:
                    buttons.append(buttonSoup)
            json_appender(buttons, 'scrappedButtonData.json')

            # class data
            for i in testSoup:
                test = i.get('class')
                if test is not None and test not in classes:
                    classes.append(test)
            json_appender(classes, 'scrappedClassData.json')

            # table data
            for i in testSoup:
                tableSoup = str(soup.find_all('tbody'))
                if tableSoup is not None and tableSoup not in tables:
                    tables.append(tableSoup)
            json_appender(tables, 'scrappedTableData.json')

            # title data
            for i in testSoup:
                test = i.get('title')
                if test is not None and test not in title:
                    title.append(test)
            json_appender(title, 'scrappedTitleData.json')
