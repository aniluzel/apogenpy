import selenium
from scrapy.crawler import CrawlerProcess
from scrapy import Item, Field
from scrapy.spidermiddlewares import offsite
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from html_similarity import style_similarity, structural_similarity, similarity
import requests
import advertools as adv
import jellyfish
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import re
from urllib.parse import urljoin
from settings import default_settings

crawled_links = []
general = []
checked = []

def crawl_one(page_url, driver):
    try:
        general = []
        # global general
        driver.get(page_url)
        # Scroll page to load whole content
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to the bottom.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load the page
            # time.sleep(2)
            # Calculate new scroll height and compare with last height.
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        htmltext = driver.page_source
        # Parse HTML structure
        soup = BeautifulSoup(htmltext, "html.parser")

        for link in soup.find_all("a", href=True):
            if urljoin(driver.current_url, link['href']) not in checked:
                if urljoin(driver.current_url, link['href']) not in general:
                    general.append(urljoin(driver.current_url, link['href']))

        for button_case in soup.find_all("button", type='submit'):
                button = driver.find_element(By.CLASS_NAME, button_case.get("class")[1])
                button.click()
                item = driver.current_url
                if item not in checked:
                    if item not in general:
                        general.append(item)

    except (selenium.common.exceptions.TimeoutException, WebDriverException, NameError,
        selenium.common.exceptions.StaleElementReferenceException, UnboundLocalError) as r:
        print(r)
    return general


counter = 0
def looping(array,domain,driver,limit=10):
    global counter
    #
    for i in array:
        if i not in checked:
            if str(domain) in str(i):
                if (counter == limit):
                    break
                checked.append(i)
                counter += 1
                looping(crawl_one(i,driver),domain,driver,limit)
    return checked

class PageInfoItem(Item):
    URL = Field()
    pass

class OffsiteMiddleware(offsite.OffsiteMiddleware):
    def get_host_regex(self, spider):
        regex = super().get_host_regex(spider)
        # Remove optional .* (any subdomains) from regex
        regex = regex.pattern.replace("(.*\.)?", "(www\.)?", 1)
        return re.compile(regex)


class CrawlingSpider(CrawlSpider):
    name = 'Kraken'
    def set_sett(val):
        custom_settings = {
            "DEPTH_LIMIT": val,
            "SPIDER_MIDDLEWARES": {"scrapy.spidermiddlewares.offsite.OffsiteMiddleware": None,
                                   OffsiteMiddleware: 500, },
            "LOG_ENABLED": False,
            "AJAXCRAWL_ENABLED": True,
            "COOKIES_ENABLED": False
        }
        return custom_settings

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

    custom_settings = set_sett(default_settings[12])

    rules = [Rule(LinkExtractor(), callback='parse_pageinfo', follow=True)]

    def parse_pageinfo(self, response):
        crawled_links.append(response.url)

# simcheck
def sim_check(data=[], web_page_similarity_percentage=0.92, web_path_similarity_percentage=0.91, param="Structural similarity",
              check_sim=True, check_url_sim=False):
    html_text = []
    result_final = []

    if check_sim:
        for i in data:
            html_text.append([i, requests.get(i).text])

        for down in html_text:
            for up in html_text:
                # Link 1 text
                req1 = down[1]
                # Link 2 text
                req2 = up[1]

                if param ==1:
                    if req1 != req2:
                        if structural_similarity(req1, req2) >= float(web_page_similarity_percentage):
                            html_text.remove(up)

                elif param == 2:
                    if down[0] != up[0]:
                        if style_similarity(req1, req2) > float(web_page_similarity_percentage):
                            html_text.remove(up)

                elif param == 0:
                    if down[0] != up[0]:
                        if similarity(req1, req2, 0.3) > float(web_page_similarity_percentage):
                            html_text.remove(up)

        # adds filtered urls
        for i in html_text:
            result_final.append(i[0])

    # if sim_check = no
    elif(check_url_sim):
        for i in data:
            result_final.append(i)

    # url check
    if check_url_sim:
        url_data = adv.url_to_df(result_final)
        domain = url_data["scheme"] + "://" + url_data["netloc"]

        for i in url_data["path"]:
            result_final.append(domain[0] + i)

        for path in result_final:
            for rev in reversed(result_final):
                if path != rev:
                    if jellyfish.jaro_distance(path, rev) > float(web_path_similarity_percentage):
                        result_final.remove(rev)
        # adding root of domain
        result_final.append(domain[0] + "/")
        result_final = list(set(result_final))

    # if both closed
    if check_sim == False and check_url_sim == False:
        for i in data:
            result_final.append(i)

    return result_final
