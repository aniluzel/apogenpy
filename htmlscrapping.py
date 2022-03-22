from bs4 import BeautifulSoup
import requests
import json
#2 libraries to get bs4 and requests to get html from webpage
url = "http://localhost:8080"

page_html = requests.get(url).text

soup = BeautifulSoup(page_html, "html.parser")
title =soup.title

buttons = soup.find_all('button')
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

print(refs)


