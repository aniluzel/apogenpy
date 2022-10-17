from scrapy.crawler import CrawlerProcess
from scrapy import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from html_similarity import style_similarity, structural_similarity, similarity
import requests
import advertools as adv
import jellyfish

crawled_links = []


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
def sim_check(data=[], web_page_similarity_percentage=0.92, web_path_similarity_percentage=0.88, param="struct",
              check_sim="sim_check = yes", check_url_sim="url_sim = no"):
    base = []
    urls = []
    html_text = []
    result_final = []

    if check_sim == "sim_check = yes":
        for i in data:
            html_text.append([i, requests.get(i).text])

        for down in html_text:
            for up in reversed(html_text):
                # Link 1
                req1 = down[1]
                # Link 2
                req2 = up[1]
                # print("structural sim", structural_similarity(req1, req2))
                if param == "struct":
                    # if (structural_similarity(req1, req2), down[0], up[0]) < web_page_similarity_percentage:
                    if down[0] != up[0]:
                        if structural_similarity(req1, req2) > web_page_similarity_percentage:
                            # print("similarity ratio is = ",(structural_similarity(req1, req2))," first link = ", down[0]," second link = ",up[0])
                            html_text.remove(up)


                elif param == "style":
                    base.append((style_similarity(req1, req2), down[0], up[0]))
                    if down[0] != up[0]:
                        if style_similarity(req1, req2) > web_page_similarity_percentage:
                            # print("similarity ratio is = ",(structural_similarity(req1, req2))," first link = ", down[0]," second link = ",up[0])
                            html_text.remove(up)

                else:
                    if down[0] != up[0]:
                        if similarity(req1, req2, 0.3) > web_page_similarity_percentage:
                            # print("similarity ratio is = ",(structural_similarity(req1, req2))," first link = ", down[0]," second link = ",up[0])
                            html_text.remove(up)

        # adds filtered urls
        for i in html_text:
            result_final.append(i[0])

    # if sim_check = no
    else:
        for i in data:
            result_final.append(i[0])

    # url check
    if check_url_sim == "url_sim = yes":
        url_data = adv.url_to_df(result_final)
        domain = url_data["scheme"] + "://" + url_data["netloc"]

        for i in url_data["path"]:
            result_final.append(domain[0] + i)

        # empty_arr = []
        for path in result_final:
            for rev in reversed(result_final):
                # print(path, "  ", rev, " =", jellyfish.jaro_distance(path, rev))
                if path != rev:
                    if web_path_similarity_percentage < jellyfish.jaro_distance(path, rev) < 0.99:
                        # print(path, "  ", rev, " =", jellyfish.jaro_distance(path, rev))
                        # empty_arr.append(path)
                        result_final.remove(rev)
        # adding root of domain
        result_final.append(domain[0] + "/")
        result_final = list(set(result_final))

    # if both closed
    if check_sim == "sim_check = no" and check_url_sim == "url_sim = no":
        for i in data:
            result_final.append(i[0])

    return result_final
