from html_similarity import style_similarity, structural_similarity, similarity
from csv import reader
import requests
import csv
import advertools as adv
import jellyfish
import numpy as np
import llist


def write_to_csv(list_input):
    # The scraped info will be written to a CSV here.
    try:
        with open("filtered.csv", 'w', newline='') as fopen:  # Open the csv file.
            for domain in list_input:
                fopen.write(domain + '\n')
    except:
        return False


# 0.48
def sim_check(web_page_similarity_percentage=0.60, web_path_similarity_percentage=0.88, param="struct"):
    links = []
    base = []
    urls = []
    html_text = []

    with open('URls.csv', 'r') as read_obj:
        csv_reader = reader(read_obj, delimiter=',')
        header = next(csv_reader)

        if header is not None:
            for row in csv_reader:
                links.append(row)

        # print(len(links))

    tmp_array = []
    empty_list = llist.sllist()
    empty_url = llist.sllist()
    for i in links:
        # text = requests.get(i[0]).text
        empty_url.append(i[0])
        empty_list.append(requests.get(i[0]).text)
        html_text.append((i[0], requests.get(i[0]).text))
        tmp_array.append(i[0])

    for down in empty_url:
        for up in reversed(empty_url):
            # Link 1
            #req1 = down[1]

            # Link 2
            #req2 = up[1]
            # print("structural sim", structural_similarity(req1, req2))
            if param == "struct":
                if structural_similarity(requests.get(down).text, requests.get(up).text) < web_page_similarity_percentage:
                    empty_url.remove(down)
                # if down[0] not in base and up[0] not in base:
                #     base.append((structural_similarity(req1, req2), down[0], up[0]))
                #     empty_url.remove(down[0])
            # print("styles =", style_similarity(req1, req2))
            # elif param == "style":
            #     base.append((style_similarity(req1, req2), down[0], up[0]))
            # # print("sim", similarity(req1, req2))
            # else:
            #     base.append((similarity(req1, req2), down[0], up[0]))
    # print(len(base))
    for n in base:
        if n[0] < web_page_similarity_percentage:
            # print(n[2])
            if n[2] not in urls:
                print(n[2] + " from " + str(n[0]) + " sim percentage" + n[1] + " idnot know what")
                urls.append(n[2])
    print(len(empty_url))
    return urls, web_path_similarity_percentage
    # print(tmp_array)
    # print(urls)
    # urls = set(urls)
    # urls = list(set(urls))
    # print(len(urls), "urls")
    # seen = set()
    # result = []
    # for item in urls:
    #     if item not in seen:
    #         seen.add(item)
    #         result.append(item)
    # print("list of urls", len(urls))
    # print(len(result))
    # url_data = adv.url_to_df(result)


def path_sim(urls, web_path_similarity_percentage):
    url_data = adv.url_to_df(urls)

    result_final = []
    domain = url_data["scheme"] + "://" + url_data["netloc"]

    tmp_2 = []
    for i in url_data["path"]:
        tmp_2.append(i)

    for path in tmp_2:
        for rev in reversed(tmp_2):
            # print(path, "  ", rev, " =", jellyfish.jaro_distance(path, rev))
            if web_path_similarity_percentage < jellyfish.jaro_distance(path, rev) < 0.99:
                # print(path, "  ", rev, " =", jellyfish.jaro_distance(path, rev))
                tmp_2.remove(rev)

    # print(tmp_2)
    # tmp = domain[0]+"/"
    result_final.append(domain[0])

    for i in tmp_2:
        whole_url = domain[0] + i
        if whole_url not in result_final:
            result_final.append(domain[0] + i)
    print(result_final)
    # result_final = list(set(result_final[0]))
    print(len(result_final))
    write_to_csv(result_final)


set = sim_check()
# print(set[0])
write_to_csv(set[0])
# path_sim(set[0],set[1])

# sim_check()
