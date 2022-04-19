from scrapy.crawler import CrawlerProcess

import crawl
from sim_check import sim_check
import time

c = CrawlerProcess({

    'FEED_FORMAT': 'csv',
    'FEED_URI': 'output.csv',
})
#find all cites
c.crawl(crawl.KrakenSpider, start_urls=["http://localhost:8080/owners?lastName="])
c.start()

#filter

sim_check()
