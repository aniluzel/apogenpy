from scrapy.crawler import CrawlerProcess
from scrapy import Item, Field
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

crawled_links = []
# Define Browser Options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Hides the browser window
# Reference the local Chromedriver instance
#chrome_path = r'C:\chromedriver.exe'
chrome_path = r'/Users/denis/Documents/CS401/apogenpyfolder/apogenpy/106/chromedriver'
driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
# Run the Webdriver, save page an quit browser
#driver.get("http://localhost:8080/owners/find")

general = []

checked = []


def crawl_one(page_url, domain):
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

        if link.get('class') is not None:

            if link.get('class')[0] == "btn":
                tmp = link.get('href')
                tmp = tmp.split("/", 2)
                if driver.current_url + link.get('href') not in checked:
                    if driver.current_url + "/" + link.get('href') not in checked:
                        prev = driver.current_url
                        # print(prev)
                        # print(link.text)
                        #  if "\n" not in link.text:
                        #     # print("here")
                        #      bt = driver.find_element(By.PARTIAL_LINK_TEXT, link.text)
                        #  else:
                        #      # print(link.text)
                        #      yyt = link.text.split("\n", 1)
                        #
                        #      yyt = yyt[0] + yyt[1]
                        #
                        #      yyt = yyt.split(" ", 1)
                        #    #  print(yyt[0])
                        #      yyt = yyt[0].replace(" ", "") +" "+ yyt[1].lstrip(' ')
                        #      # print(len(yyt))
                        #    #  print(yyt + " ytt")
                        #      bt = driver.find_element(By.PARTIAL_LINK_TEXT, yyt)
                        bt = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//a[@href="' + link.get('href') + '"]')))
                        bt.click()
                        print(driver.current_url + " == btn")
                        general.append(driver.current_url)
                        driver.get(prev)


            # navlink parsing
            elif link.get('class')[0] == "nav-link":
                if domain + link.get('href') not in checked:
                    print(domain + link.get('href') + " == navlink")
                    general.append(domain + link.get('href'))

            else:
                tmp3 = link.get('href')
                tmp3 = tmp3.split("/", 1)

                if link.get('class')[0] == "fa":
                    if domain + link.get('href') not in checked:
                        print(domain + link.get('href') + " == forward")
                        general.append(domain + link.get('href'))

                elif driver.current_url + link.get('href') not in checked:
                    if driver.current_url + "/" + tmp3[1] not in checked:
                        if tmp3[1] != "":
                            print(driver.current_url + "/" + tmp3[1] + " == not btn")

                            general.append(driver.current_url + "/" + tmp3[1])



        else:
            tmp2 = link.get('href')
            tmp2 = tmp2.split("/", 1)

            if driver.current_url + link.get('href') not in checked:
                if driver.current_url + "/" + tmp2[1] not in checked:
                    prev1 = driver.current_url
                    # print(driver.current_url + " ==  current page")
                    # press = driver.find_element(By.PARTIAL_LINK_TEXT, element[0].lstrip(" ") + " " + element[1].lstrip(" "))

                    press = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//a[@href="' + link.get('href') + '"]')))

                    # press = driver.find_element(By.XPATH, '//a[@href="'+link.get('href')+'"]')
                    try:
                        press.click()
                        print(driver.current_url + " == no class")
                        general.append(driver.current_url)
                        driver.get(prev1)
                    except WebDriverException:
                        print("Element is not clickable")
                    # else:
                    #
                    #
                    #     # if len(element) == 1:
                    #     # # element[0] = element[0].replace("'", "")
                    #     # # element[0] = element[0].replace("'", "")
                    #     #     press = driver.find_element(By.PARTIAL_LINK_TEXT, str(element[0]))
                    #     # else:
                    #     #     press = driver.find_element(By.PARTIAL_LINK_TEXT, element)
                    #     press = WebDriverWait(driver, 10).until(
                    #         EC.element_to_be_clickable((By.XPATH, '//a[@href="' + link.get('href') + '"]')))
                    #     press.click()

    # else:
    #     # print(link.get('href'))
    #     # print("not here")
    #     tmp2 = link.get('href')
    #     tmp2 = tmp2.split("/", 1)
    #     if link.get('class') is not None:
    #
    #         # print(link.get('class')[0])
    #         if link.get('class')[0] == "nav-link":
    #             if domain + link.get('href')not in checked:
    #                 print(domain + link.get('href')+" == navlink 2")
    #                 general.append(domain + link.get('href'))
    #                 count.append(0)
    #     else:
    #      if driver.current_url + link.get('href') not in checked:
    #         if driver.current_url + "/" + tmp2[1] not in checked:
    #             print(driver.current_url + "/" + tmp2[1] + " == array empty")
    #             general.append(driver.current_url + link.get('href'))
    #             count.append(0)

    for button_case in soup.find_all("button", type='submit'):
        if button_case.get('class')[1] == "btn-primary":

            button = driver.find_element(By.CLASS_NAME, button_case.get("class")[1])
            button.click()

            item = driver.current_url

            if item not in checked:
                print(item + " == submit button")
                general.append(item)

    return general


def looping(array, domain):
    for i in array:
        if i not in checked:
            #if(i.__contains__(domain)):
                checked.append(i)
                looping(crawl_one(i, domain), domain)
    return checked


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
        crawled_links.append(response.url)


# simcheck
# 0.48
def sim_check(data=[], web_page_similarity_percentage=0.92, web_path_similarity_percentage=0.88, param="Structural similarity",
              check_sim=True, check_url_sim=False):
    html_text = []
    result_final = []

    if check_sim:
        for i in data:
            html_text.append([i, requests.get(i).text])

        for down in html_text:
            for up in reversed(html_text):
                # Link 1
                req1 = down[1]
                # Link 2
                req2 = up[1]
                # print("structural sim", structural_similarity(req1, req2))
                if param == 1:
                    # if (structural_similarity(req1, req2), down[0], up[0]) < web_page_similarity_percentage:
                    if down[0] != up[0]:
                        if structural_similarity(req1, req2) > float(web_page_similarity_percentage):
                            #print("similarity ratio is = ",(structural_similarity(req1, req2))," first link = ", down[0]," second link = ",up[0])
                            html_text.remove(up)


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
