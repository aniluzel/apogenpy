from collections import OrderedDict

from html_similarity import style_similarity, structural_similarity, similarity
from csv import reader
import requests
import csv
import advertools as adv
import jellyfish


def sim_check():
    array = []
    struct = []
    style = []
    sim = []
    sorted = []
    new_array = []
    with open('output.csv', 'r') as read_obj:
        csv_reader = reader(read_obj, delimiter=',')
        header = next(csv_reader)

        if header is not None:
            for row in csv_reader:
                array.append(row)

    for i in array:
        new_array.append((i[0], requests.get(i[0]).text))

    for down in new_array:
        for up in reversed(new_array):
            # Link 1
            # req1 = requests.get(down).text
            req1 = down[1]
            # Link 2
            # req2 = requests.get(up).text
            req2 = up[1]
            # print("structural sim", structural_similarity(req1, req2))
            struct.append((structural_similarity(req1, req2), down[0], up[0]))
            # print("styles =", style_similarity(req1, req2))
            style.append((style_similarity(req1, req2), down[0], up[0]))
            # print("sim", similarity(req1, req2))
            sim.append((similarity(req1, req2), down[0], up[0]))

    for n in struct:
        if n[0] < 0.48:
            # print(n[0])
            sorted.append(n[2])

    sorted = set(sorted)
    sorted = list(set(sorted))

    seen = set()
    result = []
    for item in sorted:
        if item not in seen:
            seen.add(item)
            result.append(item)
    # print("list of urls", len(sorted))
    # for i in result:
    #     print(i)

    url_data = adv.url_to_df(result)
    tmp = url_data.copy()
    tmp = tmp.set_index("path")
    tmp.head()
    # print(url_data["url"])
    url_cof = []
    result_final = []
    domain = url_data["scheme"] + "://" + url_data["netloc"]

    tmp_2=[]
    for i in url_data["path"]:
        tmp_2.append(i)


    for path in tmp_2:
        for rev in reversed(tmp_2):
            #print(jellyfish.jaro_distance(path, rev))
            #url_cof.append((rev, jellyfish.jaro_distance(path, rev)))
            if jellyfish.jaro_distance(path, rev) > 0.8:
                tmp_2.remove(rev)
                #tmp.drop(path)
                print("droped")
                #url_cof.append((rev ,0))
               # result_final.append(domain[0] + rev["path"])
            # print(path, rev)
    print(tmp_2)
    # for i in url_cof:
    #     #print(i[0])
    #     if i[1] < 0.9:
    #         result_final.append(domain[0] + i[0])
    result_final = list(set(result_final))
    print(len(result_final))
    print(result_final)
    with open('filtered_output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # writer.writerow('\n')
        # old
        writer.writerow(result)
        # writer.writerow(result[1])
        f.close()


#sim_check()
