import math

from html_similarity import style_similarity, structural_similarity, similarity
from csv import reader
import requests
import csv
import advertools as adv
import jellyfish
from decimal import Decimal, ROUND_HALF_EVEN


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


# 0.48
def sim_check(web_page_similarity_percentage=0.92, web_path_similarity_percentage=0.88, param="struct"):
    links = []
    base = []
    urls = []
    html_text = []

    with open('output.csv', 'r') as read_obj:
        csv_reader = reader(read_obj, delimiter=',')
        header = next(csv_reader)

        if header is not None:
            for row in csv_reader:
                links.append(row)

        #print(len(links))
    for i in links:
        html_text.append([i[0], requests.get(i[0]).text])
    dataw = []
    for down in html_text:
        for up in reversed(html_text):
            # Link 1

            req1 = down[1]
            # Link 2
            req2 = up[1]
            # print("structural sim", structural_similarity(req1, req2))
            if param == "struct":
                #if (structural_similarity(req1, req2), down[0], up[0]) < web_page_similarity_percentage:
               if down[0] != up[0]:
                if  similarity(req1,req2,0.3) > web_page_similarity_percentage:
                    print("similarity ratio is = ",(structural_similarity(req1, req2))," first link = ", down[0]," second link = ",up[0])
                    dataw.append(down[0])
                    html_text.remove(up)
                    #up[0] = down[0]
                    #base.append((structural_similarity(req1, req2), down[0], up[0]))
            # print("styles =", style_similarity(req1, req2))
            elif param == "style":
                base.append((style_similarity(req1, req2), down[0], up[0]))
            # print("sim", similarity(req1, req2))
            else:
                base.append((similarity(req1, req2), down[0], up[0]))
    print(len(html_text))
   # print(html_text[0][0])
    for i in html_text:
        print(i[0])
    #print(len(dataw))

    for n in base:
        if n[0] > web_page_similarity_percentage:
            urls.append(n[2])
            print(len(base))
            # try:
            #     base.remove(n)
            # except KeyError as e:
            #     failing_data = e.args[0]



    #print(base)
   # print(len(urls))
    # urls = set(urls)
    # urls = list(set(urls))
    # seen = set()
    # result = []
    # for item in urls:
    #     if item not in seen:
    #         seen.add(item)
    #         result.append(item)

    url_data = adv.url_to_df(urls)

    result_final = []
    domain = url_data["scheme"] + "://" + url_data["netloc"]


    for i in url_data["path"]:
        result_final.append(domain[0]+i)

   # empty_arr = []
    for path in result_final:
        for rev in reversed(result_final):
            #print(path, "  ", rev, " =", jellyfish.jaro_distance(path, rev))
            if web_path_similarity_percentage < jellyfish.jaro_distance(path, rev) < 0.99:
                #print(path, "  ", rev, " =", jellyfish.jaro_distance(path, rev))
                #empty_arr.append(path)
                result_final.remove(rev)


    #adding root of domain
    result_final.append(domain[0]+"/")


    result_final = list(set(result_final))
    print(result_final)
    with open('filtered_output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(result_final)
        f.close()


#sim_check()
