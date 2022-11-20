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
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import utils
import re

crawled_links = []
# Define Browser Options
  # Hides the browser window
# Reference the local Chromedriver instance
#chrome_path = r'C:\chromedriver.exe'
#chrome_path = r'/Users/denis/Documents/CS401/apogenpyfolder/apogenpy/106/chromedriver'

# Run the Webdriver, save page an quit browser
#driver.get("http://localhost:8080/owners/find")

general = []

checked = []


def crawl_one(page_url, domain, driver):
    general = []
    # global general
    driver.get(page_url)
    # Scroll page to load whole content
    last_height = driver.execute_script("return document.body.scrollHeight")
    try:
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

            if link.get('class') is not None:

                if link.get('class')[0] == "btn":

                    if driver.current_url + link.get('href') not in checked:
                        if driver.current_url + link.get('href') not in general:
                            if driver.current_url + "/" + link.get('href') not in checked:
                                if driver.current_url + "/" + link.get('href') not in general:
                                    prev = driver.current_url
                                    bt = WebDriverWait(driver, 10).until(
                                        EC.element_to_be_clickable((By.XPATH, '//a[@href="' + link.get('href') + '"]')))
                                    bt.click()
                                    #print(driver.current_url + " == btn")
                                    #if(domain in str(driver.current_url) ):
                                    general.append(driver.current_url)
                                    driver.get(prev)


                # navlink parsing
                elif link.get('class')[0] == "nav-link":
                    if domain + link.get('href') not in checked:
                        if domain + link.get('href') not in general:
                            #print(domain + link.get('href') + " == navlink")
                            #if(domain in str(domain + link.get('href'))):
                            general.append(domain + link.get('href'))

                else:
                    tmp3 = link.get('href')
                    tmp3 = tmp3.split("/", 1)

                    if link.get('class')[0] == "fa":
                        if domain + link.get('href') not in checked:
                            if domain + link.get('href') not in general:
                                #print(domain + link.get('href') + " == forward")
                                #if(domain in str(domain + link.get('href'))):
                                general.append(domain + link.get('href'))

                    elif driver.current_url + link.get('href') not in checked:
                        if driver.current_url + link.get('href') not in general:
                            if(len(tmp3) >= 2):
                                if tmp3[1] != "":
                                    if driver.current_url + "/" + tmp3[1] not in checked:
                                        if driver.current_url + "/" + tmp3[1] not in general:
                                            #print(driver.current_url + "/" + tmp3[1] + " == not btn")
                                            #print(str(driver.current_url + "/" + tmp3[1]),"sd;fasdfsdf")
                                            #print(domain,'dsfasdfs')
                                            #if(domain in str(driver.current_url + "/" + tmp3[1])):
                                            general.append(driver.current_url + "/" + tmp3[1])



            else:
                tmp2 = link.get('href')
                tmp2 = tmp2.split("/", 1)

                if driver.current_url + link.get('href') not in checked:
                    if driver.current_url + link.get('href') not in general:
                        if len(tmp2) >=2:
                            if driver.current_url + "/" + tmp2[1] not in checked:
                                if driver.current_url + "/" + tmp2[1] not in general:
                                    prev1 = driver.current_url
                                    # print(driver.current_url + " ==  current page")
                                    # press = driver.find_element(By.PARTIAL_LINK_TEXT, element[0].lstrip(" ") + " " + element[1].lstrip(" "))
                                    press = WebDriverWait(driver, 30).until(
                                        EC.element_to_be_clickable((By.XPATH, '//a[@href="' + link.get('href') + '"]')))
                                    press.click()
                                    #print(driver.current_url + " == no class")
                                    #if(domain in str(driver.current_url)):
                                    general.append(driver.current_url)
                                    driver.get(prev1)



        for button_case in soup.find_all("button", type='submit'):
            if button_case.get('class')[1] == "btn-primary":
                button = driver.find_element(By.CLASS_NAME, button_case.get("class")[1])
                button.click()
                item = driver.current_url

                if item not in checked:
                    if item not in general:
                        #print(item + " == submit button")
                        #if(domain in str(item)):
                        general.append(item)

    except (selenium.common.exceptions.TimeoutException, WebDriverException, NameError,
        selenium.common.exceptions.StaleElementReferenceException, UnboundLocalError) as r:
        print(r)
    return general


counter = 0
def looping(array,domain,driver,limit=20000):
    global counter
    for i in array:
        if i not in checked:
            if str(domain) in str(i):
                if (counter == limit):
                    break
                checked.append(i)
                counter += 1
                looping(crawl_one(i, domain,driver),domain,driver,limit)
    return checked

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_driver_path = utils.chromedriver_path_name()
# #print(chrome_driver_path)
# driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
# print(len(looping(["http://localhost:8080"],"http://localhost:8080",driver,20000)))
# driver.quit()
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

    custom_settings = {
        "DEPTH_LIMIT": 50,
        "SPIDER_MIDDLEWARES":{"scrapy.spidermiddlewares.offsite.OffsiteMiddleware": None,
        OffsiteMiddleware: 500,},
        "LOG_ENABLED": False,
        "AJAXCRAWL_ENABLED": True,
        "COOKIES_ENABLED": False
    }

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

                # print("structural sim", structural_similarity(req1, req2))

                if param ==1:
                    if req1 != req2:
                        if structural_similarity(req1, req2) >= float(web_page_similarity_percentage):
                            print("similarity ratio is = ", (structural_similarity(req1, req2)), " first link = ",
                                  down[0], " second link = ", up[0])
                            html_text.remove(up)


                # if param == 1:
                #     #
                #     if down[0] != up[0]:
                #         if structural_similarity(req1, req2) > float(web_page_similarity_percentage):
                #             #print("similarity ratio is = ",(structural_similarity(req1, req2))," first link = ", down[0]," second link = ",up[0])
                #             html_text.remove(up)


                elif param == 2:
                    if down[0] != up[0]:
                        if style_similarity(req1, req2) > float(web_page_similarity_percentage):
                            #print("similarity ratio is = ",(style_similarity(req1, req2))," first link = ", down[0]," second link = ",up[0])
                            html_text.remove(up)

                elif param == 0:
                    if down[0] != up[0]:
                        if similarity(req1, req2, 0.3) > float(web_page_similarity_percentage):
                            #print("similarity ratio is = ",(similarity(req1, req2,0.3))," first link = ", down[0]," second link = ",up[0])
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

        # empty_arr = []
        for path in result_final:
            for rev in reversed(result_final):
                # print(path, "  ", rev, " =", jellyfish.jaro_distance(path, rev))
                if path != rev:
                    if  jellyfish.jaro_distance(path, rev) > float(web_path_similarity_percentage):
                        print(path, "  ", rev, " =", jellyfish.jaro_distance(path, rev))
                        # empty_arr.append(path)
                        result_final.remove(rev)
        # adding root of domain
        result_final.append(domain[0] + "/")
        result_final = list(set(result_final))

    # if both closed
    if check_sim == False and check_url_sim == False:
        for i in data:
            result_final.append(i)


    return result_final
