from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service(r'C:\chromedriver.exe')
browser = webdriver.Chrome(service=service)


browser.get("http://localhost:8080/owners/find")

url = "http://localhost:8080/owners/find"

page_html = requests.get(url).text

soup = BeautifulSoup(page_html, "html.parser")
title =soup.title
#titles = soup.find_all('title')
#buttons = soup.find_all('button')
button2= soup.find_all(class_="btn btn-primary")
#print(titles)

print(button2)

print("----------------------------")
AddOwner=browser.find_element(By.CSS_SELECTOR, ".btn-primary")
#time.sleep(3)
AddOwner.click()
items = soup.find_all('item')
print('title: '+title.string)
div_tags = soup.find_all('div')
ids = []

for div in div_tags:
     ID = div.get('id')
     if ID is not None:
         ids.append(ID)


classes_= soup.find_all(class_="")
tables = soup.find_all('tbody')
refs = soup.find_all('href')
#print(soup.tbody.contents)
#print(refs)
#print(buttons)
#print(ids)

def jsonAppender(elemToAdd, filename):
    with open(filename, mode='w') as f:
        json.dump(elemToAdd, f)


jsonAppender(ids,'scrappedData.json')
refs = soup.find_all('a',href=True)
for i in refs:
    jsonAppender(i.text, 'scrappedHrefData.json')
#print(refs)


