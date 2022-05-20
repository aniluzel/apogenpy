from scrapy.crawler import CrawlerProcess

import crawl
#import sim_check
import time

c = CrawlerProcess({

    'FEED_FORMAT': 'csv',
    'FEED_URI': 'output.csv',
})
#find all cites

#http://localhost:8080/owners?lastName=
c.crawl(crawl.KrakenSpider, start_urls=["http://localhost:8080/owners/"])
c.start()

#filter

#sim_check.sim_check()
