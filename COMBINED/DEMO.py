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


def name_changer(name):
    invalid = '<>:"/\|?* '
    for char in invalid:
        name = name.replace(char, '_').removeprefix('http://localhost:8080')
    return name

def csv_writer(data, filename):




    with open("GENERATED_CSV/"+name_changer(filename)+".csv", 'a') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerows(data)

#DATA FROM CRAWLER NEEDS TO BE FED
#-------------------------------------------------------------------------------



def demo_fun(array):
    #if header is not None:
    for row in array[0]:
            url = row
            page_html = requests.get(url).text
            print("parsing: " + row)
            soup = BeautifulSoup(page_html, "html.parser")

            testSoup = soup.find_all('a')
            divSoup = soup.find_all('div')
            #divSoup.append(soup.find_all('form'))
            idSoup = [tag['id'] for tag in soup.find_all(id=True)]
            #xpathSoup = [tag['href'] for tag in soup.find_all(href=True) if tag.text]
            #linkSoup = [a['href'] for a in soup.find_all('a', href=True) if a.text]
            #nameSoup = [a['name'] for a in soup.find_all('a', name=True)]
            classSoup = [tag['class'] for tag in soup.find_all(class_=True)]

            # xpath data
            for i in testSoup:
                test = i.get('href')
                if test is not None and test not in href:
                    href.append(test)
            #print("XPATH DATA")
            #print(href)
            #print(xpathSoup)
            #csv_writer('xpath',href)

            # name data
            #print("NAME DATA")
            #print(nameSoup)

            # link text data
            #print("LINK TEXT DATA")
            #print(linkSoup)

            # id data
            print("ID DATA")
            print(idSoup)

            csv_writer([idSoup],row)

            # button data
            for i in divSoup:
                buttonSoup = str(soup.find_all('button'))
                if buttonSoup is not None and buttonSoup not in buttons:
                    buttons.append(buttonSoup)
            print("BUTTON DATA")

            print(buttons)
            csv_writer([buttons],row)

            # class data
            for i in testSoup:
                test = i.get('class')
                if test is not None and test not in classes:
                    classes.append(test)
            print("CLASS DATA")
            #print(classes)
            print(classSoup)
            csv_writer(classSoup,row)

            # css data
            #print("CSS DATA")
            #print(cssSoup)
            something(name_changer(row))



#what this does?????
def something(filename):
    with open("GENERATED_CSV/"+filename+".csv", "r") as myfile:
        data = myfile.read().replace(',', '\n')

    with open("GENERATED_CSV/"+filename+"_ALT.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([data])
