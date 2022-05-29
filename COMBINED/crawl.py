from scrapy.crawler import CrawlerProcess
from scrapy import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector



class PageInfoItem(Item):
    URL = Field()
    pass


class CrawlingSpider(CrawlSpider):

    name = 'Kraken'

    def __init__(self, allowed_domains=None, start_urls=None):
        super().__init__()

        if allowed_domains is None:
            self.allowed_domains = []
        else:
            self.allowed_domains = allowed_domains

        if start_urls is None:
            self.start_urls = []
        else:
            self.start_urls = start_urls

    rules = [Rule(LinkExtractor(), callback='parse_pageinfo', follow=True)]

    def parse_pageinfo(self, response):
        #sel = Selector(response)
        item = PageInfoItem()
        item['URL'] = response.url
        # Specify which part of the page to scrape
        # In addition to specifying in xPath format, it is also possible to specify in CSS format
        #item['title'] = sel.xpath('/html/head/title/text()').extract()
        return item



# --- run without creating project and save in `output.csv` ---
# c = CrawlerProcess({
#     # save in file as CSV, JSON or XML
#     'FEED_FORMAT': 'csv',  # csv, json, xml
#     'FEED_URI': 'output.csv',  #
# })
#
# c.crawl(KrakenSpider, start_urls=["http://localhost:8080/owners?lastName="])
# c.start()
