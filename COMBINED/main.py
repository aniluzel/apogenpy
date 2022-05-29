import csv

from scrapy.crawler import CrawlerProcess

import crawl
from sim_check import sim_check
import time
import FILE_GEN
import DEMO

c = CrawlerProcess({

    'FEED_FORMAT': 'csv',
    'FEED_URI': 'output.csv',
})
# find all cites
c.crawl(crawl.CrawlingSpider, start_urls=["http://localhost:8080/owners?lastName="])
c.start()

# filter

sim_check()

with open('filtered_output.csv', 'r') as read_obj:
    # csv_reader = reader(read_obj, delimiter=',')
    file_read = csv.reader(read_obj)

    array = list(file_read)
    read_obj.close()

DEMO.demo_fun(array)

for url in array[0]:
    FILE_GEN.gen(url)
