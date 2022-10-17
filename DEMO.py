from bs4 import BeautifulSoup
import requests
import csv

href = []
ids = []
buttons = []
classes = []
tables = []
title = []

# obsolete
def name_changer(name):
    invalid = '<>:"/\|?* '
    for char in invalid:
        name = name.replace(char, '_').removeprefix('http://localhost:8080')
    return name

# obsolete
def csv_writer(data, filename):

    with open("GENERATED_CSV/"+name_changer(filename)+".csv", 'a') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerows(data)


def demo_fun(array):
            url = array
            print()
            page_html = requests.get(url).text
            print("parsing: " + array)
            soup = BeautifulSoup(page_html, "html.parser")

            testSoup = soup.find_all('a')
            divSoup = soup.find_all('div')
            idSoup = [tag['id'] for tag in soup.find_all(id=True)]
            classSoup = [tag['class'] for tag in soup.find_all(class_=True)]

            # xpath data
            for i in testSoup:
                test = i.get('href')
                if test is not None and test not in href:
                    href.append(test)
            # id data
            print("ID DATA")
            print(idSoup)

            csv_writer([idSoup],array)

            # button data
            for i in divSoup:
                buttonSoup = str(soup.find_all('button'))
                if buttonSoup is not None and buttonSoup not in buttons:
                    buttons.append(buttonSoup)
            print("BUTTON DATA")

            print(buttons)
            csv_writer([buttons],array)

            # class data
            for i in testSoup:
                test = i.get('class')
                if test is not None and test not in classes:
                    classes.append(test)
            print("CLASS DATA")
            print(classSoup)
            csv_writer(classSoup,array)

            # css data
            something(name_changer(array))

# obsolete
def something(filename):
    with open("GENERATED_CSV/"+filename+".csv", "r") as myfile:
        data = myfile.read().replace(',', '\n')
