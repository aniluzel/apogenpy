from bs4 import BeautifulSoup
import requests
import csv
from csv import reader

csv_id = 0

with open("scrappedData.csv", 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['csv', 'id', 'name', 'xpath', 'text', 'tag', 'class', 'css'])
    writer.writeheader()


def csv_writer(field, data):
    with open("scrappedData.csv", 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['csv', 'id', 'name', 'xpath', 'text', 'tag', 'class', 'css'])
        writer.writerows(data)


with open('output.csv', 'r') as read_obj:
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
            csv_writer(href)

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
            csv_writer(ids)

            # button data
            for i in divSoup:
                buttonSoup = str(soup.find_all('button'))
                if buttonSoup is not None and buttonSoup not in buttons:
                    buttons.append(buttonSoup)
            csv_writer(buttons)

            # class data
            for i in testSoup:
                test = i.get('class')
                if test is not None and test not in classes:
                    classes.append(test)
            csv_writer(classes)

            # table data
            for i in testSoup:
                tableSoup = str(soup.find_all('tbody'))
                if tableSoup is not None and tableSoup not in tables:
                    tables.append(tableSoup)
            csv_writer(tables)

            # title data
            for i in testSoup:
                test = i.get('title')
                if test is not None and test not in title:
                    title.append(test)
            csv_writer(title)

